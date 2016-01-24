#!/bin/bash
screen -S flask-server -X quit
screen -S flask-server -d -m uwsgi -s /tmp/uwsgi.sock -w index:app  --chmod-socket=666
#screen uwsgi -s /tmp/uwsgi.sock -w index:app  --chmod-socket=666
