<html>
<head>
<title>test page</title>
</head>
<body>
<h1>list of records</h1>
<ol>
%for i in range(0, len(the_records)):
<li>{{ the_records[i] }}</li>
%end
</ol>
</body>
</html>
