from tkinter import *
from tkinter.filedialog import askopenfile, asksaveasfile
import numpy as np

CLIENT_SIZE = (800,600)
EDITOR_TAB_SIZE = (200,600)
DEFAULT_MAP_SIZE = (20,20)
RENDER_FPS = 20
MIN_MAP_SIZE = (20,20)
MAX_MAP_SIZE = (60,60)

class MapCreator:
    def __init__(self):

        def new():

            if self.f is not None:
                save()
                self.f.close()
                self.f = None

            self.map_size = DEFAULT_MAP_SIZE
            x_scale = self.map_size[0] / (CLIENT_SIZE[0] - EDITOR_TAB_SIZE[0])
            y_scale = self.map_size[1] / CLIENT_SIZE[1]
            self.scale = 1/max(x_scale, y_scale)
            self.x_start = EDITOR_TAB_SIZE[0] + (CLIENT_SIZE[0] - EDITOR_TAB_SIZE[0] - (self.map_size[0]*self.scale)) / 2
            self.y_start = (CLIENT_SIZE[1] - (self.map_size[1]*self.scale)) / 2
            self.x_end = self.x_start + self.map_size[0]*self.scale
            self.y_end = self.y_start + self.map_size[1]*self.scale
            if self.base is not None:
                self.canvas.delete(self.base)
            self.base = self.canvas.create_rectangle(self.x_start, self.y_start, self.x_end, self.y_end, fill='white')
            self.terrain_map = np.ones(self.map_size, dtype=bool)
            self.r_locs = []
            self.b_locs = []
            
            self.canvas.pack()

        def open_map():
            if self.f is not None:
                save()
                self.f.close()
                self.f = None

            self.f = askopenfile(mode = 'r+', filetypes=[('Map Files', '*txt')])
            if self.f is not None:
                self.r_locs = []
                self.b_locs = []
                lines = self.f.readlines()
                self.map_size = tuple(map(int,lines[0].split()))
                self.terrain_map = np.ones(self.map_size, dtype=bool)
                for y in range(self.map_size[1]):
                    line = lines[1+y]
                    for x in range(self.map_size[0]):
                        if line[x] == '-':
                            continue
                        elif line[x] == 'x':
                            self.terrain_map[x][y] = False
                        elif line[x] == 'r':
                            self.r_locs.append((x,y))
                        elif line[x] == 'b':
                            self.b_locs.append((x,y))
                
                
                self.map_name = self.f.name
                x_scale = self.map_size[0] / (CLIENT_SIZE[0] - EDITOR_TAB_SIZE[0])
                y_scale = self.map_size[1] / CLIENT_SIZE[1]
                self.scale = 1/max(x_scale, y_scale)
                self.x_start = EDITOR_TAB_SIZE[0] + (CLIENT_SIZE[0] - EDITOR_TAB_SIZE[0] - (self.map_size[0]*self.scale)) / 2
                self.y_start = (CLIENT_SIZE[1] - (self.map_size[1]*self.scale)) / 2
                self.x_end = self.x_start + self.map_size[0]*self.scale
                self.y_end = self.y_start + self.map_size[1]*self.scale
                if self.base is not None:
                    self.canvas.delete(self.base)
                self.base = self.canvas.create_rectangle(self.x_start, self.y_start, self.x_end, self.y_end, fill='white')
                y = 0
                for row in self.terrain_map:
                    x = 0
                    for t in row:
                        if not t:
                            real_x,real_y = self.get_real_coords(x,y)
                            self.canvas.create_rectangle(real_x, real_y, real_x+self.scale,real_y+self.scale,fill='green')
                self.canvas.pack()
                print(self.x_start,self.x_end,self.y_start,self.y_end)

        def save():
            if self.f is None:
                self.f = asksaveasfile(mode = 'w', filetypes=[('Map Files', '*txt')])
                if self.f is not None:
                    self.f.write(str(self.map_size[0]) + " " + str(self.map_size[1]) + "\n")
                    y = 0
                    for row in self.terrain_map:
                        x = 0
                        for t in row:
                            if (x,y) in self.r_locs:
                                self.f.write('r')
                            elif (x,y) in self.b_locs:
                                self.f.write('b')
                            elif not t:
                                self.f.write('x')
                            else:
                                self.f.write('-')
                        self.f.write("\n")
            else:
                self.f.truncate(0)
                self.f.close()
                self.f = open(self.f.name, 'r+')
                self.f.write(str(self.map_size[0]) + " " + str(self.map_size[1]) + "\n")
                y = 0
                for row in self.terrain_map:
                    x = 0
                    for t in row:
                        if (x,y) in self.r_locs:
                            self.f.write('r')
                        elif (x,y) in self.b_locs:
                            self.f.write('b')
                        elif not t:
                            self.f.write('x')
                        else:
                            self.f.write('-')
                    self.f.write("\n")


        def clean_exit():
            if self.f is not None:
                self.f.close()
            self.root.quit()

        self.root = Tk("Replay Client")
        self.root.geometry(str(CLIENT_SIZE[0]) + "x" + str(CLIENT_SIZE[1]))
        self.root.bind("<Button-1>", self.left_click_handler)
        self.root.bind("<Button-3>", self.right_click_handler)
        self.root.protocol('WM_DELETE_WINDOW', clean_exit)
        menu = Menu(self.root)
        self.root.config(menu=menu)
        menu.add_command(label="New", command=new)
        menu.add_command(label="Open", command=open_map)
        menu.add_command(label="Save", command=save)
        self.canvas = Canvas(self.root, bg="black",height=CLIENT_SIZE[1],width=CLIENT_SIZE[0])
        self.canvas.create_rectangle(0,0,EDITOR_TAB_SIZE[0],EDITOR_TAB_SIZE[1], fill="gray")

        """
            - Add combobox or spinbox for symmetry
                * Horizontal
                * Vertical
                * Rotational
            - Add 2 Scales for controlling Map Size
                * Between MIN_MAP_SIZE and MAX_MAP_SIZE
            - Add combobox for changing what to add/delete
                * Walls (Terrain)
                * Starting Bots
                * Resources (Should also add a scale for controlling
                how much resource to add)

            Replace .pack with .place formatting
        """


        self.map_size = None
        self.terrain_map = None
        self.scale = None
        self.x_start = None
        self.y_start = None
        self.x_end = None
        self.y_end = None
        self.base = None
        self.map_name = None
        self.f = None
        self.r_locs = []
        self.b_locs = []
        self.terrain_graphics = []
        self.bot_graphics = []

    def get_real_coords(self,x,y):
        real_x = self.x_start + x*self.scale
        real_y = self.y_start + y*self.scale
        return real_x, real_y
    
    def get_map_coords(self,real_x,real_y):
        x = int((real_x - self.x_start) / self.scale)
        y = int((real_y - self.y_start) / self.scale)
        if x < 0 or x >= self.map_size[0] or y < 0 or y >= self.map_size[1]:
            return None, None
        return x,y

    def render(self):
        self.canvas.after(int(1000 / RENDER_FPS), self.render)
        if self.map_size is None:
            return
        for t in self.terrain_graphics:
            self.canvas.delete(t)
        self.terrain_graphics = []

        for b in self.bot_graphics:
            self.canvas.delete(b)
        self.bot_graphics = []

        y = 0
        for row in self.terrain_map:
            x = 0
            for t in row:
                if not t:
                    real_x,real_y = self.get_real_coords(x,y)
                    square = self.canvas.create_rectangle(real_x, real_y, real_x+self.scale,real_y+self.scale,fill='green')
                    self.terrain_graphics.append(square)
                x += 1
            y += 1
        for rx,ry in self.r_locs:
            real_x,real_y = self.get_real_coords(rx,ry)
            square = self.canvas.create_rectangle(real_x, real_y, real_x+self.scale,real_y+self.scale,fill='red')
            self.bot_graphics.append(square)
        for bx,by in self.b_locs:
            real_x,real_y = self.get_real_coords(bx,by)
            square = self.canvas.create_rectangle(real_x, real_y, real_x+self.scale,real_y+self.scale,fill='blue')
            self.bot_graphics.append(square)

    def left_click_handler(self, event):
        if self.map_size is None:
            return
        x,y = self.get_map_coords(event.x, event.y)
        if x is None or y is None:
            return
        if self.terrain_map[y][x]:
            self.terrain_map[y][x] = False
    
    def right_click_handler(self, event):
        if self.map_size is None:
            return
        x,y = self.get_map_coords(event.x, event.y)
        if x is None or y is None:
            return
        if not self.terrain_map[y][x]:
            self.terrain_map[y][x] = True

    def run(self):
        self.render()
        mainloop()

mc = MapCreator()
mc.run()