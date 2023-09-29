import logging
import configparser
import os
import sys
from renogybt import RoverClient
from flask import Flask
from prometheus_client import Enum, Gauge, Summary, generate_latest

app = Flask(__name__)

REQUEST_TIME = Summary("request_processing_seconds", "Time spent processing request")

# Renogy Metrics
battery_percentage = Gauge("battery_percentage", "Battery capacity percentage")
battery_voltage = Gauge("battery_voltage", "Battery volage in volts")
battery_current = Gauge("battery_current", "Battery current in amps")
battery_temperature = Gauge("battery_temperature", "Battery temperature in celsius")
battery_type = Enum("battery_type", "Chemistry setting for battery pack", 
        states=['open','sealed','gel','lithium','self-customized'])
controller_temperature = Gauge(
    "controller_temperature", "Controller temperature in celsius"
)
load_status = Enum("load_status", "Load status true when load is on", states=['on', 'off'])
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
charging_status = Enum('charging_status', "The state of charge from solar to battery", 
        states=['deactivated','activated','mppt','equalizing','boost','floating','current limiting'])
connection_status = Enum('connection_status', 'Status of connection between monitor and bluetooth radio',
        states=['starting', 'connected', 'disconnected', 'not_found'])

# logging.basicConfig(level=logging.WARNING)
logging.basicConfig(level=logging.DEBUG)

config_file = sys.argv.get[1] if len(sys.argv) > 1 else "config.ini"
config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), config_file)
config = configparser.ConfigParser()
config.read(config_path)


def on_data_received(client, data):
    logging.debug("{} => {}".format(client.device.alias(), data))
    battery_percentage.set(data.get('battery_percentage'))
    battery_voltage.set(data.get('battery_voltage'))
    battery_current.set(data.get('battery_current'))
    battery_temperature.set(data.get('battery_temperature'))
    battery_type.set(data.get('battery_type'))
    controller_temperature.set(data.get('controller_temperature'))
    load_status.state(data.get('load_status'))
    load_voltage.set(data.get('load_voltage'))
    load_current.set(data.get('load_current'))
    load_power.set(data.get('load_power'))
    pv_voltage.set(data.get('pv_voltage'))
    pv_current.set(data.get('pv_current'))
    pv_power.set(data.get('pv_power'))
    max_charging_power_today.set(data.get('max_charging_power_today'))
    max_discharging_power_today.set(data.get('max_discharging_power_today'))
    charging_amp_hours_today.set(data.get('charging_amp_hours_today'))
    discharging_amp_hours_today.set(data.get('discharging_amp_hours_today'))
    power_generation_today.set(data.get('power_generation_today'))
    power_consumption_today.set(data.get('power_consumption_today'))
    power_generation_total.set(data.get('power_generation_total'))
    charging_status.state(data.get('charging_status'))
    connection_status.state('connected')
    logging.debug("Done passing data to prometheus, disconnecting...")
    client.disconnect()


@app.route("/metrics")
@REQUEST_TIME.time()
def metrics():
    connection_status.state('starting')
    try:
        RoverClient(config, on_data_received).connect()
    except Exception as e:
        connection_status.state('not_found')
        logging.warning(f"Exception occured: {e}")
        pass

    return generate_latest()


@app.route("/health")
def health():
    # TODO: Only attempt to connect if a mac address was passed
    try:
        RoverClient(config).connect()
    except Exception as e:
        logging.warning(f"Exception occured: {e}")
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
    app.run(host="0.0.0.0", port=9030)
