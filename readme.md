# Renogy Solar Controller Exporter

Start server: `pipenv run python3 ./solar-cli.py`

## Installing

## Usage

The following metrics are used.

### Metrics

function: READ,
model: string,
battery_percentage: number,
battery_voltage: float,
battery_current: float,
battery_temperature: number,
controller_temperature: number,
load_status: off | on,
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
charging_status: "deactivated",
battery_type: 'sealed',
**device: 'BT-TH-300DC793',
**client: 'RoverClient'

### Config

- `mac_addr`: String
- `alias`: String

## Docker

## TODO

- Make port configurable
- If no `mac_addr` is given, attempt to connect to the first discovered address, otherwise throw `Error` (but allow the server to start)