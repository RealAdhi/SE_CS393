from hypothesis import given, strategies as st
from thermostat_control import parse_setpoint, average_temperature, schedule_slot


@given(st.text() | st.none())
def test_parse_setpoint_no_crash(s):
    try:
        parse_setpoint(s)
    except Exception as e:
        assert False, f"parse_setpoint crashed with: {e!r} on input {s!r}"


@given(st.text() | st.none())
def test_average_temperature_no_crash(s):
    try:
        average_temperature(s)
    except Exception as e:
        assert False, f"average_temperature crashed with: {e!r} on input {s!r}"


@given(st.text() | st.none())
def test_schedule_slot_no_crash(s):
    try:
        schedule_slot(s)
    except Exception as e:
        assert False, f"schedule_slot crashed with: {e!r} on input {s!r}"
