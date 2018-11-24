"""Hive Weather Module."""
from .hive_data import Data


class Weather:
        """Hive Weather Code."""
        @staticmethod
        def temperature():
            """Get Hive Weather temperature."""
            return Data.w_temperature_value
