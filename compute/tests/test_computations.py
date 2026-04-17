from django.test import TestCase
from ..views.computations import Exposure, ControlMode
import math


class ExposureTests(TestCase):

    def setUp(self):
        # Basic setup data for tests
        self.kwargs = {
            'report_description': 'Test Report',
            'antenna_description': 'Test Antenna',
            'effective_power': 100.0,  # watts
            'antenna_gain': 2.0,  # dBi
            'frequency_mode': 0,
            'frequency_position': 1,
            'frequency': 14.0,  # MHz (in 20 meters band)
            'ground_reflection': True,
            'duty_factor': 0.5,  # 50% duty cycle
            'transmit_time': 2.0,  # minutes
            'receive_time': 4.0  # minutes
        }
        self.exposure = Exposure(**self.kwargs)

    def test_calculate_compliance_distance_controlled(self):
        """Test compliance distance calculation for controlled environment"""
        freq = 14.0  # MHz in the 20-meter band
        control_mode = ControlMode.CONTROLLED

        max_density, min_distance_feet, intermediates = self.exposure.calculate_compliance_distance(freq, control_mode)

        # Assert max density and min distance in controlled environment
        self.assertAlmostEqual(max_density, 4.59, places=2)
        self.assertTrue(min_distance_feet > 0)

    def test_calculate_compliance_distance_uncontrolled(self):
        """Test compliance distance calculation for uncontrolled environment"""
        freq = 14.0  # MHz in the 20-meter band
        control_mode = ControlMode.UNCONTROLLED

        max_density, min_distance_feet, intermediates = self.exposure.calculate_compliance_distance(freq, control_mode)

        # Assert max density and min distance in uncontrolled environment
        self.assertAlmostEqual(max_density, 0.918, places=2)
        self.assertTrue(min_distance_feet > 0)

    def test_calculate_compliance_distance_with_low_frequency(self):
        """Test compliance distance for a very low frequency (below 1.34 MHz)"""
        freq = 1.0  # MHz
        control_mode = ControlMode.CONTROLLED

        max_density, min_distance_feet, intermediates = self.exposure.calculate_compliance_distance(freq, control_mode)

        # Assert max density and min distance for low frequency
        self.assertAlmostEqual(max_density, 100.0, places=2)
        self.assertTrue(min_distance_feet > 0)

    def test_calculate_transmit_time_ratio_complete_cycle(self):
        """Test transmit time ratio when cycle is complete"""
        ratio = self.exposure._calculate_transmit_time_ratio(6.0)  # 6 minutes interval (Controlled)
        expected_ratio = (math.floor(6 / (2 + 4)) * 2 + min(2, 6 % (2 + 4))) / 6.0
        self.assertAlmostEqual(ratio, expected_ratio)

    def test_calculate_transmit_time_ratio_longer_tx(self):
        """Test transmit time ratio when transmit time is longer than the interval"""
        self.exposure.transmit_time = 10.0
        ratio = self.exposure._calculate_transmit_time_ratio(6.0)  # 6 minutes interval (Controlled)
        self.assertEqual(ratio, 1.0)  # Should return 1.0 since tx time is longer than interval

    def test_maximum_power_density_for_low_frequency(self):
        """Test maximum power density calculation for a low frequency"""
        freq = 1.0  # MHz
        controlled_density, uncontrolled_density = self.exposure._maximum_power_density(freq)

        # Assert densities for low frequency
        self.assertEqual(controlled_density, 100.0)
        self.assertEqual(uncontrolled_density, 100.0)

    def test_maximum_power_density_for_high_frequency(self):
        """Test maximum power density calculation for a higher frequency"""
        freq = 200.0  # MHz (in VHF range)
        controlled_density, uncontrolled_density = self.exposure._maximum_power_density(freq)

        # Assert densities for higher frequency
        self.assertAlmostEqual(controlled_density, 1.0, places=2)
        self.assertAlmostEqual(uncontrolled_density, 0.2, places=2)

    def test_ground_reflection_multiplier_true(self):
        """Test ground reflection multiplier when reflection is enabled"""
        self.assertEqual(self.exposure.ground_reflection_multiplier, 0.64)

    def test_ground_reflection_multiplier_false(self):
        """Test ground reflection multiplier when reflection is disabled"""
        exposure_no_reflection = Exposure(**{**self.kwargs, 'ground_reflection': False})
        self.assertEqual(exposure_no_reflection.ground_reflection_multiplier, 0.25)
