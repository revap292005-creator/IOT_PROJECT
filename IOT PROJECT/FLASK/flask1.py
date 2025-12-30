from flask import Flask
import mysql.connector

app = Flask(__name__)  # fixed: __name__ instead of _name_

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="environmental monitoring"
)

@app.route("/")
def dashboard():
    cur = db.cursor()
    cur.execute("SELECT temperature,humidity,gas,status FROM sensor_data ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    if row:
        t, h, g, s = row
        color = {"NORMAL":"green","WARNING":"orange","DANGER":"red"}[s]
        return f"""
        <h1>Smart Environment Monitoring</h1>
        <h3>Temperature: {t} °C</h3>
        <h3>Humidity: {h} %</h3>
        <h3>Gas Level: {g}</h3>
        <h2 style='color:{color}'>STATUS: {s}</h2>
        """
    else:
        return "<h1>No data available</h1>"

# Run the Flask app
app.run(host="0.0.0.0", port=5000, debug=True)