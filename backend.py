
from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve form data
        sensorName = request.form['sensorName']
        observedEntity = request.form['observedEntity']
        minVal = float(request.form['minVal'])
        maxVal = float(request.form['maxVal'])
        
        # Connect to the database and perform database operations
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Ska@2557",
            database="dcp"
        )

        if conn.is_connected():
            print("Connected to the database")
        else:
            print("Connection failed")

        # Create a cursor
        cursor = conn.cursor()

        # Insert data into ObservedEntities table
        sql1 = "INSERT INTO ObservedEntities (EntityName) VALUES (%s)"
        cursor.execute(sql1, (observedEntity,))
        conn.commit()

        # Get the last inserted entity ID
        entityID = cursor.lastrowid

        # Insert data into Sensors table
        sql2 = "INSERT INTO Sensors (SensorName, ObservedEntityID) VALUES (%s, %s)"
        cursor.execute(sql2, (sensorName, entityID))
        conn.commit()
        sql3 = "INSERT INTO PerformanceLevels (SensorID, MinVal, MaxVal) VALUES (%s, %s, %s)"
        cursor.execute(sql3, (cursor.lastrowid, minVal, maxVal))
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return "Data successfully inserted!"

    return render_template('index.html')


if __name__ == '__main__':
   app.run(debug=True)

