#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import config
import email
import fbchat

EX_TEMPFAIL=75
EX_UNAVAILABLE=69

if len(sys.argv) < 2:
    print("Usage: %s MAIL" % (sys.argv[0]))
    sys.exit(EX_TEMPFAIL)
if sys.argv[1] in config.ADDRESS_MAP:
    msggrp = config.ADDRESS_MAP[sys.argv[1]]
else:
    print("%s: address map not found" % (sys.argv[1]))
    sys.exit(EX_UNAVAILABLE)

mail = ''.join(sys.stdin.readlines())
parser = email.parser.Parser()
content = parser.parsestr(mail)

if content.is_multipart():
    for payload in content.get_payload():
        if payload.get_content_type() == 'text/plain':
            data = payload.get_payload(decode=True)
elif content.get_content_type() == 'text/plain':
    data = content.get_payload(decode=True)

client = fbchat.Client(config.ACCOUNT, config.PASSWORD, False)
sent = client.send(msggrp[0], data, msggrp[1])
