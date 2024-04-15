import tkinter as tk

def calculate():
    try:
        result = eval(entry.get())  # Evaluate the expression entered in the entry widget
        result_label.config(text="Result: " + str(result))  # Update the label with the result
    except Exception as e:
        result_label.config(text="Error: " + str(e))  # Display error message if evaluation fails

# Create the main tkinter window
window = tk.Tk()
window.title("Simple Calculator")
window.geometry("300x400")  # Set window size

# Create an entry widget for user input
entry = tk.Entry(window, width=30, borderwidth=5, font=("Arial", 14))
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Create buttons for digits and operators
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3)
]

# Function to add a digit or operator to the entry widget
def add_to_entry(symbol):
    current_text = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current_text + symbol)

# Loop to create buttons
for (text, row, col) in buttons:
    button = tk.Button(window, text=text, padx=20, pady=20, font=("Arial", 12),
                        command=lambda t=text: add_to_entry(t))
    button.grid(row=row, column=col, padx=5, pady=5)

# Create a label to display the result
result_label = tk.Label(window, text="", padx=10, font=("Arial", 14))
result_label.grid(row=5, column=0, columnspan=4)

# Create a button to calculate the result
calc_button = tk.Button(window, text="Calculate", padx=20, pady=10, font=("Arial", 12),
                        command=calculate)
calc_button.grid(row=6, column=0, columnspan=4, pady=10)

# Run the Tkinter event loop
window.mainloop()
