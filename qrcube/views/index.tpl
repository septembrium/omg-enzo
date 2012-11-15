<!DOCTYPE HTML>
<html>
<head>
	<link type="text/css" rel="stylesheet" href="css/bootstrap.css" />
</head>
<body>
	<h1 class="well span6">QRCube landingpage</h1>
	<h2>log-in / register</h2>
	<form action="/login" method="POST">
	
	</form> 
	<h2 class="well span6">pick what the QR Code should do</h2>
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
