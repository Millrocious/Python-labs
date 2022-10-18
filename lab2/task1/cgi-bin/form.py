#!/usr/bin/env python3

from http import cookies
import os
import cgi
import html

form = cgi.FieldStorage()
x = int(form.getfirst("xxx", 0))
y = int(form.getfirst("yyy", 20))
test_input = html.escape(form.getfirst("test", ""))
if form.getvalue("dropdown"):
    course = form.getvalue("dropdown")
else:
    course = 'не обрано'

math = form.getvalue("maths")
physics = form.getvalue("physics")

checkbox_list = []
if math is not None:
    checkbox_list.append(math)

if physics is not None:
    checkbox_list.append(physics)

lang = form.getvalue("lang")

cs = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
if "count" in cs:
    count_cook = int(cs.get("count").value) + 1
    print(f"Set-cookie: count={count_cook}")
else:
    print(f"Set-cookie: count=0")
    count_cook = 0


def myfunc(x, y):
    result = str(list(range(x, y)))
    return result


agent = os.environ["HTTP_USER_AGENT"]

HTML = f'''<!DOCTYPE html>
<html lang="en-US">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width" />
    <title>My test page</title>
  </head>
  <body>
  <h1>Hello world!</h1>
  <h2>result {myfunc(x, y)}</h2>
  <p>{test_input}</p>
  <p>Selected: {course}</p>
  <p>Selected checkbox: {checkbox_list} </p>
  <p>Selected radio: [ {lang} ]</p>
  <h2>agent: {agent}</h2>
  <p>Cookie forms post requests count: {count_cook}</p>
  </body>
</html>'''

print("Content-type: text/html\n")
print(HTML)
print(form)
