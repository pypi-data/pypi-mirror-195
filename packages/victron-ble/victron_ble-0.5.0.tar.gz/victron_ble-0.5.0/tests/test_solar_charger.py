from victron_ble.devices.solar_charger import SolarCharger
from victron_ble.devices.base import OperationMode


class TestSolarChargwer:
    def test_parse_data(self) -> None:
        data = "100242a0016207adceb37b605d7e0ee21b24df5c"
        actual = SolarCharger("adeccb947395801a4dd45a2eaa44bf17").parse(
            bytes.fromhex(data)
        )

        assert actual.get_charge_state() == OperationMode.ABSORPTION
        assert actual.get_battery_voltage() == 13.88
        assert actual.get_battery_charging_current() == 1.4
        assert actual.get_yield_today() == 30
        assert actual.get_solar_power() == 19
        assert actual.get_external_device_load() == 0.0
        assert actual.get_model_name() == "BlueSolar MPPT 75|15"

    def test_bulk_charge(self) -> None:
        data = "100242a0015939a26cc2941a491e766be8457386"
        actual = SolarCharger("a2781bef23aecd48d6b9397350724c67").parse(
            bytes.fromhex(data)
        )
        assert actual.get_charge_state() == OperationMode.BULK

    def test_parse_mppt100(self) -> None:
        data = "100249a0013a399bbb3e36d7237c7687f96e45dc"
        actual = SolarCharger("9b3509d3d7aba706846214ca64500d0c").parse(
            bytes.fromhex(data)
        )
        assert actual.get_battery_charging_current() == 10.1
        assert actual.get_battery_voltage() == 25.55
        assert actual.get_charge_state() == OperationMode.BULK
        assert actual.get_solar_power() == 265
        assert actual.get_yield_today() == 500
        assert actual.get_external_device_load() is None
        assert actual.get_model_name() == "BlueSolar MPPT 100|50 rev2"
