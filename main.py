from flask import Flask, request, redirect
import requests
import logging

app = Flask(__name__)

# Configure logging to a file
logging.basicConfig(
    filename='ip_logs.txt',
    level=logging.INFO,
    format='%(asctime)s %(message)s'
)

# Destination URL to redirect users after logging
TARGET_URL = "https://yourdestination.com"  # Replace with your final URL
# GeoIP API URL (using ip-api.com for free geo lookup)
GEOIP_API_URL = "http://ip-api.com/json/"

@app.route('/<short_code>')
def track_ip(short_code):
    # Get the visitor's IP address and User-Agent
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    # Perform a GeoIP lookup
    try:
        geo_response = requests.get(GEOIP_API_URL + ip, timeout=5)
        geo_data = geo_response.json()
        location = f"{geo_data.get('city')}, {geo_data.get('regionName')}, {geo_data.get('country')}"
    except Exception as e:
        location = "Geo lookup failed"

    # Create a log message
    log_message = (
        f"Short code: {short_code} | IP: {ip} | "
        f"User-Agent: {user_agent} | Location: {location}"
    )
    app.logger.info(log_message)
    logging.info(log_message)

    # Redirect the user to the target URL
    return redirect(TARGET_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
