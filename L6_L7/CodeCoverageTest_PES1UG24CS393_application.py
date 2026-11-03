import pytest
from thermostat_control import target_temperature, hvac_action, energy_alert

# Line coverage: make sure every statement runs at least once.

def test_away_mode():
    assert target_temperature("away", True, 12) == 16

def test_sleep_night_returns_18():
    assert target_temperature("sleep", True, 23) == 18

def test_sleep_day_returns_20():
    assert target_temperature("sleep", True, 12) == 20

def test_unoccupied_returns_18():
    assert target_temperature("home", False, 12) == 18

def test_morning_occupied_returns_22():
    assert target_temperature("home", True, 7) == 22

def test_evening_occupied_returns_21():
    assert target_temperature("home", True, 18) == 21

def test_midday_occupied_returns_20():
    assert target_temperature("home", True, 12) == 20

def test_hvac_idle():
    assert hvac_action(20, 20.5, 10) == "idle"

def test_hvac_heat_boost():
    assert hvac_action(18, 22, 2) == "heat_boost"

def test_hvac_heat():
    assert hvac_action(18, 22, 10) == "heat"

def test_hvac_cool_boost():
    assert hvac_action(26, 20, 35) == "cool_boost"

def test_hvac_cool():
    assert hvac_action(26, 20, 15) == "cool"

def test_energy_alert_no_readings():
    assert energy_alert([], 10) == "ok"

def test_energy_alert_ok():
    assert energy_alert([1, 2, 3], 10) == "ok"

def test_energy_alert_warning():
    assert energy_alert([5, 12, 6, 7], 10) == "warning"

def test_energy_alert_critical():
    assert energy_alert([12, 13, 5], 10) == "critical"
