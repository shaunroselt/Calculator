import ast
import sys
import tkinter as tk
from tkinter import Button

if sys.platform == 'darwin':
    from tkmacosx import Button


class Calculator:
    def __init__(self):
        """Initializing variables for the calculator"""
        self.error_window = None
        self.solution_area = "0"
        self.prev_solution_area = ""
        self.prev_solution_label = None
        self.solution_label = None
        self.squared_formula = ""
        self.create_interface()

    def create_interface(self):
        """Creating a GUI interface for the calculator"""

        # Solution label
        self.solution_label = tk.Label(text=self.solution_area,
                                       bg='#292c32', anchor='se',
                                       width=18, font=("Trebuchet MS", 39),
                                       )
        self.solution_label.place(x=0, y=90)

        # Previous solution label
        self.prev_solution_label = tk.Label(text=self.prev_solution_area,
                                            bg='#292c32', anchor='se',
                                            width=29, font=("Trebuchet MS", 23),
                                            )
        self.prev_solution_label.place(x=0, y=20)

        main_buttons = [
            "CE", "<", ">", "(", ")",
            "1", "2", "3", "%", "X^2",
            "4", "5", "6", "*", "/",
            "7", "8", "9", "+", "-",
            "", "0", ".", "DEL", "="
        ]
        position_mb_x = 5
        position_mb_y = 180

        for btn in main_buttons:
            self.create_button(btn, position_mb_x, position_mb_y)
            position_mb_x += 80
            if position_mb_x > 400:
                position_mb_x = 5
                position_mb_y += 83.5

    def create_button(self, btn_symbol, x, y):
        """Creating calculator buttons"""

        comm = lambda: self.logicalc(btn_symbol)
        Button(text=btn_symbol, bg='#30343a',
               activebackground='#292c32',
               font=("Times New Roman", 18), fg='white',
               activeforeground='white',
               command=comm,
               ).place(x=x, y=y, width=70, height=79)

    def logicalc(self, action):
        """Logic of button actions"""
        overload_words = {"0", "Error", "True", "False"}
        block_ops = {"DEL", "=", "*", "/", ">", "<", "%"}
        formula = self.solution_area

        # Clear the solution area
        if action == "CE":
            formula = ""

        # Checking the area of the formula
        elif formula in overload_words:
            formula = self.check_formula_area(action, formula, block_ops)

        # Write the equation in parentheses
        elif action == "(":
            formula += f"( )"

        # Writing a quadratic equation
        elif action == "X^2":
            formula += f"( )²"

        # Writing a formula inside the equation in parentheses
        elif formula[-1] in [")", "²"] and action not in ["=", "DEL"]:
            formula = self.bracketed_action(formula, action)

        # Delete the last character
        elif action == "DEL":
            # Delete the last character in parentheses
            formula = self.delete_action(formula)

        # Calculating the formula in the area
        elif action == "=":
            formula = self.equals_action(formula)

        # Adding characters to the area
        else:
            if " " in formula:
                formula = formula.replace(" ", action)
            else:
                formula += action

        self.solution_area = formula
        self.update()

    @staticmethod
    def check_formula_area(action, formula, block_ops):
        if action not in block_ops:
            if formula == "0" and action == ".":
                formula += action
            elif action == "(":
                formula = f"( )"
            elif action == "X^2":
                formula = f"( )²"
            else:
                formula = action
        return formula

    def bracketed_action(self, formula, action):
        formula = formula.replace(" ", "")

        # Exit condition for the equation
        if action != ")":
            if formula[-1] == ")":
                formula = formula[:len(formula) - 1] + ''.join(
                    action) + formula[(len(formula) - 1):]
            elif formula[-1] == "²":
                formula = formula[:len(formula) - 2] + ''.join(action) + \
                          formula[(len(formula) - 2):]
                if action == "%":
                    self.squared_formula = "/100"
                else:
                    self.squared_formula += action
        elif formula[-1] == "²":
            self.squared_formula += "|"
            formula += " "
        else:
            formula += " "
        return formula

    def delete_action(self, formula):
        if formula[-1] == ")":
            if not formula[-2] == "(":
                formula = formula[:len(formula) - 2] + ")"
            else:
                formula = formula[:len(formula) - 2]
        elif formula[-1] == "²":
            if formula[-3] != "(":
                formula = formula[:len(formula) - 3] + ")²"
                self.squared_formula = self.squared_formula[0:-1]
            else:
                formula = formula[:len(formula) - 3]
        else:
            formula = formula[0:-1]
        return formula

    def equals_action(self, formula):
        saved_formula = formula
        # Warning of a user error
        try:
            # Calculating a formula with percentages
            if "%" in formula:
                formula = formula.replace("%", "/100")
            # Checking for and calculating a quadratic equation
            if "²" in formula:
                count_squared_parentheses = formula.count("²")
                self.squared_formula = self.squared_formula.split("|")
                for count in range(count_squared_parentheses):
                    solution_squared = str(eval(self.squared_formula[count]) ** 2)
                    formula = formula.replace(f"({self.squared_formula[count]})²", f"{solution_squared}")
                self.squared_formula = ""
            formula = str(eval(formula))
        except (SyntaxError, ZeroDivisionError, NameError, TypeError) as exception:
            error_message = f"{type(exception).__name__}: {exception.args[0]}"
            self.error_warning(error_message)
            formula = "Error"
        self.squared_formula = ""
        # Writing down the whole equation with the answer
        self.prev_solution_label.configure(text=f"{saved_formula} = {formula}")
        return formula

    def error_warning(self, message):
        """Create a new window for an error"""
        self.error_window = tk.Toplevel()
        self.error_window.geometry("390x75+5+55")
        self.error_window.title('Error message')
        self.error_window.config(bg='#292c32')
        tk.Label(self.error_window, text=f'{message}', bg='#FF6666',
                 font='Arial 15 bold', fg='white', height=2, width=40, wraplength=370
                 ).place(relx=0.5, rely=0.5, anchor="center")
        self.error_window.overrideredirect(True)
        self.error_window.after(3000, lambda: self.error_window.destroy())

    def update(self):
        """Updating the solution area during actions"""
        if self.solution_area == "":
            self.solution_area = "0"
        self.solution_label.configure(text=self.solution_area)


if __name__ == "__main__":
    """Creating a window and running the program"""
    win = tk.Tk()
    win_w, win_h = 400, 600
    win.title("Calculator")
    win.geometry(f"{win_w}x{win_h}+0+10")
    win.config(bg='#292c32')
    win.resizable(False, False)
    tk.Label(win, bg='#30343a',
             padx=200, pady=210).place(x=0, y=160)
    app = Calculator()
    win.mainloop()
