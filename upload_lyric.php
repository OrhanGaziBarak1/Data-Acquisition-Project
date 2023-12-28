<?php include("header2.php"); ?>
<!-- Main -->
<section id="main" class="container medium">
    <header>
        <br>
        <br>
        <h2>Lyric Upload</h2>
        <br>
        <br>
        <form id="uploadForm" enctype="multipart/form-data">
            <input
                name="file"
                type="file"
                multiple
                type="file" name="file" accept=".txt" />
            <button type="button" onclick="uploadFiles()">Upload</button>
        </form>

        <progress value="0" max="100"></progress>

        <p>
            <strong>Uploading status:</strong>
            <span id="statusMessage">🤷‍♂ Nothing's uploaded</span>
        </p>

        <p>
            <strong>Uploaded files:</strong>
            <span id="fileNum">0</span>
        </p>

        <ul id="fileListMetadata"></ul>
    </header>
</section>
<!-- Footer -->
<?php include("footer.php"); ?>
<script src="upload_lyric.js"></script>
