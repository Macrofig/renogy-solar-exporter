import logging
import configparser
import os
import sys
from renogybt import RoverClient
from flask import Flask
from prometheus_client import Gauge, Summary, generate_latest

app = Flask(__name__)

REQUEST_TIME = Summary("request_processing_seconds", "Time spent processing request")

# Renogy Metrics
battery_percentage = Gauge("battery_percentage", "Battery capacity percentage")
battery_voltage = Gauge("battery_voltage", "Battery volage in volts")
battery_current = Gauge("battery_current", "Battery current in amps")
battery_temperature = Gauge("battery_temperature", "Battery temperature in celsius")
controller_temperature = Gauge(
    "controller_temperature", "Controller temperature in celsius"
)
load_status = Gauge("load_status", "Load status true when load is on")
load_voltage = Gauge("load_voltage", "Load voltage in volts")
load_current = Gauge("load_current", "Load current in amps")
load_power = Gauge("load_power", "Load power in watts")
pv_voltage = Gauge("pv_voltage", "Solar (PV) voltage in volts")
pv_current = Gauge("pv_current", "Solar (PV) current in amps")
pv_power = Gauge("pv_power", "Solar (PV) power in watts")
max_charging_power_today = Gauge(
    "max_charging_power_today", "Maximum charging power in watts"
)
max_discharging_power_today = Gauge(
    "max_discharging_power_today", "Maximum discharging power in watts"
)
charging_amp_hours_today = Gauge(
    "charging_amp_hours_today", "Charging amp-hours for current day"
)
discharging_amp_hours_today = Gauge(
    "discharging_amp_hours_today", "Discharging amp-hours for the current day"
)
power_generation_today = Gauge(
    "power_generation_today", "Power generated in watts for current day"
)
power_consumption_today = Gauge(
    "power_consumption_today", "Power consumed in watts for current day"
)
power_generation_total = Gauge(
    "power_generation_total", "Total power generated in watts"
)

logging.basicConfig(level=logging.WARNING)

config_file = sys.argv.get[1] if len(sys.argv) > 1 else "config.ini"
config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), config_file)
config = configparser.ConfigParser()
config.read(config_path)


def on_data_received(client, data):
    logging.debug("{} => {}".format(client.device.alias(), data))
    battery_percentage.set(data.battery_percentage)
    client.disconnect()


@app.route("/metrics")
@REQUEST_TIME.time()
def metrics():
    try:
        RoverClient(config, on_data_received).connect()
    except:
        logging.warning("It broke")
        pass

    return generate_latest()


@app.route("/health")
def health():
    # TODO: Only attempt to connect if a mac address was passed
    try:
        RoverClient(config).connect()
    except:
        logging.warning("It broke")
        return "NOT FOUND"

    return "AVAILABLE"


@app.route("/")
def index():
    return """<html>
        <head><title>Renogy Solar Charger Exporter</title></head>
        <body>
            <h1>Renogy Solar Charger Exporter</h1>
            <p><a href='/metrics'>Metrics</a></p>
            <p><a href='/health'>Health (Bluetooth connection state to charge controller)</a></p>
        </body>
    </html>"""


if __name__ == "__main__":
    # TODO Make port configurable
    app.run(host="0.0.0.0", port=5000)
