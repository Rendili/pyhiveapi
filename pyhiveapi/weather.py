"""Weather.py"""
from .data import Data as Dt


class Weather:
        """Hive Weather."""
        @staticmethod
        def temperature():
            """Get Hive Weather temperature."""
            return Dt.w_temperature_value
