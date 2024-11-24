import dht11
import RPi.GPIO as GPIO
import time
from time import sleep
import subprocess
import cv2
from datetime import datetime

# Constants and Configurations
DHT_PIN = 35             # Pin 35 (GPIO 19) for DHT11 sensor
SOIL_PIN = 5             # GPIO 5 for soil moisture sensor
BUZZER_PIN = 33          # Pin 33 (GPIO 13) for the buzzer
LONG_INTERVAL = 900      # Long interval (15 minutes)
DEFAULT_INTERVAL = 300   # Default interval (5 minutes)
SHORT_INTERVAL = 60      # Short interval (1 minute)
IMAGE_CAPTURE_INTERVAL = DEFAULT_INTERVAL
MAX_RETRIES = 5          # Maximum retries for DHT11 readings

# Setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(SOIL_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Initialize DHT11 sensor
dht_instance = dht11.DHT11(pin=DHT_PIN)

# Dynamic Intervals
sensor_interval = DEFAULT_INTERVAL
stable_readings_count = 0

# Thresholds (loaded from configuration file)
humidity_threshold = 50
temperature_threshold = 15
soil_moisture_threshold = 300

# Logging Function
def log_event(event):
    try:
        with open("events_log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()}: {event}\n")
        print(event)
    except Exception as e:
        print(f"Logging error: {e}")

# Load Configuration from File
def load_configuration():
    global humidity_threshold, temperature_threshold, soil_moisture_threshold
    try:
        with open("configuration.txt", "r") as config_file:
            for line in config_file:
                if "air_humidity" in line:
                    humidity_threshold = int(line.split(">")[1].strip())
                elif "air_temperature" in line:
                    temperature_threshold = int(line.split("<")[1].strip())
                elif "soil_humidity" in line:
                    soil_moisture_threshold = int(line.split("<")[1].strip())
        log_event("Configuration loaded successfully.")
    except Exception as e:
        log_event(f"Error loading configuration: {e}")

# Buzzer Notification
def buzz(times):
    try:
        for _ in range(times):
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            sleep(0.5)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            sleep(0.5)
        log_event(f"Buzzer buzzed {times} times.")
    except Exception as e:
        log_event(f"Buzzer error: {e}")

# Read Temperature and Humidity with Retry Mechanism
def read_temperature_humidity():
    retries = 0
    while retries < MAX_RETRIES:
        result = dht_instance.read()
        if result.is_valid():
            return result.humidity, result.temperature
        else:
            retries += 1
            sleep(1)
    return None, None

# Read Soil Moisture
def read_soil_moisture():
    try:
        moisture = GPIO.input(SOIL_PIN)
        log_event(f"Soil moisture reading: {moisture}")
        return moisture
    except Exception as e:
        log_event(f"Error reading soil moisture sensor: {e}")
        return None

# Capture Image and Analyze Plant Health
def capture_and_analyze_image():
    try:
        image_path = f"plant_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        result = subprocess.run(
            ["libcamera-still", "-o", image_path, "-t", "2000"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            log_event(f"Captured image: {image_path}")
            analyze_image(image_path)
        else:
            log_event("Failed to capture image.")
    except Exception as e:
        log_event(f"Error capturing image: {e}")

# Analyze Image for Plant Distress
def analyze_image(image_path):
    try:
        image = cv2.imread(image_path)
        if image is None:
            log_event("Error loading image for analysis.")
            return

        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_yellow = (20, 100, 100)
        upper_yellow = (30, 255, 255)
        mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
        yellow_percentage = (cv2.countNonZero(mask) / mask.size) * 100

        if yellow_percentage > 10:
            log_event("Detected yellowing leaves.")
            buzz(3)
    except Exception as e:
        log_event(f"Error analyzing image: {e}")

# Main Monitoring Loop
def main():
    global sensor_interval, IMAGE_CAPTURE_INTERVAL, stable_readings_count
    load_configuration()
    last_image_capture = time.time()

    try:
        while True:
            humidity, temperature = read_temperature_humidity()
            soil_moisture = read_soil_moisture()

            if humidity is None or temperature is None or soil_moisture is None:
                sleep(sensor_interval)
                continue

            log_event(f"Humidity: {humidity}%, Temperature: {temperature}C, Soil Moisture: {soil_moisture}")

            if humidity > humidity_threshold:
                log_event("High humidity detected.")
                buzz(1)
            if temperature < temperature_threshold:
                log_event("Low temperature detected.")
                buzz(2)
            if soil_moisture < soil_moisture_threshold:
                log_event("Low soil moisture detected.")
                buzz(3)

            stable_readings_count += 1
            if stable_readings_count >= 12:
                log_event("Stable conditions detected. Increasing intervals.")
                sensor_interval = LONG_INTERVAL
                IMAGE_CAPTURE_INTERVAL = LONG_INTERVAL
            else:
                sensor_interval = SHORT_INTERVAL
                IMAGE_CAPTURE_INTERVAL = SHORT_INTERVAL

            if time.time() - last_image_capture > IMAGE_CAPTURE_INTERVAL:
                capture_and_analyze_image()
                last_image_capture = time.time()

            sleep(sensor_interval)

    except KeyboardInterrupt:
        log_event("Monitoring stopped by user.")
    finally:
        GPIO.cleanup()
        log_event("GPIO cleanup complete.")

if __name__ == "__main__":
    main()

