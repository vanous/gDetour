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
    import { useSvelteFlow } from "@xyflow/svelte";
    import { edges, nodes, dmx_mapping } from "./flow_stores.js";
    import { Panel } from "@xyflow/svelte";

    import {
        SvelteFlow,
        Controls,
        Background,
        BackgroundVariant,
        Position,
    } from "@xyflow/svelte";

    import ButtonEdge from "./ButtonEdge.svelte";
    const edgeTypes = {
        button: ButtonEdge,
    };
    import "@xyflow/svelte/dist/style.css";
    import ButtonOneToMany from "./ButtonOneToMany.svelte";
    import ButtonSelectSameAttribute from "./ButtonSelectSameAttribute.svelte";

    const removeNode = (node) => {
        setElements((els) => removeElements([node], els));
    };

    async function sendMapping() {
        try {
            const response = await fetch("/dmx_mapping", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify($dmx_mapping),
            });
            const data = await response.json();
            console.log("Success:", data);
        } catch (error) {
            console.error("Error:", error);
        }
    }

    $: update_dmx_mapping($edges);

    function update_dmx_mapping() {
        console.log("updating", edges);

        let new_dmx_mapping = [];
        $edges.forEach((edge) => {
            let x = Number(edge.source.replace("i", ""));
            let y = Number(edge.target.replace("o", ""));
            //new_dmx_mapping[x] = y;
            new_dmx_mapping.push([x, y]);
            edge.type = "button"; // for the remove button

            const output_node = $nodes.find((node) => node.id === edge.target);
            output_node.connectable = false;
        });
        dmx_mapping.set(new_dmx_mapping);
        console.log("dmx mapping", dmx_mapping);

        $edges = $edges;
        $nodes = $nodes;

        sendMapping();
    }
    const snapGrid = [25, 25];
    const proOptions = { hideAttribution: true };
</script>

<div style="height:100vh;">
    <SvelteFlow {nodes} {edges} {edgeTypes} {snapGrid} {proOptions} fitView>
        <Controls />

        <Panel position="top-right">
            <ButtonOneToMany />
        </Panel>
        <Panel position="bottom-right">
            <ButtonSelectSameAttribute />
        </Panel>
        <Background bgColor="#1d72aa" variant={BackgroundVariant.Dots} />
    </SvelteFlow>
</div>

<!-- 
<div>{JSON.stringify($edges)}</div>
<div>{JSON.stringify($dmx_mapping)}</div>
-->

<style>
    :global(.svelte-flow .svelte-flow__node) {
        border-radius: 0%;
        background-color: #fff;
        height: 5px;
        width: 200px;
        display: flex;
        align-items: center;
    }
</style>
