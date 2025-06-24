from flask import Flask ,render_template ,request ,flash,session
import random

import mysql.connector

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64


app=Flask(__name__)
app.secret_key = 'bernet123@'

#database connection

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Automation@16",
    database="HOME"
)


cursor =conn.cursor(dictionary=True)

conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Automation (
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    student_number VARCHAR(20) NOT NULL UNIQUE,
    email_address VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    account_type VARCHAR(20) NOT NULL
);
""")
conn.commit()


# Route to receive ESP32 sensor data
@app.route('/update', methods=['POST'])
def update():
    data = request.json
    sql = """INSERT INTO sensors 
             (DS18B20_Temperature,  LDR_1, Humidity, LDR_2, InfraRed) 
             VALUES (%s, %s, %s, %s, %s)"""

    values = (
        data["DS18B20_Temperature"],
        
        data["LDR_1"],
        data["Humidity"],
        data["LDR_2"],
        data["InfraRed"]
    )

    cursor.execute(sql, values)
    conn.commit()

    return "Data stored successfully!"


@app.route('/base')
def base() :
    return render_template("base.html")


@app.route('/')
def welcome() :
    return render_template("welcome.html  ")

    
@app.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        cursor.execute("""
            SELECT * FROM Automation 
            WHERE email_address = %s AND account_type = 'user'
        """, (email,))
        user = cursor.fetchone()

        if user:
            if user['password'] == password:
                session['user_name'] = user['first_name']  # Optional: to show welcome on sensor pages

                # Redirect based on email
                if email == "221659595@edu.vut.ac.za":

                    cursor.execute("SELECT timestamp, DS18B20_Temperature FROM sensors ORDER BY timestamp DESC LIMIT 10")
                    data = cursor.fetchall()

    
                    timestamps = [row['timestamp'] for row in data]
                    T = [row['DS18B20_Temperature'] for row in data]

                    zip_data = zip(timestamps, T)

                    Ctemperature  = data[0]['DS18B20_Temperature'] if data else "No data"

                    # Use pandas to fetch data from MySQL
                    query = "SELECT timestamp, DS18B20_Temperature FROM sensors ORDER BY timestamp DESC LIMIT 15"
                    df = pd.read_sql(query, con=conn)

                    # Sort in ascending order for proper plotting
                    df = df.sort_values("timestamp")

                    #    Plotting
                    plt.figure(figsize=(10, 4))
                    plt.plot(df['timestamp'], df['DS18B20_Temperature'], marker='o', linestyle='-')
                    plt.xlabel("Time")
                    plt.ylabel("Temperature level")
                    plt.title("Temperature sensor Sensor Graph")
                    plt.xticks(rotation=45)
                    plt.tight_layout()

                    # Save plot to buffer
                    img = BytesIO()
                    plt.savefig(img, format='png')
                    img.seek(0)
                    graph = base64.b64encode(img.getvalue()).decode()


                    return render_template('temperature.html',user=user['first_name'],graph=graph, zip_data=zip_data, a=Ctemperature)
                    
                

                elif email == "22@edu.vut.ac.za":


                    cursor.execute("SELECT timestamp, LDR_1 FROM sensors ORDER BY timestamp DESC LIMIT 10")
                    data = cursor.fetchall()

    
                    timestamps = [row['timestamp'] for row in data]
                    ldr_value = [row['LDR_1'] for row in data]

    
                    zip_data = zip(timestamps, ldr_value)

                    # Use pandas to fetch data from MySQL
                    query = "SELECT timestamp, LDR_1 FROM sensors ORDER BY timestamp DESC LIMIT 15"
                    df = pd.read_sql(query, con=conn)

                    # Sort in ascending order for proper plotting
                    df = df.sort_values("timestamp")

                    # Plotting
                    plt.figure(figsize=(10, 4))
                    plt.plot(df['timestamp'], df['LDR_1'], marker='o', linestyle='-')
                    plt.xlabel("Time")
                    plt.ylabel("Outside Value")
                    plt.title("Light Depended Resister  Sensor Graph")
                    plt.xticks(rotation=45)
                    plt.tight_layout()

                    # Save plot to buffer
                    img = BytesIO()
                    plt.savefig(img, format='png')
                    img.seek(0)
                    graph = base64.b64encode(img.getvalue()).decode()

                    # Most recent LDR value
                    ldr_value = data[0]['LDR_1'] if data else "No data"

                    return render_template("LDR.html", graph=graph, ldr_value=ldr_value ,zip_data=zip_data,user=user['first_name'])

                

                elif email == "221551220@edu.vut.ac.za":

                    message = "Curtain system status based on current light level."

                    cursor.execute("SELECT timestamp, LDR_2 FROM sensors ORDER BY timestamp DESC LIMIT 10")
                    data = cursor.fetchall()

    
                    timestamps = [row['timestamp'] for row in data]
                    L = [row['LDR_2'] for row in data]

    
                    zip_data = zip(timestamps, L)

                    value = data[0]['LDR_2'] if data else "No data"

                    if value > 55:  # Very bright
                        badge_class = 'bg-danger'
                        button_label = 'Close the Curtains'
                        next_state = 'normal'
                    elif 45 <= value <= 55:  # Moderate light
                        badge_class = 'bg-success'
                        button_label = 'No Action Needed'
                        next_state = 'dark'
                    else:  # Dim light
                        badge_class = 'bg-warning'
                        button_label = 'Open the Curtains'
                        next_state = 'normal'

                        # Use pandas to fetch data from MySQL
                    query = "SELECT timestamp, LDR_2 FROM sensors ORDER BY timestamp DESC LIMIT 15"
                    df = pd.read_sql(query, con=conn)

                    # Sort in ascending order for proper plotting
                    df = df.sort_values("timestamp")

                    # Plotting
                    plt.figure(figsize=(10, 4))
                    plt.plot(df['timestamp'], df['LDR_2'], marker='o', linestyle='-')
                    plt.xlabel("Time")
                    plt.ylabel("House Brightness level")
                    plt.title("Light Depended Resister  Sensor Graph")
                    plt.xticks(rotation=45)
                    plt.tight_layout()

                    # Save plot to buffer
                    img = BytesIO()
                    plt.savefig(img, format='png')
                    img.seek(0)
                    graph = base64.b64encode(img.getvalue()).decode()

                    return render_template('curtains.html',user=user['first_name'],graph=graph,zip_data=zip_data,value=value,message=message,badge_class=badge_class,button_label=button_label,next_state=next_state)


                    
                
                elif email == "224071777@edu.vut.ac.za":

                    cursor.execute("SELECT timestamp, InfraRed FROM sensors ORDER BY timestamp DESC LIMIT 10")
                    data = cursor.fetchall()

    
                    timestamps = [row['timestamp'] for row in data]
                    ir = [row['InfraRed'] for row in data]

                    zip_data = zip(timestamps, ir)

                    motion  = data[0]['InfraRed'] if data else "No data"

                    if motion ==1 :
                        status_class = 'alert'
                        status_message = '⚠️ Motion detected!'
                    else:
                        status_class = 'safe'
                        status_message = '✅ Area is clear.'

                        # Use pandas to fetch data from MySQL
                    query = "SELECT timestamp, InfraRed FROM sensors ORDER BY timestamp DESC LIMIT 15"
                    df = pd.read_sql(query, con=conn)

                        # Sort in ascending order for proper plotting
                    df = df.sort_values("timestamp")

                        # Plotting
                    plt.figure(figsize=(10, 4))
                    plt.plot(df['timestamp'], df['InfraRed'], marker='o', linestyle='-')
                    plt.xlabel("Time")
                    plt.ylabel("Motion")
                    plt.title("Infra-Red  Sensor Graph")
                    plt.xticks(rotation=45)
                    plt.tight_layout()

                        # Save plot to buffer
                    img = BytesIO()
                    plt.savefig(img, format='png')
                    img.seek(0)
                    graph = base64.b64encode(img.getvalue()).decode()


                    return render_template('infrared.html',user=user['first_name'],graph=graph,zip_data=zip_data, a=motion,status_class=status_class,status_message=status_message , b=data)
                    
                

                elif email == "25@edu.vut.ac.za":

                    cursor.execute("SELECT timestamp, Humidity FROM sensors ORDER BY timestamp DESC LIMIT 10")
                    data = cursor.fetchall()

                    # Get the most recent humidity value (first item after DESC sort)
                    current_value = data[0]['Humidity'] if data else "No data"

                    timestamps = [row['timestamp'] for row in data]
                    H = [row['Humidity'] for row in data]
                    zip_data = zip(timestamps, H)

                    # Use pandas to fetch data from MySQL
                    query = "SELECT timestamp, Humidity FROM sensors ORDER BY timestamp DESC LIMIT 15"
                    df = pd.read_sql(query, con=conn)

                        # Sort in ascending order for proper plotting
                    df = df.sort_values("timestamp")

                    # Plotting
                    plt.figure(figsize=(7, 4))
                    plt.plot(df['timestamp'], df['Humidity'], marker='o', linestyle='-')
                    plt.xlabel("Time")
                    plt.ylabel("Humidity level")
                    plt.title("Humidity sensor Sensor Graph")
                    plt.xticks(rotation=45)
                    plt.tight_layout()

                        # Save plot to buffer
                    img = BytesIO()
                    plt.savefig(img, format='png')
                    img.seek(0)
                    graph = base64.b64encode(img.getvalue()).decode()


                    return render_template('humidity.html',user=user['first_name'], graph=graph,zip_data=zip_data, a=current_value)

                    
                
                else:
                    
                    return render_template("new_users.html" , user=user['first_name'])
            else:
                flash('Incorrect password.', 'error')
                return render_template("Login.html")
        else:
            flash('Incorrect email or not a user account.', 'error')
            return render_template("Login.html")

    return render_template("Login.html")



@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        first_name = request.form['name']
        last_name = request.form['lastname']
        student_number = request.form['studentnumber']
        email = request.form['email']
        password = request.form['password']
        account_type = request.form['type']

        try:
            cursor.execute("""
                INSERT INTO Automation (first_name, last_name, student_number, email_address, password, account_type)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (first_name, last_name, student_number, email, password, account_type))
            conn.commit()
            flash("Signup successful!", "success")
            return render_template("welcome.html")
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "danger")
            return render_template("signup.html")
    else:
        return render_template("signup.html")


@app.route('/admin_login')
def admin_login():
    return render_template("admin_login.html")


@app.route('/admin-authenticate', methods=['POST'])
def admin_authenticate():
    email = request.form['email']
    password = request.form['password']

    cursor.execute("""
        SELECT * FROM Automation 
        WHERE email_address = %s AND account_type = 'Admin'
    """, (email,))
    admin = cursor.fetchone()

    if admin and admin['password'] == password:
        session['admin_logged_in'] = True
        session['admin_name'] = admin['first_name']

        query = """
        SELECT timestamp, DS18B20_Temperature, LDR_1, LDR_2, Humidity, InfraRed
        FROM sensors ORDER BY timestamp DESC LIMIT 15
        """
        df = pd.read_sql(query, con=conn).sort_values("timestamp")

        # Plot combined graph
        plt.figure(figsize=(9, 6))
        plt.plot(df['timestamp'], df['DS18B20_Temperature'], marker='o', label='Temperature')
        plt.plot(df['timestamp'], df['LDR_1'], marker='o', label='Brightness level outside')
        plt.plot(df['timestamp'], df['LDR_2'], marker='o', label='House brightness level')
        plt.plot(df['timestamp'], df['Humidity'], marker='o', label='Humidity')
        plt.plot(df['timestamp'], df['InfraRed'], marker='o', label='Motion')
        plt.xlabel("Timestamp")
        plt.ylabel("Sensor Readings")
        plt.title("Combined Sensor Readings Over Time")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()

        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        graph = base64.b64encode(img.getvalue()).decode()

        cursor.execute("""
            SELECT timestamp, LDR_1, InfraRed, Humidity, LDR_2, DS18B20_Temperature
            FROM sensors ORDER BY timestamp DESC LIMIT 10
        """)
        data = cursor.fetchall()

        if not data:
            return "No sensor data available."

        # Extract values
        timestamps = [row['timestamp'] for row in data]
        ldr1 = [row['LDR_1'] for row in data]
        ldr2 = [row['LDR_2'] for row in data]
        humidity = [row['Humidity'] for row in data]
        infrared = [row['InfraRed'] for row in data]
        temperature = [row['DS18B20_Temperature'] for row in data]

        # Latest values
        ldr1_val = ldr1[0]
        ldr2_val = ldr2[0]
        humidity_val = humidity[0]
        motion_val = infrared[0]
        temperature_val = temperature[0]

        # Curtain logic
        if ldr2_val > 55:
            curtain_msg = 'Close the Curtains'
            curtain_badge = 'bg-danger'
        elif 45 <= ldr2_val <= 55:
            curtain_msg = 'No Action Needed'
            curtain_badge = 'bg-success'
        else:
            curtain_msg = 'Open the Curtains'
            curtain_badge = 'bg-warning'

        # Motion logic
        if motion_val == 1:
            motion_status = '⚠️ Motion detected!'
            motion_class = 'alert'
        else:
            motion_status = '✅ Area is clear.'
            motion_class = 'safe'

        # Light logic (LDR_1)
        if ldr1_val < 75:
            ldr1_status = "🌙 It's dark outside. Turn on the light."
        else:
            ldr1_status = "☀️ It's bright outside. No need for lights."

        # Temperature logic
        if temperature_val < 25:
            temperature_status = "❄️ It's cold inside. Turn on the heater."
        else:
            temperature_status = "🔥 It's hot inside. Turn on the AC."

        zip_data = zip(timestamps, ldr1, ldr2, humidity, infrared, temperature)

        return render_template('Home.html',
            admin_name=session['admin_name'],
            graph=graph,
            zip_data=zip_data,
            L1=ldr1_val,
            L2=ldr2_val,
            H=humidity_val,
            T=temperature_val,
            motion=motion_class,
            motion_message=motion_status,
            curtain_msg=curtain_msg,
            curtain_badge=curtain_badge,
            ldr1_status=ldr1_status,
            temperature_status=temperature_status
        )

        
    else:
        flash('Incorrect email or not an admin account.', 'error')
        return render_template('admin_login.html')


# Protect the Home route to require admin login
@app.route('/Home')
def Home():
    if not session.get('admin_logged_in'):
        return render_template('admin_login.html')
    
    admin_name = session.get('admin_name', 'Admin')



    


    return render_template("Home.html", admin_name=admin_name)


@app.route("/light")
def light():


    cursor.execute("SELECT timestamp, LDR_1 FROM sensors ORDER BY timestamp DESC LIMIT 10")
    data = cursor.fetchall()

    
    timestamps = [row['timestamp'] for row in data]
    ldr_value = [row['LDR_1'] for row in data]

    
    zip_data = zip(timestamps, ldr_value)

    # Use pandas to fetch data from MySQL
    query = "SELECT timestamp, LDR_1 FROM sensors ORDER BY timestamp DESC LIMIT 15"
    df = pd.read_sql(query, con=conn)

    # Sort in ascending order for proper plotting
    df = df.sort_values("timestamp")

    # Plotting
    plt.figure(figsize=(10, 4))
    plt.plot(df['timestamp'], df['LDR_1'], marker='o', linestyle='-')
    plt.xlabel("Time")
    plt.ylabel("Outside Value")
    plt.title("Light Depended Resister  Sensor Graph ")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save plot to buffer
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph = base64.b64encode(img.getvalue()).decode()

    # Most recent LDR value
    ldr_value = data[0]['LDR_1'] if data else "No data"

    return render_template("LDR.html", graph=graph, ldr_value=ldr_value ,zip_data=zip_data)

    
@app.route('/motion')
def motion():
     # Example distance in cm

    cursor.execute("SELECT timestamp, InfraRed FROM sensors ORDER BY timestamp DESC LIMIT 10")
    data = cursor.fetchall()

    
    timestamps = [row['timestamp'] for row in data]
    ir = [row['InfraRed'] for row in data]

    
    zip_data = zip(timestamps, ir)

    
    motion  = data[0]['InfraRed'] if data else "No data"

    
    if motion ==1 :
        status_class = 'alert'
        status_message = '⚠️ Motion detected!'
    else:
        status_class = 'safe'
        status_message = '✅ Area is clear.'


     # Use pandas to fetch data from MySQL
    query = "SELECT timestamp, InfraRed FROM sensors ORDER BY timestamp DESC LIMIT 15"
    df = pd.read_sql(query, con=conn)

    # Sort in ascending order for proper plotting
    df = df.sort_values("timestamp")

    # Plotting
    plt.figure(figsize=(10, 4))
    plt.plot(df['timestamp'], df['InfraRed'], marker='o', linestyle='-')
    plt.xlabel("Time")
    plt.ylabel("Motion")
    plt.title("Infra-Red  Sensor Graph")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save plot to buffer
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph = base64.b64encode(img.getvalue()).decode()


    return render_template('infrared.html',graph=graph,zip_data=zip_data, a=motion,status_class=status_class,status_message=status_message , b=data)


@app.route('/humidity', methods=['GET'])
def humidity():
    session.clear()

    cursor.execute("SELECT timestamp, Humidity FROM sensors ORDER BY timestamp DESC LIMIT 10")
    data = cursor.fetchall()

    # Get the most recent humidity value (first item after DESC sort)
    current_value = data[0]['Humidity'] if data else "No data"

    timestamps = [row['timestamp'] for row in data]
    H = [row['Humidity'] for row in data]
    zip_data = zip(timestamps, H)

    # Use pandas to fetch data from MySQL
    query = "SELECT timestamp, Humidity FROM sensors ORDER BY timestamp DESC LIMIT 15"
    df = pd.read_sql(query, con=conn)

    # Sort in ascending order for proper plotting
    df = df.sort_values("timestamp")

    # Plotting
    plt.figure(figsize=(7, 4))
    plt.plot(df['timestamp'], df['Humidity'], marker='o', linestyle='-')
    plt.xlabel("Time")
    plt.ylabel("Humidity level")
    plt.title("Humidity sensor Sensor Graph")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save plot to buffer
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph = base64.b64encode(img.getvalue()).decode()


    return render_template('humidity.html', graph=graph,zip_data=zip_data, a=current_value)





@app.route("/curtains", methods=['GET'])
def curtains():
 
   
    message = "Curtain system status based on current light level."

    cursor.execute("SELECT timestamp, LDR_2 FROM sensors ORDER BY timestamp DESC LIMIT 10")
    data = cursor.fetchall()

    
    timestamps = [row['timestamp'] for row in data]
    L = [row['LDR_2'] for row in data]

    
    zip_data = zip(timestamps, L)

    value = data[0]['LDR_2'] if data else "No data"

    if value > 55:  # Very bright
        badge_class = 'bg-danger'
        button_label = 'Close the Curtains'
        next_state = 'normal'
    elif 45 <= value <= 55:  # Moderate light
        badge_class = 'bg-success'
        button_label = 'No Action Needed'
        next_state = 'dark'
    else:  # Dim light
        badge_class = 'bg-warning'
        button_label = 'Open the Curtains'
        next_state = 'normal'

     # Use pandas to fetch data from MySQL
    query = "SELECT timestamp, LDR_2 FROM sensors ORDER BY timestamp DESC LIMIT 15"
    df = pd.read_sql(query, con=conn)

    # Sort in ascending order for proper plotting
    df = df.sort_values("timestamp")

    # Plotting
    plt.figure(figsize=(10, 4))
    plt.plot(df['timestamp'], df['LDR_2'], marker='o', linestyle='-')
    plt.xlabel("Time")
    plt.ylabel("House Brightness level")
    plt.title("Light Depended Resister  Sensor Graph")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save plot to buffer
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph = base64.b64encode(img.getvalue()).decode()

    return render_template('curtains.html',graph=graph,zip_data=zip_data,value=value,message=message,badge_class=badge_class,button_label=button_label,next_state=next_state)


@app.route('/temperature')
def temperature():

    cursor.execute("SELECT timestamp, DS18B20_Temperature FROM sensors ORDER BY timestamp DESC LIMIT 10")
    data = cursor.fetchall()

    
    timestamps = [row['timestamp'] for row in data]
    T = [row['DS18B20_Temperature'] for row in data]

    zip_data = zip(timestamps, T)

    Ctemperature  = data[0]['DS18B20_Temperature'] if data else "No data"

    # Use pandas to fetch data from MySQL
    query = "SELECT timestamp, DS18B20_Temperature FROM sensors ORDER BY timestamp DESC LIMIT 15"
    df = pd.read_sql(query, con=conn)

    # Sort in ascending order for proper plotting
    df = df.sort_values("timestamp")

    # Plotting
    plt.figure(figsize=(10, 4))
    plt.plot(df['timestamp'], df['DS18B20_Temperature'], marker='o', linestyle='-')
    plt.xlabel("Time")
    plt.ylabel("Temperature level")
    plt.title("Temperature sensor Sensor Graph")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save plot to buffer
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph = base64.b64encode(img.getvalue()).decode()


    return render_template('temperature.html',graph=graph, zip_data=zip_data, a=Ctemperature)
    



if __name__==("__main__"):
    app.run(debug=True ,host='0.0.0.0', port=5000)
