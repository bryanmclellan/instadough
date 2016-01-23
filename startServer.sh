#!/bin/bash
screen uwsgi -s /tmp/uwsgi.sock -w index:app  --chmod-socket=666
