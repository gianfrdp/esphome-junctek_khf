# esphome-junctek_khf
Component for esphome to read status from a Junctek KH-F coulometer/battery monitor via UART. It also reads settings so it is able correctly calculate battery percentage left. But settings are not exposed to HomeAssistant.

## Features
Connects to the Junctek KGF series battery monitor via UART (RS-485 *adapter NOT needed*) and retrieves the following values:

* Battery Voltage
* Battery Percent
* Battery Current
* Power
* Temperature
* Battery kWh Charged Total
* Battery Ah Remaining
* Battery kWh Discharged Total
* Battery Charging Power
* Battery Discharging Power
* Battery time remaining
* Output Status

## Requirements
* ESPHome

## Known problems
* If could call it a problem - when data not available from Junctek interface - you keep seeing the latest value in sensors. Which may misslead. Sensors will not be updated nor they be set to Unavailable.

## Usage
### Connect hardware.
The ESP32 TX and RX needs to be connected via Junctek LINK port using a 4P4C (RJ10) connector. Monitor SHOULD BE connected too and active. If you dont have monitor you should edit component loop method and uncomment old code, and comment out new one. Monitor makes calls to Junctek asking for data, ESP32 just reads the response and parses it. So you keep the monitor + will have data comming to your IoT system.

## ESPHOME Config
The applicable config for the device should look something like:

```yaml
substitutions:
  name: "junctek-kh140-f"
  device_name: ${name}
  device_id: junctek_kh140f
  friendly_name: "Junctek KH140F"
  device_description: "Monitor Junctek KH140F SmartShunt via RS485 Link in TTL mode"

esphome:
  name: ${name}
  friendly_name: ${friendly_name}
  comment: ${device_description}

external_components:
  #- source: github://gianfrdp/esphome-junctek_khf@junctek_khf
  - source:
      type: git
      url: https://github.com/gianfrdp/esphome-junctek_khf
      ref: junctek_khf
    components: [ junctek_khf ]

esp32:
  board: esp32dev
  framework:
    type: arduino

uart:
  tx_pin: GPIO17
  rx_pin: GPIO16
  id: uart_junctek
  baud_rate: 115200

junctek_khf:
  id: junctek_id
  address: 1
  invert_current: false
  update_stats_interval: 5000 # 5 seconds
  update_settings_interval: 30000 # 30 seconds
  uart_id: uart_junctek

sensor:
  - platform: junctek_kgf
    junctek_id: junctek_id
    voltage:
      name: "${name} Voltage"
      id: ${device_id}_voltage
    current:
      name: "${name} Current"
      id: ${device_id}_current
    battery_level:
      name: "${name} SoC"
      id: ${device_id}_battery_level
    power:
      name: "${name} Power"
      id: ${device_id}_power
    amp_hour_remain:
      name: "${name} Remaining Capacity"
      id: ${device_id}_remaining_capacity
    battery_capacity:
      name: "${name} Total Capacity"
      id: ${device_id}_battery_capacity
    energy_charged:
      name: "${name} Charging Energy"
      id: ${device_id}_charging_energy
    energy_discharged:
      name: "${name} Discharging Energy"
      id: ${device_id}_discharging_energy
    temperature:
      name: "${name} Temperature"
      id: ${device_id}_temperature
    remaining_time:
      name: "${name} Remaining Time"
      id: ${device_id}_remaining_time
    charging_power:
      name: "${name} Charging Power"
      id: ${device_id}_charging_power
    discharging_power:
      name: "${name} Discharging Power"   
      id: ${device_id}_discharging_power

text_sensor:
  - platform: junctek_khf
    junctek_id: junctek_id
    output_status:
      name: "${name} Output Status"
      id: ${device_id}_output_status

```

Not all sensors need to be added.
Address is assumed to be 1 if not provided. (this is configured on the monitor)
invert_current: This inverts the reported current, it's recommended to include this option with either true or false (which ever makes the current make more sense for your setup). The default is currently false (and false will match previous behaviour), but may change to true in future updates.

