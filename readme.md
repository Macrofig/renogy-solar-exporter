# Renogy Solar Controller Exporter

Start server: `pipenv run python3 ./src/main.py`

Start Docker: `docker run --net=host -v /run/dbus:/run/dbus:ro --privileged -t ghcr.io/macrofig/renogy-solar-exporter`

NOTE: Will only run on Linux because `gatt` only has files for Linux platforms, it returns noops on other platforms.

## Installing

## Usage

The following metrics are used.

### Metrics

battery_percentage: number,
battery_voltage: float,
battery_current: float,
battery_temperature: number,
battery_type: 'open','sealed','gel','lithium','self-customized'
controller_temperature: number,
load_status: off, on,
load_voltage: float,
load_current: float,
load_power: number,
pv_voltage: float,
pv_current: float,
pv_power: number,
max_charging_power_today: number,
max_discharging_power_today: number,
charging_amp_hours_today: number,
discharging_amp_hours_today: number,
power_generation_today: number,
power_consumption_today: number,
power_generation_total: number,
charging_status: 'deactivated','activated','mppt','equalizing','boost','floating','current limiting'
connection_status: 'starting', 'connected', 'disconnected', 'not_found'

### Config

- `mac_addr`: String
- `alias`: String


## Build

### Docker
`docker build -t ghcr.io/macrofig/renogy-solar-exporter .`
`docker push ghcr.io/macrofig/renogy-solar-exporter:latest`

### Pi

`sudo apt install python3-pip python3-dbus`
`pip install -r ./src/requirements.txt`

## TODO

- Make port configurable
- If no `mac_addr` is given, attempt to connect to the first discovered address, otherwise throw `Error` (but allow the server to start)
- Handle errors from Renogy BT better; server should never stop from a RenogyBT error. Errors should be reported for Prometheus.
- Improve logging
- Make config an environment variable
- Consume renogy-bt repo more cleanly (as a dependancy rather than copy/paste)
- Clean up this Readme