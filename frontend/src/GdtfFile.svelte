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
    let files = [];
    let uploadedFiles = [];
    let status = "";

    async function fetchUploadedFiles() {
        try {
            const response = await fetch("/files");
            if (response.ok) {
                const result = await response.json();
                uploadedFiles = result.files;
            } else {
                console.error("Failed to fetch uploaded files.");
            }
        } catch (error) {
            console.error("Error fetching uploaded files:", error);
        }
    }
    async function uploadFiles(selectedFiles) {
        status = ""
        const formData = new FormData();
        Array.from(selectedFiles).forEach((file) => {
            formData.append("files", file);
        });

        try {
            const response = await fetch("/upload", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                const result = await response.json();
                status = "Files uploaded successfully: " + result.filenames.join( ", ")
            } else {
                status = "File upload failed.";
            }
        } catch (error) {
            console.error("Error uploading files:", error);
            status = "An error occurred while uploading the files.";
        }
        fetchUploadedFiles();
    }

    function handleFileChange(event) {
        const selectedFiles = event.target.files;
        if (selectedFiles.length > 0) {
            uploadFiles(selectedFiles);
        }
    }
    onMount(() => {
        //fetchUploadedFiles(); // Fetch the list of uploaded files on component mount
    });
</script>

<div class="columns">
    <div class="column">
        <label class="file file-label button has-text-centered">
            <input
                class="file-input"
                type="file"
                name="resume"
                id="gdtfinput"
                accept=".gdtf"
                on:change={handleFileChange}
                multiple
            />
            Upload GDTF Files
        </label>
    </div>
</div>

<div class="columns">
    <div class="column">
        <div>{status}</div>
    </div>
</div>
