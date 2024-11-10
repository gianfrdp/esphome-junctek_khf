#pragma once

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include "esphome/components/uart/uart.h"

namespace esphome {

namespace junctek_khf {

class JuncTekKHF
  : public esphome::Component
  , public uart::UARTDevice
{
public:
  JuncTekKHF(unsigned address = 1, bool invert_current=false);

  void set_voltage_sensor(sensor::Sensor *voltage_sensor) { voltage_sensor_ = voltage_sensor; }
  void set_current_sensor(sensor::Sensor *current_sensor) { current_sensor_ = current_sensor; }
  void set_temperature_sensor(sensor::Sensor *temperature) { temperature_ = temperature; }
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
  void set_output_status_text_sensor(text_sensor::TextSensor *output_status_text_sensor) { output_status_text_sensor_ = output_status_text_sensor; }
  void set_power_sensor(sensor::Sensor *power_sensor) { power_sensor_ = power_sensor; }
  void set_remaining_time_sensor(sensor::Sensor *remaining_time_sensor) { remaining_time_sensor_ = remaining_time_sensor; }
  void set_runtime_sensor(sensor::Sensor *runtime_sensor) { runtime_sensor_ = runtime_sensor; }
  void set_battery_capacity_sensor(sensor::Sensor *battery_capacity_sensor) { battery_capacity_sensor_ = battery_capacity_sensor; }

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
  sensor::Sensor* temperature_{nullptr};
  sensor::Sensor* current_direction_sensor_{nullptr};
  sensor::Sensor* battery_ohm_sensor_{nullptr};
  sensor::Sensor* battery_level_sensor_{nullptr};

  sensor::Sensor* amp_hour_remain_sensor_{nullptr};
  sensor::Sensor* energy_discharged_sensor_{nullptr};
  sensor::Sensor* energy_charged_sensor_{nullptr};
  sensor::Sensor* charging_power_sensor_{nullptr};
  sensor::Sensor* discharging_power_sensor_{nullptr};

  text_sensor::TextSensor* output_status_text_sensor_{nullptr};
  sensor::Sensor* power_sensor_{nullptr};
  sensor::Sensor* runtime_sensor_{nullptr};
  sensor::Sensor* remaining_time_sensor_{nullptr};
  sensor::Sensor* battery_capacity_sensor_{nullptr};

  static constexpr int MAX_LINE_LEN = 120;
  std::array<char, MAX_LINE_LEN> line_buffer_;
  size_t line_pos_ = 0;

  optional<float> battery_capacity_;
  optional<unsigned long> last_settings_;
  optional<unsigned long> last_stats_;
  bool invert_current_;
};

}  // namespace junctek_khf
}  // namespace esphome