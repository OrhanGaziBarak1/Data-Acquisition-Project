<?php

include("header2.php");
?>
<!-- Main -->
<section id="main" class="container medium">
    <header>
        <br>
        <br>
        <h2>File Upload</h2>
        <br>
        <br>
        <form>
    <input
      name="file"
      type="file"
      multiple
      type="file" name="file" accept=".mp3"    />
    <button type="submit">Upload</button>
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

<!-- Footer -->
<?php 

include("footer.php"); ?>

<script src="upload_sound.js"></script>
