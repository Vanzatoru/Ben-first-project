#library versions
#matplotlib         3.8.3
#numpy              1.26.4
#openpyxl           3.1.2
#pandas             2.2.1
#pillow             10.2.0
#pip                24.0
#QuantStats         0.0.62
#scipy              1.13.0
#seaborn            0.13.2
#ttkbootstrap       1.10.1




import tkinter as tk
from tkinter import ttk
from subprocess import call
from reporting import *
from PIL import Image, ImageTk
import pandas as pd

# Here are fucntions for GUIs (all functions are at the top)

# MAIN WINDOW
root = tk.Tk()
root.geometry("1415x800+140+100")
root.iconbitmap(r"C:\Users\neb\Desktop\TradingSimula_18-2022\Portfolio Project\Assets\chart_line.ico")


# Strategy List
stratlist = tk.Listbox(root, width=50, font="Bold 13", height=10, relief="groove")
stratlist.place(anchor="nw", x=10, y=10)

stratlist.insert(2, " TF-Covel")
stratlist.insert(3, " TF-Keltner")
stratlist.insert(4, " TF-LinReg")
stratlist.insert(5, " TF-SwingBO")
stratlist.insert(6, " TF-System #1")
stratlist.insert(7, " TF-System #2")
stratlist.insert(8, " TF-System #3")
stratlist.insert(9, " TF-System #4")
stratlist.insert(10, " TF-System #5")
stratlist.insert(11, " TF-System #6")
stratlist.insert(12, " TF-System #7")
stratlist.insert(13, " TF-TMA")

stratlist.insert(15, " TF-TurtleSystem2")
stratlist.insert(16, " TF-ADX-Individ")
stratlist.insert(17, " TF-Bollinger")
stratlist.insert(18, " TF-BollingerATRNorm")
stratlist.insert(19, " TF-BollingerDonch")


stratlist.insert(22, " TF-BollingerNOTNorm")
stratlist.insert(23, " TF-BollingerOmni1")
stratlist.insert(24, " TF-BollingerOmni2")
stratlist.insert(25, " TF-BollingerOmni4")
stratlist.insert(26, " TF-BollingerOnClose")
stratlist.insert(27, " TF-BollingerOnOpen")
stratlist.insert(28, " TF-BollingerORBO")
stratlist.insert(29, " TF-BollingerParadigm")
stratlist.insert(30, " TF-BollingerPB")
stratlist.insert(32, " TF-BollingerRiskFilter1")
stratlist.insert(33, " TF-BollingerRiskFilter2")
stratlist.insert(34, " TF-BollingerTM")




# UI Lines, Images, and Titles (as labels)
line1 = tk.Label(root, text="——————————Data——————————",  font="7")
line1.place(anchor="nw", x=10, y=230)

line2 = tk.Label(root, text="—————————————————————————————————————")
line2.place(anchor="nw", x=10, y=775)

line3 = tk.Label(root, text="Current Positions", font='Calibri 13')
line3.place(anchor="nw", x=665, y=15)

line4 = tk.Label(root, text="Trades to be made", font='Calibri 13')
line4.place(anchor="nw", x=1100, y=15)

img1 = tk.Label(root, text="◉", font="Calibri 21",fg="#7ac722")
img1.place(anchor="nw", x=1385, y=765)

txt1 = tk.Label(root, text="Connected", font="Calibri 10")
txt1.place(anchor="nw", x=1320, y=776)





# File Path (this is what is used to frick about with data)
file_path = "MainFile.por"


# Checkboxes, List, and other processes
def checkfun():
    with open(file_path, "w") as f:
        newlistofx = []
        listofx = [x.get(),x2.get(),x3.get(),x4.get(),x5.get(),x6.get(),x7.get(),x8.get(),x9.get(),x10.get(),x11.get(),x12.get(),x13.get(),x14.get(),x15.get(),x16.get(),x17.get(),x18.get(),x19.get(),x20.get(),x21.get()]
        for i in listofx:
            if i != "":
                newlistofx.append(i)
        f.write(str(newlistofx).replace('[','').replace(']','').replace(',','').replace("'",'').replace(' ', '\n'))
    # Notice how the function below gets used here
    selecstrat()

    # Making new window and congfiguring it
    plotwin = tk.Toplevel(master=root, )
    plotwin.iconbitmap(r"C:\Users\neb\Desktop\TradingSimula_18-2022\Portfolio Project\Assets\chart_line.ico")
    plotwin.lift(root)
    plotwin.geometry('1000x800+140+100')
    plotwin.resizable(False, True)

    # Making canvas object and configuring it
    plotcanvas = tk.Canvas(plotwin, bg="red", width=1000, height=800, scrollregion=(0,0,2000,3950))
    plotcanvas.pack(expand=True, fill="both")

    #plotting QS report
    plotx = tk.PhotoImage(file= "out.png")
    plotcanvas.create_image(500,1980,image=plotx)

    # Mouswheel Scroll Stuff
    plotcanvas.bind('<MouseWheel>', lambda event: plotcanvas.yview_scroll(int(-event.delta / 60), "units"))

    #scrollbar stuff & Further plotting
    scrollbar = ttk.Scrollbar(plotwin, orient="vertical", command=plotcanvas.yview)
    plotcanvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.place(relx=1, rely=0, relheight=1, anchor="ne")

    plotwin.mainloop()
    #global treefile
    #treefile = 'TF-LinReg_1R-PosMatrix.txt'
    #t1()

# Function that controls what strategy gets ran
def selecstrat():
    if stratlist.get(stratlist.curselection()) == " TF-Covel":
        call(["python", "TF-Covel_1R.py"])
        qsreport('TF-Covel_1R-PosMatrix.txt')
        treefile = "TF-Covel_1R-PosMatrix.txt"

    if stratlist.get(stratlist.curselection()) == " TF-Keltner":
        call(["python", "TF-Keltner_1R.py"])
        qsreport('TF-Keltner_1R-PosMatrix.txt')
        treefile = "TF-Keltner_1R-PosMatrix.txt"

    if stratlist.get(stratlist.curselection()) == " TF-LinReg":
        call(["python", "TF-LinReg_1R.py"])
        qsreport('TF-LinReg_1R-PosMatrix.txt')
        treefile = "TF-LinReg_1R-PosMatrix.txt"

    if stratlist.get(stratlist.curselection()) == " TF-SwingBO":
        call(["python", "TF-SwingBO_1R.py"])
        qsreport('TF-SwingBO_1R-PosMatrix.txt')
        treefile = "TF-SwingBO_1R-PosMatrix.txt"

    if stratlist.get(stratlist.curselection()) == " TF-System #1":
        call(["python", "TF-System#1_1R.py"])
        qsreport('TF-System#1_1R-PosMatrix.txt')
        treefile = "TF-System#1_1R-PosMatrix.txt"

    if stratlist.get(stratlist.curselection()) == " TF-System #2":
        call(["python", "TF-System#2_1R.py"])
        qsreport('TF-System#2_1R-PosMatrix.txt')
        treefile = "TF-System#2_1R-PosMatrix.txt"

    if stratlist.get(stratlist.curselection()) == " TF-System #3":
        call(["python", "TF-System#3_1R.py"])
        qsreport('TF-System#3_1R-PosMatrix.txt')
        treefile = "TF-System#3_1R-PosMatrix.txt"

    if stratlist.get(stratlist.curselection()) == " TF-System #4":
        call(["python", "TF-System#4_1R.py"])
        qsreport('TF-System#4_1R-PosMatrix.txt')
        treefile = "TF-System#4_1R-PosMatrix.txt"

    if stratlist.get(stratlist.curselection()) == " TF-System #5":
        call(["python", "TF-System#5_1R.py"])
        qsreport('TF-System#5_1R-PosMatrix.txt')
        treefile = "TF-System#5_1R-PosMatrix.txt"

    if stratlist.get(stratlist.curselection()) == " TF-System #6":
        call(["python", "TF-System#6_1R.py"])
        qsreport('TF-System#6_1R-PosMatrix.txt')
        treefile = "TF-System#6_1R-PosMatrix.txt"

    if stratlist.get(stratlist.curselection()) == " TF-System #7":
        call(["python", "TF-System#7_1R.py"])
        qsreport('TF-System#7-PosMatrix.txt')
        treefile = "TF-System#7-PosMatrix.txt"

    if stratlist.get(stratlist.curselection()) == " TF-TMA":
        call(["python", "TF-TMA_1R.py"])
        qsreport('TF-TMA_1R-PosMatrix.txt')
        treefile = "TF-TMA_1R-PosMatrix.txt"


    if stratlist.get(stratlist.curselection()) == " TF-TurtleSystem2":
        call(["python", "PythonTurtleSystem_1R_ver2.py"])
        qsreport('PythonTurt_1R_ver2-PosMatrix.txt')
 

    if stratlist.get(stratlist.curselection()) == " TF-ADX-Individ":
        call(["python", "TF-ADX-Individ_1R.py"])
        qsreport('TF-ADX-INDIV_1R-PosMatrix.txt')


    if stratlist.get(stratlist.curselection()) == " TF-Bollinger":
        call(["python", "TF-Bollinger_1R.py"])
        qsreport('TF-Bollinger_1R-PosMatrix.txt')


    if stratlist.get(stratlist.curselection()) == " TF-BollingerATRNorm":
        call(["python", "TF-BollingerATRNorm_1R.py"])
        qsreport('TF-Boll-ATRNORM_1R-PosMatrix.txt')


    if stratlist.get(stratlist.curselection()) == " TF-BollingerDonch":
        call(["python", "TF-BollingerDonch_1R.py"])
        qsreport('TF-Boll.Donch_1R-PosMatrix.txt')


    if stratlist.get(stratlist.curselection()) == " TF-BollingerNOTNorm":
        call(["python", "TF-BollingerNOTNorm_1R.py"])
        qsreport('TF-Boll-Notional-PosMatrix.txt')


    if stratlist.get(stratlist.curselection()) == " TF-BollingerOmni1":
        call(["python", "TF-BollingerOmni_1R.py"])
        qsreport('TF-Boll-Omni_1R-PosMatrix.txt')


    if stratlist.get(stratlist.curselection()) == " TF-BollingerOmni2":
        call(["python", "TF-BollingerOmni2_1R.py"])
        qsreport('TF-Boll-Omni2_1R-PosMatrix.txt')


    if stratlist.get(stratlist.curselection()) == " TF-BollingerOmni4":
        call(["python", "TF-BollingerOmni4_1R.py"])
        qsreport('TF-Boll-Omni4_1R-PosMatrix.txt')


    if stratlist.get(stratlist.curselection()) == " TF-BollingerOnClose":
        call(["python", "TF-BollingerOnClose_1R.py"])
        qsreport('TF-BollOnClose_1R-PosMatrix.txt')


    if stratlist.get(stratlist.curselection()) == " TF-BollingerOnOpen":
        call(["python", "TF-BollingerOnOpen_1R.py"])
        qsreport('TF-BollOnOpen_1R-PosMatrix.txt')


    if stratlist.get(stratlist.curselection()) == " TF-BollingerORBO":
        call(["python", "TF-BollingerORBO_1R.py"])
        qsreport('TF-BollwBO-PosMatrix.txt')


    if stratlist.get(stratlist.curselection()) == " TF-BollingerParadigm":
        call(["python", "TF-BollingerParadigm_1R.py"])
        qsreport('TF-BollPdigm-PosMatrix.txt')


    if stratlist.get(stratlist.curselection()) == " TF-BollingerPB":
        call(["python", "TF-BollingerPB_1R.py"])
        qsreport('TF-Bollinger_PB_1R-PosMatrix.txt')


    if stratlist.get(stratlist.curselection()) == " TF-BollingerRiskFilter1":
        call(["python", "TF-BollingerRiskFilter_1R.py"])
        qsreport('TF-Boll-RiskFilt_1R-PosMatrix.txt')


    if stratlist.get(stratlist.curselection()) == " TF-BollingerRiskFilter2":
        call(["python", "TF-BollingerRiskFilter2_1R.py"])
        qsreport('TF-Boll-RiskFilt2_1R-PosMatrix.txt')

    
    if stratlist.get(stratlist.curselection()) == " TF-BollingerTM":
        call(["python", "TF-BollingerTM_1R.py"])
        qsreport('TF-Boll-TM-PosMatrix.txt')




























def t1():
    df = pd.read_csv(treefile)
# For Table Number 1
    for count in range(len(df.columns) - 2):
        for i in df.iloc[:,count + 1]:
            if i == 1 and not tree.exists(f"{df.columns[count + 1]} {treefile}"):
                tree.insert("", tk.END, text=f"{df.columns[count + 1]}", values=(df.columns[count + 1], 1, "null"), iid=f"{df.columns[count + 1]} {treefile}")
            if i == 0 and tree.exists(df.columns[count + 1]):
                tree.delete(f"{df.columns[count + 1]} {treefile}")




def fcurr():
    if xcurr.get() == 1:
        check.select()
        check2.select()
        check3.select()
    elif xcurr.get() == 0:
        check.deselect()
        check2.deselect()
        check3.deselect()

def curr_():
    if x.get() != "" and x2.get() != "" and x3.get() != "":
        curr.select()
    else:
        curr.deselect()

def ftreas():
    if xtreas.get() == 1:
        check4.select()
        check5.select()
        check6.select()
    elif xtreas.get() == 0:
        check4.deselect()
        check5.deselect()
        check6.deselect()

def treas_():
    if x4.get() != "" and x5.get() != "" and x6.get() != "":
        treas.select()
    else:
        treas.deselect()
        
def findex():
    if xindex.get() == 1:
        check7.select()
        check8.select()
        check9.select()
    elif xindex.get() == 0:
        check7.deselect()
        check8.deselect()
        check9.deselect()

def index_():
    if x7.get() != "" and x8.get() != "" and x9.get() != "":
        index.select()
    else:
        index.deselect()

def fnrg():
    if xnrg.get() == 1:
        check10.select()
        check11.select()
        check12.select()
    elif xnrg.get() == 0:
        check10.deselect()
        check11.deselect()
        check12.deselect()

def nrg_():
    if x10.get() != "" and x11.get() != "" and x12.get() != "":
        nrg.select()
    else:
        nrg.deselect()

def fmetal():
    if xmetal.get() == 1:
        check13.select()
        check14.select()
        check15.select()
    elif xmetal.get() == 0:
        check13.deselect()
        check14.deselect()
        check15.deselect()

def metal_():
    if x13.get() != "" and x14.get() != "" and x15.get() != "":
        metal.select()
    else:
        metal.deselect()

def fgrain():
    if xgrain.get() == 1:
        check16.select()
        check17.select()
        check18.select()
    elif xgrain.get() == 0:
        check16.deselect()
        check17.deselect()
        check18.deselect()

def grain_():
    if x16.get() != "" and x17.get() != "" and x18.get() != "":
        grain.select()
    else:
        grain.deselect()

def fsoft():
    if xsoft.get() == 1:
        check19.select()
        check20.select()
        check21.select()
    elif xsoft.get() == 0:
        check19.deselect()
        check20.deselect()
        check21.deselect()

def soft_():
    if x19.get() != "" and x20.get() != "" and x21.get() != "":
        soft.select()
    else:
        soft.deselect()




# Checkbox Variables
x = tk.StringVar()
x2 = tk.StringVar()
x3 = tk.StringVar()
x4 = tk.StringVar()
x5 = tk.StringVar()
x6 = tk.StringVar()
x7 = tk.StringVar()
x8 = tk.StringVar()
x9 = tk.StringVar()
x10 = tk.StringVar()
x11 = tk.StringVar()
x12 = tk.StringVar()
x13 = tk.StringVar()
x14 = tk.StringVar()
x15 = tk.StringVar()
x16 = tk.StringVar()
x17 = tk.StringVar()
x18 = tk.StringVar()
x19 = tk.StringVar()
x20 = tk.StringVar()
x21 = tk.StringVar()


xcurr = tk.IntVar()
xtreas = tk.IntVar()
xindex = tk.IntVar()
xnrg = tk.IntVar()
xmetal = tk.IntVar()
xgrain = tk.IntVar()
xsoft = tk.IntVar()






# Data CheckBox
check = tk.Checkbutton(root,text="EC - Euro Currency", variable=x, onvalue="EC.CSV", offvalue="",command=curr_)
check.place(anchor="nw", x = 10, y = 260)

check2 = tk.Checkbutton(root,text="JY - Japanese Yen", variable=x2, onvalue="JY.CSV", offvalue="",command=curr_)
check2.place(anchor="nw", x = 10, y = 280)

check3 = tk.Checkbutton(root,text="BP - British Pound", variable=x3, onvalue="BP.CSV", offvalue="",command=curr_)
check3.place(anchor="nw", x = 10, y = 300)

check4 = tk.Checkbutton(root,text="TY - 10yr T.Note", variable=x4, onvalue="TY.CSV", offvalue="",command=treas_)
check4.place(anchor="nw", x = 10, y = 320)

check5 = tk.Checkbutton(root,text="FV - 5yr T.Note", variable=x5, onvalue="FV.CSV", offvalue="",command=treas_)
check5.place(anchor="nw", x = 10, y = 340)

check6 = tk.Checkbutton(root,text="ZB or US - 30yr T.Note", variable=x6, onvalue="US.CSV", offvalue="",command=treas_)
check6.place(anchor="nw", x = 10, y = 360)

check7 = tk.Checkbutton(root,text="SP or ES - E-mini S&P", variable=x7, onvalue="ES.CSV", offvalue="",command=index_)
check7.place(anchor="nw", x = 10, y = 380)

check8 = tk.Checkbutton(root,text="ND or NQ - Emini Nasdaq", variable=x8, onvalue="NQ.CSV", offvalue="",command=index_)
check8.place(anchor="nw", x = 10, y = 400)

check9 = tk.Checkbutton(root,text="DJ or EM - Emini Dow", variable=x9, onvalue="EM.CSV", offvalue="",command=index_)
check9.place(anchor="nw", x = 10, y = 420)

check10 = tk.Checkbutton(root,text="CL - Crude Oil (WTI)", variable=x10, onvalue="CL.CSV", offvalue="",command=nrg_)
check10.place(anchor="nw", x = 10, y = 440)

check11 = tk.Checkbutton(root,text="NG - Natural Gas (H.Hub)", variable=x11, onvalue="NG.CSV", offvalue="",command=nrg_)
check11.place(anchor="nw", x = 10, y = 460)

check12 = tk.Checkbutton(root,text="HO - ULSD (Heating Oil)", variable=x12, onvalue="HO.CSV", offvalue="",command=nrg_)
check12.place(anchor="nw", x = 10, y = 480)

check13 = tk.Checkbutton(root,text="GC - Gold", variable=x13, onvalue="GC.CSV", offvalue="",command=metal_)
check13.place(anchor="nw", x = 10, y = 500)

check14 = tk.Checkbutton(root,text="HG - Copper", variable=x14, onvalue="HG.CSV", offvalue="",command=metal_)
check14.place(anchor="nw", x = 10, y = 520)

check15 = tk.Checkbutton(root,text="SI - Silver", variable=x15, onvalue="SI.CSV", offvalue="",command=metal_)
check15.place(anchor="nw", x = 10, y = 540)

check16 = tk.Checkbutton(root,text="CO or 'C_' - Corn", variable=x16, onvalue="C_.CSV", offvalue="",command=grain_)
check16.place(anchor="nw", x = 10, y = 560)

check17 = tk.Checkbutton(root,text="SO or 'S_' - Soybeans", variable=x17, onvalue="S_.CSV", offvalue="",command=grain_)
check17.place(anchor="nw", x = 10, y = 580)

check18 = tk.Checkbutton(root,text="ZW or 'W_' - Wheat (SRW)", variable=x18, onvalue="W_.CSV", offvalue="",command=grain_)
check18.place(anchor="nw", x = 10, y = 600)

check19 = tk.Checkbutton(root,text="SB - Sugar", variable=x19, onvalue="SB.CSV", offvalue="",command=soft_)
check19.place(anchor="nw", x = 10, y = 620)

check20 = tk.Checkbutton(root,text="KC - Coffee", variable=x20, onvalue="KC.CSV", offvalue="",command=soft_)
check20.place(anchor="nw", x = 10, y = 640)

check21 = tk.Checkbutton(root,text="CT - Cotton", variable=x21, onvalue="CT.CSV", offvalue="",command=soft_)
check21.place(anchor="nw", x = 10, y = 660)

check22 = tk.Checkbutton(root,text="MBTC - Micro Bitcoin")
check22.place(anchor="nw", x = 10, y = 720)



curr = tk.Checkbutton(root, text="Currencies", variable=xcurr, onvalue=1, offvalue=0, command=fcurr)
curr.place(anchor="nw", x = 350, y = 260)

treas = tk.Checkbutton(root, text="Treasuries", variable=xtreas, onvalue=1, offvalue=0, command=ftreas)
treas.place(anchor="nw", x = 350, y = 320)

index = tk.Checkbutton(root, text="Indexes", variable=xindex, onvalue=1, offvalue=0, command=findex)
index.place(anchor="nw", x = 350, y = 380)

nrg = tk.Checkbutton(root, text="Energies", variable=xnrg, onvalue=1, offvalue=0, command=fnrg)
nrg.place(anchor="nw", x = 350, y = 440)

metal = tk.Checkbutton(root, text="Precious Metals", variable=xmetal, onvalue=1, offvalue=0, command=fmetal)
metal.place(anchor="nw", x = 350, y = 500)

grain = tk.Checkbutton(root, text="Grains", variable=xgrain, onvalue=1, offvalue=0, command=fgrain)
grain.place(anchor="nw", x = 350, y = 560)

soft = tk.Checkbutton(root, text="Softs", variable=xsoft, onvalue=1, offvalue=0, command=fsoft)
soft.place(anchor="nw", x = 350, y = 620)











# TABLE NUMBER 1

    # Create a Treeview widget
tree = ttk.Treeview(root)

    # Define columns
tree["columns"] = ("Symbol", "Pos-Size", "Date of Trade")

    # Format columns
tree.column("#0", width=0, stretch=tk.NO)  # Hidden column
tree.column("Symbol", anchor=tk.W, width=200)
tree.column("Pos-Size", anchor=tk.CENTER, width=75)
tree.column("Date of Trade", anchor=tk.CENTER, width=150)

    # Create headings
tree.heading("#0", text="", anchor=tk.W)
tree.heading("Symbol", text="Symbol", anchor=tk.W)
tree.heading("Pos-Size", text="Pos-Size", anchor=tk.CENTER)
tree.heading("Date of Trade", text="Date of Trade", anchor=tk.CENTER)

    # Insert data

tree.insert("", tk.END, text="one", values=("John Doe", 30, "Male"), iid="1")
tree.insert("", tk.END, text="2", values=("Jane Smith", 25, "Female"), iid="2")


    # Pack the treeview widget
tree.place(anchor="nw", x=490, y=40, height=200, width=460)





# TABLE NUMBER 2

    # Create a Treeview widget
tree2 = ttk.Treeview(root)

    # Define columns
tree2["columns"] = ("Symbol", "Trade Size")

    # Format columns
tree2.column("#0", width=0, stretch=tk.NO)  # Hidden column
tree2.column("Symbol", anchor=tk.W, width=200)
tree2.column("Trade Size", anchor=tk.CENTER, width=85) # NOTICE: width arguement seems not to do anything...?

    # Create headings
tree2.heading("#0", text="", anchor=tk.W)
tree2.heading("Symbol", text="Symbol", anchor=tk.W)
tree2.heading("Trade Size", text="Trade Size", anchor=tk.CENTER)

    # Insert data
for i in range(15):
    tree2.insert("", tk.END, text="1", values=("John Doe", 30))
    tree2.insert("", tk.END, text="2", values=("Jane Smith", 25))


    # Pack the treeview widget
tree2.place(anchor="nw", x=965, y=40, height=120, width=400)




# BUTTONS HERE -------------------
run = tk.Button(root, text="Run", command=checkfun)
run.place(anchor="nw", x=520, y=730)

# BUTTONS HERE -------------------
report = tk.Button(root, text="Show Report")
report.place(anchor="nw", x=600, y=730)

# BUTTONS HERE -------------------
showtsi = tk.Button(root, text="Show TSI")
showtsi.place(anchor="nw", x=720, y=730)




# The Keystone (initialized the loop and plots GUI)
root.mainloop()