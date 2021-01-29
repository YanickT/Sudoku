import tkinter as tk
import logik
import time


class Widget(tk.Tk):

    def __init__(self):
        """
        Initialize a GUI for easier interactions.
        """
        tk.Tk.__init__(self)

        self.inputs = []

        self.title("Sudoku Solutions")
        self.geometry("500x500")

        self.lab01 = tk.Label(self, text="Sudoku", font=("Helvetica", 22))
        self.lab01.place(relx=0.05, rely=0.02, relwidth=0.9)

        self.but01 = tk.Button(self, text="Berechnen", command=self.calc)
        self.but01.place(relx=0.05, rely=0.9, relwidth=0.675)

        self.but02 = tk.Button(self, text="Neu", command=self.clear)
        self.but02.place(relx=0.75, rely=0.9, relwidth=0.2)

        self.ents = []
        for y in range(0, 9):
            row = []
            for x in range(0, 9):
                row.append(tk.Entry(self, justify='center'))
                row[-1].place(relx=0.108 + x * 0.085 + 0.006 * (x // 3),
                              rely=0.1 + y * 0.085 + 0.006 * (y // 3), relwidth=0.08, relheight=0.08)
            self.ents.append(row)

        self.mainloop()

    def calc(self):
        """
        Calculate the result for the sudoku field.
        :return: void
        """
        # extract numbers from GUI
        input_field = [[int(entry.get()) if entry.get().isdigit() else None for entry in row] for row in self.ents]

        t1 = time.time()
        result = logik.run_solver(input_field)
        t2 = time.time()

        print(f"Solved in : {t2 - t1} s")
        self.show(result)

    def show(self, result):
        """
        Display result in the GUI
        :param result: List[List[int]] = sudoku-field
        :return: void
        """
        ent_results = [zip(ents, results) for ents, results in zip(self.ents, result)]
        for row in ent_results:
            for ent, result in row:
                ent.delete(0, tk.END)
                ent.insert(tk.END, str(result))

    def clear(self):
        """
        Delete all number in the GUI.
        :return: void
        """
        for row in self.ents:
            for ent in row:
                ent.delete(0, tk.END)


if __name__ == "__main__":
    Widget()
