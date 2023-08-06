from tkinter import *
root = Tk()
root.title("py-photo-viewer")
root.geometry("800x600")
imgpath = input("Enter the path of the image: ")
img = PhotoImage(file=imgpath)
viewport = Label(image=img)
viewport.pack()


root.mainloop()
