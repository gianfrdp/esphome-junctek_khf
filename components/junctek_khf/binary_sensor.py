import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.const import (
    CONF_ID,
    ICON_EMPTY,
    ENTITY_CATEGORY_DIAGNOSTIC,
)
from . import CONF_JUNCTEK_ID, JuncTekKHF

DEPENDENCIES = ["junctek_khf"]
AUTO_LOAD = ["binary_sensor"]

CONF_RELAY_NORMALLY_OPEN = "relay_normally_open"
CONF_LOG_ENABLED = "log_enabled"
CONF_CHARGING = "charging"
CONF_DISCHARGING = "discharging"

BINARY_SENSORS = [
    CONF_RELAY_NORMALLY_OPEN,
    CONF_LOG_ENABLED,
    CONF_CHARGING,
    CONF_DISCHARGING,
]

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_JUNCTEK_ID): cv.use_id(JuncTekKHF),
        cv.Optional(CONF_RELAY_NORMALLY_OPEN): binary_sensor.binary_sensor_schema(
            icon="mdi:electric-switch",
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        ),
        cv.Optional(CONF_LOG_ENABLED): binary_sensor.binary_sensor_schema(
            icon="mdi:math-log",
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        ),
        cv.Optional(CONF_CHARGING): binary_sensor.binary_sensor_schema(
            icon=ICON_EMPTY,
        ),
        cv.Optional(CONF_DISCHARGING): binary_sensor.binary_sensor_schema(
            icon=ICON_EMPTY,
        ),
    }
)
   
async def to_code(config):
    hub = await cg.get_variable(config[CONF_JUNCTEK_ID])
    for key in BINARY_SENSORS:
        if key in config:
            conf = config[key]
            sens = cg.new_Pvariable(conf[CONF_ID])
            await binary_sensor.register_binary_sensor(sens, conf)
            cg.add(getattr(hub, f"set_{key}_binary_sensor")(sens))
