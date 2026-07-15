from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from db_helper import (
    add_captain,
    add_passenger,
    add_ride,
    get_waiting_rides,
    accept_ride,
    update_ride_status
)


ride = {

    "status": "waiting",

    "from": "",

    "to": "",

    "captain": {},

    "passenger_phone": "",

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

            return



        if self.path == "/rides":


            self.send_response(200)

            self.send_header(
                "Content-Type",
                "application/json"
            )

            self.send_cors()

            self.end_headers()


            self.wfile.write(
                json.dumps(
                    get_waiting_rides()
                ).encode()
            )

            return





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

            ride["passenger_phone"] = data.get(
                "phone",
                ""
            )

            ride["status"] = "waiting"


            add_ride(

                ride["passenger_phone"],

                ride["from"],

                ride["to"]

            )





        elif self.path == "/accept":


            accept_ride(

                data["ride_id"],

                data["phone"]

            )


            ride["status"] = "accepted"

            ride["captain"] = data





        elif self.path == "/start":


            update_ride_status(

                data["ride_id"],

                "started"

            )


            ride["status"] = "started"






        elif self.path == "/finish":


            update_ride_status(

                data["ride_id"],

                "finished"

            )


            ride["status"] = "finished"






        elif self.path == "/location":


            ride["passenger_location"] = data






        elif self.path == "/captain_location":


            ride["captain_location"] = data





        self.send_response(200)

        self.send_cors()

        self.end_headers()





server = HTTPServer(

    ("0.0.0.0",9000),

    Handler

)



print("RideX Backend Running on 9000")


server.serve_forever()
