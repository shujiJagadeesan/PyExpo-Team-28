import tkinter as tk
import tkinter.ttk as ttk
from tika import parser
import re
import csv
import time
from tkinter import font
from tkinter import filedialog
from tkinter.constants import BOTTOM, CENTER, LEFT, SW
# creating the root window
root = tk.Tk()
root.geometry("700x700")
root.configure(background='#c5c6d0')
root.title('pyexpo 28')
# writes the columns (Email, Phone Number) into the CSV file(data.csv) as the first row.
with open('./data.csv','a', newline='') as file:
    file.truncate(0)
    myWriter = csv.writer(file,quoting=csv.QUOTE_MINIMAL)
    myWriter.writerow(['Email','Phone Number'])

# function to clear all the widgets in the corresponding window
def clearWidgets():
    for widget in root.pack_slaves():
        widget.destroy()

# function from where the execution starts, acts as the home page of the application
def mainProcess():
    clearWidgets()

    mainFrame = tk.Frame(root,bg='#c5c6d0')
    mainFrame.pack(fill='both')

    heading = tk.Label(mainFrame,text="Email and Phone number Extractor", bg= "#235789", fg ="white",font=("serif",25))
    heading.pack(fill='x')

    labelFrame = tk.LabelFrame(mainFrame,text="description",bg='#c5c6d0', font=("monospace",25))
    labelFrame.pack(pady=(30,0))    

    projectDescription = tk.Label(labelFrame,text="You can input a paragraph using the below text box or upload a file (.pdf, .txt, .docx) using the button on the top-left from which the EMAILs and PHONE NUMBERs are extracted for making your job easy.",font=18,wraplength=800,bg='#c5c6d0')
    projectDescription.pack()

    enterTextLabel = tk.Label(mainFrame, text="Enter the text to search from", font=20)
    # enterTextLabel.config(anchor=CENTER)
    enterTextLabel.pack(pady=(100,0))

    inputParagraph = tk.Text(mainFrame,width=100,height=15)
    inputParagraph.insert(1.0,"type the paragraph....")
    inputParagraph.pack()

    messageLabel = tk.Label(mainFrame,text="",bg='#c5c6d0',fg="red",font=15)
    messageLabel.pack()

    submitButton = tk.Button(mainFrame, text="SUBMIT", command=lambda : processInput(inputParagraph,messageLabel,mainFrame))
    submitButton.pack(pady=(20,0))

    uploadPDFButton = tk.Button(mainFrame, text="UPLOAD FILE", command= goToUploadPage)
    uploadPDFButton.place(x=10,y=10)
    # to display the window 
    root.mainloop()

# function that creates a button that takes us to the home page
def goToHomeButton(frame):
    goToHomeButton = tk.Button(frame, text="BACK",command= mainProcess)
    goToHomeButton.pack(pady=(10,50),padx=10)

# function to navigate to the upload page to upload a file
def goToUploadPage():
    clearWidgets()
    uploadFrame = tk.Frame(root,bg='#c5c6d0')
    uploadFrame.pack(fill="both")
    file = filedialog.askopenfilename()
    if file:
        waitLabel = tk.Label(uploadFrame,text="Please wait till the file loads....",bg='#c5c6d0',font=("serif",18))
        waitLabel.pack(pady=(180,5))
        pb1 = ttk.Progressbar(
        uploadFrame,
        orient= 'horizontal',    
        length=300, 
        mode='determinate'
        )
        pb1.pack(pady=200)
        for i in range(5):
            uploadFrame.update_idletasks()
            pb1['value'] += 35
            time.sleep(1)

        waitLabel.destroy()
        pb1.destroy()
        status = tk.Label(uploadFrame, text='File Uploaded Successfully!', fg='green',bg='#c5c6d0', font=("serif",25))
        status.pack()
        data = parser.from_file(file)
        text = data['content']
        text = str(text).strip() # converting the read data into string
        if text != "None": # by default an empty file has text 'None'in it.
            phoneNumbers= re.findall('[0-9]{10}',text)
            emails = re.findall('\S+@\S+',text)
            displayData(emails,phoneNumbers)
            writeIntoCSV(emails,phoneNumbers)
        else:
            noDataLabel = tk.Label(uploadFrame,text="File is Empty !!",fg="red",bg='#c5c6d0',font=15)
            noDataLabel.pack(pady=20)
            goToHomeButton(uploadFrame)
    else:   
        status = tk.Label(uploadFrame, text="File Upload Failed", fg="red",bg='#c5c6d0',font=("serif",25))
        status.pack()
        goToHomeButton(uploadFrame)
    
# function to display the email(s) and phone numbers(s)
def displayData(emails,phoneNumbers):
    clearWidgets()
    
    displayFrame = tk.Frame(root,bg='#c5c6d0')
    displayFrame.pack(fill="both")
    goToHomeButton(displayFrame)

    if len(emails) >0:
        emailHeadingLabel = tk.Label(displayFrame, text="Emails :", font=35,bg='#c5c6d0')
        emailHeadingLabel.pack()
        for email in emails:
            emailLabel= tk.Label(displayFrame, text= email, font=20,bg='#c5c6d0')
            emailLabel.pack()
    
    if len(phoneNumbers)> 0:
        phoneNumberLabel = tk.Label(displayFrame, text="Phone Numbers :", font=35,bg='#c5c6d0')
        phoneNumberLabel.pack(pady=(100,0))
        for number in phoneNumbers:
            numberLabel = tk.Label(displayFrame, text=number, font=20,bg='#c5c6d0')
            numberLabel.pack()

    if len(emails) == 0 and len(phoneNumbers) == 0:
        noDataLabel = tk.Label(displayFrame,text="NO EMAIL(S) AND NO PHONE NUMBER(S)",fg="red",bg='#c5c6d0',font=25)
        noDataLabel.pack()

# function to write the extracted data into the CSV file (data.csv)
def writeIntoCSV(emails, phoneNumbers):
    emailsSize = len(emails)
    phoneNumbersSize = len(phoneNumbers)
    minimum = min(emailsSize, phoneNumbersSize)
    maximum = max(emailsSize, phoneNumbersSize)
    for i in range(minimum):
        with open('./data.csv','a', newline='') as file:
            myWriter = csv.writer(file,quoting=csv.QUOTE_MINIMAL)
            myWriter.writerow([emails[i],phoneNumbers[i]])
    if minimum == maximum:
        return
    isEmailMinimum = True if len(emails)<len(phoneNumbers) else False
    if isEmailMinimum:
        for j in range(minimum,maximum):
            with open('./data.csv','a', newline='') as file:
                myWriter = csv.writer(file,quoting=csv.QUOTE_MINIMAL)
                myWriter.writerow(["    ",phoneNumbers[j]])
    else:
        for j in range(minimum,maximum):
            with open('./data.csv','a', newline='') as file:
                myWriter = csv.writer(file,quoting=csv.QUOTE_MINIMAL)
                myWriter.writerow([emails[j],"  "])

# function to process the entered input i.e extracting the email(s) and password(s)                   
def processInput(inputParagraph,messageLabel,mainFrame):
    enteredInput = inputParagraph.get(1.0,"end-1c")
    phoneNumbers= re.findall('[0-9]{10}',enteredInput)
    emails = re.findall('\S+@\S+',enteredInput)
        
    if len(emails)== 0 and len(phoneNumbers)==0:
        messageLabel.config(text="NO EMAILS AND NO PHONE NUMBER")
        try:
            # findDataButton.destroy()
            pass
        except:
            print("error while removing the button that takes to the CSV Page")
    else:
        messageLabel.config(text="")
        findDataButton = tk.Button(mainFrame, text="DATA",command=lambda:displayData(emails,phoneNumbers)) 
        writeIntoCSV(emails,phoneNumbers)
        findDataButton.pack(side="bottom",pady=20)

# execution starts here..
mainProcess()
