<!DOCTYPE HTML>
<html>
<head>
	<link type="text/css" rel="stylesheet" href="css/bootstrap.css" />
</head>
<body>
	<h1>QR Cube</h1>
	<form class="well span6" action="/generate" method="POST">
		<label>Content:</label>
		<input name="content" type="text" class="span3" /><br />
		<label>Alttag:</label>
		<input name="alttag" type="text" class="span3" /><br />
		<label>Titletag:</label>
		<input name="titletag" type="text" class="span3" /><br />
		<label>error correction level:</label>
		<input name="eclevel" type="text" class="span3" /><br />
		<label>author id:</label>
		<input name="author_id" type="text" class="span3" /><br />
		
		<button class="btn btn-primary">Submit</button>	
		<button class="btn">Clear</button>
	</form>
	
	<p class="span6">
		<strong>{{ error_msg }}</strong>
	</p>

	<script src="js/bootstrap.js"></script>
</body>
</html>
