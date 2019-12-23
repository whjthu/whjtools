#!/bin/bash

./memUsage.py &
#./signaltest.py &
pid=$!
sleep 3
kill $pid
sleep 1
kill -9 $pid
