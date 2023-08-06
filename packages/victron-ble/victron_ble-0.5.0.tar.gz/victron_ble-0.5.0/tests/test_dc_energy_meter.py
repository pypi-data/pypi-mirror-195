from victron_ble.devices.battery_monitor import AuxMode
from victron_ble.devices.dc_energy_meter import DcEnergyMeter, MeterType


class TestDcEnergyMeter:
    def test_parse_data(self) -> None:
        data = "100289a30d787fafde83ccec982199fd815286"
        actual = DcEnergyMeter("aff4d0995b7d1e176c0c33ecb9e70dcd").parse(
            bytes.fromhex(data)
        )

        assert actual.get_meter_type() == MeterType.FUEL_CELL
        assert actual.get_aux_mode() == AuxMode.STARTER_VOLTAGE
        assert actual.get_current() == 0.0
        assert actual.get_voltage() == 12.52
        assert actual.get_starter_voltage() == -0.01

        assert actual.get_alarm() == None

        assert actual.get_temperature() == None
        assert actual.get_model_name() == "SmartShunt 500A/50mV"

    def test_aux_starter(self) -> None:
        data = "100289a30d787fafde83ccec982199fd815286"
        actual = DcEnergyMeter("aff4d0995b7d1e176c0c33ecb9e70dcd").parse(
            bytes.fromhex(data)
        )
        assert actual.get_starter_voltage() == -0.01

    def test_aux_temperature(self) -> None:
        data = "108289a30df07faf9629bfb8c0153f431362c4"
        actual = DcEnergyMeter("aff4d0995b7d1e176c0c33ecb9e70dcd").parse(
            bytes.fromhex(data)
        )
        assert actual.get_temperature() == 382.2
