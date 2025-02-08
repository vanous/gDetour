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
    let selectedForInOutConnection = false;
    let singleSelectedAttribute = null
    let manySelectedCount = null

    function createEdges() {
        const inputs = $nodes.filter(
            (node) => node.type === "input" && node.selected
        );
        const outputs = $nodes.filter(
            (node) => node.type === "output" && node.selected
        );
        if (!(inputs.length == 1 && outputs.length > 0)) {
            return;
        }
        let new_edges = [];

        inputs.forEach((input) => {
            outputs.forEach((output) => {
                new_edges.push({
                    source: input.id,
                    target: output.id,
                    id: `xy-edge__${input.id}-${output.id}`,
                    type: "button",
                });
            });
        });
        edges.set([...new_edges, ...$edges]);
    }


    function checkSelected() {
        const inputs = $nodes.filter(
            (node) => node.type === "input" && node.selected
        );
        console.log("inputs", inputs, inputs.length);
        const outputs = $nodes.filter(
            (node) => node.type === "output" && node.selected
        );
        console.log("outputs", outputs, outputs.length);
        const sel = inputs.length == 1 && outputs.length > 0;
        console.log("check selected", sel);
        if (inputs.length == 1 && outputs.length > 0){
            let input = inputs[0]
            singleSelectedAttribute = input.attribute
            manySelectedCount = outputs.length
            return true
        }else{
            singleSelectedAttribute = null
            manySelectedCount = null
            return false
        }
    }
    $: if (checkSelected($nodes)) {
        selectedForInOutConnection = true;
    } else {
        selectedForInOutConnection = false;
    }
</script>

    <button
        class="button"
        disabled={!selectedForInOutConnection}
        on:click={createEdges}
        title="Select exactly one Input channel and one or more Output channels. Use Shift and Shift Control for multiple selection."
        >{singleSelectedAttribute? "Connect " + singleSelectedAttribute + " to " + manySelectedCount + " nodes" : "Connect One to Many"}</button
    >
