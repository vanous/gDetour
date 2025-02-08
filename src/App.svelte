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
    //import "./mybulma.scss";
    import "bulma/css/bulma.css";
    import WebSocketHandler from "./WebSocketHandler.svelte";
    import DMXControl from "./DMXControl.svelte";
    import Flow from "./Flow.svelte";
    import DmxMapping from "./DmxMapping.svelte";
    import GdtfFile from "./GdtfFile.svelte";
    import Modes from "./Modes.svelte";
    import Edges from "./Edges.svelte";
    import Mappings from "./Mappings.svelte";

    let showExtras = false;
    let dmx_mapping = [];
    let flow_nodes = [];
    function toggleExtras() {
        showExtras = !showExtras;
    }
</script>

<div class="columns">
    <div class="column is-4 has-background-success">
        <div class="title is-2 has-text-centered">gDetour</div>
        <div class="extras-container" class:hidden={showExtras}>
            <Modes node_mode="input" />
            <Modes node_mode="output" />
            <Edges />
            <Mappings />
        </div>
        <div class="extras-container" class:hidden={!showExtras}>
            <WebSocketHandler />
            <DMXControl />
            <GdtfFile />
        </div>
        <div class="columns">
            <div class="column">
                <button class="button is-fullwidth" on:click={toggleExtras}>
                    {showExtras ? "Hide Extras" : "Show Extras"}
                </button>
            </div>
        </div>
    </div>

    <div class="column has-background-info-dark">
        <Flow bind:dmx_mapping />
    </div>
</div>

<style>
    .hidden {
        display: none;
    }
</style>
