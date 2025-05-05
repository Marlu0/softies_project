import unittest
from file_reader import read_file  # Adjust import to your actual module

class TestFileReading(unittest.TestCase):

    def test_read_txt(self):
        content = read_file("test_files/example.txt")
        self.assertIn("This is a test file.", content)

    def test_read_py(self):
        content = read_file("test_files/example.py")
        self.assertIn("def greet():", content)

    def test_read_csv(self):
        content = read_file("test_files/example.csv")
        self.assertEqual(content[0], ['name', 'age'])

    def test_read_c(self):
        content = read_file("test_files/example.c")
        self.assertIn("printf", content)

    def test_read_java(self):
        content = read_file("test_files/example.java")
        self.assertIn("public class HelloWorld", content)

    def test_unsupported_file(self):
        with self.assertRaises(ValueError):
            read_file("test_files/example.pdf")

if __name__ == '__main__':
    unittest.main()
