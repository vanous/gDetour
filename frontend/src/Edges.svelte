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
    function createEdges() {
        let new_edges = [];

        const inputs = $nodes.filter((node) => node.type === "input");
        const outputs = $nodes.filter((node) => node.type === "output");

        inputs.forEach((input) => {
            outputs.forEach((output) => {
                if (input.address === output.address) {
                    new_edges.push({
                        source: input.id,
                        target: output.id,
                        id: `xy-edge__${input.id}-${output.id}`,
                        type: "button",
                    });
                }
            });
        });
        edges.set(new_edges);
    }
    function clearEdges() {
        edges.set([]);

        // makes output nodes connectable after clearing all mappings
        const outputs = $nodes.filter((node) => node.type === "output");
        outputs.forEach((output) => {
            output.connectable = true;
        });
        $nodes = $nodes;
    }
</script>

<div class="columns">
    <div class="column">
        <button class="button is-fullwidth" on:click={createEdges}
            >Auto Mapping
        </button>
    </div>
    <div class="column">
        <button class="button is-fullwidth" on:click={clearEdges}
            >Clear Mapping</button
        >
    </div>
</div>
