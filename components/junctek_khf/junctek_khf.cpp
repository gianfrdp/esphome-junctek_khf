#include "junctek_khf.h"
#include "esphome/core/log.h"
#include "esphome/core/optional.h"
#include <string>
#include <string.h>
#include <setjmp.h>

namespace esphome {
namespace junctek_khf {

static jmp_buf parsing_failed;
static const char *const TAG = "JunkTek KH-F";

esphome::optional<int> try_getval(const char*& cursor)
{
  long val;
  const char* pos = cursor;
  char* end = nullptr;
  val = strtoll(pos, &end, 10);
  if (end == pos || end == nullptr)
  {
    return nullopt;
  }
  if (*end != ',' && *end != '.')
  {
    ESP_LOGE(TAG, "Error no coma %s", cursor);
    return nullopt;
  }
  cursor = end + 1; // Skip coma
  return val;
}

// Get a value where it's expected to be "<number>[,.], incrementing the cursor past the end"
int getval(const char*& cursor)
{
  auto val = try_getval(cursor);
  if (!val)
  {
    longjmp(parsing_failed, 1);
  }
  return *val;
}
  

JuncTekKHF::JuncTekKHF(unsigned address, bool invert_current)
  : address_(address)
  , invert_current_(invert_current)
{

  
}

void JuncTekKHF::dump_config()
{
  ESP_LOGCONFIG(TAG, "junctek_khf:");
  ESP_LOGCONFIG(TAG, "  Address: %d", this->address_);
  ESP_LOGCONFIG(TAG, "  Invert Current: %s", this->invert_current_ ? "True" : "False");
  ESP_LOGCONFIG(TAG, "  Update Settings Interval: %d", this->update_settings_interval_);
  ESP_LOGCONFIG(TAG, "  Update Stats Interval: %d", this->update_stats_interval_);
}

void JuncTekKHF::handle_settings(const char* buffer)
{
  ESP_LOGD(TAG, "Settings %s", buffer);
  const char* cursor = buffer;
  const int address = getval(cursor);

  if (address != this->address_)
    return;

  const int checksum = getval(cursor);
  
  if (! verify_checksum(checksum, cursor))
    return;

  const float overVoltage = getval(cursor) / 100.0;
  const float underVoltage = getval(cursor) / 100.0;
  const float positiveOverCurrent = getval(cursor) / 1000.0;
  const float negativeOverCurrent = getval(cursor) / 100.00;
  const float overPowerProtection = getval(cursor) / 100.00;
  const float overTemperature = getval(cursor) - 100.0;
  const int protectionRecoverySeconds = getval(cursor);
  const int delayTime = getval(cursor);
  const float batteryAmpHourCapacity = getval(cursor) / 10.0;
  const int voltageCalibration = getval(cursor);
  const int currentCalibration = getval(cursor);
  const float temperatureCalibration = getval(cursor) - 100.0;
  const int reserved = getval(cursor);
  const int relayNormallyOpen = getval(cursor);
  const int currentratio = getval(cursor);

  if (battery_capacity_sensor_)
    this->battery_capacity_sensor_->publish_state(batteryAmpHourCapacity);

  // Save the capacity for calculating the %
  this->battery_capacity_ = batteryAmpHourCapacity;
  this->last_settings_ = esphome::millis();
  this->last_stats_  = this->last_settings_;
}

void JuncTekKHF::handle_status(const char* buffer)
{
  ESP_LOGV(TAG, "Status %s", buffer);
  const char* cursor = buffer;
  const int address = getval(cursor); //0
  if (address != this->address_)
    return;
 
  const int checksum = getval(cursor); //1
  if (! verify_checksum(checksum, cursor))
    return;

  const float voltage = getval(cursor) / 100.00; //2 in V
  const float amps = getval(cursor) / 100.00; //3 in A

  const float ampHourRemaining = getval(cursor) / 1000.0; //4 in Ah
  const float discharging_energy = getval(cursor) / 100000.0; //5 in kWh
  const float charging_energy = getval(cursor) / 100000.0; //6 in kWh

  const int operational = getval(cursor); //7
  const float temperature = getval(cursor) - 100.0; //8
  const int function = getval(cursor); //9
  const int outputStatus = getval(cursor); //10
  const int direction = getval(cursor); //11
  const float batteryLifeMinutes = getval(cursor); //12 in minutes
  const int time_adjustment = getval(cursor); //13
  const int date = getval(cursor); //14
  const int time = getval(cursor); //15
  
  const bool is_charging = direction == 1;

  ESP_LOGD(TAG, "Received : %f %f %f %f %f %d %f %d %d %d %f %d %d %d", 
         voltage, amps, ampHourRemaining, 
         discharging_energy, charging_energy, operational, 
         temperature, function, outputStatus, 
         direction, batteryLifeMinutes, time_adjustment, 
         date, time);

  if (voltage_sensor_)
    this->voltage_sensor_->publish_state(voltage);

  if (battery_level_sensor_ && this->battery_capacity_)
  {
    float battLvl = ampHourRemaining * 100.0 / * this->battery_capacity_;

    //prevent from publishing crazy numbers.
    if(battLvl < 100 && battLvl > 0)
      this->battery_level_sensor_->publish_state(battLvl);
  }

  if (current_sensor_) {
    float adjustedCurrent = is_charging ? amps : -amps;
    if (invert_current_)
      adjustedCurrent *= -1;
    current_sensor_->publish_state(adjustedCurrent);
  }

  if (current_direction_sensor_)
    this->current_direction_sensor_->publish_state(direction == 0);

  if (amp_hour_remain_sensor_)
    this->amp_hour_remain_sensor_->publish_state(ampHourRemaining);

  if (energy_discharged_sensor_)
  this->energy_discharged_sensor_->publish_state(discharging_energy);

  if (energy_charged_sensor_)
  this->energy_charged_sensor_->publish_state(charging_energy);

  if (output_status_text_sensor_) {
    std::string output_status = "";
    // 0-ON, 1-OVP, 2-OCP, 3-LVP,4-NCP, 5-OPP, 6-OTP, 99-OFF
    switch(outputStatus) {
      case 0:
        output_status = "ON";
        break;
      case 1:
        output_status = "OVP";
        break;
      case 3:
        output_status = "OCP";
        break;
      case 4:
        output_status = "LVP";
        break;
      case 5:
        output_status = "OPP";
        break;
      case 6:
        output_status = "OTP";
        break;
      case 99:
        output_status = "OFF";
        break;
      default:
        output_status = "Unknown";
    }

    this->output_status_text_sensor_->publish_state(output_status);
  }

  if (temperature_)
    this->temperature_->publish_state(temperature);

  if (power_sensor_) {
    float adjustedCurrent = is_charging ? amps : -amps;
    if (invert_current_)
      adjustedCurrent *= -1;
    float watts = voltage * adjustedCurrent;
    this->power_sensor_->publish_state(watts);
  }

  if (charging_power_sensor_) {
    float adjustedCurrent = amps;
    if (invert_current_)
      adjustedCurrent *= -1;
    float watts = voltage * adjustedCurrent;

    //we only care about amps that came into battery
    if(direction == 1)
      this->charging_power_sensor_->publish_state(watts); // should be power, not energy
    else
      this->charging_power_sensor_->publish_state(0);
  }

  if (discharging_power_sensor_) {

    float adjustedCurrent = amps;
    if (invert_current_)
      adjustedCurrent *= -1;
    float watts = voltage * adjustedCurrent;

    //we only care about amps that came from battery
    if(direction == 0)
      this->discharging_power_sensor_->publish_state(watts); // should be power, not energy
    else
      this->discharging_power_sensor_->publish_state(0);
  }

  if (remaining_time_sensor_)
      this->remaining_time_sensor_->publish_state(batteryLifeMinutes);

  this->last_stats_ = esphome::millis();
}

void JuncTekKHF::handle_line()
{
  //A failure in parsing will return back to here with a non-zero value
  if (setjmp(parsing_failed)){
    ESP_LOGE(TAG, "parsing_failed");
    return;
  }

  const char* buffer = &this->line_buffer_[0];

  if (buffer[0] != ':' || buffer[1] != 'r') {
    return;
  }

  if (strncmp(&buffer[2], "50=", 3) == 0)
    handle_status(&buffer[5]);
  else if (strncmp(&buffer[2], "51=", 3) == 0)
    handle_settings(&buffer[5]);
  else
    ESP_LOGD(TAG, "buffer: %s", buffer);

  return;
}

bool JuncTekKHF::readline()
{
  while (available()) {
    const char readch = read();
    if (readch > 0) {
      switch (readch) {
        case '\r': // Ignore carriage return
          break;
        case '\n': // Return on line feed
          this->line_pos_ = 0;  // Reset position index ready for next time
          return true;
        default:
          if (this->line_pos_ < MAX_LINE_LEN - 1)
          {
            this->line_buffer_[this->line_pos_++] = readch;
            this->line_buffer_[this->line_pos_] = 0;
          }
      }
    }
  }
  return false;
}

bool JuncTekKHF::verify_checksum(int checksum, const char* buffer)
{
  long total = 0;
  while (auto val = try_getval(buffer))
  {
    total += *val;
  }
  const bool checksum_valid = (total % 255) + 1 == checksum;
  ESP_LOGD(TAG, "Recv checksum %d total %ld valid %d", checksum, total, checksum_valid);
  return checksum_valid;
}

void JuncTekKHF::loop()
{
//todo not needed. uncomment if you do not receive any data, or dont use monitor, or monitor data refresh is turned of

//  const unsigned long start_time = esphome::millis();
//
//  if (!this->last_settings_ || (*this->last_settings_ + this->update_settings_interval_) < start_time)
//  {
//    this->last_settings_ = start_time;
//    char buffer[20];
//    sprintf(buffer, ":R51=%d,2,1,\r\n", this->address_);
//    write_str(buffer);
//  }
//
//  if (!this->last_stats_ || (*this->last_stats_ + this->update_stats_interval_) < start_time)
//  {
//    this->last_stats_ = start_time;
//    char buffer[20];
//    sprintf(buffer, ":R50=%d,2,1,\r\n", this->address_);
//    write_str(buffer);
//  }

  const unsigned long start_time = esphome::millis();
 
  if (!this->last_stats_ || ((*this->last_stats_ + this->update_stats_interval_) < start_time))
  {
    if (readline())
    {      
      handle_line();
    }
  }
}

float JuncTekKHF::get_setup_priority() const
{
  return setup_priority::DATA;
}

}  // namespace junctek_khf
}  // namespace esphome