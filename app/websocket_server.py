# Copyright (C) 2025 vanous
#
# This file is part of gDetour.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import threading

import websockets
from websockets.sync.server import serve

from app.sacn_manager import sAcnManager


class WebSocketServer:
    def __init__(self, port=8765):
        self.port = port
        self.manager = sAcnManager()
        self.connected_clients = set()  # Track connected clients

        self.manager.register_ws_callback(self.send_data_to_clients)

    def handler(self, websocket):
        self.connected_clients.add(websocket)
        try:
            for message in websocket:
                pass
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            # Unregister the client on disconnect
            self.connected_clients.remove(websocket)
        print("client exited")

    def send_data_to_clients(self, index, data):
        for client in (
            self.connected_clients.copy()
        ):  # prevent error when client disconnect and it modifies the list
            message = json.dumps({"dmx_data": [index, list(data)]})
            try:
                client.send(message)
            except Exception as e:
                print(f"Failed to send message to client: {e}")

    def start(self):
        server = serve(self.handler, "localhost", self.port)
        server.serve_forever()
