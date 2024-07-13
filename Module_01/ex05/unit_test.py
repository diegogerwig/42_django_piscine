import unittest
from subprocess import run, PIPE


class TestAllInScript(unittest.TestCase):
    def run_script(self, args):
        result = run(["python3", "all_in.py"] + args, stdout=PIPE, stderr=PIPE, text=True)
        return result

    def test_01_with_subject_params(self):
        print("\nTesting with subject params 'New jersey, Tren ton, NewJersey, Trenton, toto,    ,      sAlem'")
        result = self.run_script(["New jersey, Tren ton, NewJersey, Trenton, toto,    ,      sAlem"])
        expected_output = "Trenton is the capital of New Jersey\nTren Ton is neither a capital city nor a state\nNewjersey is neither a capital city nor a state\nTrenton is the capital of New Jersey\nToto is neither a capital city nor a state\nSalem is the capital of Oregon"
        self.assertEqual(result.stdout.strip(), expected_output)

    def test_02_with_invalid_city(self):
        print("\nTesting with invalid city 'denver'")
        result = self.run_script(["denver"])
        expected_output = "Denver is the capital of Colorado"
        self.assertEqual(result.stdout.strip(), expected_output)

    def test_03_with_unknown_city(self):
        print("\nTesting with unknown city 'Bilbao'")
        result = self.run_script(["Bilbao"])
        expected_output = "Bilbao is neither a capital city nor a state"
        self.assertEqual(result.stdout.strip(), expected_output)

    def test_04_with_empty_string(self):
        print("\nTesting with empty string")
        result = self.run_script([""])
        expected_output = ""
        self.assertEqual(result.stdout.strip(), expected_output)

    def test_05_without_any_arguments(self):
        print("\nTesting without any arguments")
        result = self.run_script([])
        expected_output = ""
        self.assertEqual(result.stdout.strip(), expected_output)

    def test_06_multiple_arguments(self):
        print("\nTesting multiple arguments: 'Salem', 'salem'")
        result = self.run_script(["Salem", "salem"])
        expected_output = ""
        self.assertEqual(result.stdout.strip(), expected_output)


if __name__ == "__main__":
    unittest.main()
