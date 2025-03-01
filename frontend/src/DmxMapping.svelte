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
    import { edges, nodes, dmx_mapping} from './flow_stores.js';

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

</script>

<button  style="width: 200px;" class="button" on:click={sendMapping}>Apply Mapping</button>
