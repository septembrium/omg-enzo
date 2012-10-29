from bottle import route, run, request, response, redirect

def make_something(makefunction, a, b):
	print "making something now with %s and %s" % (a, b)
	return makefunction(a, b)

def plak_aaneen(a, b):
	return a + " en " +  b

def keerom_en_plak_aaneen(a, b):
	c = a[::-1] + " en " + b[::-1]
	return c

def check_login(name, password):
	if name == "Yoda" and password == "van StarWars":
		return True
	else:
		return False

@route('/hello')
def hello_again():
        count = int( request.cookies.get('counter', '0') )
        count += 1
        response.set_cookie('counter', str(count))
        return 'You visited %s times' % counti

@route('/wrong/url')
def wrong():
        redirect("http://www.google.com")

@route('/welcome')
def welcome():
        if request.get_cookie("visited"):
                return "Welcome back! Nice to see you again!"
        else:
                response.set_cookie("visited", "yes")
                return "hello, cookie set"

@route('/login', method='POST')
def login():
	name = request.forms.get('name')
	password = request.forms.get('password')
	if check_login(name, password):
		return "<p>correct it was, your login</p>"
	else:
		return "<p>failed, your attempt to log in is</p>"

@route('/login', method='GET')
def login_form():
	return '''
	<form action='/login' method='post'>
		<input name="name" type="text" />
		<input name="password" type="password" />
		<input name="submit" type="submit" />
	</form>
'''

@route('/hello/:name')
def hello_name(name="stranger"):
	return '<h1>Hello %s!</h1>' % name

@route('/:functie/:a/:b')
def experiment(functie, a, b):
	if functie == "plak":
		return make_something(plak_aaneen, a, b)
	elif functie == "smodder":
		return make_something(keerom_en_plak_aaneen, a, b)
	else:
		return "wtf zijt ge mee bezig!?"

@route('/:gottacatchemall')
def den_default(gottacatchemall):
	return "hoera, dit is geen route!"

run(host='localhost', port=8080)

