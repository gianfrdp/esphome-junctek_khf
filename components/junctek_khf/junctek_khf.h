#pragma once

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include "esphome/components/binary_sensor/binary_sensor.h"
#include "esphome/components/uart/uart.h"

namespace esphome {

namespace junctek_khf {

class JuncTekKHF
  : public esphome::Component
  , public uart::UARTDevice
{
public:
  JuncTekKHF(unsigned address = 1, bool invert_current=false);

  // Sensors
  // R50 sensors
  void set_voltage_sensor(sensor::Sensor *voltage_sensor) { voltage_sensor_ = voltage_sensor; }
  void set_current_sensor(sensor::Sensor *current_sensor) { current_sensor_ = current_sensor; }
  void set_temperature_sensor(sensor::Sensor *temperature_sensor) { temperature_sensor_ = temperature_sensor; }
  void set_update_settings_interval(uint32_t interval) { update_settings_interval_ = interval; }
  void set_update_stats_interval(uint32_t interval) { update_stats_interval_ = interval; }
  void set_current_direction_sensor(sensor::Sensor *current_direction_sensor) { current_direction_sensor_ = current_direction_sensor; }
  void set_battery_ohm_sensor(sensor::Sensor *battery_ohm_sensor) { battery_ohm_sensor_ = battery_ohm_sensor; }
  void set_battery_level_sensor(sensor::Sensor *battery_level_sensor) { battery_level_sensor_ = battery_level_sensor; }
  void set_amp_hour_remain_sensor(sensor::Sensor *amp_hour_remain_sensor) { amp_hour_remain_sensor_ = amp_hour_remain_sensor; }
  void set_energy_discharged_sensor(sensor::Sensor *energy_discharged_sensor) { energy_discharged_sensor_ = energy_discharged_sensor; }
  void set_energy_charged_sensor(sensor::Sensor *energy_charged_sensor) { energy_charged_sensor_ = energy_charged_sensor; }
  void set_charging_power_sensor(sensor::Sensor *charging_power_sensor) { charging_power_sensor_ = charging_power_sensor; }
  void set_discharging_power_sensor(sensor::Sensor *discharging_power_sensor) { discharging_power_sensor_ = discharging_power_sensor; }
  void set_power_sensor(sensor::Sensor *power_sensor) { power_sensor_ = power_sensor; }
  void set_remaining_time_sensor(sensor::Sensor *remaining_time_sensor) { remaining_time_sensor_ = remaining_time_sensor; }
  void set_runtime_sensor(sensor::Sensor *runtime_sensor) { runtime_sensor_ = runtime_sensor; }
  // R51 sensors
  void set_over_voltage_protection_sensor(sensor::Sensor *over_voltage_protection_sensor) { over_voltage_protection_sensor_ = over_voltage_protection_sensor; }
  void set_under_voltage_protection_sensor(sensor::Sensor *under_voltage_protection_sensor) { under_voltage_protection_sensor_ = under_voltage_protection_sensor; }
  void set_over_discharge_current_protection_sensor(sensor::Sensor *over_discharge_current_protection_sensor) { over_discharge_current_protection_sensor_ = over_discharge_current_protection_sensor; }
  void set_over_charge_current_protection_sensor(sensor::Sensor *over_charge_current_protection_sensor) { over_charge_current_protection_sensor_ = over_charge_current_protection_sensor; }
  void set_over_power_protection_sensor(sensor::Sensor *over_power_protection_sensor) { over_power_protection_sensor_ = over_power_protection_sensor; }
  void set_over_temperature_protection_sensor(sensor::Sensor *over_temperature_protection_sensor) { over_temperature_protection_sensor_ = over_temperature_protection_sensor; }
  void set_under_temperature_protection_sensor(sensor::Sensor *under_temperature_protection_sensor) { under_temperature_protection_sensor_ = under_temperature_protection_sensor; }
  void set_protection_recovery_time_sensor(sensor::Sensor *protection_recovery_time_sensor) { protection_recovery_time_sensor_ = protection_recovery_time_sensor; }
  void set_protection_delay_time_sensor(sensor::Sensor *protection_delay_time_sensor) { protection_delay_time_sensor_ = protection_delay_time_sensor; }
  void set_battery_capacity_sensor(sensor::Sensor *battery_capacity_sensor) { battery_capacity_sensor_ = battery_capacity_sensor; }
  void set_voltage_calibration_sensor(sensor::Sensor *voltage_calibration_sensor) { voltage_calibration_sensor_ = voltage_calibration_sensor; }
  void set_current_calibration_sensor(sensor::Sensor *current_calibration_sensor) { current_calibration_sensor_ = current_calibration_sensor; }
  void set_temperature_calibration_sensor(sensor::Sensor *temperature_calibration_sensor) { temperature_calibration_sensor_ = temperature_calibration_sensor; }
  void set_full_battery_voltage_sensor(sensor::Sensor *full_battery_voltage_sensor) { full_battery_voltage_sensor_ = full_battery_voltage_sensor; }
  void set_low_battery_voltage_sensor(sensor::Sensor *low_battery_voltage_sensor) { low_battery_voltage_sensor_ = low_battery_voltage_sensor; }
  void set_full_charge_current_sensor(sensor::Sensor *full_charge_current_sensor) { full_charge_current_sensor_ = full_charge_current_sensor; }
  void set_monitoring_time_sensor(sensor::Sensor *monitoring_time_sensor) { monitoring_time_sensor_ = monitoring_time_sensor; }
  void set_bt_password_sensor(sensor::Sensor *bt_password_sensor) { bt_password_sensor_ = bt_password_sensor; }
  void set_data_logging_interval_sensor(sensor::Sensor *data_logging_interval_sensor) { data_logging_interval_sensor_ = data_logging_interval_sensor; }

  // TextSensors
  void set_output_status_text_sensor(text_sensor::TextSensor *output_status_text_sensor) { output_status_text_sensor_ = output_status_text_sensor; }
  void set_temperature_uom_text_sensor(text_sensor::TextSensor *temperature_uom_text_sensor) { temperature_uom_text_sensor_ = temperature_uom_text_sensor; }
  
  // BinarySensors
  void set_relay_normally_open_binary_sensor(binary_sensor::BinarySensor *relay_normally_open_binary_sensor) { relay_normally_open_binary_sensor_ = relay_normally_open_binary_sensor; }
  void set_log_enabled_binary_sensor(binary_sensor::BinarySensor *log_enabled_binary_sensor) { log_enabled_binary_sensor_ = log_enabled_binary_sensor; }
  void set_charging_binary_sensor(binary_sensor::BinarySensor *charging_sensor) { charging_sensor_ = charging_sensor; }
  void set_discharging_binary_sensor(binary_sensor::BinarySensor *discharging_sensor) { discharging_sensor_ = discharging_sensor; }

  void dump_config() override;
  void loop() override;
  float get_setup_priority() const;// override;

protected:
  bool readline();
  void handle_line();
  void handle_status(const char* buffer);
  void handle_settings(const char* buffer);
  void request_data(uint8_t data_id);
  void decode_data(std::vector<uint8_t> data);
  bool verify_checksum(int checksum, const char* buffer);

  const unsigned address_;
  uint32_t update_settings_interval_ = 30000;
  uint32_t update_stats_interval_ = 1000;

  sensor::Sensor* voltage_sensor_{nullptr};
  sensor::Sensor* current_sensor_{nullptr};
  sensor::Sensor* temperature_sensor_{nullptr};
  sensor::Sensor* current_direction_sensor_{nullptr};
  sensor::Sensor* battery_ohm_sensor_{nullptr};
  sensor::Sensor* battery_level_sensor_{nullptr};

  sensor::Sensor* amp_hour_remain_sensor_{nullptr};
  sensor::Sensor* energy_discharged_sensor_{nullptr};
  sensor::Sensor* energy_charged_sensor_{nullptr};
  sensor::Sensor* charging_power_sensor_{nullptr};
  sensor::Sensor* discharging_power_sensor_{nullptr};

  sensor::Sensor* power_sensor_{nullptr};
  sensor::Sensor* runtime_sensor_{nullptr};
  sensor::Sensor* remaining_time_sensor_{nullptr};
  sensor::Sensor* battery_capacity_sensor_{nullptr};
  sensor::Sensor* over_voltage_protection_sensor_{nullptr};
  sensor::Sensor* under_voltage_protection_sensor_{nullptr};
  sensor::Sensor* over_discharge_current_protection_sensor_{nullptr};
  sensor::Sensor* over_charge_current_protection_sensor_{nullptr};
  sensor::Sensor* over_power_protection_sensor_{nullptr};
  sensor::Sensor* over_temperature_protection_sensor_{nullptr};
  sensor::Sensor* under_temperature_protection_sensor_{nullptr};
  sensor::Sensor* protection_recovery_time_sensor_{nullptr};
  sensor::Sensor* protection_delay_time_sensor_{nullptr};
  sensor::Sensor* voltage_calibration_sensor_{nullptr};
  sensor::Sensor* current_calibration_sensor_{nullptr};
  sensor::Sensor* temperature_calibration_sensor_{nullptr};
  sensor::Sensor* full_battery_voltage_sensor_{nullptr};
  sensor::Sensor* low_battery_voltage_sensor_{nullptr};
  sensor::Sensor* full_charge_current_sensor_{nullptr};
  sensor::Sensor* monitoring_time_sensor_{nullptr};
  sensor::Sensor* bt_password_sensor_{nullptr};
  sensor::Sensor* data_logging_interval_sensor_{nullptr};

  text_sensor::TextSensor* output_status_text_sensor_{nullptr};
  text_sensor::TextSensor* temperature_uom_text_sensor_{nullptr};

  binary_sensor::BinarySensor* relay_normally_open_binary_sensor_{nullptr};
  binary_sensor::BinarySensor* log_enabled_binary_sensor_{nullptr};
  binary_sensor::BinarySensor* charging_sensor_{nullptr};
  binary_sensor::BinarySensor* discharging_sensor_{nullptr};

  static constexpr int MAX_LINE_LEN = 120;
  std::array<char, MAX_LINE_LEN> line_buffer_;
  size_t line_pos_ = 0;

  optional<float> battery_capacity_;
  optional<unsigned long> last_settings_;
  optional<unsigned long> last_stats_;
  bool invert_current_;
  optional<float> last_charged_energy_ = 0;
  optional<float> last_discharged_energy_ = 0;
};

}  // namespace junctek_khf
}  // namespace esphome