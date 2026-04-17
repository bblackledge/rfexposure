import unittest
from ..views.computations import get_amateur_band_description


class TestGetAmateurBandDescription(unittest.TestCase):
    def test_valid_band_frequencies(self):
        """Test valid frequencies that fall within known amateur bands."""
        self.assertEqual(get_amateur_band_description(1.85), "160 meters")
        self.assertEqual(get_amateur_band_description(3.6), "80 meters")
        self.assertEqual(get_amateur_band_description(5.35), "60 meters")
        self.assertEqual(get_amateur_band_description(7.2), "40 meters")
        self.assertEqual(get_amateur_band_description(10.12), "30 meters")
        self.assertEqual(get_amateur_band_description(14.2), "20 meters")
        self.assertEqual(get_amateur_band_description(18.1), "17 meters")
        self.assertEqual(get_amateur_band_description(21.25), "15 meters")
        self.assertEqual(get_amateur_band_description(24.95), "12 meters")
        self.assertEqual(get_amateur_band_description(28.5), "10 meters")
        self.assertEqual(get_amateur_band_description(51.0), "6 meters")
        self.assertEqual(get_amateur_band_description(145.0), "2 meters")
        self.assertEqual(get_amateur_band_description(220.5), "1.25 meters")
        self.assertEqual(get_amateur_band_description(435.0), "70 centimeters")
        self.assertEqual(get_amateur_band_description(915.0), "33 centimeters")
        self.assertEqual(get_amateur_band_description(1260.0), "23 centimeters")

    def test_boundary_band_frequencies(self):
        """Test boundary values at the edge of amateur bands."""
        self.assertEqual(get_amateur_band_description(1.8), "160 meters")
        self.assertEqual(get_amateur_band_description(2.0), "160 meters")
        self.assertEqual(get_amateur_band_description(3.5), "80 meters")
        self.assertEqual(get_amateur_band_description(4.0), "80 meters")
        self.assertEqual(get_amateur_band_description(50.0), "6 meters")
        self.assertEqual(get_amateur_band_description(54.0), "6 meters")
        self.assertEqual(get_amateur_band_description(144.0), "2 meters")
        self.assertEqual(get_amateur_band_description(148.0), "2 meters")

    def test_out_of_band_frequencies(self):
        """Test frequencies that do not belong to any amateur band."""
        self.assertEqual(get_amateur_band_description(1.5), "Unknown")
        self.assertEqual(get_amateur_band_description(4.5), "Unknown")
        self.assertEqual(get_amateur_band_description(30.5), "Unknown")
        self.assertEqual(get_amateur_band_description(200.0), "Unknown")
        self.assertEqual(get_amateur_band_description(500.0), "Unknown")
        self.assertEqual(get_amateur_band_description(1500.0), "Unknown")
        self.assertEqual(get_amateur_band_description(2000.0), "Unknown")

    def test_edge_case_frequencies(self):
        """Test frequencies just outside amateur bands."""
        self.assertEqual(get_amateur_band_description(2.01), "Unknown")
        self.assertEqual(get_amateur_band_description(4.01), "Unknown")
        self.assertEqual(get_amateur_band_description(54.1), "Unknown")
        self.assertEqual(get_amateur_band_description(148.1), "Unknown")
        self.assertEqual(get_amateur_band_description(1300.1), "Unknown")


if __name__ == '__main__':
    unittest.main()
