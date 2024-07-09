import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()

# Create a Canvas widget
canvas = tk.Canvas(root, width=300, height=200)
canvas.pack()

# Load the image
image = Image.open(r"C:\Users\neb\Desktop\TradingSimula_18-2022\log_returns_plot.png")  # Replace "example.png" with your image file
photo = ImageTk.PhotoImage(image)

# Add the image to the Canvas
canvas.create_image(150, 100, image=photo)

root.mainloop()