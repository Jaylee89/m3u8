import unittest
import xmlrunner

if __name__ == "__main__":
    xml_test_runner = xmlrunner.XMLTestRunner(output="build/reports")
    xml_test_runner.run(unittest.TestLoader().discover("."))
