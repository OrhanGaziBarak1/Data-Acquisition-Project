<?php

include("header2.php");
?>
<!-- Main -->
<section id="main" class="container medium">
    <header>
        <br>
        <br>
        <h2>Music Upload</h2>
        <br>
        <br>
        <form method="post" enctype="multipart/form-data">
      <input type="file" name="files[]" multiple />
      <input type="submit" value="Upload File" name="submit" />
    </form>


<?php include("footer.php"); ?>

<script src="upload_music.js"></script>
