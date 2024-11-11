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
    ENTITY_CATEGORY_DIAGNOSTIC,
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
    UNIT_SECOND,
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
from . import CONF_JUNCTEK_ID, JuncTekKHF

UNIT_AMPER_HOURS = 'Ah'
DEPENDENCIES = ["junctek_khf"]
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
CONF_POWER = "power"
CONF_BATTERY_CAPACITY = "battery_capacity"
CONF_OVER_VOLTAGE_PROTECTION = "over_voltage_protection"
CONF_UNDER_VOLTAGE_PROTECTION = "under_voltage_protection"
CONF_OVER_DISCHARGE_CURRENT_PROTECTION = "over_discharge_current_protection"
CONF_OVER_CHARGE_CURRENT_PROTECTION = "over_charge_current_protection"
CONF_OVER_POWER_PROTECTION = "over_power_protection"
CONF_OVER_TEMPERATURE_PROTECTION = "over_temperature_protection"
CONF_UNDER_TEMPERATURE_PROTECTION = "under_temperature_protection"
CONF_PROTECTION_RECOVERY_TIME = "protection_recovery_time"
CONF_PROTECTION_DELAY_TIME = "protection_delay_time"
CONF_FULL_BATTERY_VOLTAGE = "full_battery_voltage"
CONF_LOW_BATTERY_VOLTAGE = "low_battery_voltage"
CONF_FULL_CHARGE_CURRENT = "full_charge_current"
CONF_MONITORING_TIME = "monitoring_time"
CONF_BT_PASSWORD = "bt_password"
CONF_LOGGING_INTERVAL = "data_logging_interval"

SENSORS = [
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
    CONF_POWER,
    CONF_BATTERY_CAPACITY,
    CONF_OVER_VOLTAGE_PROTECTION,
    CONF_UNDER_VOLTAGE_PROTECTION,
    CONF_OVER_DISCHARGE_CURRENT_PROTECTION,
    CONF_OVER_CHARGE_CURRENT_PROTECTION,
    CONF_OVER_POWER_PROTECTION,
    CONF_OVER_TEMPERATURE_PROTECTION,
    CONF_UNDER_TEMPERATURE_PROTECTION,
    CONF_PROTECTION_RECOVERY_TIME,
    CONF_PROTECTION_DELAY_TIME,
    CONF_FULL_BATTERY_VOLTAGE,
    CONF_LOW_BATTERY_VOLTAGE,
    CONF_FULL_CHARGE_CURRENT,
    CONF_MONITORING_TIME,
    CONF_BT_PASSWORD,
    CONF_LOGGING_INTERVAL,
]

CONFIG_SCHEMA = cv.Schema(
        {
            cv.GenerateID(CONF_JUNCTEK_ID): cv.use_id(JuncTekKHF),
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
            cv.Optional(CONF_OVER_VOLTAGE_PROTECTION): sensor.sensor_schema(
                unit_of_measurement=UNIT_VOLT,
                icon=ICON_EMPTY,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_VOLTAGE,
                state_class=STATE_CLASS_MEASUREMENT,
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
            ),
            cv.Optional(CONF_UNDER_VOLTAGE_PROTECTION): sensor.sensor_schema(
                unit_of_measurement=UNIT_VOLT,
                icon=ICON_EMPTY,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_VOLTAGE,
                state_class=STATE_CLASS_MEASUREMENT,
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
            ),
            cv.Optional(CONF_OVER_DISCHARGE_CURRENT_PROTECTION): sensor.sensor_schema(
                unit_of_measurement=UNIT_AMPERE,
                icon=ICON_EMPTY,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_CURRENT,
                state_class=STATE_CLASS_MEASUREMENT,
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
            ),
            cv.Optional(CONF_OVER_CHARGE_CURRENT_PROTECTION): sensor.sensor_schema(
                unit_of_measurement=UNIT_AMPERE,
                icon=ICON_EMPTY,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_CURRENT,
                state_class=STATE_CLASS_MEASUREMENT,
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
            ),
            cv.Optional(CONF_OVER_POWER_PROTECTION): sensor.sensor_schema(
                unit_of_measurement=UNIT_WATT,
                icon=ICON_EMPTY,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_POWER,
                state_class=STATE_CLASS_MEASUREMENT,
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
            ),
            cv.Optional(CONF_OVER_TEMPERATURE_PROTECTION): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                icon=ICON_EMPTY,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
            ),
            cv.Optional(CONF_UNDER_TEMPERATURE_PROTECTION): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                icon=ICON_EMPTY,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
            ),
            cv.Optional(CONF_PROTECTION_RECOVERY_TIME): sensor.sensor_schema(
                unit_of_measurement=UNIT_SECOND,
                icon=ICON_TIMER,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_DURATION,
                state_class=STATE_CLASS_MEASUREMENT,
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
            ),
            cv.Optional(CONF_PROTECTION_DELAY_TIME): sensor.sensor_schema(
                unit_of_measurement=UNIT_SECOND,
                icon=ICON_TIMER,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_DURATION,
                state_class=STATE_CLASS_MEASUREMENT,
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
            ),
            cv.Optional(CONF_FULL_BATTERY_VOLTAGE): sensor.sensor_schema(
                unit_of_measurement=UNIT_VOLT,
                icon=ICON_EMPTY,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_VOLTAGE,
                state_class=STATE_CLASS_MEASUREMENT,
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
            ),
            cv.Optional(CONF_LOW_BATTERY_VOLTAGE): sensor.sensor_schema(
                unit_of_measurement=UNIT_VOLT,
                icon=ICON_EMPTY,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_VOLTAGE,
                state_class=STATE_CLASS_MEASUREMENT,
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
            ),
            cv.Optional(CONF_FULL_CHARGE_CURRENT): sensor.sensor_schema(
                unit_of_measurement=UNIT_AMPERE,
                icon=ICON_EMPTY,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_CURRENT,
                state_class=STATE_CLASS_MEASUREMENT,
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
            ),
            cv.Optional(CONF_MONITORING_TIME): sensor.sensor_schema(
                unit_of_measurement=UNIT_SECOND,
                icon=ICON_TIMER,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_DURATION,
                state_class=STATE_CLASS_MEASUREMENT,
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
            ),
            cv.Optional(CONF_BT_PASSWORD): sensor.sensor_schema(
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
            ),
            cv.Optional(CONF_LOGGING_INTERVAL): sensor.sensor_schema(
                unit_of_measurement=UNIT_SECOND,
                icon=ICON_TIMER,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_DURATION,
                state_class=STATE_CLASS_MEASUREMENT,
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
            ),
            
            cv.Optional(CONF_CURRENT_DIRECTION, default=True): cv.boolean,
        }
    )

async def to_code(config):
    hub = await cg.get_variable(config[CONF_JUNCTEK_ID])
    for key in SENSORS:
        if key in config:
            conf = config[key]
            sens = await sensor.new_sensor(conf)
            cg.add(getattr(hub, f"set_{key}_sensor")(sens))
