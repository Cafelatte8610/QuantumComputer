import tkinter

def create_window(self): 
     window = tkinter.Tk() 
    self.canvas = tkinter.Canvas(window, bg = "white",width = 300, height = 300 )

    self.canvas.pack() 
    quit_button = tkinter.Button(window, text = "quit", command = window.quit) 
    quit_button.pack(side = tkinter.RIGHT) 
 
    self.canvas.bind("<ButtonPress-1>", self.on_pressed) 
    self.canvas.bind("<B1-Motion>", self.on_dragged)

