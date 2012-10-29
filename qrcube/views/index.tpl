<!DOCTYPE HTML>
<html>
<head>
	<link type="text/css" rel="stylesheet" href="css/bootstrap.css" />
</head>
<body>
	<h1>QR Code Generator</h1>
	<form class="well span6" action="/generate" method="POST">
		<label>QR Code text:</label>
		<input name="qrtext" type="text" class="span3" placeholder="enter text here ..." /><br />
		<button class="btn btn-primary">Submit</button>	
		<button class="btn">Clear</button>
	</form>
	
	<p class="span6">
		<strong>{{ error_msg }}</strong>
	</p>

	<script src="js/bootstrap.js"></script>
</body>
</html>
