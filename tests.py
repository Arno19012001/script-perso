import unittest
import os
import pandas as pd
from io import StringIO
from main import InventoryManager
import sys


class TestInventoryManager(unittest.TestCase):

    def setUp(self):
        """Set up a test instance of InventoryManager."""
        self.manager = InventoryManager()

    def capture_output(self, func, *args, **kwargs):
        """
        Utility method to capture stdout during function execution.

        Args:
            func (callable): The function to execute.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.

        Returns:
            str: Captured output from stdout.
        """
        captured_output = StringIO()
        original_stdout = sys.stdout  # Save the original stdout
        sys.stdout = captured_output  # Redirect stdout
        try:
            func(*args, **kwargs)
        finally:
            sys.stdout = original_stdout  # Restore the original stdout
        return captured_output.getvalue()

    def test_load_valid_files(self):
        """Test loading valid CSV files into the inventory."""
        # Create temporary CSV files for testing
        os.makedirs('test_data', exist_ok=True)
        with open('test_data/file1.csv', 'w') as f:
            f.write("category,quantity,unit_price\nA,10,5.5\nB,20,7.0")
        with open('test_data/file2.csv', 'w') as f:
            f.write("category,quantity,unit_price\nA,15,6.0\nC,5,8.0")

        output = self.capture_output(self.manager.do_load, 'test_data')
        self.assertIn("Loaded: file1.csv", output)
        self.assertIn("All CSV files have been consolidated.", output)
        self.assertEqual(len(self.manager.inventory), 4)

        # Clean up
        os.remove('test_data/file1.csv')
        os.remove('test_data/file2.csv')
        os.rmdir('test_data')

    def test_load_invalid_folder(self):
        """Test loading from an invalid folder path."""
        output = self.capture_output(self.manager.do_load, 'nonexistent_folder')
        self.assertIn("Folder not found.", output)
        self.assertTrue(self.manager.inventory.empty)

    def test_search_existing_value(self):
        """Test searching for an existing value in the inventory."""
        data = """category,quantity,unit_price\nA,10,5.5\nB,20,7.0\n"""
        self.manager.inventory = pd.read_csv(StringIO(data))

        output = self.capture_output(self.manager.do_search, 'category=A')
        self.assertIn("A", output)

    def test_search_nonexistent_value(self):
        """Test searching for a value that does not exist in the inventory."""
        data = """category,quantity,unit_price\nA,10,5.5\nB,20,7.0\n"""
        self.manager.inventory = pd.read_csv(StringIO(data))

        output = self.capture_output(self.manager.do_search, 'category=Z')
        self.assertIn("No results found.", output)

    def test_summary(self):
        """Test generating a summary report."""
        data = """category,quantity,unit_price\nA,10,5.5\nA,15,6.0\nB,20,7.0\n"""
        self.manager.inventory = pd.read_csv(StringIO(data))

        output = self.capture_output(self.manager.do_summary, 'summary_test.csv')
        self.assertIn("Summary report exported to summary_test.csv.", output)
        self.assertTrue(os.path.exists('summary_test.csv'))
        os.remove('summary_test.csv')

    def test_show(self):
        """Test displaying the first rows of the inventory."""
        data = """category,quantity,unit_price\nA,10,5.5\nB,20,7.0\nC,5,8.0\n"""
        self.manager.inventory = pd.read_csv(StringIO(data))

        output = self.capture_output(self.manager.do_show, '2')
        self.assertIn("A", output)
        self.assertIn("B", output)


if __name__ == '__main__':
    unittest.main()





