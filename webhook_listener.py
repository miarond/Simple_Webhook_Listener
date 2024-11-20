"""
Copyright (c) 2023 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

__author__ = "Aron Donaldson <ardonald@cisco.com>"
__contributors__ = ""
__copyright__ = "Copyright (c) 2023 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

import json
import socket
from argparse import ArgumentParser
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/webhook', methods=['POST', 'PUT', 'PATCH', 'GET'])
def webhook_handler():
    print('\n' + ('=' * 40) + '\n')
    print(f'Remote Host: {request.remote_addr}')
    print(request.headers)
    if request.is_json:
        print(json.dumps(request.json, indent=4))
    else:
        print(request.data)
    print('\n' + ('=' * 40) + '\n')
    return Response(status=200)


def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

if __name__ == '__main__':
    parser = ArgumentParser(description='This script will enable a simple Webhook listener server, using the Python Flask package.')
    parser.add_argument('-s', '--ssl', help='Configure Flask to use a self-signed SSL certificate and enable the HTTPS protocol.', action='store_true')
    args = parser.parse_args()

    # Print all app routes
    print("****************************\n* All available app routes *\n****************************\n")
    for rule in app.url_map.iter_rules():
        print(rule)
    print("\n****************************\n")
    
    # By default, Flask runs on port 5000 on the loopback IP (127.0.0.1)
    port = 5000
    while is_port_in_use(port) and port <= 65535:
        port += 1
    print(f'==========================\n= \033[1mLISTENING ON PORT {port}\033[0m =\n==========================\n')
    if args.ssl:
        app.run(host='0.0.0.0', port=port, ssl_context='adhoc')
    else:
        app.run(host='0.0.0.0', port=port)
