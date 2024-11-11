import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor
from esphome.const import (
    CONF_ID,
    ENTITY_CATEGORY_DIAGNOSTIC,
)
from . import CONF_JUNCTEK_ID, JuncTekKHF

DEPENDENCIES = ["junctek_khf"]
AUTO_LOAD = ["sensor"]

CONF_OUTPUT_STATUS = "output_status"
CONF_TEMPERATURE_UOM = "temperature_uom"

TEXT_SENSORS = [
    CONF_OUTPUT_STATUS,
    CONF_TEMPERATURE_UOM,
]

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_JUNCTEK_ID): cv.use_id(JuncTekKHF),
        cv.Optional(CONF_OUTPUT_STATUS): text_sensor.text_sensor_schema(
            icon="mdi:list-status",
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        ),
        cv.Optional(CONF_TEMPERATURE_UOM): text_sensor.text_sensor_schema(
            icon="mdi:thermometer-auto",
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        ),
    }
)
   
async def to_code(config):
    hub = await cg.get_variable(config[CONF_JUNCTEK_ID])
    for key in TEXT_SENSORS:
        if key in config:
            conf = config[key]
            sens = cg.new_Pvariable(conf[CONF_ID])
            await text_sensor.register_text_sensor(sens, conf)
            cg.add(getattr(hub, f"set_{key}_text_sensor")(sens))
