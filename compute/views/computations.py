import math
from typing import Dict, Any, Tuple

from icecream import ic
from enum import Enum


class ControlMode(Enum):
    CONTROLLED = 1
    UNCONTROLLED = 2


class Exposure:
    """ Amateur Radio HF Exposure Computation """

    def __init__(self, **kwargs):
        self.report_description: str = kwargs.get('report_description', '')
        self.antenna_description: str = kwargs.get('antenna_description', '')
        self.effective_power: float = kwargs.get('effective_power', 0.0)
        self.antenna_gain: float = kwargs.get('antenna_gain', 1.0)
        self.frequency_mode: int = kwargs.get('frequency_mode', 0)
        self.frequency_position: int = kwargs.get('frequency_position', 0)
        self.frequency: float = kwargs.get('frequency', 3.0)
        self.ground_reflection: bool = kwargs.get('ground_reflection'
                                                  , False)
        self.duty_factor: float = float(kwargs.get('duty_factor', 1.0))
        self.transmit_time: float = float(kwargs.get('transmit_time', 1.0))
        self.receive_time: float = float(kwargs.get('receive_time', 1.0))

        # === Computed Ground Reflection Constant ===
        self.ground_reflection_multiplier = 0.64 if self.ground_reflection else 0.25

    def calculate_compliance_distance(self, freq: float, control_mode: ControlMode) -> Tuple[float, float, Dict[str, Any]]:
        """
        Calculate the compliance distance.
        :param freq: operating frequency in MHz
        :param control_mode: 'ControlMode.CONTROLLED' or 'ControlMode.UNCONTROLLED'
        :return: compliance distance in meters
        """

        # 6 min or 30 min per Spec in a Controlled vs. Uncontrolled Environment Respectively
        interval = 6 if control_mode == ControlMode.CONTROLLED else 30

        transmit_mw_power = self.effective_power * 1000
        transmit_time_percentage = self._calculate_transmit_time_ratio(interval)
        power = transmit_mw_power * self.duty_factor * transmit_time_percentage
        antenna_gain_numeric = 10 ** (self.antenna_gain / 10.0)                                 # === G ===
        power_gain_factor = power * antenna_gain_numeric                                        # === P x G ==
        controlled_max_density, uncontrolled_max_density = self._maximum_power_density(freq)

        max_density = controlled_max_density if control_mode == ControlMode.CONTROLLED else uncontrolled_max_density
        min_distance = math.sqrt((self.ground_reflection_multiplier * power_gain_factor) / (max_density * math.pi))
        min_distance_feet = min_distance / 30.48
        min_distance_meter = min_distance_feet * 0.3048

        intermediates = {
            'interval': interval,
            'transmit_time': self.transmit_time,
            'receive_time':  self.receive_time,
            'transmit_milli_watts_power': transmit_mw_power,
            'transmit_time_percentage': transmit_time_percentage,
            'antenna_gain': antenna_gain_numeric,
            'power': power,
            'power_gain_factor': power_gain_factor,
            'controlled_max_density': controlled_max_density,
            'uncontrolled_max_density': uncontrolled_max_density,
            'control_mode': control_mode,
            'ground_reflection_multiplier': self.ground_reflection_multiplier,
            'max_density': max_density,
            'min_distance': min_distance,
            'min_distance_feet': min_distance_feet,
            'min_distance_meter': min_distance_meter
        }

        return max_density, min_distance_feet, intermediates

    def _calculate_transmit_time_ratio(self, interval: float) -> float:
        """
        Transmission Time to Fixed Interval Ratio
        Fixed Interval is either 6 min or 30 min per spec in a controlled vs. uncontrolled environment respectively
        :param interval: minutes of interval (or less)
        :return: transmit_time_ratio
        :example: cycle = 2      remainder = 6 % 2 = 0      tx_complete_cycles = 6/2 = 3.0 * 1 = 3
        """

        cycle = self.transmit_time + self.receive_time  # Cycle = Tx + Rx minutes

        if self.transmit_time >= interval:              # Tx time is longer than interval (6 or 30 min.)
            return 1.0                                  # Return 1.0 (100% Transmit During Interval)
        elif cycle >= interval:                         # Tx + Rx is greater than interval (6 or 30 min.)
            return self.transmit_time / interval        # Return tx % of interval (6 or 30 min.)
        else:
            complete_cycles = math.floor(interval / cycle)
            remainder = interval % cycle                # Remaining Tx Minutes
            tx_time = min(self.transmit_time, remainder)
            return (complete_cycles * self.transmit_time + tx_time) / interval

    @staticmethod
    def _maximum_power_density(freq: float) -> Tuple[float, float]:
        """
        Return the maximum power density for the passed frequency (range).
        This calculation is essentially a table lookup in the following table:
        * Table 1. FCC Limits for Maximum Permissible Exposure (MPE) *
        Page 47 of Supplement B (Edition 97-01) to OET Bulletin 65 (Edition 97-01)

        :param freq: operating frequency in MHz
        :return: Tuple[controlled, uncontrolled] maximum density in mW/cm²
        """

        if freq < 1.34:
            return 100.0, 100.0
        elif freq < 3:
            return 100.0, 180.0 / (freq ** 2)
        elif freq < 30:
            return 900.0 / (freq ** 2), 180.0 / (freq ** 2)
        elif freq < 300.0:
            return 1.0, 0.2
        elif freq < 1500.0:
            return freq / 300.0, freq / 1500.0
        elif freq < 100000.0:
            return 5.0, 1.0
        else:
            return 0.0, 0.0


def compute_report(**kwargs) -> Dict[str, Any]:
    """ Compute Exposure Report """

    e = Exposure(**kwargs)
    frequency_mode = str(e.frequency_mode)
    frequency_position = str(e.frequency_position)

    ic(frequency_mode, frequency_position)

    if frequency_mode == "0":       # MF/HF Mode Selected
        # frequency_list = [2.0, 4.0, 5.3, 7.3, 10.15, 14.074, 18.168, 21.450, 24.990, 29.7, 54]
        band_list = ['160', '80', '60', '40', '30', '20', '17', '15', '12', '10', '6']
        frequency_list = get_frequency_list(band_list, frequency_position)

    else:                           # VHF/UHF Mode Selected
        # frequency_list = [54.0, 148.0, 225.0, 450.0, 928.0, 1300.0]
        band_list = ['50', '2', '1.25', '70cm', '33cm', '23cm']
        frequency_list = get_frequency_list(band_list, frequency_position)

    if e.frequency:                 # Custom Frequency Value Selected
        frequency_list = [e.frequency]
        band_list = [get_amateur_band_description(e.frequency)]

    results_list = []

    for band, frequency in zip(band_list, frequency_list):
        c_results = e.calculate_compliance_distance(frequency, ControlMode.CONTROLLED)
        u_results = e.calculate_compliance_distance(frequency, ControlMode.UNCONTROLLED)

        results_dict = {
            'band': band,
            'frequency': f"{frequency:.3f}",
            'c_max_density': f"{c_results[0]:.3f}",
            'c_min_distance_feet': f"{c_results[1]:.3f}",
            'u_max_density': f"{u_results[0]:.3f}",
            'u_min_distance_feet': f"{u_results[1]:.3f}",
            'c_intermediates': c_results[2],
            'u_intermediates': u_results[2],
        }
        results_list.append(results_dict)

    return {**kwargs, 'results_list': results_list}


def get_amateur_band_description(frequency: float) -> str:
    """
    Return the US Amateur Band Plan a Frequency Resides
    :param frequency: frequency in MHz: float
    :return Band Plan a Frequency Resides: str
    :status Stable
    """

    band_plan = [
        (1.8, 2.0, "160 meters"),
        (3.5, 4.0, "80 meters"),
        (5.3305, 5.4035, "60 meters"),
        (7.0, 7.3, "40 meters"),
        (10.1, 10.15, "30 meters"),
        (14.0, 14.35, "20 meters"),
        (18.068, 18.168, "17 meters"),
        (21.0, 21.45, "15 meters"),
        (24.89, 24.99, "12 meters"),
        (28.0, 29.7, "10 meters"),
        (50.0, 54.0, "6 meters"),
        (144.0, 148.0, "2 meters"),
        (219.0, 220.0, "1.25 meters"),
        (420.0, 450.0, "70 centimeters"),
        (902.0, 928.0, "33 centimeters"),
        (1240.0, 1300.0, "23 centimeters")
    ]

    for (low, high, band) in band_plan:
        if low <= frequency <= high:
            return band
    return "Unknown"


def get_frequency_list(band_list, frequency_position):
    """
    Function to get frequency list based on user frequency selection
    :param band_list [] List Of Bands
    :param frequency_position float Frequency Position (Low, Center, High)
    :return frequency_list [] List of Frequencies
    :Status Stable
    """

    band_frequencies = {
        '160': [1.8, 1.9, 2.0],  # Low, Center, High
        '80': [3.5, 3.75, 4.0],
        '60': [5.3305, 5.4, 5.4035],
        '40': [7.0, 7.15, 7.3],
        '30': [10.1, 10.125, 10.15],
        '20': [14.0, 14.175, 14.35],
        '17': [18.068, 18.1, 18.168],
        '15': [21.0, 21.2, 21.45],
        '12': [24.89, 24.9, 24.99],
        '10': [28.0, 29.0, 29.7],
        '6': [50.0, 52.0, 54.0],
        '50': [50.0, 52.0, 54.0],  # VHF Bands
        '2': [144.0, 146.0, 148.0],
        '1.25': [219.0, 222.0, 225.0],
        '70cm': [420.0, 440.0, 460.0],
        '33cm': [902.0, 928.0, 928.0],
        '23cm': [1240.0, 1300.0, 1300.0]
    }

    frequency_list = []
    for band in band_list:
        if band in band_frequencies:
            if frequency_position == '0':    # Low
                frequency_list.append(band_frequencies[band][0])
            elif frequency_position == '1':  # Center
                frequency_list.append(band_frequencies[band][1])
            elif frequency_position == '2':  # High
                frequency_list.append(band_frequencies[band][2])
            else:
                raise ValueError("Invalid frequency selection")
    return frequency_list
