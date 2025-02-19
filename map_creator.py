from tkinter import *
from tkinter.ttk import Combobox
from tkinter.filedialog import askopenfile, asksaveasfile
import numpy as np

CLIENT_SIZE = (600,800)
EDITOR_TAB_SIZE = (600,200)
DEFAULT_MAP_SIZE = (20,20)
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
            x_scale = self.map_size[1] / (CLIENT_SIZE[1] - EDITOR_TAB_SIZE[1])
            y_scale = self.map_size[0] / CLIENT_SIZE[0]
            self.scale = 1/max(x_scale, y_scale)
            self.x_start = (CLIENT_SIZE[1] - EDITOR_TAB_SIZE[1] - (self.map_size[1]*self.scale)) / 2
            self.y_start = (CLIENT_SIZE[0] - (self.map_size[0]*self.scale)) / 2
            self.x_end = self.x_start + self.map_size[0]*self.scale
            self.y_end = self.y_start + self.map_size[1]*self.scale
            if self.base is not None:
                self.canvas.delete(self.base)
            self.base = self.canvas.create_rectangle(self.x_start, self.y_start, self.x_end, self.y_end, fill='white')
            self.terrain_map = np.ones(self.map_size, dtype=bool)
            self.resource_map = np.zeros(self.map_size, dtype=int)
            self.r_locs = []
            self.b_locs = []
            for g in self.terrain_graphics.values():
                self.canvas.delete(g)
            self.terrain_graphics = {}
            for g in self.resource_graphics.values():
                self.canvas.delete(g)
            self.resource_graphics = {}
            for g in self.bot_graphics.values():
                self.canvas.delete(g)
            self.bot_graphics = {}
            
            self.canvas.pack()

        def open_map():
            if self.f is not None:
                save()
                self.f.close()
                self.f = None

            self.f = askopenfile(mode = 'r+', filetypes=[('Map Files', '*txt')])
            if self.f is not None:
                lines = self.f.readlines()
                if lines[2].strip() not in ('HORIZONTAL', 'VERTICAL', 'ROTATIONAL'):
                    print("Invalid Symmetry = ", lines[1])
                    return
                self.map_name = lines[0]
                self.map_size = tuple(map(int,lines[1].split()))
                self.symmetry_combobox.set(lines[2].strip())
                self.horizontal_size_scale.set(self.map_size[1])
                self.vertical_size_scale.set(self.map_size[0])
                self.terrain_map = np.ones(self.map_size, dtype=bool)
                self.resource_map = np.zeros(self.map_size, dtype=int)
                for y in range(self.map_size[0]):
                    line = lines[3+y]
                    x = 0
                    for t in line.split(',')[:-1]:
                        if t == 'x':
                            self.terrain_map[y][x] = False
                        x += 1
                for y in range(self.map_size[0]):
                    line = lines[self.map_size[0]+3+y]
                    x = 0
                    for r in line.split(',')[:-1]:
                        self.resource_map[y][x] = int(r)
                        x += 1
                self.r_locs = []
                self.b_locs = []
                for line in lines[self.map_size[0]*2+3:]:
                    x,y = tuple(map(int,line.split()))
                    self.r_locs.append((x,y))
                    if self.symmetry_string_var.get() == "ROTATIONAL":
                        self.b_locs.append((self.map_size[1]-x-1,self.map_size[0]-y-1))
                    elif self.symmetry_string_var.get() == "VERTICAL":
                        self.b_locs.append((x,self.map_size[0]-y-1))
                    else:
                        self.b_locs.append((self.map_size[1]-x-1,y))
                

                
                
                
                x_scale = self.map_size[1] / (CLIENT_SIZE[1] - EDITOR_TAB_SIZE[1])
                y_scale = self.map_size[0] / CLIENT_SIZE[0]
                self.scale = 1/max(x_scale, y_scale)
                self.x_start = (CLIENT_SIZE[1] - EDITOR_TAB_SIZE[1] - (self.map_size[1]*self.scale)) / 2
                self.y_start = (CLIENT_SIZE[0] - (self.map_size[0]*self.scale)) / 2
                self.x_end = self.x_start + self.map_size[1]*self.scale
                self.y_end = self.y_start + self.map_size[0]*self.scale
                if self.base is not None:
                    self.canvas.delete(self.base)
                self.base = self.canvas.create_rectangle(self.x_start, self.y_start, self.x_end, self.y_end, fill='white')

                for g in self.terrain_graphics.values():
                    self.canvas.delete(g)
                self.terrain_graphics = {}
                for g in self.resource_graphics.values():
                    self.canvas.delete(g)
                self.resource_graphics = {}
                for g in self.bot_graphics.values():
                    self.canvas.delete(g)
                self.bot_graphics = {}

                y = 0
                for row in self.terrain_map:
                    x = 0
                    for t in row:
                        if not t:
                            real_x,real_y = self.get_real_coords(x,y)
                            self.terrain_graphics[self.get_index_for_tuple(x,y)] = self.canvas.create_rectangle(real_x, real_y, real_x+self.scale,real_y+self.scale,fill='green')
                        x += 1
                    y += 1

                y = 0
                for row in self.resource_map:
                    x = 0
                    for r in row:
                        if r > 0:
                            real_x,real_y = self.get_real_coords(x,y)
                            self.resource_graphics[self.get_index_for_tuple(x,y)] = self.canvas.create_oval(real_x, real_y, real_x+self.scale,real_y+self.scale,fill='yellow')
                        x  += 1
                    y += 1

                for x,y in self.r_locs:
                    real_x,real_y = self.get_real_coords(x,y)
                    self.bot_graphics[self.get_index_for_tuple(x,y)] = self.canvas.create_rectangle(real_x, real_y, real_x+self.scale,real_y+self.scale,fill='red')
                for x,y in self.b_locs:
                    real_x,real_y = self.get_real_coords(x,y)
                    self.bot_graphics[self.get_index_for_tuple(x,y)] = self.canvas.create_rectangle(real_x, real_y, real_x+self.scale,real_y+self.scale,fill='blue')

                

                self.canvas.pack()

        def save():
            if self.f is None:
                self.f = asksaveasfile(mode = 'w', filetypes=[('Map Files', '*txt')])
                if self.f is not None:
                    self.f.write(self.f.name + "\n")
                    self.f.write(self.symmetry_string_var.get() + "\n")
                    self.f.write(str(self.map_size[0]) + " " + str(self.map_size[1]) + "\n")
                    for row in self.terrain_map:
                        for t in row:
                            if not t:
                                self.f.write("x,")
                            else:
                                self.f.write(" ,")
                        self.f.write("\n")
                    for row in self.resource_map:
                        for r in row:
                            self.f.write(str(r) + ",")
                        self.f.write("\n")
                    for x,y in self.r_locs:
                        self.f.write(str(x) + " " + str(y) + "\n")
                    

            else:
                self.f.truncate(0)
                self.f.close()
                self.f = open(self.f.name, 'r+')
                self.f.write(self.f.name + "\n")
                self.f.write(str(self.map_size[0]) + " " + str(self.map_size[1]) + "\n")
                self.f.write(self.symmetry_string_var.get() + "\n")
                for row in self.terrain_map:
                    for t in row:
                        if not t:
                            self.f.write("x,")
                        else:
                            self.f.write(" ,")
                    self.f.write("\n")
                for row in self.resource_map:
                    for r in row:
                        self.f.write(str(r) + ",")
                    self.f.write("\n")
                for x,y in self.r_locs:
                    self.f.write(str(x) + " " + str(y) + "\n")


        def clean_exit():
            if self.f is not None:
                self.f.close()
            self.root.quit()        

        self.root = Tk("Replay Client")
        self.root.geometry(str(CLIENT_SIZE[1]) + "x" + str(CLIENT_SIZE[0]))
        
        self.root.protocol('WM_DELETE_WINDOW', clean_exit)
        menu = Menu(self.root)
        self.root.config(menu=menu)
        menu.add_command(label="New", command=new)
        menu.add_command(label="Open", command=open_map)
        menu.add_command(label="Save", command=save)

        #TODO: Make the canvas take up space that the editor tab does not take
        self.canvas = Canvas(self.root, bg="black",height=CLIENT_SIZE[0],width=CLIENT_SIZE[1]-EDITOR_TAB_SIZE[1])
        self.canvas.pack(fill='both',side='right')
        self.canvas.bind("<Button-1>", self.left_click_handler)
        self.canvas.bind("<Button-3>", self.right_click_handler)

        #TODO: Maybe remove this entirely
        #self.editor_tab = self.canvas.create_rectangle(0,0,EDITOR_TAB_SIZE[1],EDITOR_TAB_SIZE[0], fill="gray")
        self.editor_tab = Frame(self.root, width=EDITOR_TAB_SIZE[1], height=EDITOR_TAB_SIZE[0], bg='gray')
        self.editor_tab.pack(fill='both',side='left')

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

        self.symmetry_string_var = StringVar()
        self.symmetry_combobox = Combobox(self.editor_tab, width = 20, textvariable=self.symmetry_string_var)
        self.symmetry_combobox['values'] = ('HORIZONTAL', 'VERTICAL', 'ROTATIONAL')
        self.symmetry_combobox.current(2)
        self.symmetry_combobox.pack()
        self.symmetry_combobox.bind("<<ComboboxSelected>>", self.clear)
        
        self.symmetry_label = Label(self.editor_tab, text = "Symmetry")
        self.symmetry_label.pack()

        self.edit_string_var = StringVar()
        self.edit_combobox = Combobox(self.editor_tab, width = 20, textvariable=self.edit_string_var)
        self.edit_combobox['values'] = ('WALLS', 'BOTS', 'RESOURCES')
        self.edit_combobox.current(0)
        self.edit_combobox.pack()

        self.edit_label = Label(self.editor_tab, text = "Attribute to Edit")
        self.edit_label.pack()

        self.team_var = BooleanVar(value=True)
        self.team_checkbox = Checkbutton(self.editor_tab, text="Red?", variable=self.team_var)
        self.team_checkbox.pack()

        self.resource_var = IntVar(value=1)
        self.resource_scale = Scale(self.editor_tab, variable=self.resource_var, from_=1, to=100)
        self.resource_scale.pack()

        self.horizontal_size_var = IntVar(value=DEFAULT_MAP_SIZE[1])
        self.horizontal_size_scale = Scale(self.editor_tab, variable=self.horizontal_size_var, from_ = MIN_MAP_SIZE[1], to = MAX_MAP_SIZE[1])
        self.horizontal_size_scale.pack()
        self.horizontal_size_scale.bind("<ButtonRelease-1>", self.resize)

        self.vertical_size_var = IntVar(value=DEFAULT_MAP_SIZE[0])
        self.vertical_size_scale = Scale(self.editor_tab, variable=self.vertical_size_var, from_ = MIN_MAP_SIZE[0], to= MAX_MAP_SIZE[0])
        self.vertical_size_scale.pack()
        self.vertical_size_scale.bind("<ButtonRelease-1>", self.resize)

        self.map_size_label = Label(self.editor_tab, text="Map Size")
        self.map_size_label.pack()

        self.canvas.pack() 





        self.map_size = None
        self.terrain_map = None
        self.resource_map = None
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
        self.terrain_graphics = {}
        self.resource_graphics = {}
        self.bot_graphics = {}

    def clear(self,event):
        if self.base is not None:
            self.canvas.delete(self.base)
        self.base = self.canvas.create_rectangle(self.x_start, self.y_start, self.x_end, self.y_end, fill='white')
        self.terrain_map = np.ones(self.map_size, dtype=bool)
        self.resource_map = np.zeros(self.map_size, dtype=int)
        self.r_locs = []
        self.b_locs = []
        for g in self.terrain_graphics.values():
            self.canvas.delete(g)
        self.terrain_graphics = {}
        for g in self.resource_graphics.values():
            self.canvas.delete(g)
        self.resource_graphics = {}
        for g in self.bot_graphics.values():
            self.canvas.delete(g)
        self.bot_graphics = {}

    def resize(self,event):
        if self.map_size[1] == self.horizontal_size_var.get() and self.map_size[0] == self.vertical_size_var.get():
            return
        self.map_size = (self.horizontal_size_var.get(), self.vertical_size_var.get())
        x_scale = self.map_size[1] / (CLIENT_SIZE[1] - EDITOR_TAB_SIZE[1])
        y_scale = self.map_size[0] / CLIENT_SIZE[0]
        self.scale = 1/max(x_scale, y_scale)
        self.x_start = (CLIENT_SIZE[1] - EDITOR_TAB_SIZE[1] - (self.map_size[1]*self.scale)) / 2
        self.y_start = (CLIENT_SIZE[0] - (self.map_size[0]*self.scale)) / 2
        self.x_end = self.x_start + self.map_size[1]*self.scale
        self.y_end = self.y_start + self.map_size[0]*self.scale
        self.clear(event)

    def get_real_coords(self,x,y):
        real_x = self.x_start + x*self.scale
        real_y = self.y_start + y*self.scale
        return real_x, real_y
    
    def get_map_coords(self,real_x,real_y):
        x = int((real_x - self.x_start) / self.scale)
        y = int((real_y - self.y_start) / self.scale)
        if x < 0 or x >= self.map_size[1] or y < 0 or y >= self.map_size[0]:
            return None, None
        return x,y
    
    def get_index_for_tuple(self,x,y):
        return self.map_size[1]*y + x

    def get_symmetric_pos(self,x,y):
        if self.symmetry_string_var.get() == "ROTATIONAL":
            return self.map_size[1]-1-x, self.map_size[0]-1-y
        elif self.symmetry_string_var.get() == "VERTICAL":
            return x, self.map_size[0]-1-y
        return self.map_size[1]-1-x,y

    def left_click_handler(self, event):
        if self.map_size is None:
            return
        x,y = self.get_map_coords(event.x, event.y)
        if x is None or y is None:
            return
        x2,y2 = self.get_symmetric_pos(x,y)
        i1 = self.get_index_for_tuple(x,y)
        i2 = self.get_index_for_tuple(x2,y2)
        if self.edit_string_var.get() == "WALLS":
            self.terrain_map[y][x] = False
            if i1 not in self.terrain_graphics:
                real_x,real_y = self.get_real_coords(x,y)
                self.terrain_graphics[i1] = self.canvas.create_rectangle(real_x, real_y, real_x+self.scale,real_y+self.scale,fill='green')
            self.terrain_map[y2][x2] = False
            if i2 not in self.terrain_graphics:
                real_x,real_y = self.get_real_coords(x2,y2)
                self.terrain_graphics[i2] = self.canvas.create_rectangle(real_x, real_y, real_x+self.scale,real_y+self.scale,fill='green')
        elif self.edit_string_var.get() == "BOTS":
            if self.team_var.get():
                if (x,y) not in self.r_locs and (x,y) not in self.b_locs:
                    self.r_locs.append((x,y))
                    if i1 not in self.bot_graphics:
                        real_x, real_y = self.get_real_coords(x,y)
                        self.bot_graphics[i1] = self.canvas.create_rectangle(real_x, real_y, real_x+self.scale,real_y+self.scale,fill='red')
                    self.b_locs.append((x2,y2))
                    if i2 not in self.bot_graphics:
                        real_x, real_y = self.get_real_coords(x2,y2)
                        self.bot_graphics[i2] = self.canvas.create_rectangle(real_x, real_y, real_x+self.scale,real_y+self.scale,fill='blue')
            else:
                if (x,y) not in self.r_locs and (x,y) not in self.b_locs:
                    self.b_locs.append((x,y))
                    if i1 not in self.bot_graphics:
                        real_x, real_y = self.get_real_coords(x,y)
                        self.bot_graphics[i1] = self.canvas.create_rectangle(real_x, real_y, real_x+self.scale,real_y+self.scale,fill='blue')
                    self.r_locs.append((x2,y2))
                    if i2 not in self.bot_graphics:
                        real_x, real_y = self.get_real_coords(x2,y2)
                        self.bot_graphics[i2] = self.canvas.create_rectangle(real_x, real_y, real_x+self.scale,real_y+self.scale,fill='red')
        else:
            r = self.resource_var.get()
            self.resource_map[y][x] = r
            if not i1 in self.resource_graphics:
                real_x,real_y = self.get_real_coords(x,y)
                self.resource_graphics[i1] = self.canvas.create_oval(real_x, real_y, real_x+self.scale,real_y+self.scale,fill='yellow')
            self.resource_map[y2][x2] = r
            if not i2 in self.resource_graphics:
                real_x,real_y = self.get_real_coords(x2,y2)
                self.resource_graphics[i2] = self.canvas.create_oval(real_x, real_y, real_x+self.scale,real_y+self.scale,fill='yellow')
            
    
    def right_click_handler(self, event):
        if self.map_size is None:
            return
        x,y = self.get_map_coords(event.x, event.y)
        if x is None or y is None:
            return
        x2,y2 = self.get_symmetric_pos(x,y)
        i1 = self.get_index_for_tuple(x,y)
        i2 = self.get_index_for_tuple(x2,y2)
        if self.edit_string_var.get() == "WALLS":
            self.terrain_map[y][x] = True
            if i1 in self.terrain_graphics:
                self.canvas.delete(self.terrain_graphics[i1])
                del self.terrain_graphics[i1]
            self.terrain_map[y2][x2] = True
            if i2 in self.terrain_graphics:
                self.canvas.delete(self.terrain_graphics[i2])
                del self.terrain_graphics[i2]
        elif self.edit_string_var.get() == "BOTS":
            if (x,y) in self.r_locs or (x,y) in self.b_locs:
                if (x,y) in self.r_locs:
                    self.r_locs.remove(i1)
                if (x,y) in self.b_locs:
                    self.b_locs.remove((x,y))
                if i1 in self.bot_graphics:
                    self.canvas.delete(self.bot_graphics[i1])
                    del self.bot_graphics[i1]
                if (x2,y2) in self.r_locs:
                    self.r_locs.remove((x2,y2))
                if (x2,y2) in self.b_locs:
                    self.b_locs.remove((x2,y2))
                if i2 in self.bot_graphics:
                    self.canvas.delete(self.bot_graphics[i2])
                    del self.bot_graphics[i2]
        else:
            self.resource_map[y][x] = 0
            if i1 in self.resource_graphics:
                self.canvas.delete(self.resource_graphics[i1])
                del self.resource_graphics[i1]
            self.resource_map[y2][x2] = 0
            if i2 in self.resource_graphics:
                self.canvas.delete(self.resource_graphics[i2])
                del self.resource_graphics[i2]
    

    def run(self):
        mainloop()

mc = MapCreator()
mc.run()