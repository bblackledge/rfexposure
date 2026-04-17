import unittest
from ..views.computations import Exposure


class TestMaximumPowerDensity(unittest.TestCase):
    def test_low_frequency_range(self):
        """Test frequencies below 1.34 MHz."""
        self.assertEqual(Exposure._maximum_power_density(1.0), (100.0, 100.0))
        self.assertEqual(Exposure._maximum_power_density(0.5), (100.0, 100.0))

    def test_mid_low_frequency_range(self):
        """Test frequencies between 1.34 MHz and 3 MHz."""
        self.assertEqual(Exposure._maximum_power_density(2.0), (100.0, 180.0 / (2.0 ** 2)))
        self.assertEqual(Exposure._maximum_power_density(2.5), (100.0, 180.0 / (2.5 ** 2)))

    def test_hf_frequency_range(self):
        """Test frequencies between 3 MHz and 30 MHz."""
        self.assertEqual(Exposure._maximum_power_density(7.0), (900.0 / (7.0 ** 2), 180.0 / (7.0 ** 2)))
        self.assertEqual(Exposure._maximum_power_density(14.0), (900.0 / (14.0 ** 2), 180.0 / (14.0 ** 2)))
        self.assertEqual(Exposure._maximum_power_density(28.0), (900.0 / (28.0 ** 2), 180.0 / (28.0 ** 2)))

    def test_vhf_range(self):
        """Test frequencies between 30 MHz and 300 MHz."""
        self.assertEqual(Exposure._maximum_power_density(50.0), (1.0, 0.2))
        self.assertEqual(Exposure._maximum_power_density(144.0), (1.0, 0.2))

    def test_uhf_range(self):
        """Test frequencies between 300 MHz and 1500 MHz."""
        self.assertEqual(Exposure._maximum_power_density(450.0), (450.0 / 300.0, 450.0 / 1500.0))
        self.assertEqual(Exposure._maximum_power_density(900.0), (900.0 / 300.0, 900.0 / 1500.0))

    def test_microwave_range(self):
        """Test frequencies between 1500 MHz and 100000 MHz."""
        self.assertEqual(Exposure._maximum_power_density(2000.0), (5.0, 1.0))
        self.assertEqual(Exposure._maximum_power_density(50000.0), (5.0, 1.0))

    def test_extreme_high_frequencies(self):
        """Test frequencies above 100000 MHz."""
        self.assertEqual(Exposure._maximum_power_density(200000.0), (0.0, 0.0))
        self.assertEqual(Exposure._maximum_power_density(500000.0), (0.0, 0.0))


if __name__ == '__main__':
    unittest.main()
