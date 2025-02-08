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
    import { edges } from "./flow_stores.js";
    import { onMount } from "svelte";
    let filename_load = "";
    let filename_save = "";
    let filenames = [];

    async function saveMapping() {
        try {
            console.log("mapping", $edges, "filename", filename_save);
            const response = await fetch("/mapping_save", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    mapping: $edges,
                    filename: filename_save,
                }),
            });
            const data = await response.json();
            console.log("Success:", data);
        } catch (error) {
            console.error("Error:", error);
        }
        fetchUploadedFiles();
    }

    async function getMapping() {
        try {
            const response = await fetch("/mapping_get", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    filename: filename_load,
                }),
            });
            const data = await response.json();
            $edges = data.mapping;
            console.log("Success:", data);
        } catch (error) {
            console.error("Error:", error);
        }
    }

    async function fetchUploadedFiles() {
        try {
            const response = await fetch("/mapping_list");
            if (response.ok) {
                const result = await response.json();
                filenames = result.files;
                console.log(filenames);
            } else {
                console.error("Failed to fetch uploaded files.");
            }
        } catch (error) {
            console.error("Error fetching uploaded files:", error);
        }
    }

    onMount(() => {
        fetchUploadedFiles(); // Fetch the list of uploaded files on component mount
    });
</script>

<div class="columns">
    <div class="column">
        <input
            class="input"
            mid="textInput"
            placeholder="FileName"
            type="text"
            bind:value={filename_save}
        />
    </div>
    <div class="column">
        <button
            disabled={!$edges.length || filename_save == ""}
            class="button is-fullwidth"
            on:click={saveMapping}>Save Mapping</button
        >
    </div>
</div>
<div class="columns">
    <div class="column">
        <div class="select is-fullwidth">
            <select bind:value={filename_load}>
                <option value="" disabled selected>Select Mapping</option>
                {#each filenames as item}
                    <option value={item}>{item.slice(0, -5)}</option>
                {/each}
            </select>
        </div>
    </div>
    <div class="column">
        <button
            class="button is-fullwidth"
            on:click={getMapping}
            disabled={filename_load == ""}>Load Mapping</button
        >
    </div>
</div>
