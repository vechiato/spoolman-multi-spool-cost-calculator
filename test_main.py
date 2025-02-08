# test_main.py

import unittest
from unittest.mock import patch
import sys

import main

class TestMainSnapshot(unittest.TestCase):
    @patch('main.save_snapshot')
    @patch('main.get_spools')
    def test_snapshot_flag(self, mock_get_spools, mock_save_snapshot):
        mock_get_spools.return_value = [
            {
                "id": 1,
                "price": 16.49,
                "remaining_weight": 912.13,
                "filament": {
                    "name": "PLA Red",
                    "material": "PLA",
                    "color_hex": "ff0000",
                },
            }
        ]
        # Preserve original argv
        original_argv = sys.argv
        # Mock sys.argv to simulate calling: python main.py --snapshot
        sys.argv = ['main.py', '--snapshot']

        main.main()

        # Restore original argv
        sys.argv = original_argv

        mock_get_spools.assert_called_once()
        mock_save_snapshot.assert_called_once()

class TestMainCompare(unittest.TestCase):
    @patch('main.compare_snapshots')
    def test_compare_snapshots(self, mock_compare_snapshots):
        # Save original argv
        original_argv = sys.argv

        # Mock arguments: python main.py --compare snapshot1.json snapshot2.json
        sys.argv = ['main.py', '--compare', 'snapshot1.json', 'snapshot2.json']
        
        main.main()

        # Restore original argv
        sys.argv = original_argv

        mock_compare_snapshots.assert_called_once_with('snapshot1.json', 'snapshot2.json')

if __name__ == '__main__':
    unittest.main()