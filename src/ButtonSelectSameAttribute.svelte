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
    import { edges, nodes, dmx_mapping } from "./flow_stores.js";
    import { Panel } from "@xyflow/svelte";
    let singleSelected = false;
    let selectedAttributeCount;
    let selectedAttributeName;

    function singleOutputSelected() {
        const outputs = $nodes.filter(
            (node) => node.type === "output" && node.selected
        );
        console.log("check single output", outputs.length);

        if (outputs.length == 1) {
            const output = outputs[0];
            selectedAttributeName = output.attribute;
            return true;
        } else {
            selectedAttributeName = null;
            return false;
        }
    }

    function selectSameNodes() {
        const outputs = $nodes.filter(
            (node) => node.type === "output" && node.selected
        );
        console.log("selecting same nodes", outputs);

        if (outputs.length != 1) {
            return;
        }
        selectedAttributeName = outputs[0].attribute;

        console.log("selected attribute", selectedAttributeName);
        const unconnectedNodes = $nodes.filter(
            (node) =>
                !$edges.some(
                    (edge) => edge.source === node.id || edge.target === node.id
                ) &&
                node.type === "output" &&
                node.attribute === selectedAttributeName
        );
        selectedAttributeCount = unconnectedNodes.length;
        singleSelected = false;
        console.log("nodes ready", unconnectedNodes);
        unconnectedNodes.forEach((node) => {
            node.selected = true; // or node.selected = true; depending on your data structure
        });
    }

    $: if (singleOutputSelected($nodes)) {
        singleSelected = true;
        selectedAttributeCount = null;
    } else {
        selectedAttributeCount = null;
        singleSelected = false;
    }
</script>

<button
    class="button"
    disabled={!singleSelected}
    on:click={selectSameNodes}
    title="Selects other unconnected Output nodes with the same attribute as a single selected Output node."
>
    {#if singleSelected}
        Click to select all {selectedAttributeName}
    {:else if selectedAttributeCount}
        Selected {selectedAttributeCount} {selectedAttributeName}
    {:else}
        Select Outputs with same attribute
    {/if}
</button>
