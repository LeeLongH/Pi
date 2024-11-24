# README for Energy-Efficient Plant Monitoring System

---

## Project Overview
The **Energy-Efficient Plant Monitoring System** is designed to monitor environmental and soil conditions for plants. It uses sensors to measure temperature, humidity, and soil moisture, along with a camera to capture plant images for health analysis. The system prioritizes energy efficiency by dynamically adjusting sensor reading intervals and camera usage based on environmental conditions.

---

## Features
- **Environmental Data Monitoring**:
  - Uses the DHT11 sensor to measure temperature and humidity.
  - Reads soil moisture levels using a digital soil moisture sensor.

- **Dynamic Sampling**:
  - Adjusts intervals based on stable or unstable environmental conditions to save energy.
  - Shortens intervals during anomalies for closer monitoring.

- **Visual Plant Health Analysis**:
  - Captures images using a camera and analyzes for visual signs of distress, such as yellowing leaves.

- **User Notifications**:
  - Alerts the user via a buzzer when thresholds for temperature, humidity, or soil moisture are crossed.

- **Energy Efficiency**:
  - Implements hierarchical sensing and adaptive sampling rates.
  - Logs events for monitoring system activity.

---

## Hardware Requirements
- Raspberry Pi with GPIO support.
- **Sensors**:
  - DHT11 Temperature and Humidity Sensor.
  - Soil Moisture Sensor.
- **Camera Module**:
  - Compatible with Raspberry Pi (e.g., Raspberry Pi Camera v2).
- **Buzzer** for notifications.
- Power supply for Raspberry Pi and peripherals.

---

## Software Requirements
- **Python** (Version 3.7 or higher).
- Required Python libraries (install in your virtual environment):
  ```bash
  pip install dht11 RPi.GPIO opencv-python
- libcamera for capturing images:
  ```bash
  sudo apt install libcamera-tools
  
---

## Usage Instructions
1. **Configuration**:
   - Update the thresholds in `configuration.txt`:
     ```
     1: air_humidity > 50
     2: air_temperature < 15
     3: soil_humidity < 300
     ```

2. **Setup Hardware**:
   - Connect sensors and peripherals to the Raspberry Pi as per the following pin configuration:
     - **DHT11**: Data pin to GPIO 35.
     - **Soil Moisture Sensor**: Data pin to GPIO 5.
     - **Buzzer**: Control pin to GPIO 33.
     - Camera connected to the Raspberry Pi camera port.

3. **Run the System**:
   - Ensure you’re in the directory containing `energyEfficient.py`.
   - Execute the script:
     ```bash
     python3 energyEfficient.py
     ```

4. **Monitor Logs**:
   - Check `events_log.txt` for activity and alerts.

---

## Energy Optimization Details
- **Dynamic Intervals**:
  - **Short Interval**: During unstable conditions.
  - **Default Interval**: During standard operations.
  - **Long Interval**: During stable conditions.

- **Idle States**:
  - Sensors are deactivated or read less frequently when conditions are stable.
  
---

## File Structure
- `energyEfficient.py`: Main script to run the system.
- `configuration.txt`: Threshold configuration file for sensor readings.
- `events_log.txt`: Log file for system events and alerts.

---

## Troubleshooting
- **Sensor Errors**:
  - Ensure proper wiring and connections.
  - Check the power supply for the Raspberry Pi and peripherals.

- **Camera Issues**:
  - Ensure `libcamera` is installed and the camera is connected.
  - Run a test capture:
    ```bash
    libcamera-still -o test.jpg
    ```

- **Permission Errors**:
  - Run the script with `sudo`:
    ```bash
    sudo python3 energyEfficient.py
    ```

---

## Acknowledgments
- Adafruit Industries for the DHT11 and CircuitPython libraries.
- OpenCV for image processing.
- Raspberry Pi Foundation for GPIO and camera support.

  
