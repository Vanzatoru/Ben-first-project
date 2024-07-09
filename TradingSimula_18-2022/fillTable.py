import tkinter as tk


def filltable(file, tree, tree2):
    first_line, last_line, second_last_line = get_lines_as_arrays(file)
    # print(second_last_line)
    # print(last_line)
    date=f"{last_line[0][:4]}/{last_line[0][4:6]}/{last_line[0][6:]}"
    for i, item in enumerate(last_line[:-2]):
# forcing a change from 0 to 1 to show that the table 2 works
        # if last_line[i + 1] == '0':
        # last_line[i+1] = '7'

        if last_line[i+1] == '1':
            tree.insert("", tk.END, text=i, values=(first_line[i+1], 1, date), iid=i)

        if second_last_line[i+1] == '0' and last_line[i+1] != '0':
            tree2.insert("", tk.END, text=i, values=(first_line[i+1], last_line[i+1]))


def get_lines_as_arrays(file):
    try:
        with open(file, 'r') as file_handle:
            lines = file_handle.readlines()
            if not lines:
                return [], [], []  # Return empty arrays if the file is empty

            first_line = lines[0].strip().split(',')
            last_line = lines[-1].strip().split(',')
            second_last_line = lines[-2].strip().split(',')

            return first_line, second_last_line, last_line
    except FileNotFoundError:
        print(f"The file {file} was not found.")
        return [], [], []
