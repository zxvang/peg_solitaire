# Sprint 0

**Due:** September 18

## 1. Key Decisions of the Solitaire Project

1. **Object-oriented programming language:** Python
2. **GUI library:** Tkinter
3. **IDE:** Visual Studio Code
4. **xUnit framework:** PyUnit
5. **Programming style guide:** Google Python Style Guide
6. **Project hosting site:** GitHub
7. **Other:** None

## 2. Unit Testing

Find a tutorial for the selected unit test framework and write at least two xUnit tests for a program you have written or found elsewhere. Attach a screenshot of the program execution and the program source code.

Source code and tutorial: [Real Python: Organizing Your Tests with the TestCase Class](https://realpython.com/python-unittest/#organizing-your-tests-with-the-testcase-class)

```python
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
```

## 3. GUI Programming

Write a GUI program in the language selected for the Solitaire project. The program must include text, lines, a check box, and radio buttons.

```python
import tkinter as tk
from tkinter import messagebox


def show_message(title, message):
    messagebox.showinfo(title, message)


def main():
    root = tk.Tk()
    root.title("Peg Solitaire Game")

    label = tk.Label(root, text="Welcome to Peg Solitaire Game")
    label.pack(pady=50)

    line1 = tk.Label(root, text="------------------------------")
    line1.pack()

    button = tk.Button(
        root,
        text="Click Here to Start the Game",
        command=lambda: show_message(
            "Game Start", "Starting the Peg Solitaire Game..."
        ),
    )
    button.pack(pady=15)

    checkbox_var = tk.BooleanVar()
    checkbox = tk.Checkbutton(
        root, text="I am ready to play", variable=checkbox_var
    )
    checkbox.pack(pady=5)

    radio_var = tk.StringVar(value="Language")
    radio1 = tk.Radiobutton(
        root, text="English", variable=radio_var, value="English"
    )
    radio1.pack(pady=5)
    radio2 = tk.Radiobutton(
        root, text="Spanish", variable=radio_var, value="Spanish"
    )
    radio2.pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()