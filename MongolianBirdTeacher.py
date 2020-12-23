import os
import random as rd
import tkinter as tk

from tkinter import font
from PIL import ImageTk, Image

# Clear the terminal at the start of each run
os.system('cls' if os.name == 'nt' else 'clear')

# Set the background image and the path to the picture folder
backgroundImageName = 'Background.png'
birdFolder = 'BirdPics/'

# Open the list of names
nameFile = open('Names.txt', 'r')
lines = nameFile.readlines()
birdArray = []

# Add all of the picture paths to an array
for name in lines:
    name = name.strip()
    pictureLocation = birdFolder + name + '.png'
    birdArray.append(pictureLocation)
    rd.shuffle(birdArray)

# Initialize the tracking variables
counter = 0
right = 0
total = 0
repeat = False
repeatShow = False
moveOn = 0

# Default path and label
birdPath = birdArray[counter]
birdImageLabel = 0

# Update the picture to the next bird
def nextBird(dir):
    global counter
    global birdPath
    global birdImageLabel
    global repeat

    # Reset the answer label to be white and blank
    labelTextAnswer.set(' ')
    labelAnswer.config(bg = 'white')
    repeat = False

    entryBox.delete(0, 'end')
    entryBox.insert(0, '')

    if dir == 1:
        counter += 1
    elif dir == 0:
        counter -= 1
    else:
        counter += 0

    if counter >= len(birdArray):
        counter = 0

    # Create a label that displays the bird image and then scales it
    birdPath = birdArray[counter]
    birdPhotoImage = scaleImage()
    birdImageLabel.configure(image = birdPhotoImage)
    birdImageLabel.image = birdPhotoImage

    # Generate the dashes that give a hint of the name and update the label
    dashLength = generateDash()
    labelTextLetters.set(dashLength)

    labelTextGuess.set('Waiting for a guess...')

# Update the guess label with the guess
def displayGuess(entry):
    global right
    global total
    global repeat
    global moveOn

    entry = entry.lower()
    labelTextGuess.set(entry)

    answer = (birdPath[9:(len(birdPath) - 4)]).lower()

    repeat, total, right, moveOn = fractionUpdate(repeat, entry, answer, total, right, moveOn)
    
    moveOn = setColor(entry, answer, moveOn, counter)

# Sets the color based on the answer
def setColor(entryVar, answerVar, moveOnVar, counterVar):
    if entryVar == answerVar:
        labelTextAnswer.set('Correct')
        labelAnswer.config(bg = 'green')

        if moveOnVar < 2:
            moveOnVar = 2
            birdArray.remove(birdArray[counterVar])
        elif moveOnVar == 2:
            nextBird(1)

    else:
        labelTextAnswer.set('Wrong')
        labelAnswer.config(bg = 'red')

    return moveOnVar

# Update the correct fraction
def fractionUpdate(repeatVar, entryVar, answerVar, totalVar, rightVar, moveOnVar):
    if repeatVar is False:
        repeatVar = True
        totalVar += 1

        if entryVar == answerVar:
            rightVar += 1
            fraction = str(rightVar) + ' / ' + str(totalVar) 
            labelPercentValue.set(fraction)
            moveOnVar = 1
        else:
            fraction = str(rightVar) + ' / ' + str(totalVar) 
            labelPercentValue.set(fraction) 
            moveOnVar = 0

    return repeatVar, totalVar, rightVar, moveOnVar  

# Add functionality to the reset button
def resetButton():
    global repeat
    global right
    global total

    labelTextAnswer.set('This will display if you are correct or not')
    labelTextGuess.set('Waiting for a guess...')
    labelGuess.config(bg = 'white')
    labelAnswer.config(bg = 'white')

    repeat = False
    right = 0
    total = 0
    
    labelPercentValue.set('0 / 0')

    entryBox.delete(0, 'end')
    entryBox.insert(0, '')

# Add functionality to the show button
def showButton():
    global total
    global repeatShow

    if repeatShow is False:
        repeatShow = True

        total += 1
        fraction = str(right) + ' / ' + str(total) 
        labelPercentValue.set(fraction)

    bird = birdPath[9:(len(birdPath) - 4)]
    labelTextGuess.set(bird)

# Generate the dashes that give a hint of the name
def generateDash():
    dashLength = ''
    bird = birdPath[9:(len(birdPath) - 4)]

    for char in bird:
        if char == ' ':
            dashLength += '  '
        elif char == '-':
            dashLength += '- '
        else:
            dashLength += '_ '

    return dashLength

# Scale the next image to fit the screen
def scaleImage():
    # Open an image and convert it to a photoimage
    birdImage = Image.open(birdPath)
    birdPhotoImage = ImageTk.PhotoImage(birdImage)

    # Get the height and width of the image
    imageHeight = birdPhotoImage.height()
    imageWidth = birdPhotoImage.width()
    ratio = 1

    # If the image is too wide, scale it down
    if imageWidth > imageHeight and imageWidth > 400:
        ratio = imageHeight/imageWidth
        imageWidth = 400
        imageHeight = int(imageWidth * ratio)

        resizedBirdImage = birdImage.resize((imageWidth, imageHeight), Image.ANTIALIAS)
        return ImageTk.PhotoImage(resizedBirdImage)

    # If the image is too tall, scale it down
    elif imageHeight > imageWidth and imageWidth > 400:
        ratio = imageWidth/imageHeight
        imageHeight = 400
        imageWidth = int(imageHeight * ratio)

        resizedBirdImage = birdImage.resize((imageWidth, imageHeight), Image.ANTIALIAS)
        return ImageTk.PhotoImage(resizedBirdImage)

# This creates the main window of an application
window = tk.Tk()

# Get the screen height and width
WIDTH = window.winfo_screenwidth() * 0.9
HEIGHT = window.winfo_screenheight() * 0.9

# This makes the window open at a given size
canvas = tk.Canvas(window, height = HEIGHT, width = WIDTH)
canvas.pack()

# Add the background image over the whole canvas
backgroundImage = tk.PhotoImage(file = backgroundImageName)
backgroundLabel = tk.Label(window, image = backgroundImage)
backgroundLabel.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)

# The name displayed above the canvas
window.title('Mongolian Bird Species Teacher')

# Creates a canvas where widgets can be placed, size is controled by height and width constants
frame = tk.Frame(window, bg = '#81a2d6')
frame.place(relx = 0.1, rely = 0.1, relheight = 0.8, relwidth = 0.8)

# Creates the text entry box at the bottom middle of the screen
entryBox = tk.Entry(frame, font = ('Calibre', 16))
entryBox.place(relx = 0.35, rely = 0.25, relheight = 0.075, relwidth = 0.6)
entryBox.bind('<Return>', (lambda event: displayGuess(entryBox.get())))

# Creates a button that calls a function to show the next bird
button = tk.Button(frame, command = lambda: nextBird(0), text = 'Prev', font = ('Calibre', 16))
button.place(relx = 0.05, rely = 0.05, relwidth = 0.12, relheight = 0.075)

# Creates a button that calls a function to show the previous bird
button = tk.Button(frame, command = lambda: nextBird(1), text = 'Next', font = ('Calibre', 16))
button.place(relx = 0.18, rely = 0.05, relwidth = 0.12, relheight = 0.075)

# Creates a button to reset the fraction tracker
reset = tk.Button(frame, command = lambda: resetButton(), text = 'Reset', font = ('Calibre', 16))
reset.place(relx = 0.05, rely = 0.25, relwidth = 0.25, relheight = 0.075)

# Creates a button to show the answer when you are stuck
show = tk.Button(frame, command = lambda: showButton(), text = 'Show Answer', font = ('Calibre', 16))
show.place(relx = 0.05, rely = 0.35, relwidth = 0.25, relheight = 0.075)

# Create a string var used to change the label through a function
labelTextGuess = tk.StringVar(window, 'Waiting for a guess...')
labelTextAnswer = tk.StringVar(window, 'This will display if you are correct or not')

# Generate the dashes that give a hint of the name and update the label
dashLength = generateDash()
labelTextLetters = tk.StringVar(window, dashLength)

# The initial value of the amount correct
labelPercentValue = tk.StringVar(window, '0 / 0')

# Create a label to display the last typed guess
labelGuess = tk.Label(frame, textvariable = labelTextGuess, font = ('Calibre', 16))
labelGuess.place(relx = 0.35, rely = 0.05, relwidth = 0.6, relheight = 0.075)

# Create a label to display the correct answer
labelAnswer = tk.Label(frame, textvariable = labelTextAnswer, font = ('Calibre', 16))
labelAnswer.place(relx = 0.35, rely = 0.15, relwidth = 0.6, relheight = 0.075)

# Create a label to display the number of letters in the bird's name
labelLetters = tk.Label(frame, bg = '#81a2d6', textvariable = labelTextLetters, font = ('Calibre', 20))
labelLetters.place(relx = 0.35, rely = 0.35, relwidth = 0.6, relheight = 0.075)

# Create a label to display the amount right and wrong
labelPercent = tk.Label(frame, bg = '#81a2d6', textvariable = labelPercentValue, font = ('Calibre', 20))
labelPercent.place(relx = 0.05, rely = 0.15, relwidth = 0.25, relheight = 0.075)

# Create a label that displays the bird image and then center it
birdPhotoImage = scaleImage()
birdImageLabel = tk.Label(frame, image = birdPhotoImage)
birdImageLabel.place(relx = 0.05, rely = 0.95, anchor = 'sw')

# Start the GUI
window.mainloop()