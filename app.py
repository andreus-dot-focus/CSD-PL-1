from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server
import json
import datetime
import pytz
from tzlocal import get_localzone

all_tz = pytz.all_timezones

def time_handler(tz = get_localzone(),date = pytz.utc.localize(datetime.datetime.utcnow())):
    if date is time_handler.__defaults__[1]:
        return date.astimezone(tz)
    if date is not time_handler.__defaults__[1]:
        return tz.localize(date)

def app(environ, start_response):
    ok = '200 OK'
    not_found = '404 NOT FOUND'
    html_type = [('Content-type', 'text/html')]
    json_type = [('Content-type', 'application/json')]

    setup_testing_defaults(environ)
    if environ['REQUEST_METHOD'] == 'GET':
        if environ['PATH_INFO'] == '/':

            start_response(ok, html_type)
            return [(
                    '''<body>
                        <h2>LOCAL TIME</h2>
                        <time>''' +str(time_handler())[:16]+ '''</time>
                    </body> '''
                        ).encode()]


        if environ['PATH_INFO'][1:] in all_tz:
            start_response(ok, html_type)
            required_tz = pytz.timezone(environ['PATH_INFO'][1:])
            return [(
                    '''<body>
                        <h2>''' + environ['PATH_INFO'][1:] + '''</h2>
                        <time>''' +str(time_handler(required_tz))[:16]+ '''</time>
                    </body> '''
                        ).encode()]
        else:
            start_response(not_found, html_type)
            return [(
                    '''<body>
                        <h2>WRONG TZ</h2>
                        <h3>TZ LIST:</h3>
                        <time>''' +str(all_tz)+ '''</time>
                    </body> '''
                        ).encode("utf-8")]

    if environ['REQUEST_METHOD'] == 'POST':
        try:
            try:
                request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            except (ValueError):
                request_body_size = 0

            request_body = environ['wsgi.input'].read(request_body_size)
            body = json.loads(request_body)
        except:
            start_response(not_found, json_type)
            data = json.dumps({"Error:":'DATA NOT FOUND'})
            return data.encode().splitlines()

        if environ['PATH_INFO'] == '/api/v1/date':
            try:
                tz = body['tz']
            except:
                start_response(ok, json_type)
                data = json.dumps({"Answer:":str(time_handler())[:10]})
                return data.encode().splitlines()
            if tz in all_tz:
                start_response(ok, json_type)
                required_tz = pytz.timezone(tz)
                data = json.dumps({"Answer:":str(time_handler(required_tz))[:10]})
                return data.encode().splitlines()
            else:
                start_response(not_found, json_type)
                data = json.dumps({"Error:":'tz not found'})
                return data.encode().splitlines()

        if environ['PATH_INFO'] == '/api/v1/time':
            try:
                tz = body['tz']
            except:
                start_response(ok, json_type)
                data = json.dumps({"Answer:":str(datetime.datetime.time(time_handler()))[:8]})
                return data.encode().splitlines()

            if tz in all_tz:
                    start_response(ok, json_type)
                    required_tz = pytz.timezone(tz)
                    data = json.dumps({"Answer:":str(datetime.datetime.time(time_handler(required_tz)))[:8]})
                    return data.encode().splitlines()
            else:
                start_response(not_found, json_type)
                data = json.dumps({"Error:":'tz not found'})
                return data.encode().splitlines()


        if environ['PATH_INFO'] == '/api/v1/datediff':
            try:
                start_date = datetime.datetime.strptime(body['start']['date'], '%m.%d.%Y %H:%M:%S')
                if 'tz' in body['start']:
                    start_tz = pytz.timezone(body['start']['tz'])
                    start_date = time_handler(start_tz,start_date)
                else:
                    start_date = time_handler(date = start_date)

                end_date = datetime.datetime.strptime(body['end']['date'], '%m.%d.%Y %H:%M:%S')
                if 'tz' in body['end']:
                    end_tz = pytz.timezone(body['end']['tz'])
                    end_date = time_handler(end_tz,end_date)
                else:
                    end_date = time_handler(date=end_date)
            except:
                start_response(not_found, json_type)
                data = json.dumps({"Error:":'BAD DATA'})
                return data.encode().splitlines()

            delta = start_date - end_date
            start_response(ok, json_type)
            data = json.dumps({"Answer:": str(delta)})
            return data.encode().splitlines()

        else:
            start_response(not_found, json_type)
            data = json.dumps({"Error:":'API NOT FOUND'})
            return data.encode().splitlines()

def main():
    httpd = make_server('', 8080, app)
    print("Serving on port 8080...")
    httpd.serve_forever()

main()
