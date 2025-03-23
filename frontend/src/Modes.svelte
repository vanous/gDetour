<!--

    Copyright (C) 2025 Kwimbee, vanous

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
    import { edges, nodes, dmx_mapping } from "./flow_stores.js";
    import {
        SvelteFlow,
        Controls,
        Background,
        BackgroundVariant,
        Position,
    } from "@xyflow/svelte";
    import { onMount } from "svelte";
    export let node_mode;
    let fixture = "";
    let modes = [];
    let mode = [];
    let fixtures = [];
    let new_nodes = [];
    let old_nodes = [];
    let default_dmx = [];

    async function fetchUploadedFiles() {
        try {
            const response = await fetch("/files");
            if (response.ok) {
                const result = await response.json();
                fixtures = result.files;
                console.log(fixtures);
            } else {
                console.error("Failed to fetch uploaded files.");
            }
        } catch (error) {
            console.error("Error fetching uploaded files:", error);
        }
    }

    async function getModes() {
        try {
            const response = await fetch("/modes", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ fixture: fixture }),
            });
            const data = await response.json();
            modes = data.data;
            console.log("Success:", modes);
        } catch (error) {
            console.error("Error:", error);
        }
    }

    async function sendDefault() {
        try {
            const response = await fetch("/default", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(default_dmx),
            });
            const data = await response.json();
            console.log("Success:", data);
        } catch (error) {
            console.error("Error:", error);
        }
    }
    function getMode() {
        console.log("mode", mode);
        new_nodes = [];
        let node_x;
        let node_y;
        let node_position;
        let node_type;
        let node_i;
        let node_edge;
        default_dmx = [];
        const inputs = $nodes.filter((node) => node.type === "input");
        const outputs = $nodes.filter((node) => node.type === "output");

        // Determine node properties based on node_mode
        if (node_mode === "input") {
            node_x = 0;
            node_y = 50;
            node_position = Position.Right;
            node_type = "input";
            node_i = "i";
            node_edge = "sourcePosition";
            old_nodes = outputs; //keep the other side
        } else {
            node_x = 500;
            node_y = 50;
            node_position = Position.Left;
            node_type = "output";
            node_i = "o";
            node_edge = "targetPosition";
            old_nodes = inputs; //keep the other side
        }
        mode.forEach((item, index) => {
            new_nodes.push({
                id: node_i + item.dmx,
                dmx: item.dmx,
                default: item.default,
                attribute: item.attribute,
                geometry: item.geometry,
                type: node_type,
                [node_edge]: node_position,
                data: {
                    label: `${item.dmx} ${item.geometry}: ${item.attribute}`,
                },
                address: `${item.geometry}_${item.attribute}`,
                position: { x: node_x, y: node_y * index },
                connectable: true,
            });

            console.log(
                `DMX: ${item.dmx}, Geo: ${item.geometry}, Attr: ${item.attribute}`
            );
            default_dmx.push(item.default);
        });
        console.log("nodes", new_nodes);
        set_nodes();

        if (node_mode === "output") {
            sendDefault();
        }
    }

    function set_nodes() {
        $nodes = [...new_nodes, ...old_nodes];
    }
    onMount(() => {
        fetchUploadedFiles(); // Fetch the list of uploaded files on component mount
    });
</script>

<div class="columns">
    <div class="column">
        <!-- Adjust column size as needed -->
        <div class="select is-fullwidth">
            <select
                bind:value={fixture}
                on:change={getModes}
                on:focus={fetchUploadedFiles}
            >
                <option value="" disabled selected
                    >Select {node_mode} fixture</option
                >
                {#each fixtures as item}
                    <option value={item}>{item.slice(0, -5)}</option>
                {/each}
            </select>
        </div>
    </div>

    <div class="column">
        <!-- Adjust column size as needed -->
        <div class="select is-fullwidth">
            <!-- Added is-fullwidth here -->
            <select bind:value={mode} on:change={getMode}>
                {#each modes as item}
                    <option value={item.dmx_channels}>
                        {item.name} ({item.dmx_channels_count}ch)
                    </option>
                {/each}
            </select>
        </div>
    </div>
</div>
