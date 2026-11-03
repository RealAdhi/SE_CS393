import pytest
from thermostat_control import target_temperature, hvac_action, energy_alert

#Example test cases:
def test_away_mode():
    assert target_temperature("away", True, 12) == 16

def test_no_readings():
    assert energy_alert([], 10) == "ok"

#Write the rest of the test cases so that the code is 90- 100% covered.

# target_temperature

def test_sleep_before_6_is_18():
    assert target_temperature("sleep", True, 5) == 18

def test_sleep_at_or_after_22_is_18():
    assert target_temperature("sleep", False, 22) == 18

def test_sleep_daytime_is_20():
    assert target_temperature("sleep", True, 12) == 20

def test_unoccupied_is_18():
    assert target_temperature("home", False, 12) == 18

def test_morning_occupied_is_22():
    assert target_temperature("home", True, 6) == 22
    assert target_temperature("home", True, 8) == 22

def test_evening_occupied_is_21():
    assert target_temperature("home", True, 17) == 21
    assert target_temperature("home", True, 21) == 21

def test_midday_occupied_is_20():
    assert target_temperature("home", True, 10) == 20

def test_late_night_occupied_is_20():
    assert target_temperature("home", True, 23) == 20

# hvac_action

def test_idle_when_difference_under_one():
    assert hvac_action(20, 20.5, 10) == "idle"
    assert hvac_action(20, 19.5, 10) == "idle"

def test_heat_when_outside_is_mild():
    assert hvac_action(18, 22, 5) == "heat"
    assert hvac_action(18, 22, 10) == "heat"

def test_heat_boost_when_very_cold_outside():
    assert hvac_action(18, 22, 4) == "heat_boost"

def test_cool_boost_when_very_hot_outside():
    assert hvac_action(26, 20, 31) == "cool_boost"

def test_cool_when_hot_outside_is_not_extreme():
    assert hvac_action(26, 20, 30) == "cool"
    assert hvac_action(26, 20, 15) == "cool"

# energy_alert

def test_energy_alert_warning_when_minority_over_limit():
    assert energy_alert([5, 12, 6, 7], 10) == "warning"

def test_energy_alert_critical_when_majority_over_limit():
    assert energy_alert([12, 13, 5], 10) == "critical"

def test_energy_alert_warning_when_exactly_half_over():
    # over * 2 == len is not > len, so exactly half over is a warning
    assert energy_alert([12, 5], 10) == "warning"

def test_energy_alert_ok_when_none_over_limit():
    assert energy_alert([1, 2, 3], 10) == "ok"
