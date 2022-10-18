import cgi

form = b'''
<html>
    <head>
        <title>Hello User!</title>
    </head>
    <body>
        <form method="post">
            x: <input type="text" name="xxx"><br><br>
            y: <input type="text" name="yyy"><br><br>
            <input type="submit" value="Go">
        </form>
        Sum = 
    </body>
</html>
'''


def app(environ, start_response):
    html = form

    if environ['REQUEST_METHOD'] == 'POST':
        post_env = environ.copy()
        post_env['QUERY_STRING'] = ''
        post = cgi.FieldStorage(
            fp=environ['wsgi.input'],
            environ=post_env,
            keep_blank_values=True
        )
        try:
            suma = int(post['xxx'].value) + int(post['yyy'].value)
        except:
            suma = "Not a number values or some field is empty"

        html += f"{suma}".encode("utf-8")

    start_response('200 OK', [('Content-Type', 'text/html')])
    return [html]


if __name__ == '__main__':
    try:
        from wsgiref.simple_server import make_server

        httpd = make_server('', 8000, app)
        print('Serving on port 8000...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Goodbye.')
