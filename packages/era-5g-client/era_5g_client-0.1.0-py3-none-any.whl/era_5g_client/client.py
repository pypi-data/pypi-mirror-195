import base64
import os
from collections.abc import Callable
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np
import requests
import socketio
from requests import HTTPError, Response

from era_5g_client.exceptions import FailedToConnect, NetAppNotReady
from era_5g_client.middleware_resource_checker import MiddlewareResourceChecker

buffer: List[Tuple[np.ndarray, Optional[str]]] = []

# port of the netapp's server
NETAPP_PORT = int(os.getenv("NETAPP_PORT", 5896))

"""
TODO ZdenekM: I would divide this to
    NetAppClientBase (without middleware),
    NetAppClient (derived from the above, which will be using middleware)
"""


class NetAppClient:
    """Basic implementation of the NetApp client.

    It creates the Requests object with session and bind callbacks for
    connection info and results from the NetApp.
    """

    def __init__(
        self,
        host: str,
        user_id: str,
        password: str,
        task_id: str,
        resource_lock: bool,
        results_event: Callable,
        use_middleware: bool = True,
        wait_for_netapp: bool = True,
        netapp_uri: Optional[str] = None,
        netapp_port: Optional[int] = None,
        image_error_event: Optional[Callable] = None,
        json_error_event: Optional[Callable] = None,
    ) -> None:
        """Constructor.

        Args:
            host (str): The IP or hostname of the middleware
            user_id (str): The middleware user's id
            password (str): The middleware user's password
            task_id (str): The ID of the NetApp to be deployed
            resource_lock (bool): TBA
            results_event (Callable): callback where results will arrive
            use_middleware (bool, optional): Defines if the NetApp should be deployed by middleware.
                If False, the netapp_uri and netapp_port need to be defined, otherwise,
                they need to be left None. Defaults to True.
            wait_for_netapp (bool, optional):
            netapp_uri (str, optional): The URI of the NetApp interface. Defaults to None.
            netapp_port (int, optional): The port of the NetApp interface. Defaults to None.
            image_error_event (Callable, optional): Callback which is emited when server
                failed to process the incoming image.
            json_error_event (Callable, optional): Callback which is emited when server
                failed to process the incoming json data.

        Raises:
            FailedToConnect: When connection to the middleware could not be set or
                login failed
            FailedToObtainPlan: When the plan was not successfully returned from
                the middleware
        """

        # temporary removed asserts until the middleware will provide necessary info

        # if middleware is used, the netapp_uri and port should be obtained from it
        # assert use_middleware and not netapp_uri and not netapp_port
        # if middleware is not used, the netapp_uri and port needs to be provided
        # assert not use_middleware and netapp_uri and netapp_port

        self.sio = socketio.Client()
        self.session = requests.session()
        self.host = host.rstrip("/") if host is not None else None
        self.resource_lock = resource_lock
        self.netapp_host = netapp_uri
        self.netapp_port = netapp_port
        self.use_middleware = use_middleware
        self.sio.on("message", results_event, namespace="/results")
        self.sio.on("connect", self.on_connect_event, namespace="/results")
        self.sio.on("image_error", image_error_event, namespace="/data")
        self.sio.on("json_error", json_error_event, namespace="/data")
        self.sio.on("connect_error", self.on_connect_error, namespace="/results")
        self.session_cookie: Optional[str] = None
        self.action_plan_id: Optional[str] = None
        self.resource_checker: Optional[MiddlewareResourceChecker] = None
        self.user_id = user_id
        self.password = password
        self.task_id = task_id
        self.token: Optional[str] = None
        self.wait_for_netapp = wait_for_netapp
        self.ws_data: Optional[bool] = False
        if self.use_middleware:
            self.connect_to_middleware()

    def test(data):
        print(data)

    def connect_to_middleware(self) -> None:

        try:
            # connect to the middleware
            self.token = self.gateway_login(self.user_id, self.password)

            self.action_plan_id = self.gateway_get_plan(
                self.task_id, self.resource_lock
            )  # Get the plan_id by sending the token and task_id
            if not self.action_plan_id:
                raise FailedToConnect("Need plan id first...")

            self.resource_checker = MiddlewareResourceChecker(
                self.token,
                self.action_plan_id,
                self.build_middleware_api_endpoint("orchestrate/orchestrate/plan"),
                daemon=True,
            )
            self.resource_checker.start()
            if self.use_middleware and self.wait_for_netapp:
                self.wait_until_netapp_ready()
                print(self.resource_checker.is_ready())
                self.load_netapp_uri()
            print("Feedback: Got new plan successfully.")
        except Exception as ex:
            self.delete_all_resources()
            raise FailedToConnect(f"Can't connect to middleware: {ex}") from ex

    def register(self, ws_data: Optional[bool] = False, args: Optional[Dict] = None) -> Response:
        """Calls the /register endpoint of the NetApp interface and if the
        registration is successful, it sets up the WebSocket connection for
        results retrieval.

        Args:
            ws_data (bool): indicates if a separate websocket channel
                for data transport should be set
            args (dict): optional parameters to be passed to
            the NetApp, in the form of dict. Defaults to None.
        Returns:
            Response: response from the NetApp
        """

        if self.use_middleware:

            if not self.resource_checker:
                raise NetAppNotReady("Not connected to the middleware.")

            if not self.resource_checker.is_ready():
                raise NetAppNotReady("Not ready.")

        self.ws_data = ws_data

        response = self.session.post(
            self.build_netapp_api_endpoint("register"), json=args, headers={"Content-Type": "application/json"}
        )

        # checks whether the NetApp responded with any data
        if len(response.content) > 0:
            try:
                data = response.json()
            except ValueError as ex:
                raise FailedToConnect(f"Decoding JSON has failed: {ex}, response: {response}")
            # checks if an error was returned
            if "error" in data:
                raise FailedToConnect(f"{response.status_code}: {data['error']}")

        self.session_cookie = response.cookies["session"]

        # creates the WebSocket connection
        if ws_data:
            self.sio.connect(
                self.build_netapp_api_endpoint(""),
                namespaces=["/results", "/data"],
                headers={"Cookie": f"session={self.session_cookie}"},
                wait_timeout=10,
            )
        else:
            self.sio.connect(
                self.build_netapp_api_endpoint(""),
                namespaces=["/results"],
                headers={"Cookie": f"session={self.session_cookie}"},
                wait_timeout=10,
            )

        return response

    def disconnect(self) -> None:
        """Calls the /unregister endpoint of the server and disconnects the
        WebSocket connection."""

        if self.netapp_host is not None and self.netapp_port is not None:
            self.session.post(self.build_netapp_api_endpoint("unregister"))
        self.sio.disconnect()
        if self.use_middleware:
            self.delete_all_resources()

    def build_middleware_api_endpoint(self, path: str) -> str:
        """Builds an API endpoint on the NetApp interface.

        Args:
            path (str): endpoint path
        Returns:
            _type_: complete URI to requested endpoint
        """

        return f"http://{self.host}/{path}"

    def build_netapp_api_endpoint(self, path: str) -> str:
        """Builds an API endpoint on the NetApp interface.

        Args:
            path (str): endpoint path
        Returns:
            _type_: complete URI to requested endpoint
        """

        return f"http://{self.netapp_host}:{self.netapp_port}/{path}"

    def wait(self) -> None:
        """Blocking infinite waiting."""
        self.sio.wait()

    def on_connect_event(self) -> None:
        """The callback called once the connection to the NetApp is made."""
        print("Connected to server")

    def on_connect_error(self, data: str) -> None:
        """The callback called on connection error."""
        print(f"Connection error: {data}")
        # self.disconnect()

    def send_image_http(self, frame: np.ndarray, timestamp: Optional[str] = None, batch_size: int = 1) -> None:
        """Encodes the image frame to the jpg format and sends it over the
        HTTP, to the /image endpoint.

        Args:
            frame (np.ndarray): image frame
            timestamp (str, optional): Frame timestamp The timestamp format
            is defined by the NetApp. Defaults to None.
            batch_size (int, optional): If higher than one, the images are
            send in batches. Defaults to 1
        """

        assert batch_size >= 1

        _, img_encoded = cv2.imencode(".jpg", frame)

        if len(buffer) < batch_size:
            buffer.append((img_encoded, timestamp))

        if len(buffer) == batch_size:
            # TODO find out right type annotation
            files = [("files", (f"image{i + 1}", buffer[i][0], "image/jpeg")) for i in range(batch_size)]

            timestamps: List[Optional[str]] = [b[1] for b in buffer]
            self.session.post(
                self.build_netapp_api_endpoint("image"),
                files=files,  # type: ignore
                params={"timestamps[]": timestamps},  # type: ignore
            )
            buffer.clear()

    def send_image_ws(self, frame: np.ndarray, timestamp: Optional[str] = None):
        """Encodes the image frame to the jpg format and sends it over the
        websocket, to the /data namespace.

        Args:
            frame (np.ndarray): Image frame
            timestamp (Optional[str], optional): Frame timestamp The timestamp format
            is defined by the NetApp. Defaults to None.
        """
        assert self.ws_data

        _, img_encoded = cv2.imencode(".jpg", frame)
        self.sio.emit("image", {"timestamp": timestamp, "frame": base64.b64encode(img_encoded)}, "/data")

    def send_json_ws(self, json: dict):
        """Sends netapp-specific json data.

        Args:
            json (dict): Json data in the form of Python dictionary
        """
        assert self.ws_data
        self.sio.emit("json", json, "/data")

    def wait_until_netapp_ready(self) -> None:
        """Blocking wait until the NetApp is running.

        Raises:
            NetAppNotReady: _description_
        """
        if not self.resource_checker:
            raise NetAppNotReady("Not connected to middleware.")
        self.resource_checker.wait_until_resource_ready()

    def load_netapp_uri(self) -> None:
        if not (self.resource_checker and self.resource_checker.is_ready()):
            raise NetAppNotReady
        self.netapp_host = self.resource_checker.url
        self.netapp_port = NETAPP_PORT

    def gateway_login(self, id: str, password: str) -> str:
        print("Trying to log into the middleware")
        # Request Login
        try:
            r = requests.post(self.build_middleware_api_endpoint("Login"), json={"Id": id, "Password": password})
            response = r.json()
            if "errors" in response:
                raise FailedToConnect(str(response["errors"]))
            new_token = response["token"]  # Token is stored here
            # time.sleep(10)
            if not isinstance(new_token, str) or not new_token:
                raise FailedToConnect("Invalid token.")
            return new_token

        except requests.HTTPError as e:
            raise FailedToConnect(f"Could not login to the middleware gateway, status code: {e.response.status_code}")
        except KeyError as e:
            raise FailedToConnect(f"Could not login to the middleware gateway, the response does not contain {e}")

    def gateway_get_plan(self, taskid: str, resource_lock: bool) -> str:
        # Request plan
        try:
            print("Goal task is: " + str(taskid))
            hed = {"Authorization": f"Bearer {str(self.token)}"}
            data = {"TaskId": str(taskid), "LockResourceReUse": resource_lock}
            response = requests.post(self.build_middleware_api_endpoint("Task/Plan"), json=data, headers=hed).json()

            if not isinstance(response, dict):
                raise FailedToConnect("Invalid response.")

            if "statusCode" in response and (response["statusCode"] == 500 or response["statusCode"] == 400):
                raise FailedToConnect(f"response {response['statusCode']}: {response['message']}")
            # todo:             if "errors" in response:
            #                 raise FailedToConnect(str(response["errors"]))
            # print(action_sequence)
            action_plan_id = str(response["ActionPlanId"])
            print("ActionPlanId ** is: " + str(self.action_plan_id))
            return action_plan_id
        except KeyError as e:
            raise FailedToConnect(f"Could not get the plan: {e}")

    def delete_all_resources(self) -> None:
        if self.token is None or self.action_plan_id is None:
            return

        try:
            hed = {"Authorization": "Bearer " + str(self.token)}
            url = self.build_middleware_api_endpoint(f"orchestrate/orchestrate/plan/{str(self.action_plan_id)}")
            response = requests.delete(url, headers=hed)

            if response.ok:
                print("Resource deleted")

        except HTTPError as e:
            print(e.response.status_code)
            raise FailedToConnect("Error, could not get delete the resource, revisit the log files for more details.")

    def delete_single_resource(self) -> None:
        raise NotImplementedError  # TODO

    def gateway_log_off(self) -> None:
        print("Middleware log out successful")
        # TODO
        pass
