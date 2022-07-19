from tkinter import *

def dbl_click(event):
    root.title("Двойной клик ЛКМ")


def move(event):
    x = event.x
    y = event.y
    s = "Движение мышью {}x{}".format(x, y)
    root.title(s)


root = Tk()
root.minsize(width=500, height=400)

root.bind('<Double-Button-1>', dbl_click)
root.bind('<Motion>', move)

root.mainloop()