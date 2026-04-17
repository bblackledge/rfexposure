import unittest
from ..views.computations import get_frequency_list

class TestGetFrequencyList(unittest.TestCase):
    def test_valid_low_frequency_selection(self):
        """Test valid frequency bands with 'Low' selection (position '0')."""
        self.assertEqual(get_frequency_list(['160'], '0'), [1.8])
        self.assertEqual(get_frequency_list(['80'], '0'), [3.5])
        self.assertEqual(get_frequency_list(['60'], '0'), [5.3305])
        self.assertEqual(get_frequency_list(['40'], '0'), [7.0])
        self.assertEqual(get_frequency_list(['20'], '0'), [14.0])

    def test_valid_center_frequency_selection(self):
        """Test valid frequency bands with 'Center' selection (position '1')."""
        self.assertEqual(get_frequency_list(['160'], '1'), [1.9])
        self.assertEqual(get_frequency_list(['80'], '1'), [3.75])
        self.assertEqual(get_frequency_list(['60'], '1'), [5.4])
        self.assertEqual(get_frequency_list(['40'], '1'), [7.15])
        self.assertEqual(get_frequency_list(['20'], '1'), [14.175])

    def test_valid_high_frequency_selection(self):
        """Test valid frequency bands with 'High' selection (position '2')."""
        self.assertEqual(get_frequency_list(['160'], '2'), [2.0])
        self.assertEqual(get_frequency_list(['80'], '2'), [4.0])
        self.assertEqual(get_frequency_list(['60'], '2'), [5.4035])
        self.assertEqual(get_frequency_list(['40'], '2'), [7.3])
        self.assertEqual(get_frequency_list(['20'], '2'), [14.35])

    def test_multiple_band_selections(self):
        """Test multiple band selections at different positions."""
        self.assertEqual(get_frequency_list(['160', '40', '20'], '0'), [1.8, 7.0, 14.0])
        self.assertEqual(get_frequency_list(['80', '60', '15'], '1'), [3.75, 5.4, 21.2])
        self.assertEqual(get_frequency_list(['10', '6', '2'], '2'), [29.7, 54.0, 148.0])

    def test_invalid_band_selection(self):
        """Test an invalid band that is not in the frequency mapping."""
        with self.assertRaises(ValueError):
            get_frequency_list(['invalid_band'], '0')

    def test_invalid_frequency_position(self):
        """Test an invalid frequency position input."""
        with self.assertRaises(ValueError):
            get_frequency_list(['160'], '3')
        with self.assertRaises(ValueError):
            get_frequency_list(['40'], '-1')
        with self.assertRaises(ValueError):
            get_frequency_list(['20'], 'invalid')

    def test_empty_band_list(self):
        """Test an empty band list, expecting an empty frequency list in return."""
        self.assertEqual(get_frequency_list([], '0'), [])


if __name__ == '__main__':
    unittest.main()
