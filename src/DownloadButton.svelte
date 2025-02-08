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
<script lang="ts">
    import { toPng } from "html-to-image";
    import {
        Panel,
        getNodesBounds,
        getViewportForBounds,
        useNodes,
    } from "@xyflow/svelte";

    const nodes = useNodes();

    const imageWidth = 2048;
    const imageHeight = 1536;

    function handleClick() {
        const nodesBounds = getNodesBounds($nodes);
        const viewport = getViewportForBounds(
            nodesBounds,
            imageWidth,
            imageHeight,
            0.5,
            2.0,
            0.2
        );

        const viewportDomNode = document.querySelector<HTMLElement>(
            ".svelte-flow__viewport"
        )!;

        if (viewport) {
            toPng(viewportDomNode, {
                backgroundColor: "#ffffff",
                width: imageWidth,
                height: imageHeight,
                style: {
                    width: `${imageWidth}px`,
                    height: `${imageHeight}px`,
                    transform: `translate(${viewport.x}px, ${viewport.y}px) scale(${viewport.zoom})`,
                },
            }).then((dataUrl) => {
                const link = document.createElement("a");
                link.download = "svelte-flow.png";
                link.href = dataUrl;
                link.click();
            });
        }
    }
</script>

<Panel position="top-right">
    <button on:click={handleClick}>Download Image</button>
</Panel>
