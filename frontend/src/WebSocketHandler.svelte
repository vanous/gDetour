<!--

    Copyright (C) 2025 vanous

    This file is part of gDetour.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

-->
<script>
    import { onMount, createEventDispatcher } from "svelte";
    let data = "";
    let dmx_data = [];
    function onDataReceived(data_in) {
        data = data_in;
    }

    function onDMXReceived(dmx) {
        dmx_data[dmx[0]] = JSON.stringify(dmx[1]);
    }

    let socket;
    let isConnected = false; // Track the connection state

    // Function to handle WebSocket connection
    function connectWebSocket() {
        if (!socket) {
            socket = new WebSocket("ws://localhost:8765");

            socket.onopen = () => {
                console.log("WebSocket connection established");
                onDataReceived("Waiting for data");
            };

            socket.onmessage = (event) => {
                const message = JSON.parse(event.data);
                //console.log("message", message.dmx_data);
                onDataReceived("");
                onDMXReceived(message.dmx_data);
            };

            socket.onerror = (error) => {
                console.error("WebSocket error:", error);
                onDataReceived("WebSocket error");
            };

            socket.onclose = () => {
                console.log("WebSocket connection closed");
                onDataReceived("Disconnected from server.");
                socket = null; // Reset socket to null on close
            };
        }
    }

    // Function to handle WebSocket disconnection
    function disconnectWebSocket() {
        if (socket) {
            socket.close();
        }
    }

    // Watch for changes in isConnected
    $: if (isConnected) {
        connectWebSocket();
    } else {
        disconnectWebSocket();
        dmx_data = [];
    }

    // Cleanup on component destroy
    onMount(() => {
        return () => {
            disconnectWebSocket();
        };
    });
</script>

<div class="columns">
    <label for="111" class="column checkbox">Enable live sACN data:</label>
    <div class="column">
        <input type="checkbox" id="111" style="min-height:25px;min-width:25px;" bind:checked={isConnected} />
    </div>
</div>

{#if data}
    <div>{data}</div>
{/if}

{#if dmx_data.length}
    <div class="data-container">Rcvd: {dmx_data[1]}</div>
    <br />
    <div class="data-container">Sent: {dmx_data[2]}</div>
    <br />
{/if}

<style>
    .data-container {
        max-height: 150px; /* Set a fixed height for the container */
        overflow-y: auto; /* Enable vertical scrolling */
        white-space: pre-wrap; /* Preserve whitespace and wrap lines */
        word-wrap: break-word; /* Break long words if necessary */
        overflow-wrap: break-word; /* Break long words if necessary */
        padding: 10px; /* Optional: Add some padding */
        margin-right: 10px; /* Optional: Add some margin on top */
    }
</style>
