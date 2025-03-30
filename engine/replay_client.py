from tkinter import *
from tkinter.filedialog import askopenfile
import numpy as np

from utility import BotType

CLIENT_SIZE = (600,800)
EDITOR_TAB_SIZE = (600,200)
RENDER_FPS = 128
MAX_RPS = 2**7

class ReplayClient:
    def __init__(self):
        def load():
            # Open a file in replays
            f = askopenfile(mode = 'r', filetypes=[('Replay Files', '*rpy')])
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
                        bot_info = int(bot_s[0]), int(bot_s[1]), int(bot_s[2]), bot_s[3], int(bot_s[4]), True if bot_s[5] == "True" else False, int(bot_s[6]), int(bot_s[7]), int(bot_s[8]), bot_s[9]
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

                self.tile_info_display_x = None
                self.tile_info_display_y = None
                self.bot_info_display_id = None
                self.tile_to_highlight_x = None
                self.tile_to_highlight_y = None
                self.tile_info_frame.pack_forget()
                self.bot_info_frame.pack_forget()

        def play_pause():
            self.paused = not self.paused

        def restart():
            # Go to round 1 and pause
            self.round = 1
            self.paused = True
            self.round_string.set("Round " + str(self.round))

        def reverse():
            self.rps = -self.rps
            self.rps_string.set("x" + str(self.rps))
            self.paused = True

        def step_forward():
            # Pause, then step forward 1 round
            if self.round < self.total_rounds:
                self.round += 1
            self.paused = True
            self.round_string.set("Round " + str(self.round))

        def step_backward():
            # Pause, then step backward 1 round
            if self.round > 1:
                self.round -= 1
            self.paused = True
            self.round_string.set("Round " + str(self.round))
        
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

        self.reverse_button = Button(self.tab, text="Reverse", command=reverse)
        self.reverse_button.pack()

        self.rps = 1
        self.rps_string = StringVar()
        self.rps_string.set("x1")

        self.speed_label = Label(self.tab, textvariable=self.rps_string)
        self.speed_label.pack()

        self.step_forward_button = Button(self.tab,text="Step Forward",command=step_forward)
        self.step_forward_button.pack()

        self.step_backward_button = Button(self.tab,text="Step Backward",command=step_backward)
        self.step_backward_button.pack()

        self.round_string = StringVar()
        self.round_string.set("Round 1")
        self.round_label = Label(self.tab, textvariable=self.round_string)
        self.round_label.pack()

        
        # Bot info UI

        self.bot_info_display_id = None

        self.bot_info_frame = Frame(self.tab)
        self.bot_info_frame.pack_forget()

        self.bot_info_id = StringVar()
        self.bot_info_id_label = Label(self.bot_info_frame, textvariable=self.bot_info_id)
        self.bot_info_id_label.pack()

        self.bot_info_loc = StringVar()
        self.bot_info_loc_label = Label(self.bot_info_frame, textvariable=self.bot_info_loc)
        self.bot_info_loc_label.pack()

        self.bot_info_type = StringVar()
        self.bot_info_type_label = Label(self.bot_info_frame, textvariable=self.bot_info_type)
        self.bot_info_type_label.pack()

        self.bot_info_hp = StringVar()
        self.bot_info_hp_label = Label(self.bot_info_frame, textvariable=self.bot_info_hp)
        self.bot_info_hp_label.pack()

        self.bot_info_action_cooldown = StringVar()
        self.bot_info_action_cooldown_label = Label(self.bot_info_frame, textvariable=self.bot_info_action_cooldown)
        self.bot_info_action_cooldown_label.pack()

        self.bot_info_move_cooldown = StringVar()
        self.bot_info_move_cooldown_label = Label(self.bot_info_frame, textvariable=self.bot_info_move_cooldown)
        self.bot_info_move_cooldown_label.pack()

        self.bot_info_bytecode = StringVar()
        self.bot_info_bytecode_label = Label(self.bot_info_frame, textvariable=self.bot_info_bytecode)
        self.bot_info_bytecode_label.pack()

        self.bot_info_str = StringVar()
        self.bot_info_str_label = Label(self.bot_info_frame, textvariable=self.bot_info_str)
        self.bot_info_str_label.pack()



        # Tile info UI

        self.tile_info_display_x = None
        self.tile_info_display_y = None

        self.tile_info_frame = Frame(self.tab)
        self.tile_info_frame.pack_forget()

        self.tile_info_loc = StringVar()
        self.tile_info_loc_label = Label(self.tile_info_frame, textvariable=self.tile_info_loc)
        self.tile_info_loc_label.pack()

        self.tile_info_resources = StringVar()
        self.tile_info_resources_label = Label(self.tile_info_frame, textvariable=self.tile_info_resources)
        self.tile_info_resources_label.pack()

        self.tile_info_passable = StringVar()
        self.tile_info_passable_label = Label(self.tile_info_frame, textvariable=self.tile_info_passable)
        self.tile_info_passable_label.pack()

        self.canvas.bind("<Button-1>", self.left_click_handler)
        self.tile_to_highlight_x = None
        self.tile_to_highlight_y = None
        self.highlight = None



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
            self.round_string.set("Round " + str(self.round))
            self.canvas.after(int(1000 / self.rps), self.progress_round)
        elif not self.paused and self.rps < 0:
            if self.round > 1:
                self.round -= 1
            self.round_string.set("Round " + str(self.round))
            self.canvas.after(int(1000 / -self.rps), self.progress_round)
        else:
            self.canvas.after(1, self.progress_round)

    def get_map_coords(self,real_x,real_y):
        x = int((real_x - self.x_start) / self.scale)
        y = int((real_y - self.y_start) / self.scale)
        if x < 0 or x >= self.map_size[1] or y < 0 or y >= self.map_size[0]:
            return None, None
        return x,y

    def get_tile_info(self, x, y):
        resources = self.resources[self.round]
        return x,y,resources[y][x],self.terrain_map[y][x]

    def get_bot_info_for_id(self, id):
        bots = self.bots[self.round]
        for bot in bots:
            if bot[0] == id:
                return bot
        return None

    def get_bot_info_at_loc(self, x, y):
        bots = self.bots[self.round]
        for bot in bots:
            if bot[1] == x and bot[2] == y:
                return bot
        return None

    def update_info_display(self):
        if self.bot_info_display_id is not None:
            bot = self.get_bot_info_for_id(self.bot_info_display_id)
            if bot is None:
                self.bot_info_display_id = None
                self.bot_info_frame.pack_forget()
            else:
                self.tile_to_highlight_x = bot[1]
                self.tile_to_highlight_y = bot[2]
                self.bot_info_id.set("Bot ID = " + str(bot[0]))
                self.bot_info_loc.set("Location = (" + str(bot[1]) + ", " + str(bot[2]) + ")")
                self.bot_info_type.set("Type = " + bot[3])
                self.bot_info_hp.set("HP = " + str(bot[4]))
                self.bot_info_action_cooldown.set("Action Cooldown = " + str(bot[6]))
                self.bot_info_move_cooldown.set("Move Cooldown = " + str(bot[7]))
                self.bot_info_bytecode.set("Bytecode used = " + str(bot[8]))
                self.bot_info_str.set(bot[9])
        elif self.tile_info_display_x is not None and self.tile_info_display_y is not None:
            tile = self.get_tile_info(self.tile_info_display_x, self.tile_info_display_y)
            self.tile_to_highlight_x = tile[0]
            self.tile_to_highlight_y = tile[1]
            self.tile_info_loc.set("(" + str(tile[0]) + ", " + str(tile[1]) + ")")
            self.tile_info_resources.set("Resources = " + str(tile[2]))
            self.tile_info_passable.set("Is Passable? " + str(tile[3]))
        else:
            self.tile_to_highlight_x = None
            self.tile_to_highlight_y = None

    def left_click_handler(self, event):
        if self.map_size is None:
            return
        x,y = self.get_map_coords(event.x, event.y)
        if x is None or y is None:
            return
        bot = self.get_bot_info_at_loc(x,y)
        if self.tile_info_display_x is not None and self.tile_info_display_x == x and self.tile_info_display_y is not None and self.tile_info_display_y == y:
            # We are currently displaying tile info at (x,y) already. Instead, stop showing it
            self.tile_info_display_x = None
            self.tile_info_display_y = None
            self.tile_info_frame.pack_forget()
        elif self.bot_info_display_id is not None and bot is not None and bot[0] == self.bot_info_display_id:
            # We are currently displaying the bot's info already. Instead, stop showing it
            self.bot_info_display_id = None
            self.bot_info_frame.pack_forget()
        elif bot is not None:
            # Display info about bot
            self.bot_info_display_id = bot[0]
            self.tile_info_display_x = None
            self.tile_info_display_y = None
            self.bot_info_frame.pack()
            self.tile_info_frame.pack_forget()
        else:
            # Display info about tile
            self.tile_info_display_x = x
            self.tile_info_display_y = y
            self.bot_info_display_id = None
            self.tile_info_frame.pack()
            self.bot_info_frame.pack_forget()

    def render(self):
        self.update_info_display()
        self.canvas.after(int(1000 / RENDER_FPS), self.render)
        if self.map_size is None:
            return
        
        if self.highlight is not None:
            for g in self.highlight:
                self.canvas.delete(g)
        if self.tile_to_highlight_x is not None and self.tile_to_highlight_y is not None:
            h_x,h_y = self.get_real_coords(self.tile_to_highlight_x, self.tile_to_highlight_y)
            self.highlight = []
            self.highlight.append(self.canvas.create_line(h_x, h_y, h_x+self.scale, h_y, fill='orange',width=2))
            self.highlight.append(self.canvas.create_line(h_x, h_y+self.scale, h_x+self.scale, h_y+self.scale, fill='orange',width=2))
            self.highlight.append(self.canvas.create_line(h_x, h_y, h_x, h_y+self.scale, fill='orange',width=2))
            self.highlight.append(self.canvas.create_line(h_x+self.scale, h_y, h_x+self.scale, h_y+self.scale, fill='orange',width=2))

        if self.round == self.prev_round:
            return
        self.prev_round = self.round

        self.update_info_display()

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
            type = bot[3]
            # HP Fraction remaining = current / starting_hp
            s_hp = BotType(type).get_starting_hp()
            if type == "Base":
                size = int(self.scale * (bot[4] + s_hp)/(2*s_hp))
            else:
                size = int(0.5*self.scale * (bot[4] + s_hp)/(2*s_hp))
            team = bot[5]
            real_x,real_y = self.get_real_coords(x,y)
            r_start_x = real_x + (self.scale - size) / 2
            r_start_y = real_y + (self.scale - size) / 2
            b_g = None
            if type == "Base":
                if team:
                    b_g = self.canvas.create_rectangle(r_start_x, r_start_y, r_start_x+size,r_start_y+size,fill='red')
                else:
                    b_g = self.canvas.create_rectangle(r_start_x, r_start_y, r_start_x+size,r_start_y+size,fill='blue')
            elif type == "Basic":
                if team:
                    b_g = self.canvas.create_rectangle(r_start_x, r_start_y, r_start_x+size,r_start_y+size,fill='red')
                else:
                    b_g = self.canvas.create_rectangle(r_start_x, r_start_y, r_start_x+size,r_start_y+size,fill='blue')
            self.bot_graphics.append(b_g)

        

    def run(self):
        self.render()
        self.progress_round()
        mainloop()

rc = ReplayClient()
rc.run()