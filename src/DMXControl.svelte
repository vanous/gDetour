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
    import { onMount } from "svelte";
    let result = "";
    let sacn_settings = [1, 2, "127.0.0.1"]; // Array to hold two selected numbers
    let network_interfaces = [];

    function handleSelectChange(index, event) {
        console.log("handle", event.target.value);
        sacn_settings[index] = Number(event.target.value);
        result = "Applying settings";
        sendSettings();
    }
    function handleNetworkChange(index, event) {
        console.log("handle", event.target.value);
        sacn_settings[index] = event.target.value;
        result = "Applying settings";
        sendSettings();
    }
    async function fetchNetworkInterfaces() {
        try {
            const response = await fetch("/interfaces");
            if (response.ok) {
                const result = await response.json();
                network_interfaces = result.data;
                if (network_interfaces.length) {
                    sacn_settings[2] = network_interfaces[0][0];
                }
                console.log(network_interfaces);
            } else {
                console.error("Failed to fetch network interfaces.");
            }
        } catch (error) {
            console.error("Error fetching network interfaces:", error);
        }
    }

    async function getSettings() {
        try {
            const response = await fetch("/sacn");
            if (response.ok) {
                const res = await response.json();
                result = res.status
                const data = res.data;
                if (data.length) {
                    sacn_settings = data;
                }
                console.log(network_interfaces);
            } else {
                console.error("Failed to fetch network interfaces.");
            }
        } catch (error) {
            console.error("Error fetching network interfaces:", error);
        }
    }
    async function sendSettings() {
        console.log("settings", sacn_settings);
        try {
            const response = await fetch("/sacn", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(sacn_settings),
            });
            const data = await response.json();
            result = data.status;
            console.log("Success:", result);
        } catch (error) {
            console.error("Error:", error);
        }
    }
    function startReceiver() {
        fetch("/start_receiver", { method: "POST" })
            .then((response) => response.json())
            .then((data) => {
                result = data.status;
            })
            .catch((error) => {
                console.error("Error:", error);
            });
    }

    function stopReceiver() {
        fetch("/stop_receiver", { method: "POST" })
            .then((response) => response.json())
            .then((data) => {
                result = data.status;
            })
            .catch((error) => {
                console.error("Error:", error);
            });
    }

    function startSender() {
        fetch("/start_sender", { method: "POST" })
            .then((response) => response.json())
            .then((data) => {
                result = data.status;
            })
            .catch((error) => {
                console.error("Error:", error);
            });
    }

    function stopSender() {
        fetch("/stop_sender", { method: "POST" })
            .then((response) => response.json())
            .then((data) => {
                result = data.status;
            })
            .catch((error) => {
                console.error("Error:", error);
            });
    }

    onMount(() => {
        console.log("mount dmx control");
        fetchNetworkInterfaces();
        getSettings();
    });
</script>

<!--

<div class="data">
    <div>
        <button style="width: 200px;" class="button" on:click={startReceiver}
            >Start Receiver</button
        >
        <button style="width: 200px;" class="button" on:click={stopReceiver}
            >Stop Receiver</button
        >
    </div>

    <div>
        <button style="width: 200px;" class="button" on:click={startSender}
            >Start Sender</button
        >
        <button style="width: 200px;" class="button" on:click={stopSender}
            >Stop Sender</button
        >
        </div>
</div>
-->

<div class="columns">
    <div class="column line">Receiving Universe:</div>
    <div class="column">
        <div class="select">
            <select
                id="receiving"
                style="width: 80px;"
                on:change={(event) => handleSelectChange(0, event)}
                bind:value={sacn_settings[0]}
            >
                <option value="" disabled>Select a number</option>
                {#each Array(10) as _, number}
                    <option value={number + 1}>{number + 1}</option>
                {/each}
            </select>
        </div>
    </div>
</div>
<div class="columns">
    <div class="column line">Sending Universe:</div>
    <div class="column">
        <div class="control is-inline">
            <div class="select">
                <select
                    id="sending"
                    style="width: 80px;"
                    on:change={(event) => handleSelectChange(1, event)}
                    bind:value={sacn_settings[1]}
                >
                    <option value="" disabled>Select a number</option>
                    {#each Array(10) as _, number}
                        <option value={number + 1}>{number + 1}</option>
                    {/each}
                </select>
            </div>
        </div>
    </div>
</div>
<div class="columns">
    <div class="column line">Network Interface:</div>
    <div class="column">
        <div class="select">
            <select
                on:change={(event) => handleNetworkChange(2, event)}
                bind:value={sacn_settings[2]}
            >
                {#each network_interfaces as item}
                    <option value={item[0]}>{item[1]}: {item[0]}</option>
                {/each}
            </select>
        </div>
    </div>
</div>
<div class="columns">
    <div class="column">
        <div>{JSON.stringify(result)}</div>
    </div>
</div>

<style>
    .line {
        line-height: 2.5;
    }
</style>
