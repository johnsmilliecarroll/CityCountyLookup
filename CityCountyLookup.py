import csv
import tkinter as tk
from tkinter import Canvas
from tkinter import Radiobutton
from tkinter import PhotoImage
from tkinter import messagebox
from tkinter import filedialog
from os.path import exists
from PIL import Image

if not exists('data.txt'):  # create file if it doesn't exist
    #  set up CSV
    myfile = open("MontanaCounties.csv")

    mycsv = csv.reader(myfile)  # read file

    next(mycsv)  # read past header
    rows = []
    for row in mycsv:
        rows.append(row)  # add rows to array

    with open('data.txt', 'w') as txt:  # create file
        for y in rows:
            txt.write(y[0] + "," + y[1] + "," + y[2] + "\n")  # write values to text file
    txt.close()  # close file
    print("text file created")

# create dictionary of values based off those in data.txt
countyDict = {}
prefixes = []  # keep track of prefixes to avoid duplicates
with open('data.txt') as txt:  # open file for reading
    lines = txt.readlines()
    for line in lines:
        elements = line.split(',')
        # insert values into dictionary, lowercase city key.
        countyDict[elements[1].lower()] = {'County': elements[0], 'Num': elements[2].strip()}
        prefixes.append(elements[2].strip()) # insert prefix into list
txt.close()  # close file

# set up GUI
winwidth = 640
winheight = 480

wn = tk.Tk()
wn.title("County License Plate Prefixes")
wn.geometry(str(winwidth) + "x" + str(winheight))
canvas = Canvas(wn, width=winwidth, height=winheight)
canvas.pack()

myValue = tk.StringVar()  # text entry value

myState = tk.Label(wn)  # county name
myState.place(x=winwidth * 0.25, y=winheight / 4, anchor='center')
mySeat = tk.Label(wn)  # county seat
mySeat.place(x=winwidth * 0.75, y=winheight / 4, anchor='center')
radioValue = tk.StringVar(wn, '2')  # radio button value
img1 = PhotoImage(master=wn)
img2 = PhotoImage(master=wn)
Image1 = canvas.create_image(winwidth * 0.25, winheight * 0.60, image=img1, anchor='center')
Image2 = canvas.create_image(winwidth * 0.75, winheight * 0.60, image=img2, anchor='center')

# second window
wn2 = tk.Tk()
wn2.withdraw()
winwidth2 = 600
winheight2 = 480
canvas2 = Canvas(wn2, width=winwidth2, height=winheight2)
canvas2.pack()
secondWindow = False
cityEntry = tk.Entry(wn2)
countyEntry = tk.Entry(wn2)
numEntry = tk.Entry(wn2)
entryimg1 = PhotoImage(master=wn2)
entryimg2 = PhotoImage(master=wn2)
entryImage1 = 0
entryImage2 = 0
entryfile1 = ''
entryfile2 = ''
errorLabel = tk.Label(wn2)


def imagefromfile1():  # city image choose file dialogue
    global entryimg1
    global entryfile1
    entryfile1 = filedialog.askopenfilename(title='Open')  # open file explorer
    if entryfile1 != '':  # if you chose something, grab path and set image display
        entryimg1 = PhotoImage(master=wn2, file=entryfile1)
        canvas2.itemconfig(entryImage1, image=entryimg1, anchor='center')


def imagefromfile2():  # county image choose file dialogue
    global entryimg2
    global entryfile2
    entryfile2 = filedialog.askopenfilename(title='Open')
    if entryfile2 != '':
        entryimg2 = PhotoImage(master=wn2, file=entryfile2)
        canvas2.itemconfig(entryImage2, image=entryimg2, anchor='center')


def wn2entries():  # tkinter objects placed on the new entry window
    # second window gui
    global cityEntry
    global countyEntry
    global numEntry
    global entryimg1
    global entryimg2
    global entryImage1
    global entryImage2
    global canvas2
    global wn2
    global errorLabel
    global secondWindow
    wn2 = tk.Tk()  # recreate window values
    wn2.title("Create New Entry")
    wn2.geometry(str(winwidth2) + "x" + str(winheight2))
    canvas2 = Canvas(wn2, width=winwidth2, height=winheight2)
    canvas2.pack()
    myLabel2 = tk.Label(wn2, text="Fill in the fields:")
    myLabel2.place(x=winwidth2 / 2, y=15, anchor='center')

    errorLabel = tk.Label(wn2, text="", fg='red')
    errorLabel.place(x=winwidth2 / 2, y=155, anchor='center')

    cityLabel = tk.Label(wn2, text="City:")
    cityLabel.place(x=winwidth2 / 4, y=40, anchor='e')

    cityEntry = tk.Entry(wn2)
    cityEntry.place(x=winwidth2 / 2, y=40, anchor='center')
    cityEntry.insert(0, str(myValue.get()))  # set the text field to the value you previously inserted

    countyLabel = tk.Label(wn2, text="County:")
    countyLabel.place(x=winwidth2 / 4, y=80, anchor='e')

    countyEntry = tk.Entry(wn2)
    countyEntry.place(x=winwidth2 / 2, y=80, anchor='center')

    numLabel = tk.Label(wn2, text="Prefix:")
    numLabel.place(x=winwidth2 / 4, y=120, anchor='e')

    numEntry = tk.Entry(wn2)
    numEntry.place(x=winwidth2 / 2, y=120, anchor='center')

    btnMyButton2 = tk.Button(wn2, text="Submit", command=submit)  # submit button
    btnMyButton2.place(x=winwidth2 / 2, y=190, anchor='center')

    imgLabel1 = tk.Label(wn2, text="County Image:")
    imgLabel1.place(x=winwidth2 * 0.25, y=200, anchor='center')
    imgLabel2 = tk.Label(wn2, text="City Image:")
    imgLabel2.place(x=winwidth2 * 0.75, y=200, anchor='center')

    btnImageUpload1 = tk.Button(wn2, text="Open", command=imagefromfile1)  # open image files
    btnImageUpload1.place(x=winwidth2 * 0.25, y=240, anchor='center')
    btnImageUpload2 = tk.Button(wn2, text="Open", command=imagefromfile2)
    btnImageUpload2.place(x=winwidth2 * 0.75, y=240, anchor='center')

    entryImage1 = canvas2.create_image(winwidth2 * 0.25, winheight2 * 0.75, image='', anchor='center')  # image displays
    entryImage2 = canvas2.create_image(winwidth2 * 0.75, winheight2 * 0.75, image='', anchor='center')
    secondWindow = True


def returninfo():  # populate the gui with the information
    global img1
    global img2
    global secondWindow
    global wn2
    global canvas2
    if myValue.get().lower() in countyDict.keys():  # lowercase value before checking
        if myValue.get() != "":  # make sure it isn't empty
            dictEntry = countyDict.get(myValue.get().lower())
            myStateVal = dictEntry['County']
            mySeatVal = dictEntry['Num']
            path1 = "images/" + mySeatVal + "-0.png"  # get path for images
            path2 = "images/" + mySeatVal + "-1.png"
            if radioValue.get() == '0':  # radio button is only county
                myState["text"] = "County Name: " + myStateVal
                mySeat["text"] = ""
                if exists(path1):  # make sure image exists
                    img1 = PhotoImage(file=path1)
                else:
                    img1 = PhotoImage()
                img2 = PhotoImage()
                # place county label and images in center
                myState.place(x=winwidth / 2, y=winheight / 4, anchor='center')
                mySeat.place(x=winwidth, y=winheight / 4, anchor='center')  # move seat label to the side
                canvas.coords(Image1, winwidth / 2, winheight * 0.60)
            elif radioValue.get() == '1':  # radio button is only seat
                myState["text"] = ""
                mySeat["text"] = "Seat City: " + mySeatVal
                img1 = PhotoImage()
                if exists(path1):  # make sure image exists
                    img2 = PhotoImage(file=path2)
                else:
                    img2 = PhotoImage()
                # place seat label and images in center
                myState.place(x=winwidth, y=winheight / 4, anchor='center')
                mySeat.place(x=winwidth / 2, y=winheight / 4, anchor='center')  # move county label to the side
                canvas.coords(Image2, winwidth / 2, winheight * 0.60)
            else:  # radio button is both
                myState["text"] = "County Name: " + myStateVal
                mySeat["text"] = "License Prefix: " + mySeatVal
                if exists(path1):  # make sure image exists
                    img1 = PhotoImage(file=path1)
                else:
                    img1 = PhotoImage()
                if exists(path2):
                    img2 = PhotoImage(file=path2)
                else:
                    img2 = PhotoImage()
                # set image and label position to stand next to one another
                myState.place(x=winwidth * 0.25, y=winheight / 4, anchor='center')
                mySeat.place(x=winwidth * 0.75, y=winheight / 4, anchor='center')
                canvas.coords(Image1, winwidth * 0.25, winheight * 0.60)
                canvas.coords(Image2, winwidth * 0.75, winheight * 0.60)
            canvas.itemconfig(Image1, image=img1, anchor='center')  # change images
            canvas.itemconfig(Image2, image=img2, anchor='center')
    else:  # if value is not in the dictionary, prompt them to make a new entry
        if messagebox.askyesno("Entry not Found",
                               "That entry doesn't exist yet! Would you like to create a new entry?"):
            wn2entries()


def submit():  # submit a new entry
    city = str(cityEntry.get())
    county = str(countyEntry.get())
    num = str(numEntry.get())
    if city == '' or county == '' or num == '':  # check if fields were all filled in
        errorLabel.config(text='Please fill in all of the above fields.')
    elif city in countyDict:  # check if city already exist in dict
        errorLabel.config(text='City already exists in our data!')
    elif num in prefixes:  # check if prefix is in use
        errorLabel.config(text='Prefix already being used')
    elif not num.isnumeric():  # check that prefix is a number
        errorLabel.config(text='Prefix is not a valid number')
    else:  # we're ok to submit the entry
        with open('data.txt', 'a') as txtf:  # open file for appending
            # write value to text file
            txtf.write(county + "," + city + "," + num + "\n")
        txtf.close()  # close file
        # add values to dictionary
        countyDict[city.lower()] = {'County': county, 'Num': num}
        prefixes.append(num)  # add prefix to list
        print("inserted City:" + city + ", County:" + county + ", Prefix:" + num)
        if entryfile1 != '':
            Image.open(entryfile1).save("images/" + num + "-0.png")
        if entryfile2 != '':
            Image.open(entryfile2).save("images/" + num + "-1.png")
        wn2.destroy()  # close the window when done


# set up the rest of the gui

myLabel = tk.Label(wn, text="Enter City Seat:")
myLabel.place(x=winwidth / 2, y=15, anchor='center')

txtEntry = tk.Entry(wn, textvariable=myValue)
txtEntry.place(x=winwidth / 2, y=40, anchor='center')

radio0 = Radiobutton(wn, text="County", variable=radioValue, value='0')
radio0.place(x=winwidth * 0.25, y=70, anchor='center')
radio1 = Radiobutton(wn, text="Prefix", variable=radioValue, value='1')
radio1.place(x=winwidth * 0.5, y=70, anchor='center')
radio2 = Radiobutton(wn, text="Both", variable=radioValue, value='2')
radio2.place(x=winwidth * 0.75, y=70, anchor='center')

btnMyButton = tk.Button(wn, text="Enter", command=returninfo)
btnMyButton.place(x=winwidth / 3, y=40, anchor='center')

btnNewEntry = tk.Button(wn, text="New Entry", command=wn2entries)
btnNewEntry.place(x=40, y=40, anchor='center')


def close():  # set secondWindow value to false when closing it
    global secondWindow
    secondWindow = False


def terminate():  # end the program
    quit()


wn2.protocol("WM_DELETE_WINDOW", close)  # when you close the second window, call close()
wn.protocol("WM_DELETE_WINDOW", terminate)  # when you close the first window, end program

wn.mainloop()
if secondWindow:  # if second window is open run a loop.
    wn2.mainloop()
