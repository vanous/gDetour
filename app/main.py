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

import signal
import sys
import threading
import webbrowser

from backend import app  # Import the Flask app from the app package

from app.sacn_manager import sAcnManager  # Import the ThreadManager
from app.websocket_server import WebSocketServer

# Create an instance of ThreadManager
sacn_manager = sAcnManager()
ws_server = WebSocketServer()


def run_flask():
    app.run(
        debug=True, use_reloader=False
    )  # use_reloader=False to prevent the app from starting twice


def signal_handler(sig, frame):
    print("Stopping threads...")
    sacn_manager.stop_sender()  # Stop the sender thread
    sacn_manager.stop_receiver()  # Stop the receiver thread
    sys.exit()


def main():
    signal.signal(signal.SIGINT, signal_handler)

    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask, name="gDetour Flask")
    flask_thread.start()
    ws_thread = threading.Thread(target=ws_server.start, name="gDetour Websockets")
    ws_thread.start()
    webbrowser.open("http://127.0.0.1:5000")

    # Start the sACN receiver and sender threads
    sacn_manager.start_receiver()
    sacn_manager.start_sender()

    # Wait for the Flask app to finish
    flask_thread.join()
    sacn_manager.stop_sender()
    sacn_manager.stop_receiver()
    ws_thread.join()


if __name__ == "__main__":
    main()
