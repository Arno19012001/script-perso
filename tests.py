import unittest
import os
import pandas as pd
from io import StringIO
from main import InventoryManager


class TestInventoryManager(unittest.TestCase):

    def setUp(self):
        """Set up a test instance of InventoryManager."""
        self.manager = InventoryManager()

    def test_load_valid_files(self):
        """Test loading valid CSV files into the inventory."""
        # Create temporary CSV files for testing
        os.makedirs('test_data', exist_ok=True)
        with open('test_data/file1.csv', 'w') as f:
            f.write("category,quantity,unit_price\nA,10,5.5\nB,20,7.0")
        with open('test_data/file2.csv', 'w') as f:
            f.write("category,quantity,unit_price\nA,15,6.0\nC,5,8.0")

        self.manager.do_load('test_data')
        self.assertEqual(len(self.manager.inventory), 4)
        self.assertIn('category', self.manager.inventory.columns)

        # Clean up
        os.remove('test_data/file1.csv')
        os.remove('test_data/file2.csv')
        os.rmdir('test_data')

    def test_load_invalid_folder(self):
        """Test loading from an invalid folder path."""
        self.manager.do_load('nonexistent_folder')
        self.assertTrue(self.manager.inventory.empty)

    def test_search_existing_value(self):
        """Test searching for an existing value in the inventory."""
        data = """category,quantity,unit_price\nA,10,5.5\nB,20,7.0\n"""
        self.manager.inventory = pd.read_csv(StringIO(data))

        with self.assertLogs(level='INFO') as log:
            self.manager.do_search('category=A')
        self.assertTrue(any("A" in message for message in log.output))

    def test_search_nonexistent_value(self):
        """Test searching for a value that does not exist in the inventory."""
        data = """category,quantity,unit_price\nA,10,5.5\nB,20,7.0\n"""
        self.manager.inventory = pd.read_csv(StringIO(data))

        with self.assertLogs(level='INFO') as log:
            self.manager.do_search('category=Z')
        self.assertTrue(any("No results found" in message for message in log.output))

    def test_summary(self):
        """Test generating a summary report."""
        data = """category,quantity,unit_price\nA,10,5.5\nA,15,6.0\nB,20,7.0\n"""
        self.manager.inventory = pd.read_csv(StringIO(data))

        self.manager.do_summary('summary_test.csv')
        self.assertTrue(os.path.exists('summary_test.csv'))
        os.remove('summary_test.csv')

    def test_show(self):
        """Test displaying the first rows of the inventory."""
        data = """category,quantity,unit_price\nA,10,5.5\nB,20,7.0\nC,5,8.0\n"""
        self.manager.inventory = pd.read_csv(StringIO(data))

        with self.assertLogs(level='INFO') as log:
            self.manager.do_show('2')
        self.assertTrue(any("A" in message for message in log.output))
        self.assertTrue(any("B" in message for message in log.output))


if __name__ == '__main__':
    unittest.main()



