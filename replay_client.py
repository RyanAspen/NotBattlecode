from tkinter import *
from tkinter.filedialog import askopenfile
import numpy as np

CLIENT_SIZE = (600,800)
EDITOR_TAB_SIZE = (600,200)
RENDER_FPS = 128
MAX_RPS = 2**7

class ReplayClient:
    def __init__(self):
        def load():
            # Open a file in replays
            f = askopenfile(mode = 'r', filetypes=[('Replay Files', '*txt')])
            if f is not None:
                lines = f.readlines()
                self.map_size = tuple(map(int,lines[0].split(',')))
                self.terrain_map = np.array([bit == '1' for bit in lines[1][:-1]]).reshape(self.map_size)

                # From here, we swap between resource list and a list of bot info
                self.resources = {}
                self.bots = {}
                i = 2
                r = 1
                n = len(lines)
                while i < n:
                    # Read resource list
                    resource_map_round = np.array(list(map(int, lines[i].split(',')[:-1]))).reshape(self.map_size)
                    self.resources[r] = resource_map_round
                    i += 1
                    num_bots = int(lines[i])
                    i += 1

                    bot_round = []
                    for j in range(num_bots):
                        # Read 
                        bot_s = lines[i+j].strip().split(",")
                        bot_info = int(bot_s[0]), int(bot_s[1]), int(bot_s[2]), bot_s[3], int(bot_s[4]), True if bot_s[5] == "True" else False
                        bot_round.append(bot_info)

                    self.bots[r] = bot_round
                    i += num_bots
                    
                    r += 1
                self.total_rounds = r - 1

                """
                Draw map here.
                
                Find the map axis that is larger relative to the client.
                Scale that axis up so that it fills the full client, and
                scale the other axis by the same amount.

                """
                self.round = 1
                self.rounds_per_second = 0
                x_scale = self.map_size[1] / (CLIENT_SIZE[1] - EDITOR_TAB_SIZE[1])
                y_scale = self.map_size[0] / CLIENT_SIZE[0]
                self.scale = 1/max(x_scale, y_scale)
                self.x_start = (CLIENT_SIZE[1] - EDITOR_TAB_SIZE[1] - (self.map_size[1]*self.scale)) / 2
                self.y_start = (CLIENT_SIZE[0] - (self.map_size[0]*self.scale)) / 2
                self.x_end = self.x_start + self.map_size[1]*self.scale
                self.y_end = self.y_start + self.map_size[0]*self.scale
                self.base = self.canvas.create_rectangle(self.x_start, self.y_start, self.x_end, self.y_end, fill='white')
                self.resource_graphics = []
                self.bot_graphics = []

                """
                Now, draw terrain, since that doesn't change with round
                """
                y = 0
                for row in self.terrain_map:
                    x = 0
                    for t in row:
                        if not t:
                            real_x,real_y = self.get_real_coords(x,y)
                            self.canvas.create_rectangle(real_x, real_y, real_x+self.scale,real_y+self.scale,fill='green')
                        x += 1
                    y += 1
                self.canvas.pack()

        def play_pause():
            self.paused = not self.paused

        def restart():
            # Go to round 1 and pause
            self.round = 1
            self.paused = True

        def step_forward():
            # Pause, then step forward 1 round
            if self.round < self.total_rounds:
                self.round += 1
            self.paused = True

        def step_backward():
            # Pause, then step backward 1 round
            if self.round > 1:
                self.round -= 1
            self.paused = True
        
        def speed_up():
            if abs(self.rps) < MAX_RPS:
                self.rps *= 2
                self.rps_string.set("x" + str(self.rps))
                
        
        def slow_down():
            if abs(self.rps) > 1:
                self.rps = int(self.rps/2)
                self.rps_string.set("x" + str(self.rps))
        
        self.root = Tk("Replay Client")
        self.root.geometry(str(CLIENT_SIZE[1]) + "x" + str(CLIENT_SIZE[0]))
        menu = Menu(self.root)
        self.root.config(menu=menu)
        menu.add_command(label="Load", command=load)
        menu.add_command(label="Restart", command=restart)

        self.round = 0
        self.prev_round = 0
        self.total_rounds = 0
        self.paused = True
        self.resources = {}
        self.bots = {}
        self.map_size = None
        self.terrain_map = None
        self.canvas = Canvas(self.root, bg="black",height=CLIENT_SIZE[0],width=CLIENT_SIZE[1]-EDITOR_TAB_SIZE[1])
        self.canvas.pack(fill='both',side='right')

        self.tab = Frame(self.root, width=EDITOR_TAB_SIZE[1], height=EDITOR_TAB_SIZE[0], bg='gray')
        self.tab.pack(fill='both',side='left')

        self.play_pause_button = Button(self.tab, text="Play/Pause", command=play_pause)
        self.play_pause_button.pack()

        self.speed_up_button = Button(self.tab,text="Speed Up", command=speed_up)
        self.speed_up_button.pack()

        self.slow_down_button = Button(self.tab, text="Slow Down", command=slow_down)
        self.slow_down_button.pack()

        self.rps = 1
        self.rps_string = StringVar()
        self.rps_string.set("x1")

        self.speed_label = Label(self.tab, textvariable=self.rps_string)
        self.speed_label.pack()

        self.step_forward_button = Button(self.tab,text="Step Forward",command=step_forward)
        self.step_forward_button.pack()

        self.step_backward_button = Button(self.tab,text="Step Backward",command=step_backward)
        self.step_backward_button.pack()

        self.scale = None
        self.x_start = None
        self.y_start = None
        self.x_end = None
        self.y_end = None
        self.base = None
        self.resource_graphics = []
        self.bot_graphics = []        

    def get_real_coords(self,x,y):
        real_x = self.x_start + x*self.scale
        real_y = self.y_start + y*self.scale
        return real_x, real_y

    def progress_round(self):
        if self.map_size is None:
            self.canvas.after(10, self.progress_round)
            return
        if not self.paused and self.rps > 0:
            if self.round < self.total_rounds:
                self.round += 1
            self.canvas.after(int(1000 / self.rps), self.progress_round)
        elif not self.paused and self.rps < 0:
            if self.round > 1:
                self.round -= 1
            self.canvas.after(int(1000 / -self.rps), self.progress_round)
        else:
            self.canvas.after(1, self.progress_round)

    def render(self):
        self.canvas.after(int(1000 / RENDER_FPS), self.render)
        if self.map_size is None:
            return
        if self.round == self.prev_round:
            return
        self.prev_round = self.round
        for g in self.resource_graphics:
            self.canvas.delete(g)
        self.resource_graphics = []
        

        """
        A tile with resources is marked with a yellow circle. For now,
        the amount of resources is irrelevant so long as it is nonzero.
        """
        resources = self.resources[self.round]
        y = 0
        for row in resources:
            x = 0
            for r in row:
                if r > 0:
                    real_x,real_y = self.get_real_coords(x,y)
                    circle = self.canvas.create_oval(real_x, real_y, real_x+self.scale,real_y+self.scale,fill='yellow')
                    self.resource_graphics.append(circle)
                x += 1
            y += 1
        

        """
        A tile with a bot is marked with a square of the bot's team color.
        Will add more later.
        """
        for g in self.bot_graphics:
            self.canvas.delete(g)
        self.bot_graphics = []
        bots = self.bots[self.round]
        for bot in bots:
            x,y = bot[1], bot[2]
            team = bot[5]
            real_x,real_y = self.get_real_coords(x,y)
            if team:
                square = self.canvas.create_rectangle(real_x, real_y, real_x+self.scale,real_y+self.scale,fill='red')
            else:
                square = self.canvas.create_rectangle(real_x, real_y, real_x+self.scale,real_y+self.scale,fill='blue')
            self.bot_graphics.append(square)

    def run(self):
        self.render()
        self.progress_round()
        mainloop()

rc = ReplayClient()
rc.run()