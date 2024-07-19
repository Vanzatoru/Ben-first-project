import tkinter as tk


def filltable(file, tree, tree2):
    clear_treeview(tree)
    clear_treeview(tree2)
    first_line, second_last_line, last_line = get_lines_as_arrays(file)
    print(second_last_line)
    print(last_line)
    #date=f"{last_line[0][:4]}/{last_line[0][4:6]}/{last_line[0][6:]}"
    for i, item in enumerate(last_line[:-2]):
# forcing a change from 0 to 1 to show that the table 2 works
        # if last_line[i + 1] == '0':
        # last_line[i+1] = '7'

        if last_line[i+1] == '1':
            date_raw = get_data_when_bought(file,i+1)
            date = f"{date_raw[:4]}/{date_raw[4:6]}/{date_raw[6:]}"
            old_price_line = search_for_old_price(first_line[i+1]+".csv", date_raw)
            last_price_line = get_last_line_with_price(first_line[i+1]+".csv")
            old_price = float(old_price_line[-1])
            last_price = float(last_price_line[-1])
            pnl = last_price - old_price
            tree.insert("", tk.END, text=i, values=(first_line[i+1], 1, date, last_price, old_price, pnl), iid=i)

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


def search_for_old_price(file_path, data):


    try:
        with open(file_path, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                line_data = line[:8]
                if line_data == data:
                    split_line = [part.strip() for part in line.strip().split(',')]
                    return split_line
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")




def get_last_line_with_price(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip()
                split_line = [part.strip() for part in last_line.split(',')]
                return split_line
            else:
                print("The file is empty.")
                return None
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
        return None


def get_data_when_bought(file_path, index):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        num_lines = len(lines)

        for i in range(num_lines - 1, 0, -1):
            current_line = lines[i]
            current_line_split = [part.strip() for part in current_line.split(',')]
            next_line = lines[i-1]
            next_line_split = [part.strip() for part in next_line.split(',')]

            if current_line_split[index] == '1' and next_line_split[index] == '0':
                return current_line_split[0]

        return None


def clear_treeview(tree):
    for row in tree.get_children():
        tree.delete(row)