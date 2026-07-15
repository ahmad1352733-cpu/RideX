from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from db_helper import add_captain, add_passenger


ride = {

    "status": "waiting",

    "from": "",

    "to": "",

    "captain": {},

    "passenger_location": {
        "lat": 0,
        "lng": 0
    },

    "captain_location": {
        "lat": 0,
        "lng": 0
    }

}



class Handler(BaseHTTPRequestHandler):


    def send_cors(self):

        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        self.send_header(
            "Access-Control-Allow-Methods",
            "GET, POST, OPTIONS"
        )

        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type"
        )



    def do_OPTIONS(self):

        self.send_response(200)
        self.send_cors()
        self.end_headers()



    def do_GET(self):

        if self.path == "/ride":

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "application/json"
            )

            self.send_cors()

            self.end_headers()

            self.wfile.write(
                json.dumps(ride).encode()
            )



    def do_POST(self):

        global ride


        length = int(
            self.headers["Content-Length"]
        )


        data = json.loads(
            self.rfile.read(length)
        )



        if self.path == "/register_captain":


            add_captain(

                data["name"],
                data["phone"],
                data["car"],
                data["plate"],
                data["password"]

            )




        elif self.path == "/register_passenger":


            add_passenger(

                data["name"],
                data["phone"],
                data["password"]

            )




        elif self.path == "/request":


            ride["from"] = data["from"]

            ride["to"] = data["to"]

            ride["status"] = "waiting"

            ride["captain"] = {}




        elif self.path == "/location":


            ride["passenger_location"] = data




        elif self.path == "/captain_location":


            ride["captain_location"] = data




        elif self.path == "/accept":


            ride["status"] = "accepted"

            ride["captain"] = data




        elif self.path == "/start":


            ride["status"] = "started"




        elif self.path == "/finish":


            ride["status"] = "finished"





        self.send_response(200)

        self.send_cors()

        self.end_headers()





server = HTTPServer(

    ("0.0.0.0",9000),

    Handler

)



print("RIDEB Backend Running on 9000")


server.serve_forever()
