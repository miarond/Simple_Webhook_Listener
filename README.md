# Simple Webhook Listener

This project will enable a simple, lightweight Webhook listener server using Python Flask.

## Setup

Begin by installing the Python package requirements, using the following command:

*MacOS / Linux:*

```bash
pip3 install -r requirements.txt
```

*Windows:*

```powershell
py.exe -m pip install -r requirements.txt
```

## Usage

This script can accept one optional command line argument, which allows you to enable HTTPS with a self-signed SSL certificate:

*MacOS / Linux:*

```bash
python3 webhook_listener.py --help
usage: webhook_listener.py [-h] [-s]

This script will enable a simple Webhook listener server, using the Python Flask package.

options:
  -h, --help  show this help message and exit
  -s, --ssl   Configure Flask to use a self-signed SSL certificate and enable the HTTPS protocol.
```

*Windows:*

```powershell
py.exe webhook_listener.py --help
usage: webhook_listener.py [-h] [-s]

This script will enable a simple Webhook listener server, using the Python Flask package.

options:
  -h, --help  show this help message and exit
  -s, --ssl   Configure Flask to use a self-signed SSL certificate and enable the HTTPS protocol.
```

To run the script using unsecured HTTP only, you can simply execute it without any arguments:

```
% python3 webhook_listener.py
****************************
* All available app routes *
****************************

/static/<path:filename>
/webhook

****************************

==========================
= LISTENING ON PORT 5001 =
==========================

 * Serving Flask app 'webhook_listener'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5001
 * Running on http://10.0.0.1:5001
Press CTRL+C to quit
```
  > *For Windows, substitute `py.exe` in place of `python3` in the example above.*

Adding the `-s` option will cause Flask to use HTTPS instead:

```
****************************
* All available app routes *
****************************

/static/<path:filename>
/webhook

****************************

==========================
= LISTENING ON PORT 5001 =
==========================

 * Serving Flask app 'webhook_listener'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on https://127.0.0.1:5001
 * Running on https://10.0.0.1:5001
```

  > :warning: ***Note:*** *By default, Flask runs on TCP port 5000.  The script will automatically check if port 5000 is currently in use, and if it is the script increment the port number by 1 and check again.  This will continue in a loop until an open port is located, port 65,535 is reached, or the script is manually halted.*

The script will remain running, listening on the chosen TCP port, and will print out the contents of any HTTP message received at the URL `http://<ip_address>:<port>/webhook` (if SSL is enabled, the protocol will become `https://`).

## Examples

***Simple GET Request:***

```python
import requests

requests.get('http://10.0.0.1:5001/webhook')
```

```bash
========================================

Remote Host: 10.0.0.1
Host: 10.0.0.1:5001
User-Agent: python-requests/2.32.3
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive


b''

========================================

10.0.0.1 - - [20/Nov/2024 15:03:25] "GET /webhook HTTP/1.1" 200 -
```

***Simple POST Request:***

```python
import requests

requests.post('http://10.24.148.8:5001/webhook', json=[{"key": "value"}])
```

```bash
========================================

Remote Host: 10.0.0.1
Host: 10.0.0.1:5001
User-Agent: python-requests/2.32.3
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Content-Length: 18
Content-Type: application/json


[
    {
        "key": "value"
    }
]

========================================

10.0.0.1 - - [20/Nov/2024 15:08:06] "POST /webhook HTTP/1.1" 200 -
```

***HTTPS POST Request (non-JSON payload):***

```python
import requests

requests.post('https://10.0.0.1:5001/webhook', data='[{"key": "value"}]', verify=False)
```

```bash
========================================

Remote Host: 10.0.0.1
Host: 10.0.0.1:5001
User-Agent: python-requests/2.32.3
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Content-Length: 18


b'[{"key": "value"}]'

========================================

10.0.0.1 - - [20/Nov/2024 15:11:55] "POST /webhook HTTP/1.1" 200 -
```