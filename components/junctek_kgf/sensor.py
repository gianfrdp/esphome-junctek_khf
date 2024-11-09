import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart, sensor
from esphome.const import (
    CONF_RAW,
    CONF_ID,
    CONF_ADDRESS,
    CONF_INPUT,
    CONF_NUMBER,
    CONF_HARDWARE_UART,
    CONF_TEMPERATURE,
    CONF_VOLTAGE,
    CONF_CURRENT,
    CONF_BATTERY_LEVEL,
    CONF_DIRECTION,

    DEVICE_CLASS_VOLTAGE,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
    UNIT_VOLT,
    UNIT_CELSIUS,
    UNIT_AMPERE,
    UNIT_WATT,
    UNIT_OHM,
    CONF_UPDATE_INTERVAL,
    UNIT_EMPTY,
    UNIT_PERCENT,
    ICON_EMPTY,
    UNIT_KILOWATT_HOURS,
    UNIT_MINUTE,
    ICON_EMPTY,
    ICON_POWER,
    ICON_BATTERY,
    ICON_THERMOMETER,
    ICON_FLASH,
    ICON_PERCENT,
    ICON_TIMER,
    ICON_POWER,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_SWITCH,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_DURATION,
    DEVICE_CLASS_BATTERY_CHARGING,
    DEVICE_CLASS_ENERGY_STORAGE,
)

UNIT_AMPER_HOURS = 'Ah'
DEPENDENCIES = ["uart"]
AUTO_LOAD = ["sensor"]

# sensors
CONF_CURRENT_DIRECTION="current_direction"
CONF_CHARGING_POWER = 'charging_power'
CONF_DISCHARGING_POWER = 'discharging_power'
CONF_TIME_REMAINING = 'remaining_time'
CONF_BATTERY_POWER = 'battery_power'
CONF_AMP_HOUR_REMAIN = "amp_hour_remain"
CONF_ENERGY_DISCHARGED = "energy_discharged"
CONF_ENERGY_CHARGED = "energy_charged"
CONF_OUTPUT_STATUS = "output_status"
CONF_POWER = "power"
CONF_BATTERY_CAPACITY = "battery_capacity"

TYPES = [
    CONF_VOLTAGE,
    CONF_CURRENT,
    CONF_BATTERY_LEVEL,
    CONF_TEMPERATURE,
    CONF_DIRECTION,
    CONF_BATTERY_POWER,
    CONF_TIME_REMAINING,
    CONF_CHARGING_POWER,
    CONF_DISCHARGING_POWER,
    CONF_AMP_HOUR_REMAIN,
    CONF_ENERGY_DISCHARGED,
    CONF_ENERGY_CHARGED,
    CONF_OUTPUT_STATUS,
    CONF_POWER,
    CONF_BATTERY_CAPACITY
]

CONF_INVERT_CURRENT="invert_current"
CONF_UPDATE_SETTINGS_INTERVAL="update_settings_interval"
CONF_UPDATE_STATS_INTERVAL="update_stats_interval"

JuncTekKGF = cg.global_ns.class_(
    "JuncTekKGF", cg.Component, uart.UARTDevice
)

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(JuncTekKGF),
            cv.Optional(CONF_ADDRESS, default=1): cv.int_range(1, 255),
            cv.Optional(CONF_VOLTAGE): sensor.sensor_schema(
                unit_of_measurement=UNIT_VOLT,
                icon=ICON_FLASH,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_VOLTAGE,
                state_class=STATE_CLASS_MEASUREMENT                
            ),
            cv.Optional(CONF_CURRENT): sensor.sensor_schema(
                unit_of_measurement=UNIT_AMPERE,
                icon="mdi:current-dc",
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_CURRENT,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_BATTERY_LEVEL): sensor.sensor_schema(
                unit_of_measurement=UNIT_PERCENT,
                icon=ICON_PERCENT,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_BATTERY,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_TEMPERATURE): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                icon=ICON_THERMOMETER,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_DIRECTION): sensor.sensor_schema(
                accuracy_decimals=0,
            ),
            cv.Optional(CONF_OUTPUT_STATUS): sensor.sensor_schema(
                accuracy_decimals=0,
                icon="mdi:list-status"
            ),
            cv.Optional(CONF_POWER): sensor.sensor_schema(
                unit_of_measurement=UNIT_WATT,
                icon=ICON_POWER,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_POWER,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_TIME_REMAINING): sensor.sensor_schema(
                unit_of_measurement=UNIT_MINUTE,
                icon=ICON_TIMER,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_DURATION,
                state_class=STATE_CLASS_MEASUREMENT,
             ),
            cv.Optional(CONF_CHARGING_POWER): sensor.sensor_schema(
                unit_of_measurement=UNIT_WATT,
                icon="mdi:lightning-bolt",
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_POWER,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_DISCHARGING_POWER): sensor.sensor_schema(
                unit_of_measurement=UNIT_WATT,
                icon="mdi:lightning-bolt",
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_POWER,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_AMP_HOUR_REMAIN): sensor.sensor_schema(
                unit_of_measurement=UNIT_AMPER_HOURS,
                icon=ICON_BATTERY,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_BATTERY,
                state_class=STATE_CLASS_MEASUREMENT,
            ),

            cv.Optional(CONF_ENERGY_DISCHARGED): sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOWATT_HOURS,
                icon=ICON_BATTERY,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_ENERGY,
                state_class=STATE_CLASS_TOTAL_INCREASING,
            ),
            cv.Optional(CONF_ENERGY_CHARGED): sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOWATT_HOURS,
                icon=ICON_BATTERY,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_ENERGY,
                state_class=STATE_CLASS_TOTAL_INCREASING,
            ),
            cv.Optional(CONF_BATTERY_CAPACITY): sensor.sensor_schema(
                unit_of_measurement=UNIT_AMPER_HOURS,
                icon=ICON_BATTERY,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_ENERGY_STORAGE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),

            cv.Optional(CONF_INVERT_CURRENT, default=False): cv.boolean,
            cv.Optional(CONF_UPDATE_SETTINGS_INTERVAL, default=30000): cv.int_,
            cv.Optional(CONF_UPDATE_STATS_INTERVAL, default=1000): cv.int_,
            cv.Optional(CONF_CURRENT_DIRECTION, default=True): cv.boolean,
        }
    ).extend(uart.UART_DEVICE_SCHEMA)
    )

async def setup_conf(config, key, hub):
    if key in config:
        conf = config[key]
        sens = await sensor.new_sensor(conf)
        cg.add(getattr(hub, f"set_{key}_sensor")(sens))


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID], config[CONF_ADDRESS], config[CONF_INVERT_CURRENT])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)
    for key in TYPES:
        await setup_conf(config, key, var)

    cg.add(var.set_update_settings_interval(config[CONF_UPDATE_SETTINGS_INTERVAL]))
    cg.add(var.set_update_stats_interval(config[CONF_UPDATE_STATS_INTERVAL]))
