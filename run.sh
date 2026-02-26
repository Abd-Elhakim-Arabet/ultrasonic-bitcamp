#!/bin/bash
cd "$(dirname "$0")"

# create venv if missing and activate it
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# install flask
pip install flask

# clean old database
rm -f readings.db

# start sensor simulator in background
python3 ultrasonic.py &
SENSOR_PID=$!

# start web server
echo "Sensor running (PID $SENSOR_PID)"
echo "Open http://192.168.x.x:5000 in your browser"
python3 app.py

# cleanup on exit
kill $SENSOR_PID 2>/dev/null
