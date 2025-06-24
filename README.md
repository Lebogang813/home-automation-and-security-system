# Home Automation and Security System

This project is a real time home automation and security system designed to monitor and control environmental conditions such as temperature, humidity, motion, and light using an ESP32 microcontroller and various sensors. The system displays data on a secure, user-friendly web interface and stores information in a MySQL database for real-time monitoring and future analysis.

---

##  Technologies Used

- ESP32 WeMos D1 R32
- Sensors: DS18B20 (Temperature), LDR (Light), PIR (Motion), MH-series (Humidity)
- Languages: C++ (Arduino), Python (Flask)
- Database: MySQL
- Frontend: HTML, CSS, JavaScript (JSON)
- Tools: Arduino IDE, Wokwi Simulator

---

##  System Features

- Real-time sensor data collection and monitoring  
- Wireless communication via ESP32 (Wi-Fi)  
- Web-based dashboard with login/signup functionality  
- Data logging with timestamps  
- Admin dashboard with live graphs and tables  
- Responsive to motion, light, and environmental changes  
- Simple enclosure and wiring design

---

##  Project Architecture

- Sensor values are read by the ESP32
- Data is transmitted over Wi-Fi to a Flask server
- Server saves values into a MySQL database
- Web interface (HTML/CSS/JSON) fetches and displays this data live

---

## 📸 Example Screens (optional if you have screenshots)

- `Login.html`: Basic login for user access  
- `Sensors.html`: Real-time sensor display  
- `Admin.html`: Admin-only dashboard with graphs  
- `Graph.html`: Historical data plotting

---

##  Limitations

- No mobile app or cloud storage  
- Basic motion detection (no video feed or alerts)  
- System shuts down during power loss (no backup battery)  
- Sensors are affordable but not industrial-grade

---

##  Future Improvements

- Add SMS or email alerts for motion
- Upgrade sensors for better accuracy
- Integrate mobile app or cloud storage (e.g. Firebase)
- Use solar or battery backup for reliability

---

##  What I Learned

> This project helped me gain practical experience in embedded systems, IoT communication, backend integration, and web development. It also improved my troubleshooting and planning skills through real-world testing.

---

##  How to Run

1. Upload Arduino code to ESP32  
2. Set up MySQL database and tables (see `db_schema.sql` if included)  
3. Run `app.py` (Flask) on your local server  
4. Access the dashboard through your browser

---

Author: Lebogang Monyela  
Project Type: Final Year Practical Project (EIENP3A) – Vaal University of Technology  
