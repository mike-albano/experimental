"""Simple randomizer between two pics.
pip3 install pillow
install tkinter if necessary.
"""
import random
from tkinter import *
import sys

from PIL import ImageTk, Image
from tkinter import filedialog
import datetime

def spinner():
  """Spin the random wheel."""
  if random.choices(['1', '2'])[0] == '1':
    open_img('1')
  else:
    open_img('2')

def open_img(img_idx):
  img = Image.open('~/experimental/randomizer/' + img_idx + '.jpg')
  img = img.resize((250, 250), Image.ANTIALIAS)
  img = ImageTk.PhotoImage(img)

  panel = Label(root, image = img)  # Create label
  # set the image as img
  panel.image = img
  panel.grid(row = 2)  # Draw img on row 2
  root.title('Last spin at: %s' % datetime.datetime.now().strftime("%D:%H:%M:%S"))

def quit():
  sys.exit()


if __name__ == '__main__':
  root = Tk()
  root.title('Child Randomizer')
  # Allow Window to be resizable
  root.resizable(width = True, height = True)
  # Create buttons in grid layout
  spin_btn = Button(root, text='Spin The Wheel', command=spinner, width=30,
                    height=10, fg='blue').grid(row = 1, columnspan = 4)
  quit_btn = Button(root, text='Quit', command=quit, width=30, height=10, fg='red').grid(
  										row = 3, columnspan = 4)
  root.mainloop()
