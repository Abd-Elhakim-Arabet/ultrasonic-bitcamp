from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return """<!DOCTYPE html>
<html><head><title>Ultrasonic Sensor</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>body{font-family:sans-serif;max-width:900px;margin:40px auto;text-align:center}</style>
</head><body>
<h2>Ultrasonic Sensor Readings</h2>
<canvas id="chart"></canvas>
<script>
const ctx = document.getElementById('chart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Distance (cm)', data: [], borderColor: '#3b82f6', tension: 0.3, fill: false }] },
    options: { scales: { y: { beginAtZero: true, title: { display: true, text: 'cm' } }, x: { title: { display: true, text: 'Time' } } }, animation: false }
});

setInterval(async () => {
    const res = await fetch('/data');
    const rows = await res.json();
    chart.data.labels = rows.map(r => r.time);
    chart.data.datasets[0].data = rows.map(r => r.distance);
    chart.update();
}, 1000);
</script>
</body></html>"""

@app.route("/data")
def data():
    db = sqlite3.connect("readings.db")
    rows = db.execute("SELECT timestamp, distance FROM readings ORDER BY id DESC LIMIT 50").fetchall()
    db.close()
    rows.reverse()
    from datetime import datetime
    return jsonify([{"time": datetime.fromtimestamp(r[0]).strftime("%H:%M:%S"), "distance": round(r[1], 1)} for r in rows])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
