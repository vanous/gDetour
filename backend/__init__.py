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

# __init__.py
from flask import Flask, jsonify, send_from_directory, request
from app.sacn_manager import sAcnManager
import os
from pathlib import Path
import pygdtf
import json
from app.network import get_interfaces

app = Flask(__name__, static_folder="static")
sacn_manager = sAcnManager()


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/start_receiver", methods=["POST"])
def start_receiver():
    sacn_manager.start_receiver()
    return jsonify({"status": "Receiver started"}), 200


@app.route("/stop_receiver", methods=["POST"])
def stop_receiver():
    sacn_manager.stop_receiver()
    return jsonify({"status": "Receiver stopped"}), 200


@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)


@app.route("/start_sender", methods=["POST"])
def start_sender():
    sacn_manager.start_sender()
    return jsonify({"status": "Sender started"}), 200


@app.route("/stop_sender", methods=["POST"])
def stop_sender():
    sacn_manager.stop_sender()
    return jsonify({"status": "Sender stopped"}), 200


@app.route("/dmx_mapping", methods=["POST"])
def set_dmx_mapping():
    data = request.get_json()  # Get the JSON data from the request
    sacn_manager.set_mapping(data)
    print("Received DMX Mapping:", data)  # Print the received data to the console
    return jsonify(
        {"status": "success", "data": data}
    ), 200  # Respond with a success message


@app.route("/default", methods=["POST"])
def set_defaults():
    data = request.get_json()  # Get the JSON data from the request
    sacn_manager.set_default(data)
    print("Received DMX Default:", data)  # Print the received data to the console
    return jsonify(
        {"status": "success", "data": data}
    ), 200  # Respond with a success message


@app.route("/upload", methods=["POST"])
def upload_files():
    local = Path().resolve()
    filepath = Path(local / "upload")
    Path(filepath).mkdir(parents=True, exist_ok=True)
    if "files" not in request.files:
        return jsonify({"error": "No file part"}), 400

    files = request.files.getlist("files")
    if not files:
        return jsonify({"error": "No selected files"}), 400
    print("files", files)

    filenames = []
    for file in files:
        print("file", file)
        if file.filename == "":
            continue
        # Save the file
        full_path = Path(filepath / file.filename)
        print("file path", full_path)
        file.save(full_path)
        filenames.append(file.filename)

    return jsonify({"filenames": filenames}), 200


@app.route("/files", methods=["GET"])
def get_files():
    local = Path().resolve()
    folder = Path(local / "upload")
    files = [file.name for file in folder.glob("*.gdtf")]
    return jsonify({"files": files}), 200


@app.route("/modes", methods=["POST"])
def get_modes():
    data = request.get_json()  # Get the JSON data from the request
    print("data", data)
    fixture = data["fixture"]

    local = Path().resolve()
    filepath = Path(local / "upload")
    full_path = Path(filepath / fixture)
    gdtf_fixture = pygdtf.pygdtf.FixtureType(full_path)
    modes = pygdtf.utils.get_dmx_modes_info(
        gdtf_fixture, include_channels=True, include_channel_functions=True
    )
    print("Received DMX Mapping:", data)  # Print the received data to the console
    return jsonify(
        {"status": "success", "data": modes}
    ), 200  # Respond with a success message


@app.route("/mapping_save", methods=["POST"])
def save_mapping():
    data = request.get_json()  # Get the JSON data from the request
    filename = data["filename"]
    mapping = data["mapping"]
    print("Received JSON Mapping:", data)  # Print the received data to the console
    local = Path().resolve()
    filepath = Path(local / "mappings")
    Path(filepath).mkdir(parents=True, exist_ok=True)
    full_path = Path(filepath / filename)
    print("stem", full_path.suffix.lower())
    if full_path.suffix.lower() != ".json":
        full_path = Path(filepath / f"{filename}.json")

    with open(f"{full_path}", "w") as f:
        json.dump(mapping, f)

    return jsonify(
        {"status": "success", "data": data}
    ), 200  # Respond with a success message


@app.route("/mapping_get", methods=["POST"])
def get_mapping():
    data = request.get_json()  # Get the JSON data from the request
    print("data", data)
    filename = data["filename"]
    local = Path().resolve()
    filepath = Path(local / "mappings")
    Path(filepath).mkdir(parents=True, exist_ok=True)
    full_path = Path(filepath / filename)
    with open(f"{full_path}", "r") as f:
        data = json.load(f)
    return jsonify(
        {"status": "success", "mapping": data}
    ), 200  # Respond with a success message


@app.route("/mapping_list", methods=["GET"])
def get_mappings_list():
    local = Path().resolve()
    filepath = Path(local / "mappings")
    Path(filepath).mkdir(parents=True, exist_ok=True)
    files = [file.name for file in filepath.glob("*.json")]
    return jsonify({"files": files}), 200


@app.route("/sacn", methods=["POST"])
def set_sacn():
    data = request.get_json()  # Get the JSON data from the request
    result = sacn_manager.set_sacn(data)
    print("Received :", data)  # Print the received data to the console
    return jsonify({"status": result}), 200  # Respond with a success message


@app.route("/sacn", methods=["GET"])
def get_sacn():
    data, status = sacn_manager.get_sacn()
    return jsonify(
        {"status": status, "data": data}
    ), 200  # Respond with a success message


@app.route("/interfaces", methods=["GET"])
def get_ethernet_interfaces():
    data = get_interfaces()
    return jsonify(
        {"status": "success", "data": data}
    ), 200  # Respond with a success message
