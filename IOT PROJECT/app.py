from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="smart_environment_monitoring_system1"
)

@app.route("/")
def index():
    cursor = db.cursor(dictionary=True)  
    cursor.execute("""
        SELECT temp, humidity, gas
        FROM envdata
    """)
    data = cursor.fetchall()
    cursor.close()
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)