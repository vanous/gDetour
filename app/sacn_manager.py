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

# thread_manager.py
import threading
import time

import sacn

from app.network import get_interfaces


class sAcnManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(sAcnManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):  # Prevent re-initialization
            self.initialized = True
            self.received_dmx_data = None
            self.data_lock = threading.Lock()
            self.sacn_receiver_thread = None
            self.sacn_sender_thread = None
            self.receiver = None
            self.sender = None
            self.address = None
            self.mapping = []
            self.receiving_universe = 1
            self.sending_universe = 2
            self.ws_callbacks = []
            self.data_default = [
                0,
            ] * 512
            network_interfaces = get_interfaces()
            if network_interfaces:
                self.address = network_interfaces[0][0]

    def register_ws_callback(self, callback):
        self.ws_callbacks.append(callback)

    def notify_ws_callbacks(self, universe, data):
        for ws_callback in self.ws_callbacks:
            ws_callback(universe, data)

    def callback_receiving(self, packet):
        if packet.dmxStartCode == 0x00:
            # with self.data_lock:
            self.received_dmx_data = packet.dmxData

            if self.received_dmx_data is not None:
                data_in = self.received_dmx_data
                data_out = self.data_default
                for items in self.mapping:
                    chan = items[0]
                    val = items[1]
                    try:
                        data_out[val - 1] = data_in[chan - 1]
                    except:
                        ...
                print("sending data", data_out)
                self.sender[self.sending_universe].dmx_data = tuple(data_out)
                self.received_dmx_data = None
            # self.notify_ws_callbacks(self.receiving_universe, packet.dmxData)
            self.notify_ws_callbacks(1, packet.dmxData)
            print(f"Received receiving universe DMX data: {packet.dmxData[:6]}")

    def callback_sending(self, packet):
        if packet.dmxStartCode == 0x00:
            # self.notify_ws_callbacks(self.sending_universe, packet.dmxData)
            self.notify_ws_callbacks(2, packet.dmxData)
            print(f"Received sending universe DMX data: {packet.dmxData[:6]}")

    def run_sacn_receiver(self):
        print("start receiver")
        try:
            self.receiver = sacn.sACNreceiver(bind_address=self.address)
            self.receiver.start()

            self.receiver.register_listener(
                "universe", self.callback_receiving, universe=self.receiving_universe
            )
            self.receiver.register_listener(
                "universe", self.callback_sending, universe=self.sending_universe
            )

            self.receiver.join_multicast(self.receiving_universe)
            self.receiver.join_multicast(self.sending_universe)
        except Exception as e:
            print("Error starting receiver process", e)

    def run_sacn_sender(self):
        print("start sender")
        try:
            self.sender = sacn.sACNsender(
                source_name="GDetour", bind_address=self.address
            )
            self.sender.start()
            self.sender.activate_output(self.sending_universe)
            self.sender[self.sending_universe].multicast = True
        except Exception as e:
            print("Error starting sender process", e)

    def start_receiver(self):
        self.run_sacn_receiver()

    def stop_receiver(self):
        self.receiver.leave_multicast(self.sending_universe)
        self.receiver.leave_multicast(self.receiving_universe)
        self.receiver.stop()
        self.receiver.remove_listener(self.callback_sending)
        self.receiver.remove_listener(self.callback_receiving)

    def start_sender(self):
        self.run_sacn_sender()

    def stop_sender(self):
        self.sender.stop()

    def set_mapping(self, mapping):
        print("set mapping", mapping)
        self.mapping = mapping

    def set_default(self, default):
        self.data_default = default

    def set_sacn(self, data):
        print("setting sacn", data)
        try:
            self.stop_receiver()
        except Exception as e:
            print("Error stopping receiver", e)
        try:
            self.stop_sender()
        except Exception as e:
            print("Error stopping sender", e)
        self.receiving_universe = data[0]
        self.sending_universe = data[1]
        self.address = data[2]

        self.start_receiver()
        receiver_result = False
        if self.receiver is not None:
            if self.receiver._handler.socket._thread is not None:
                receiver_result = self.receiver._handler.socket._thread.is_alive()

        self.start_sender()
        sender_result = False
        if self.sender is not None:
            if self.sender._sender_handler.socket._thread is not None:
                sender_result = self.sender._sender_handler.socket._thread.is_alive()

        return {"Receiver started": receiver_result, "Sender started": sender_result}

    def get_sacn(self):
        data = [1, 2, None]
        data[0] = self.receiving_universe
        data[1] = self.sending_universe
        data[2] = self.address
        sender_result = None
        receiver_result = None

        if self.receiver is not None:
            if self.receiver._handler.socket._thread is not None:
                receiver_result = self.receiver._handler.socket._thread.is_alive()
        if self.sender is not None:
            if self.sender._sender_handler.socket._thread is not None:
                sender_result = self.sender._sender_handler.socket._thread.is_alive()

        status = {"Receiver started": receiver_result, "Sender started": sender_result}
        return data, status
