<!DOCTYPE HTML>
<html>
<head>
	<link type="text/css" rel="stylesheet" href="css/bootstrap.css" />
</head>
<body>
	<h1>QR Code BATTLE</h1>
	<form class="well span6" action="/battle" method="POST">
		<label>Idea 1:</label>
		<input name="comp1" type="text" class="span3" placeholder="competing idea 1 goed here ..." /><br />
		<label>Idea 2:</label>
		<input name="comp2" type="text" class="span3" placeholder="competing idea 2 text here ..." /><br />
		<button class="btn btn-primary">Submit</button>	
		<button class="btn">Clear</button>
	</form>
	
	<p class="span6">
		<strong>{{ error_msg }}</strong>
	</p>

	<script src="js/bootstrap.js"></script>
</body>
</html>
