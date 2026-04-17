from __future__ import annotations

from typing import Any, Mapping


class ComputeFormServices:
    """Translate the custom compute form payload into service kwargs."""

    BAND_GROUP_MAP = {
        "MF/HF (1.8 MHz - 54.0 MHz)": "0",
        "VHF/UHF": "1",
        "MF/HF": "0",
        "VHF/UHF (50.0 MHz - 1,300 MHz)": "1",
    }

    FREQUENCY_POSITION_MAP = {
        "Lowest Frequency in Band": "0",
        "Center Frequency in Band": "1",
        "Highest Frequency in Band": "2",
    }

    DUTY_FACTOR_MAP = {
        "SSB (Conversational, No Speech Processing)  [20%]": ".2",
        "SSB (Conversational, No Speech Processing)  [50%]": ".5",
        "CW (Conversational)  [40%]": ".4",
        "FM  [100%]": "1",
        "AM  [100%]": "1",
        "AFSK (e.g., RTTY, etc.)  [100%]": "1",
        "FT4  [100%]": "1",
        "FT8  [100%]": "1",
        "Carrier for Tuning  [100%]": "1",
        "Unknown Mode (Assume Worst Case)  [100%]": "1",
    }

    TRANSMIT_RECEIVE_TIME = {
        "0.125": ".125",
        "0.25": ".25",
        "1.0": "1",
        "2.0": "2",
        "3.0": "3",
        "4.0": "4",
        "5.0": "5",
        "6.0": "6",
        "7.0": "7",
        "8.0": "8",
        "9.0": "9",
        "10.0": "10",
        "11.0": "11",
        "12.0": "12",
        "13.0": "13",
        "14.0": "14",
        "15.0": "15",
        "16.0": "16",
        "17.0": "17",
        "18.0": "18",
        "19.0": "19",
        "20.0": "20",
        "21.0": "21",
        "22.0": "22",
        "23.0": "23",
        "24.0": "24",
        "25.0": "25",
        "26.0": "26",
        "27.0": "27",
        "28.0": "28",
        "29.0": "29",
        "30.0": "30",
    }





    def normalize_post_data(self, post_data: Mapping[str, Any]) -> dict[str, Any]:
        """Convert raw HTML field names into the kwargs used by the report service."""

        normalized = {
            "report_description": self._clean_text(post_data.get("report_description")),
            "operator_name": self._clean_text(post_data.get("name")),
            "call_sign": self._clean_text(post_data.get("call_sign")),
            "email": self._clean_text(post_data.get("email")),
            "antenna_description": self._clean_text(post_data.get("antenna_description")),
            "antenna_gain": self._to_float(post_data.get("antenna_gain")),
            "ground_reflection": self._to_bool(post_data.get("ground_reflection")),
            "effective_power": self._to_float(post_data.get("transmitter_power")),
            "duty_factor": self._parse_choice(post_data.get("duty_factor"), self.DUTY_FACTOR_MAP),
            "transmit_time": self._to_float(post_data.get("tx_time")),
            "receive_time": self._to_float(post_data.get("rx_time")),
            "frequency_mode": self._parse_choice(post_data.get("band_group"), self.BAND_GROUP_MAP),
            "frequency_position": self._parse_choice(post_data.get("freq_pos"), self.FREQUENCY_POSITION_MAP),
            "frequency": self._to_optional_float(post_data.get("single_freq")),
            "include_calculations": self._to_bool(post_data.get("include_calculations")),
        }

        return normalized

    @staticmethod
    def _clean_text(value: Any) -> str:
        if value is None:
            return ""
        return str(value).strip()

    @staticmethod
    def _to_float(value: Any) -> float | None:
        if value in (None, ""):
            return None
        return float(value)

    @staticmethod
    def _to_optional_float(value: Any) -> float | None:
        if value in (None, ""):
            return None
        return float(value)

    @staticmethod
    def _to_bool(value: Any) -> bool:
        if isinstance(value, bool):
            return value
        if value is None:
            return False
        return str(value).strip().lower() not in {"", "0", "false", "off", "none"}

    @staticmethod
    def _parse_choice(value: Any, mapping: Mapping[str, Any]) -> Any:
        if value in (None, ""):
            return None
        if value in mapping:
            return mapping[value]

        text_value = str(value).strip()
        if text_value in mapping:
            return mapping[text_value]

        try:
            return int(text_value)
        except (TypeError, ValueError):
            try:
                return float(text_value)
            except (TypeError, ValueError):
                return value
