from tkinter import *
import grabber
from PIL import Image, ImageTk
from io import BytesIO

root = Tk()

def display_image(b):
    if isinstance(b, BytesIO):  # If it's already a file-like object
        img = Image.open(b)
    else:  # Otherwise, treat it as raw bytes and convert to BytesIO
        img = Image.open(BytesIO(b))
    tk_img = ImageTk.PhotoImage(img)
    label.config(image=tk_img, text=prompt.get())
    label.image = tk_img  

def x():
    notifytext.config(text="The program may freeze, but that's just the image loading.")
    item = grabber.set_up(prompt.get())
    notifytext.config(text="Completed!")
    display_image(item)

label = Label(root, text="Not Generated")
notifytext = Label(root)
prompt = Entry(root)
butt = Button(root, text="Generate", command=x)

label.pack()
notifytext.pack()
prompt.pack()
butt.pack()

root.mainloop()

# Note: The program may freeze when you click the generate button, that's just because the image is loading.