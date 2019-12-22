#!/bin/bash

./memUsage.py &
#./signaltest.py &
pid=$!
sleep 3
kill $pid
