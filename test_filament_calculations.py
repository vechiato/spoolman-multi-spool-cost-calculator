# test_filament_calculations.py

import math
import unittest

from unittest.mock import patch
from filament_calculations import (
    calculate_cost,
    calculate_mass_per_meter,
    get_spools,
    parse_filament_input,
)

class TestFilamentCalculations(unittest.TestCase):

    def test_calculate_cost(self):
        # Test normal calculation
        cost = calculate_cost(50, 1000, 30)  # 50g used, 1000g spool, $30 cost
        expected_cost = (50 / 1000) * 30
        self.assertAlmostEqual(cost, expected_cost)

        # Test zero spool weight
        with self.assertRaises(ValueError):
            calculate_cost(50, 0, 30)

        # Test negative filament used
        with self.assertRaises(ValueError):
            calculate_cost(-50, 1000, 30)

    def test_calculate_mass_per_meter(self):
        # Test with standard PLA values
        diameter_mm = 1.75
        density = 1.24  # PLA density in g/cm³
        mass_per_meter = calculate_mass_per_meter(diameter_mm, density)
        
        # Expected mass per meter calculated manually
        expected_mass_per_meter = (
            math.pi * ((diameter_mm / 10 / 2) ** 2) * density * 100
        )
        self.assertAlmostEqual(mass_per_meter, expected_mass_per_meter)

        # Test with zero diameter (should use default diameter)
        mass_per_meter_default = calculate_mass_per_meter(0, density)
        expected_mass_per_meter_default = (
            math.pi * ((1.75 / 10 / 2) ** 2) * density * 100
        )
        self.assertAlmostEqual(mass_per_meter_default, expected_mass_per_meter_default)


    def test_parse_filament_input(self):
        # Test grams input
        value, unit = parse_filament_input('100g')
        self.assertEqual(value, 100)
        self.assertEqual(unit, 'g')

        # Test meters input
        value, unit = parse_filament_input('5.5m')
        self.assertEqual(value, 5.5)
        self.assertEqual(unit, 'm')

        # Test default unit (grams)
        value, unit = parse_filament_input('200')
        self.assertEqual(value, 200)
        self.assertEqual(unit, 'g')

        # Test invalid input
        with self.assertRaises(ValueError):
            parse_filament_input('abc')

        with self.assertRaises(ValueError):
            parse_filament_input('100kg')

    @patch('filament_calculations.requests.get')
    def test_get_spools(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'id': 1, 'filament': {'name': 'PLA Red', 'material': 'PLA', 'color_hex': 'ff0000'}, 'price': 16.49, 'initial_weight': 1000, 'remaining_weight': 912.13, 'archived': False},
            {'id': 2, 'filament': {'name': 'PLA White', 'material': 'PLA', 'color_hex': 'ffffff'}, 'price': 10.99, 'initial_weight': 1000, 'remaining_weight': 440.00, 'archived': False}
        ]
        spools = get_spools("http://localhost:7912/api/v1")
        self.assertEqual(len(spools), 2)
        self.assertEqual(spools[0]['filament']['name'], 'PLA Red')

if __name__ == '__main__':
    unittest.main()