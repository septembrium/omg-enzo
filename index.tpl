<html>
<head>
<title>qrcode gen</title>
</head>
<body>
<h1>qrcode gen</h1>
<p>Knock yourself out! Generate a QR Code!</p>
<form action="/generate" method="POST">
text: <input type="text" name="qrtext" />
<input type="submit" label="generate now" />
</form>
<h2>{{ error_msg }}</h2>
<body>
</html>
