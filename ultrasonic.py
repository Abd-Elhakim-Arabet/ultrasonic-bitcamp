import time
import RPi.GPIO as GPIO
import sqlite3

TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

db = sqlite3.connect("readings.db")
db.execute("CREATE TABLE IF NOT EXISTS readings (id INTEGER PRIMARY KEY, timestamp REAL, distance REAL)")
db.commit()

try:
    while True:
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            start = time.time()
        while GPIO.input(ECHO) == 1:
            end = time.time()

        distance = (end - start) * 17150
        distance = round(distance, 1)

        db.execute("INSERT INTO readings (timestamp, distance) VALUES (?, ?)", (time.time(), distance))
        db.commit()
        print(f"{distance:.1f} cm")
        time.sleep(0.5)

except KeyboardInterrupt:
    db.close()
    GPIO.cleanup()
    print("\nStopped.")