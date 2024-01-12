#!/bin/bash

pwd # run in root directory

cd dsd_chat
./runserver &
./runtw &

cd ../worker
./server.py &