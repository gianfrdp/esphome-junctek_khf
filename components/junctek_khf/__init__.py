import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import (
    CONF_ID,
    CONF_ADDRESS,
)

CODEOWNERS = ["@gianfrdp"]
DEPENDENCIES = ['uart']
AUTO_LOAD = ['uart']

CONF_JUNCTEK_ID = "junctek_id"
CONF_INVERT_CURRENT="invert_current"
CONF_UPDATE_SETTINGS_INTERVAL="update_settings_interval"
CONF_UPDATE_STATS_INTERVAL="update_stats_interval"

junctek_ns = cg.esphome_ns.namespace("junctek_khf")

JuncTekKHF = junctek_ns.class_(
    "JuncTekKHF", cg.Component, uart.UARTDevice
)

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(JuncTekKHF),
            cv.Optional(CONF_ADDRESS, default=1): cv.int_range(1, 255),
            cv.Optional(CONF_INVERT_CURRENT, default=False): cv.boolean,
            cv.Optional(CONF_UPDATE_SETTINGS_INTERVAL, default=30000): cv.int_,
            cv.Optional(CONF_UPDATE_STATS_INTERVAL, default=1000): cv.int_,
        }
).extend(cv.COMPONENT_SCHEMA.schema).extend(uart.UART_DEVICE_SCHEMA))

def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID], config[CONF_ADDRESS], config[CONF_INVERT_CURRENT])
    yield cg.register_component(var, config)
    yield uart.register_uart_device(var, config)
    
    cg.add(var.set_update_settings_interval(config[CONF_UPDATE_SETTINGS_INTERVAL]))
    cg.add(var.set_update_stats_interval(config[CONF_UPDATE_STATS_INTERVAL]))