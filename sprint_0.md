Sprint 0 (due Sep 18)
	1. Key Decisions of the Solitaire Project
		1. Object-oriented programming language
			1. Python
		2. GUI Library
			1. Tkinter
		3. IDE
			1. Visual Studio Code
		4. xUnit Framework
			1. PyUnit
		5. Programming Style Guide
			1. Google Python Style Guide
		6. Project Housing Site
			1. github.com
		7. Other
			1. ---

	2. Unit Testing
		1. Find a tutorial of the unit test framework you have chosen and write at least two xUnit tests of a program you have written or found elsewhere. Attach a screenshot of the program execution and the source code of the program.
            1. Source Code: https://realpython.com/python-unittest/#organizing-your-tests-with-the-testcase-class
            2. '''
            import unittest

class TestAbsFunction(unittest.TestCase):

    def test_positive_number(self):
        self.assertEqual(abs(10), 10)

    def test_negative_number(self):
        self.assertEqual(abs(-10), 10)

    def test_zero(self):
        self.assertEqual(abs(0), 0)

def categorize_by_age(age):
    if 0 <= age <= 9:
        return "Child"
    elif 9 < age <= 18:
        return "Adolescent"
    elif 18 < age <= 65:
        return "Adult"
    elif 65 < age <= 150:
        return "Golden age"
    else:
        return f"Invalid age: {age}"

class TestCategorizeByAge(unittest.TestCase):
    def test_child(self):
        self.assertEqual(categorize_by_age(5), "Child")

    def test_adolescent(self):
        self.assertEqual(categorize_by_age(15), "Adolescent")

    def test_adult(self):
        self.assertEqual(categorize_by_age(30), "Adult")

    def test_golden_age(self):
        self.assertEqual(categorize_by_age(70), "Golden age")

    def test_negative_age(self):
        self.assertEqual(categorize_by_age(-1), "Invalid age: -1")

    def test_too_old(self):
        self.assertEqual(categorize_by_age(151), "Invalid age: 151")

if __name__ == '__main__':
    unittest.main(verbosity=2)
    '''

	3. GUI Programming
		1. Write a GUI program in the language for the Solitaire project.
			1. Must include text, lines, a check box and radio buttons.