from time import sleep

from ammo import *
from bubble import Collision, create_bubble
from components import *
from extras import Logging, shuffling, refresh
from teleport import *
from special import ScrolledWindow

log = Logging("logs", True, True)

log.info("<Root>", "Imports loading success")
log.info("<Root>", "Starting Game")
#
#
# def handle_exception(exc_type, exc_value, exc_traceback):
#     if issubclass(exc_type, KeyboardInterrupt):
#         sys.__excepthook__(exc_type, exc_value, exc_traceback)
#         return
#
#     log.error("?", str(exc_type.__name__) + ": " + str(exc_value))
#
#
# sys.excepthook = handle_exception


def control(root, canvas, icon, config, event, stats, temp, modes, ship, commands, ammo, tp,
            texts, foregrounds, backgrounds, bubble):
    """
    Ship-motion event
    :param commands:
    :param bubble:
    :param backgrounds:
    :param foregrounds:
    :param texts:
    :param temp:
    :param tp:
    :param ammo:
    :param ship:
    :param modes:
    :param stats:
    :param config:
    :param icon:
    :param canvas:
    :param root:
    :param event:
    """

    if (not modes["teleport"]) and (not modes["store"]) and (not modes["window"]):
        if not modes["pause"]:
            if not stats["paralis"]:
                x, y = get_coords(canvas, ship["id2"])
                if stats["speedboost"]:
                    a = 10
                else:
                    a = 0
                if event.keysym == 'Up' or event.keysym.lower() == "w":
                    if y > 72 + config["game"]["ship-radius"]:
                        canvas.move(ship["id1"], 0, -stats["shipspeed"] - a)
                        canvas.move(ship["id2"], 0, -stats["shipspeed"] - a)
                        root.update()
                elif event.keysym == 'Down' or event.keysym.lower() == "s":
                    if y < config["height"] - 105 - config["game"]["ship-radius"]:
                        canvas.move(ship["id1"], 0, stats["shipspeed"] + a)
                        canvas.move(ship["id2"], 0, stats["shipspeed"] + a)
                        root.update()
                elif event.keysym == 'Left' or event.keysym.lower() == "a":
                    if x > 0 + config["game"]["ship-radius"]:
                        canvas.move(ship["id1"], -stats["shipspeed"] - a, 0)
                        canvas.move(ship["id2"], -stats["shipspeed"] - a, 0)
                        root.update()
                elif event.keysym == 'Right' or event.keysym.lower() == "d":
                    if x < config["width"] - config["game"]["ship-radius"]:
                        canvas.move(ship["id1"], stats["shipspeed"] + a, 0)
                        canvas.move(ship["id2"], stats["shipspeed"] + a, 0)
                        root.update()
                stats["ship-position"] = get_coords(canvas, ship["id1"])
                if event.keysym == "space":
                    create_shot(canvas, ammo, config, ship, stats)

                canvas.update()
                canvas.update_idletasks()
                root.update()
                root.update_idletasks()
    if modes["store"] and commands["store"] is not None:
        if event.keysym == "Up":
            commands["store"].set_selected(canvas, -1)
        if event.keysym == "Down":
            commands["store"].set_selected(canvas, 1)
        if event.keysym == "Left":
            commands["store"].set_selected(canvas, int(-((config["height"] - 215) / 140 + 1)))
        if event.keysym == "Right":
            commands["store"].set_selected(canvas, int((config["height"] - 215) / 140 + 1))
        if event.keysym == "space":
            commands["store"].buy_selected(config, modes, log, root, canvas, stats, bubble, backgrounds,
                                           texts,
                                           commands, temp)
        if event.keysym == "BackSpace":
            commands["store"].exit(canvas, log, modes, stats, temp, commands)
            commands["store"] = None
        if event.keysym == "Escape":
            sleep(1)
            commands["store"].exit(canvas, log, modes, stats, temp, commands)
            commands["store"] = None
    if modes["present"]:
        if event.keysym == "space":
            if False != commands["present"] != True:
                commands["present"].exit(canvas)
                modes["pause"] = False
                modes["present"] = False
                stats["scorestate-time"] = temp["scorestate-save"] + time()
                stats["secure-time"] = temp["secure-save"] + time()
                stats["timebreak-time"] = temp["timebreak-save"] + time()
                stats["confusion-time"] = temp["confusion-save"] + time()
                stats["slowmotion-time"] = temp["slowmotion-save"] + time()
                stats["paralis-time"] = temp["paralis-save"] + time()
                stats["shotspeed-time"] = temp["shotspeed-save"] + time()
                stats["notouch-time"] = temp["notouch-save"] + time()
    if modes["teleport"]:
        x, y = get_coords(canvas, tp["id1"])
        if event.keysym == 'Up':
            if y > 72 + 5:
                canvas.move(tp["id1"], 0, -5)
                canvas.move(tp["id2"], 0, -5)
                canvas.move(tp["id3"], 0, -5)
                canvas.move(tp["id4"], 0, -5)
        if event.keysym == "Down":
            if y < config["height"] - 105 - 5:
                canvas.move(tp["id1"], 0, 5)
                canvas.move(tp["id2"], 0, 5)
                canvas.move(tp["id3"], 0, 5)
                canvas.move(tp["id4"], 0, 5)
        if event.keysym == "Left":
            if x > 0 + 5:
                canvas.move(tp["id1"], -5, 0)
                canvas.move(tp["id2"], -5, 0)
                canvas.move(tp["id3"], -5, 0)
                canvas.move(tp["id4"], -5, 0)
        if event.keysym == "Right":
            if x < config["width"] - 5:
                canvas.move(tp["id1"], 5, 0)
                canvas.move(tp["id2"], 5, 0)
                canvas.move(tp["id3"], 5, 0)
                canvas.move(tp["id4"], 5, 0)
        if event.keysym == "BackSpace":
            modes["pause"] = False

            stats["scorestate-time"] = temp["scorestate-save"] + time()
            stats["secure-time"] = temp["secure-save"] + time()
            stats["timebreak-time"] = temp["timebreak-save"] + time()
            stats["confusion-time"] = temp["confusion-save"] + time()
            stats["slowmotion-time"] = temp["slowmotion-save"] + time()
            stats["paralis-time"] = temp["paralis-save"] + time()
            stats["shotspeed-time"] = temp["shotspeed-save"] + time()
            stats["notouch-time"] = temp["notouch-save"] + time()
        if event.keysym == "Escape":
            modes["pause"] = False

            stats["scorestate-time"] = temp["scorestate-save"] + time()
            stats["secure-time"] = temp["secure-save"] + time()
            stats["timebreak-time"] = temp["timebreak-save"] + time()
            stats["confusion-time"] = temp["confusion-save"] + time()
            stats["slowmotion-time"] = temp["slowmotion-save"] + time()
            stats["paralis-time"] = temp["paralis-save"] + time()
            stats["shotspeed-time"] = temp["shotspeed-save"] + time()
            stats["notouch-time"] = temp["notouch-save"] + time()
            sleep(1)
        if event.keysym == "Return":
            modes["pause"] = False

            stats["scorestate-time"] = temp["scorestate-save"] + time()
            stats["secure-time"] = temp["secure-save"] + time()
            stats["timebreak-time"] = temp["timebreak-save"] + time()
            stats["confusion-time"] = temp["confusion-save"] + time()
            stats["slowmotion-time"] = temp["slowmotion-save"] + time()
            stats["paralis-time"] = temp["paralis-save"] + time()
            stats["shotspeed-time"] = temp["shotspeed-save"] + time()
            stats["notouch-time"] = temp["notouch-save"] + time()

            stats["teleports"] -= 1
            teleport(canvas, root, stats, modes, ship, tp, tp["id1"])
        if event.keysym.lower() == "space":
            modes["pause"] = False

            stats["scorestate-time"] = temp["scorestate-save"] + time()
            stats["secure-time"] = temp["secure-save"] + time()
            stats["timebreak-time"] = temp["timebreak-save"] + time()
            stats["confusion-time"] = temp["confusion-save"] + time()
            stats["slowmotion-time"] = temp["slowmotion-save"] + time()
            stats["paralis-time"] = temp["paralis-save"] + time()
            stats["shotspeed-time"] = temp["shotspeed-save"] + time()
            stats["notouch-time"] = temp["notouch-save"] + time()

            stats["teleports"] -= 1
            teleport(canvas, root, stats, modes, ship, tp, tp["id1"])
    if event.keysym == "Shift_L" and (not modes["pause"]):
        modes["pause"] = True

        canvas.delete(icon["pause"])
        icon["pause"] = canvas.create_image(config["middle-x"], config["middle-y"], image=icon["pause-id"])

        canvas.itemconfig(texts["pause"], text="")
        root.update()

        temp["scorestate-save"] = stats["scorestate-time"] - time()
        temp["secure-save"] = stats["secure-time"] - time()
        temp["timebreak-save"] = stats["timebreak-time"] - time()
        temp["confusion-save"] = stats["confusion-time"] - time()
        temp["slowmotion-save"] = stats["slowmotion-time"] - time()
        temp["paralis-save"] = stats["paralis-time"] - time()
        temp["shotspeed-save"] = stats["shotspeed-time"] - time()
        temp["notouch-save"] = stats["notouch-time"] - time()
        temp["special-level-save"] = stats["special-level-time"] - time()
    elif event.keysym == "Shift_R" and modes["pause"] and (not modes["store"]) and (not modes["teleport"]) and \
            (not modes["window"]) and (not modes["present"]) and not modes["cheater"]:
        modes["pause"] = False

        canvas.itemconfig(icon["pause"], state=HIDDEN)
        canvas.itemconfig(texts["pause"], text="")
        root.update()

        stats["scorestate-time"] = temp["scorestate-save"] + time()
        stats["secure-time"] = temp["secure-save"] + time()
        stats["timebreak-time"] = temp["timebreak-save"] + time()
        stats["confusion-time"] = temp["confusion-save"] + time()
        stats["slowmotion-time"] = temp["slowmotion-save"] + time()
        stats["paralis-time"] = temp["paralis-save"] + time()
        stats["shotspeed-time"] = temp["shotspeed-save"] + time()
        stats["notouch-time"] = temp["notouch-save"] + time()
    if event.keysym == "t" and stats["teleports"] > 0 and (not modes["teleport"]):
        modes["pause"] = True

        temp["scorestate-save"] = stats["scorestate-time"] - time()
        temp["secure-save"] = stats["secure-time"] - time()
        temp["timebreak-save"] = stats["timebreak-time"] - time()
        temp["confusion-save"] = stats["confusion-time"] - time()
        temp["slowmotion-save"] = stats["slowmotion-time"] - time()
        temp["paralis-save"] = stats["paralis-time"] - time()
        temp["shotspeed-save"] = stats["shotspeed-time"] - time()
        temp["notouch-save"] = stats["notouch-time"] - time()
        temp["special-level-save"] = stats["special-level-time"] - time()

        modes["teleport"] = True

        tp_mode(canvas, config, stats, modes, tp)
    if event.keysym.lower() == "e" and (not modes["store"]):
        modes["pause"] = True
        temp["scorestate-save"] = stats["scorestate-time"] - time()
        temp["secure-save"] = stats["secure-time"] - time()
        temp["timebreak-save"] = stats["timebreak-time"] - time()
        temp["confusion-save"] = stats["confusion-time"] - time()
        temp["slowmotion-save"] = stats["slowmotion-time"] - time()
        temp["paralis-save"] = stats["paralis-time"] - time()
        temp["shotspeed-save"] = stats["shotspeed-time"] - time()
        temp["notouch-save"] = stats["notouch-time"] - time()
        temp["special-level-save"] = stats["special-level-time"] - time()
        modes["store"] = True
        log.debug("bub_move", "Creating Store() to variable \"store\"")
        log.debug("bub_move", "storemode=" + str(modes["store"]))
        commands["store"] = Store(canvas, log, config, modes, stats, icon, foregrounds)
    # if event.char == "/":
    #     CheatEngine().event_handler(canvas, modes, stats, config, temp, log, backgrounds, bubble, event, bub)
    # if modes["cheater"]:
    #     CheatEngine().input_event_handler(canvas, log, stats, backgrounds, bubble, event, config, bub, temp,
    #                                       modes)

    if event.keysym == "Escape":
        pass
    root.update()


class Maintance:
    def __init__(self):
        pass

    @staticmethod
    def auto_save(save_name, game_stats, bubble):
        """
        Saves the game. (For Auto-Save)
        """
        import config as cfg
        cfg.Writer("saves/" + save_name + "/game.json", game_stats.copy())
        cfg.Writer("saves/" + save_name + "/bubble.json", bubble.copy())

    @staticmethod
    def auto_restore(save_name):
        """
        Restoring. (For Auto-Restore)
        """
        import config as cfg
        game_stats = cfg.Reader("saves/" + save_name + "/game.json").get_decoded()

        return game_stats

    @staticmethod
    def reset(save_name):
        """
        Resets the game fully
        """

        import config as cfg
        stats = cfg.Reader("config/reset.json").get_decoded()
        bubble = cfg.Reader("config/reset-bubble.json").get_decoded()

        cfg.Writer("saves/" + save_name + "/game.json", stats.copy())
        cfg.Writer("saves/" + save_name + "/bubble.json", bubble.copy())


def start(bubble, save_name, stats, config, bub, modes, canvas):
    bubs = Reader("saves/" + save_name + "/bubble.json").get_decoded()
    for i in range(len(bubs["bub-id"])):
        if bubs["bub-special"]:
            create_bubble(stats, config, bub, canvas, bubble, modes, i, bubs["bub-index"][i], bubs["bub-position"][i][0],
                          bubs["bub-position"][i][1], bubs["bub-radius"][i], bubs["bub-speed"][i])
        elif not bubs["bub-special"]:
            SpecialMode.create_bubble(canvas, config, bubble, stats, bub, modes, i, bubs["bub-index"][i],
                                      bubs["bub-position"][i][0],
                                      bubs["bub-position"][i][1], bubs["bub-radius"][i], bubs["bub-speed"][i])


def r_start(bubble, stats, config, bub, canvas, modes):
    for i in range(int((config["width"] - 105 - 72) / 10)):
        x = randint(0, config["width"])
        r = randint(int(config["bubble"]["min-radius"]),
                    int(config["bubble"]["max-radius"]))
        y = randint(72 + r, (config["height"] - 105 - r))
        # spd = stats["bubspeed"]
        # i = randint(0, 1600)
        create_bubble(stats, config, bub, canvas, bubble, modes, i, x=x, y=y, r=r)


class Game(Canvas):
    def __init__(self, start_time=0.0, already_opened=False):
        super().__init__()

        import config
        import os
        from tkinter import ttk
        self.log = log
        self.returnmain = False

        log.info("Game.__init__", "Started Game.")

        # print("Started Game")

        self.root = self.master
        self.time1 = start_time
        self.cfg = Maintance()
        self.save_name = "Lyfo"

        self.stats = dict()

        self.temp = dict()
        self.temp["scorestate-save"] = 0
        self.temp["secure-save"] = 0
        self.temp["timebreak-save"] = 0
        self.temp["confusion-save"] = 0
        self.temp["slowmotion-save"] = 0
        self.temp["paralis-save"] = 0
        self.temp["shotspeed-save"] = 0
        self.temp["notouch-save"] = 0
        self.temp["special-level-save"] = 0
        self.temp["found-bubble"] = False

        self.modes = dict()
        self.modes["pause"] = False
        self.modes["cheater"] = False
        self.modes["window"] = False
        self.modes["store"] = False
        self.modes["teleport"] = False
        self.modes["present"] = False

        # print("Phase 1")

        self.canvas = None

        self.icons = dict()
        self.texts = dict()

        self.back = dict()
        self.fore = dict()

        # print("Phase 2")

        self.commands = {"store": False, "present": False, "special-mode": False}

        self.ship = dict()
        self.tp = dict()

        self.config = config.Reader("config/startup.json").get_decoded()
        self.bub = dict()
        self.bub["normal"] = dict()
        self.bubbles = {"bub-id": list(), "bub-special": list(), "bub-action": list(), "bub-radius": list(),
                        "bub-speed": list(),
                        "bub-position": list(), "bub-hardness": list(), "bub-index": list(), "key-active": False}

        self.ammo = {"ammo-id": list(), "ammo-radius": 5, "ammo-speed": list(), "ammo-position": list(),
                     "ammo-damage": list(), "retime": start_time}

        # print("Phase 3")

        if self.config["game"]["fullscreen"]:
            self.root.wm_attributes("-fullscreen", True)

        self.root.update()
        res = self.config["game"]["resolution"]
        l_res = res.split("x")

        self.config["width"] = self.root.winfo_width()  # int(l_res[0])
        self.config["height"] = self.root.winfo_height()  # int(l_res[1])

        self.config["middle-x"] = self.config["width"] / 2
        self.config["middle-y"] = self.config["height"] / 2

        self.Coll = Collision()

        # self.game()

        # print("Phase 4")

        width = 16
        height = 34

        path = "saves/"
        index = os.listdir(path)
        dirs = []

        for item in index:
            file_path = path + item

            if os.path.isdir(file_path):
                dirs.append(item)

        y = -1
        x = 0
        p = 0
        i = 0

        # print("Phase 5")

        if not already_opened:
            self.close = Button(self.root, text="X", fg="white", relief=FLAT, bg="#ff0000",
                                command=lambda: self.root.destroy())
            self.close.pack(side=TOP, fill=X)

        # self.frames = []
        # self.item_info = [[[[]]]]
        self.items = list()

        # print("Phase 6")

        # self.frames.append(Frame(self.tabs, bd=1, bg="#3c3c3c"))
        # items2 = []
        # while i < len(dirs):
        #     y += 1
        #     self.item_info[p][0][x].append(dirs[i])
        #     if y >= height:
        #         y = 0
        #         self.item_info[p][0].append([])
        #         self.item_info[p][0].append([])
        #         self.item_info[p][0].append([])
        #         self.item_info[p][0].append([])
        #         x += 4
        #     if x > width:
        #         self.tabs.add(self.frames.copy()[-1], text=' {} '.format(p))
        #         self.frames.append(Frame(self.tabs, bd=1, bg="#3c3c3c"))
        #         y = 0
        #         x = 0
        #         self.item_info.append([[[]]])
        #         p += 1
        #     items2.append(dirs[i])
        #
        #     self.items.append(Button(self.frames[-1], width=30, relief=FLAT, text=dirs[i], bg="#707070"))
        #     self.items.copy()[-1].grid(column=x, row=y, padx=2, pady=2)
        #     self.items.copy()[-1].bind("<ButtonRelease-1>", self.open)
        #
        #     self.items.append(Button(self.frames[-1], relief=FLAT, text="rename", bg="#707070"))
        #     self.items.copy()[-1].grid(column=x + 1, row=y, padx=2, pady=2)
        #     self.items.copy()[-1].bind("<ButtonRelease-1>", self.rename)
        #
        #     self.items.append(Button(self.frames[-1], relief=FLAT, text="remove", bg="#707070"))
        #     self.items.copy()[-1].grid(column=x + 2, row=y, padx=2, pady=2)
        #     self.items.copy()[-1].bind("<ButtonRelease-1>", self.remove)
        #
        #     self.items.append(Button(self.frames[-1], relief=FLAT, text="", width=5, bg="#3c3c3c"))
        #     self.items.copy()[-1].grid(column=x + 3, row=y, padx=2, pady=2)
        #
        #     self.max_pages = p
        #     i += 1

        self.frame2 = Frame(bg="#5c5c5c")

        self.add = Button(self.frame2, text="Add Save", relief=FLAT, bg="#7f7f7f", fg="white", command=self.add_save)
        self.add.pack(side=RIGHT, padx=2, pady=5)
        self.add_input = Entry(self.frame2, bd=5, fg="#3c3c3c", bg="#7f7f7f", relief=FLAT)
        self.add_input.pack(side=LEFT, fill=X, expand=TRUE, padx=2, pady=5)
        self.root.update()

        self.frame2.pack(side=TOP, fill=X)

        # print("Phase 7")

        self.main_f = Frame(self.root, background="#3c3c3c", height=self.root.winfo_height()-100)
        self.main_f.pack(fill=BOTH)

        # print("Phase 7a")

        self.s_frame = Frame(self.main_f, height=self.main_f.winfo_height()-100, width=700)
        self.s_frame.pack()

        # print("Phase 7b")

        self.sw = ScrolledWindow(self.s_frame, 700, self.root.winfo_height()-100, heigh=400, width=400)

        # print("Phase 7c")

        self.canv = self.sw.canv

        # print("Phase 7d")

        self.frame = self.sw.scrollwindow
        self.frames = []

        # print("Phase 7e")

        self.canvass = []
        self.buttons = []

        # print("Phase 8")

        import os
        names = os.listdir("./saves/")

        infos = {}
        infos["dates"] = []
        infos["score"] = []
        infos["level"] = []

        import time

        for i in names:
            # print(time.localtime(int(os.path.getmtime("./saves/" + i + "/bubble.json"))))
            mtime = os.path.getmtime("./saves/" + i + "/bubble.json")
            a = time.localtime(mtime)

            b = list(a)

            if a[4] < 10:
                b[4] = "0"+str(a[4])
            else:
                b[4] = str(a[4])
            if a[5] < 10:
                b[5] = "0"+str(a[5])
            else:
                b[5] = str(a[5])

            tme_var = "%i/%i/%i %i:%s:%s" % (a[2], a[1], a[0], a[3], b[4], b[5])
            infos["dates"].append(tme_var)

            a = Reader("./saves/" + i + "/game.json").get_decoded()
            infos["score"].append(a["score"])
            infos["level"].append(a["level"])

        self.item_info = names

        # print(names)

        i = 0

        # print("Phase 9")

        for name in tuple(dirs):
            # print("Round: " + str(i))
            # print(names[i])
            self.item_info.append(i)
            self.frames.append(Frame(self.frame, height=200, width=700))
            self.canvass.append(Canvas(self.frames[-1], height=200, width=700, bg="#7f7f7f", highlightthickness=0))
            self.canvass[-1].pack()

            self.canvass[-1].create_text(10, 10, text=name, fill="gold", anchor=NW,
                                         font=("Helvetica", 26, "bold"))
            self.canvass[-1].create_text(10, 50, text=infos["dates"][i], fill="#afafaf", anchor=NW,
                                         font=("helvetica", 16))
            self.canvass[-1].create_text(240, 50, text="Level: "+str(infos["level"][i]), fill="#afafaf", anchor=NW,
                                         font=("helvetica", 16))
            self.canvass[-1].create_text(370, 50, text="Score: "+str(infos["score"][i]), fill="#afafaf", anchor=NW,
                                         font=("helvetica", 16))

            self.canvass[-1].create_rectangle(0, 0, 699, 201, outline="#3c3c3c")

            self.buttons.append(Button(self.frames[-1], relief=FLAT, text="open", bg="#afafaf", width=7))
            self.buttons.copy()[-1].place(x=675, y=175, anchor=SE)
            self.buttons.copy()[-1].bind("<ButtonRelease-1>", self.open)

            self.buttons.append(Button(self.frames[-1], relief=FLAT, text="rename", bg="#afafaf", width=7))
            self.buttons.copy()[-1].place(x=600, y=175, anchor=SE)
            self.buttons.copy()[-1].bind("<ButtonRelease-1>", self.rename)

            self.buttons.append(Button(self.frames[-1], relief=FLAT, text="remove", bg="#afafaf", width=7))
            self.buttons.copy()[-1].place(x=525, y=175, anchor=SE)
            self.buttons.copy()[-1].bind("<ButtonRelease-1>", self.remove)

            self.frames[-1].grid(row=i)

            i += 1

        # self.tabs.add(self.frames.copy()[-1], text=' {} '.format(p))
        # self.tabs.enable_traversal()
        # self.tabs.pack(side=TOP, expand=TRUE, fill=BOTH)

        self.root.mainloop()

    @staticmethod
    def copy(src, dist):
        import os
        log.info("Game.copy", "Copying " + src + " to " + dist)
        fd = os.open(src, os.O_RDONLY)
        fd2 = os.open(dist, os.O_WRONLY | os.O_CREAT)
        a = os.read(fd, 8192)
        os.write(fd2, a)
        os.close(fd)
        os.close(fd2)

    def load(self):
        import os
        from tkinter import ttk
        log.info("Game.load", "Loading...")
        # self.tabs = ttk.Notebook(self.root)
        width = 16
        height = 34

        path = "saves/"
        index = os.listdir(path)
        log.debug("Game.load", "Index of '" + path + "' is " + str(index))
        dirs = []

        for item in index:
            file_path = path + item

            if os.path.isdir(file_path):
                dirs.append(item)

        y = -1
        x = 0
        p = 0
        i = 0
        # self.frames = []
        # self.item_info = [[[[]]]]
        self.items = list()
        # self.frames.append(Frame(self.tabs, bd=1, bg="#3c3c3c"))
        # items2 = []
        #
        # while i < len(dirs):
        #     y += 1
        #     self.item_info[p][0][x].append(dirs[i])
        #     if y >= height:
        #         y = 0
        #         self.item_info[p][0].append([])
        #         self.item_info[p][0].append([])
        #         self.item_info[p][0].append([])
        #         self.item_info[p][0].append([])
        #         x += 4
        #     if x > width:
        #         self.tabs.add(self.frames.copy()[-1], text=' {} '.format(p))
        #         self.frames.append(Frame(self.tabs, bd=1, bg="#3c3c3c"))
        #         y = 0
        #         x = 0
        #         self.item_info.append([[[]]])
        #         p += 1
        #     items2.append(dirs[i])
        #
        #     self.items.append(Button(self.frames[-1], width=30, relief=FLAT, text=dirs[i], bg="#707070"))
        #     self.items.copy()[-1].grid(column=x, row=y, padx=2, pady=2)
        #     self.items.copy()[-1].bind("<ButtonRelease-1>", self.open)
        #
        #     self.items.append(Button(self.frames[-1], relief=FLAT, text="rename", bg="#707070"))
        #     self.items.copy()[-1].grid(column=x + 1, row=y, padx=2, pady=2)
        #     self.items.copy()[-1].bind("<ButtonRelease-1>", self.rename)
        #
        #     self.items.append(Button(self.frames[-1], relief=FLAT, text="remove", bg="#707070"))
        #     self.items.copy()[-1].grid(column=x + 2, row=y, padx=2, pady=2)
        #     self.items.copy()[-1].bind("<ButtonRelease-1>", self.remove)
        #
        #     self.items.append(Button(self.frames[-1], relief=FLAT, text="", width=5, bg="#3c3c3c"))
        #     self.items.copy()[-1].grid(column=x + 3, row=y, padx=2, pady=2)
        #
        #     self.max_pages = p
        #     i += 1

        self.frame2 = Frame(bg="#5c5c5c")

        self.add = Button(self.frame2, text="Add Save", relief=FLAT, bg="#7f7f7f", fg="white", command=self.add_save)
        self.add.pack(side=RIGHT, padx=2, pady=5)
        self.add_input = Entry(self.frame2, bd=5, fg="#3c3c3c", bg="#7f7f7f", relief=FLAT)
        self.add_input.pack(side=LEFT, fill=X, expand=TRUE, padx=2, pady=5)
        self.root.update()

        self.frame2.pack(side=TOP, fill=X)

        # print("Phase 7")

        self.main_f = Frame(self.root, background="#3c3c3c", height=self.root.winfo_height()-100)
        self.main_f.pack(fill=BOTH)

        # print("Phase 7a")

        self.s_frame = Frame(self.main_f, height=self.main_f.winfo_height()-100, width=700)
        self.s_frame.pack()

        # print("Phase 7b")

        self.sw = ScrolledWindow(self.s_frame, 700, self.root.winfo_height()-100, heigh=400, width=400)

        # print("Phase 7c")

        self.canv = self.sw.canv

        # print("Phase 7d")

        self.frame = self.sw.scrollwindow
        self.frames = []

        # print("Phase 7e")

        self.canvass = []
        self.buttons = []

        # print("Phase 8")

        import os
        names = os.listdir("./saves/")

        infos = {}
        infos["dates"] = []
        infos["score"] = []
        infos["level"] = []

        import time

        for i in names:
            # print(time.localtime(int(os.path.getmtime("./saves/" + i + "/bubble.json"))))
            mtime = os.path.getmtime("./saves/" + i + "/bubble.json")
            a = time.localtime(mtime)

            b = list(a)

            if a[4] < 10:
                b[4] = "0"+str(a[4])
            else:
                b[4] = str(a[4])
            if a[5] < 10:
                b[5] = "0"+str(a[5])
            else:
                b[5] = str(a[5])

            tme_var = "%i/%i/%i %i:%s:%s" % (a[2], a[1], a[0], a[3], b[4], b[5])
            infos["dates"].append(tme_var)

            a = Reader("./saves/" + i + "/game.json").get_decoded()
            infos["score"].append(a["score"])
            infos["level"].append(a["level"])

        self.item_info = names

        # print(names)

        i = 0

        # print("Phase 9")

        for name in tuple(dirs):
            # print("Round: " + str(i))
            # print(names[i])
            self.item_info.append(i)
            self.frames.append(Frame(self.frame, height=200, width=700))
            self.canvass.append(Canvas(self.frames[-1], height=200, width=700, bg="#7f7f7f", highlightthickness=0))
            self.canvass[-1].pack()

            self.canvass[-1].create_text(10, 10, text=name, fill="gold", anchor=NW,
                                         font=("Helvetica", 26, "bold"))
            self.canvass[-1].create_text(10, 50, text=infos["dates"][i], fill="#afafaf", anchor=NW,
                                         font=("helvetica", 16))
            self.canvass[-1].create_text(240, 50, text="Level: "+str(infos["level"][i]), fill="#afafaf", anchor=NW,
                                         font=("helvetica", 16))
            self.canvass[-1].create_text(370, 50, text="Score: "+str(infos["score"][i]), fill="#afafaf", anchor=NW,
                                         font=("helvetica", 16))

            self.canvass[-1].create_rectangle(0, 0, 699, 201, outline="#3c3c3c")

            self.buttons.append(Button(self.frames[-1], relief=FLAT, text="open", bg="#afafaf", width=7))
            self.buttons.copy()[-1].place(x=675, y=175, anchor=SE)
            self.buttons.copy()[-1].bind("<ButtonRelease-1>", self.open)

            self.buttons.append(Button(self.frames[-1], relief=FLAT, text="rename", bg="#afafaf", width=7))
            self.buttons.copy()[-1].place(x=600, y=175, anchor=SE)
            self.buttons.copy()[-1].bind("<ButtonRelease-1>", self.rename)

            self.buttons.append(Button(self.frames[-1], relief=FLAT, text="remove", bg="#afafaf", width=7))
            self.buttons.copy()[-1].place(x=525, y=175, anchor=SE)
            self.buttons.copy()[-1].bind("<ButtonRelease-1>", self.remove)

            self.frames[-1].grid(row=i)

            i += 1

        # self.tabs.add(self.frames.copy()[-1], text=' {} '.format(p))
        # self.tabs.enable_traversal()
        # self.tabs.pack(side=TOP, expand=TRUE, fill=BOTH)

        self.root.mainloop()

    def add_save(self):
        import os

        if len(os.listdir("saves/")) <= 4000:
            self.add_input.config(state=DISABLED)
            self.add.config(state=DISABLED)
            new = self.add_input.get()

            os.mkdir("saves/" + new)

            self.copy("config/reset.json", "saves/" + new + "/game.json")
            self.copy("config/reset-bubble.json", "saves/" + new + "/bubble.json")

            self.delete_all()
            self.load()

    # noinspection PyTypeChecker
    def remove(self, event):
        import os
        y = event.widget.master.grid_info()["row"]

        src = self.item_info[y]
        for i in os.listdir("saves/" + src):
            os.remove("saves/" + src + "/" + i)

        os.removedirs("saves/" + src)

        self.delete_all()
        self.load()

    def rename(self, event):
        import os

        y = event.widget.master.grid_info()["row"]

        src = self.item_info[y]

        new = self.add_input.get()

        # noinspection PyTypeChecker
        os.rename("saves/" + src, "saves/" + new)
        self.delete_all()
        self.load()

    def open(self, event):
        y = event.widget.master.grid_info()["row"]

        src = self.item_info[y]
        self.delete_all()
        self.run(src)

    def delete_all(self):
        self.main_f.destroy()
        self.frame2.destroy()

    def run(self, save_name):
        self.save_name = save_name

        self.stats = Reader("saves/" + self.save_name + "/game.json").get_decoded()

        self.canvas = Canvas(self.root, height=self.config["height"], width=self.config["width"], highlightthickness=0)
        self.canvas.pack(expand=TRUE)

        self.main()
        self.root.mainloop()

    def resize(self, event):
        self.config["height"] = event.height
        self.config["width"] = event.width

    def return_main(self):
        self.returnmain = True
        self.canvas.destroy()
        self.__init__(time(), True)

    def main(self):
        from threading import Thread
        from bubble import place_bubble

        self.canvas.update()

        self.config["height"] = self.canvas.winfo_height()
        self.config["width"] = self.canvas.winfo_width()

        c = self.canvas
        mid_x = self.config["width"] / 2
        mid_y = self.config["height"] / 2

        self.bub["Normal"] = dict()
        self.bub["Triple"] = dict()
        self.bub["Double"] = dict()
        self.bub["Kill"] = dict()
        self.bub["SpeedUp"] = dict()
        self.bub["SpeedDown"] = dict()
        self.bub["Ultimate"] = dict()
        self.bub["Up"] = dict()
        self.bub["Teleporter"] = dict()
        self.bub["SlowMotion"] = dict()
        self.bub["DoubleState"] = dict()
        self.bub["Protect"] = dict()
        self.bub["ShotSpdStat"] = dict()
        self.bub["HyperMode"] = dict()
        self.bub["TimeBreak"] = dict()
        self.bub["Confusion"] = dict()
        self.bub["Paralis"] = dict()
        self.bub["StoneBub"] = dict()
        self.bub["NoTouch"] = dict()
        self.bub["Key"] = dict()
        self.bub["Diamond"] = dict()
        self.bub["Present"] = dict()
        self.bub["SpecialKey"] = dict()
        for i in range(9, 61):
            self.bub["Normal"][i] = PhotoImage(file="data/bubbles/Normal/" + str(i) + "px.png")
            self.bub["Triple"][i] = PhotoImage(file="data/bubbles/Triple/" + str(i) + "px.png")
            self.bub["Double"][i] = PhotoImage(file="data/bubbles/Double/" + str(i) + "px.png")
            self.bub["SpeedDown"][i] = PhotoImage(file="data/bubbles/SpeedDown/" + str(i) + "px.png")
            self.bub["SpeedUp"][i] = PhotoImage(file="data/bubbles/SpeedUp/" + str(i) + "px.png")
            self.bub["Up"][i] = PhotoImage(file="data/bubbles/Up/" + str(i) + "px.png")
            self.bub["Ultimate"][i] = PhotoImage(file="data/bubbles/Ultimate/" + str(i) + "px.png")
            self.bub["Kill"][i] = PhotoImage(file="data/bubbles/Kill/" + str(i) + "px.png")
            self.bub["Teleporter"][i] = PhotoImage(file="data/bubbles/Teleporter/" + str(i) + "px.png")
            self.bub["SlowMotion"][i] = PhotoImage(file="data/bubbles/SlowMotion/" + str(i) + "px.png")
            self.bub["DoubleState"][i] = PhotoImage(file="data/bubbles/DoubleState/" + str(i) + "px.png")
            self.bub["Protect"][i] = PhotoImage(file="data/bubbles/Protect/" + str(i) + "px.png")
            self.bub["ShotSpdStat"][i] = PhotoImage(file="data/bubbles/ShotSpdStat/" + str(i) + "px.png")
            self.bub["HyperMode"][i] = PhotoImage(file="data/bubbles/HyperMode/" + str(i) + "px.png")
            self.bub["TimeBreak"][i] = PhotoImage(file="data/bubbles/TimeBreak/" + str(i) + "px.png")
            self.bub["Confusion"][i] = PhotoImage(file="data/bubbles/Confusion/" + str(i) + "px.png")
            self.bub["Paralis"][i] = PhotoImage(file="data/bubbles/Paralis/" + str(i) + "px.png")
            self.bub["StoneBub"][i] = PhotoImage(file="data/bubbles/StoneBub/" + str(i) + "px.png")
            self.bub["NoTouch"][i] = PhotoImage(file="data/bubbles/NoTouch/" + str(i) + "px.png")
        self.bub["Key"][60] = PhotoImage(file="data/bubbles/Key.png")
        self.bub["Diamond"][36] = PhotoImage(file="data/bubbles/Diamond.png")
        self.bub["Present"][40] = PhotoImage(file="data/bubbles/Present.png")
        # noinspection PyTypeChecker
        self.bub["Coin"] = PhotoImage(file="data/CoinBub.png")
        self.bub["SpecialKey"][48] = PhotoImage(file="data/bubbles/SpecialMode.png")
        self.ship["image"] = PhotoImage(file="data/Ship.png")

        self.stats = Maintance().auto_restore(self.save_name)

        log.info("Game.main", "Save, restore and reset methods created")
        log.info("Game.main", "Window and canvas created")
        log.debug("Game.main", "PhotoImage.__doc__=" + str(PhotoImage.__doc__))
        self.back["normal"] = PhotoImage(file="data/BackGround.png")
        self.icons["store-pack"] = list()
        self.icons["store-pack"].append(PhotoImage(file="data/Images/StoreItems/Key.png"))
        self.icons["store-pack"].append(PhotoImage(file="data/Images/StoreItems/Teleport.png"))
        self.icons["store-pack"].append(PhotoImage(file="data/Images/StoreItems/Shield.png"))
        self.icons["store-pack"].append(PhotoImage(file="data/Images/StoreItems/DiamondBuy.png"))
        self.icons["store-pack"].append(PhotoImage(file="data/Images/StoreItems/BuyACake.png"))
        self.icons["store-pack"].append(PhotoImage(file="data/Images/StoreItems/Pop_3_bubs.png"))
        self.icons["store-pack"].append(PhotoImage(file="data/Images/StoreItems/PlusLife.png"))
        self.icons["store-pack"].append(PhotoImage(file="data/Images/StoreItems/SpeedBoost.png"))
        self.icons["store-pack"].append(PhotoImage(file="data/Images/StoreItems/SpecialMode.png"))
        self.icons["store-pack"].append(PhotoImage(file="data/Images/StoreItems/DoubleScore.png"))
        self.icons["store-pack"].append(None)
        self.icons["store-pack"].append(None)
        self.icons["store-pack"].append(None)
        self.icons["store-pack"].append(None)

        self.back["line"] = PhotoImage(file="data/LineIcon.png")
        self.fore["present-fg"] = PhotoImage(file="data/EventBackground.png")
        self.icons["circle"] = PhotoImage(file="data/Circle.png")
        self.icons["present"] = PhotoImage(file="data/Present.png")
        # self.back["store-bg"] = PhotoImage(file="data/StoreBG.png")
        self.fore["store-fg"] = PhotoImage(file="data/FG2.png")
        self.icons["store-diamond"] = PhotoImage(file="data/Diamond.png")
        self.icons["store-coin"] = PhotoImage(file="data/Coin.png")
        # BubCoin = PhotoImage(file="data/CoinBub.png")
        self.icons["pause-id"] = PhotoImage(file="data/Pause.png")
        self.icons["slowmotion"] = PhotoImage(file="data/SlowMotionIcon.png")

        self.back["special"] = PhotoImage(file="data/Images/Backgrounds/GameBG Special2.png")
        self.back["normal"] = PhotoImage(file="data/Images/Backgrounds/GameBG2.png")
        # self.fore["game"] = PhotoImage(file="data/Images/Foregrounds/GameFG.png")
        # self.fore["gloss"] = PhotoImage(file="data/Images/Foregrounds/Glossy.png")

        self.back["id"] = self.canvas.create_image(0, 0, anchor=NW, image=self.back["normal"])

        log.debug("Game.main", "Background=" + str(self.back["normal"]))
        # c.create_image(mid_x, mid_y, image=bg)
        self.ship["id1"] = self.canvas.create_polygon(0, 0, 0, 0, 0, 0, outline=None)
        self.ship["id2"] = c.create_image(7.5, 7.5, image=self.ship["image"])

        c.move(self.ship["id1"], self.stats["ship-position"][0], self.stats["ship-position"][1])
        c.move(self.ship["id2"], self.stats["ship-position"][0], self.stats["ship-position"][1])

        # c.create_rectangle(0, 0, self.config["width"], 69, fill="#003f3f")
        # c.create_rectangle(0, self.config["height"], self.config["width"], self.config["height"] - 102, fill="#003f3f")

        self.canvas.create_rectangle(0, 0, self.config["width"], 69, fill="#3f3f3f")
        self.canvas.create_rectangle(0, self.config["height"], self.config["width"], self.config["height"] - 102,
                                     fill="#3f3f3f")

        self.canvas.create_line(0, 70, self.config["width"], 70, fill="lightblue")
        self.canvas.create_line(0, 69, self.config["width"], 69, fill="white")
        log.info("Game.main", "Lines 1")

        self.canvas.create_line(0, self.config["height"] - 103, self.config["width"], self.config["height"] - 103,
                                fill="lightblue")
        self.canvas.create_line(0, self.config["height"] - 102, self.config["width"], self.config["height"] - 102,
                                fill="White")
        log.info("Game.main", "Lines 2")

        c.create_text(55, 30, text='Score', fill='orange')
        c.create_text(110, 30, text='Level', fill='orange')
        c.create_text(165, 30, text='Speed', fill='orange')
        c.create_text(220, 30, text='Lives', fill='orange')
        c.create_text(330, 30, text="Stat Score", fill="gold")
        c.create_text(400, 30, text="Protection", fill="gold")
        c.create_text(490, 30, text="Slowmotion", fill="gold")
        c.create_text(580, 30, text="Confusion", fill="gold")
        c.create_text(670, 30, text="Time Break", fill="gold")
        c.create_text(760, 30, text="Spd. Boost", fill="gold")
        c.create_text(850, 30, text="Paralizing", fill="gold")
        c.create_text(940, 30, text="Shot spd. time", fill="gold")
        c.create_text(1030, 30, text="No-touch time", fill="gold")
        c.create_text(1120, 30, text='Teleports', fill='gold')
        c.create_image(1185, 30, image=self.icons["store-diamond"])
        c.create_image(1185, 50, image=self.icons["store-coin"])

        self.texts["score"] = c.create_text(55, 50, fill='cyan')
        self.texts["level"] = c.create_text(110, 50, fill='cyan')
        self.texts["speed"] = c.create_text(165, 50, fill='cyan')
        self.texts["lives"] = c.create_text(220, 50, fill='cyan')
        self.texts["scorestate"] = c.create_text(330, 50, fill='cyan')
        self.texts["secure"] = c.create_text(400, 50, fill='cyan')
        self.texts["slowmotion"] = c.create_text(490, 50, fill='cyan')
        self.texts["confusion"] = c.create_text(580, 50, fill='cyan')
        self.texts["timebreak"] = c.create_text(670, 50, fill='cyan')
        self.texts["speedboost"] = c.create_text(760, 50, fill='cyan')
        self.texts["paralis"] = c.create_text(850, 50, fill='cyan')
        self.texts["shotspeed"] = c.create_text(940, 50, fill='cyan')
        self.texts["notouch"] = c.create_text(1030, 50, fill='cyan')
        self.texts["shiptp"] = c.create_text(1120, 50, fill='cyan')
        self.texts["diamond"] = c.create_text(1210, 30, fill='cyan')
        self.texts["coin"] = c.create_text(1210, 50, fill='cyan')
        self.texts["level-view"] = c.create_text(mid_x, mid_y, fill='Orange', font=("Helvetica", 50))

        self.texts["pause"] = c.create_text(mid_x, mid_y, fill='Orange', font=("Helvetica", 60, "bold"))
        self.icons["pause"] = c.create_image(mid_x, mid_y, image=self.icons["pause-id"], state=HIDDEN)

        c.create_text(50, self.config["height"] - 30, text='1x Score', fill='yellow')
        c.create_text(130, self.config["height"] - 30, text='2x Score', fill='yellow')
        c.create_text(210, self.config["height"] - 30, text='3x Score', fill='yellow')
        c.create_text(290, self.config["height"] - 30, text='-1 leven', fill='yellow')
        c.create_text(370, self.config["height"] - 30, text='Slow Motion', fill='yellow')
        c.create_text(450, self.config["height"] - 30, text='Verwarring', fill='yellow')
        c.create_text(530, self.config["height"] - 30, text='NoBubMove', fill='yellow')
        c.create_text(610, self.config["height"] - 30, text='Protectie', fill='yellow')
        c.create_text(690, self.config["height"] - 30, text='2x Pnt Status', fill='yellow')
        c.create_text(770, self.config["height"] - 30, text='Speed-up', fill='yellow')
        c.create_text(850, self.config["height"] - 30, text='Speed-down', fill='yellow')
        c.create_text(930, self.config["height"] - 30, text='Ultime Bubbel', fill='yellow')
        c.create_text(1010, self.config["height"] - 30, text='Hyper Mode', fill='yellow')
        c.create_text(1090, self.config["height"] - 30, text='Ammo speedup', fill='yellow')
        c.create_text(1170, self.config["height"] - 30, text='Teleporter', fill='yellow')
        c.create_text(1250, self.config["height"] - 30, text='No-touch', fill='yellow')
        c.create_text(1410, self.config["height"] - 30, text='Level Sleutel', fill='yellow')

        # c.create_line(-25 + (75 / 2), self.config["height"] - 101, -25 + (75 / 2), self.config["height"],
        #               fill="darkcyan")
        # c.create_line(55 + (75 / 2), self.config["height"] - 101, 55 + (75 / 2), self.config["height"], fill="darkcyan")
        # c.create_line(135 + (75 / 2), self.config["height"] - 101, 135 + (75 / 2), self.config["height"],
        #               fill="darkcyan")
        # c.create_line(215 + (75 / 2), self.config["height"] - 101, 215 + (75 / 2), self.config["height"],
        #               fill="darkcyan")
        # c.create_line(295 + (75 / 2), self.config["height"] - 101, 295 + (75 / 2), self.config["height"],
        #               fill="darkcyan")
        # c.create_line(375 + (75 / 2), self.config["height"] - 101, 375 + (75 / 2), self.config["height"],
        #               fill="darkcyan")
        # c.create_line(455 + (75 / 2), self.config["height"] - 101, 455 + (75 / 2), self.config["height"],
        #               fill="darkcyan")
        # c.create_line(535 + (75 / 2), self.config["height"] - 101, 535 + (75 / 2), self.config["height"],
        #               fill="darkcyan")
        # c.create_line(615 + (75 / 2), self.config["height"] - 101, 615 + (75 / 2), self.config["height"],
        #               fill="darkcyan")
        # c.create_line(695 + (75 / 2), self.config["height"] - 101, 695 + (75 / 2), self.config["height"],
        #               fill="darkcyan")
        # c.create_line(775 + (75 / 2), self.config["height"] - 101, 775 + (75 / 2), self.config["height"],
        #               fill="darkcyan")
        # c.create_line(855 + (75 / 2), self.config["height"] - 101, 855 + (75 / 2), self.config["height"],
        #               fill="darkcyan")
        # c.create_line(935 + (75 / 2), self.config["height"] - 101, 935 + (75 / 2), self.config["height"],
        #               fill="darkcyan")
        # c.create_line(1015 + (75 / 2), self.config["height"] - 101, 1015 + (75 / 2), self.config["height"],
        #               fill="darkcyan")
        # c.create_line(1095 + (75 / 2), self.config["height"] - 101, 1095 + (75 / 2), self.config["height"],
        #               fill="darkcyan")
        # c.create_line(1175 + (75 / 2), self.config["height"] - 101, 1175 + (75 / 2), self.config["height"],
        #               fill="darkcyan")
        # c.create_line(1255 + (75 / 2), self.config["height"] - 101, 1255 + (75 / 2), self.config["height"],
        #               fill="darkcyan")
        # c.create_line(1335 + (75 / 2), self.config["height"] - 101, 1335 + (75 / 2), self.config["height"],
        #               fill="darkcyan")
        # c.create_line(1415 + (75 / 2), self.config["height"] - 101, 1415 + (75 / 2), self.config["height"],
        #               fill="darkcyan")
        # log.info("Game.main", "Lines for bubble info created.")

        place_bubble(self.canvas, self.bub, 50, self.config["height"] - 75, 25, "Normal")
        place_bubble(self.canvas, self.bub, 130, self.config["height"] - 75, 25, "Double")
        place_bubble(self.canvas, self.bub, 210, self.config["height"] - 75, 25, "Triple")
        place_bubble(self.canvas, self.bub, 290, self.config["height"] - 75, 25, "Kill")
        place_bubble(self.canvas, self.bub, 370, self.config["height"] - 75, 25, "SlowMotion")
        place_bubble(self.canvas, self.bub, 450, self.config["height"] - 75, 25, "Confusion")
        place_bubble(self.canvas, self.bub, 530, self.config["height"] - 75, 25, "TimeBreak")
        place_bubble(self.canvas, self.bub, 610, self.config["height"] - 75, 25, "Protect")
        place_bubble(self.canvas, self.bub, 690, self.config["height"] - 75, 25, "DoubleState")
        place_bubble(self.canvas, self.bub, 770, self.config["height"] - 75, 25, "SpeedUp")
        place_bubble(self.canvas, self.bub, 850, self.config["height"] - 75, 25, "SpeedDown")
        place_bubble(self.canvas, self.bub, 930, self.config["height"] - 75, 25, "Ultimate")
        place_bubble(self.canvas, self.bub, 1010, self.config["height"] - 75, 25, "HyperMode")
        place_bubble(self.canvas, self.bub, 1090, self.config["height"] - 75, 25, "ShotSpdStat")
        place_bubble(self.canvas, self.bub, 1170, self.config["height"] - 75, 25, "Teleporter")
        place_bubble(self.canvas, self.bub, 1250, self.config["height"] - 75, 25, "NoTouch")
        place_bubble(self.canvas, self.bub, 1410, self.config["height"] - 75, 25, "LevelKey")
        log.info("Game.main", "Virtual bubbles for info created.")

        c.bind_all('<Key>', lambda event: control(self.root, self.canvas, self.icons, self.config, event, self.stats,
                                                  self.temp, self.modes, self.ship, self.commands, self.ammo, self.tp,
                                                  self.texts, self.fore, self.back, self.bubbles))
        # Thread(None, lambda: c.bind("<Motion>", MotionEventHandler)).start()
        # Thread(None, lambda: c.bind("<ButtonPress-1>", Button1PressEventHandler)).start()
        # Thread(None, lambda: c.bind("<ButtonRelease-1>", Button1ReleaseEventHandler)).start()
        c.bind_all('<KeyRelease-Escape>', lambda event: self.return_main())
        c.bind_all('Configure', lambda event: self.resize)

        log.info("Game.main", "Key-bindings binded to 'move_ship'")

        # MAIN GAME LOOP

        # print(BubPos)
        # print
        # print(BubPos0)

        log.debug("Game.main", "Current Bubble pos. is '" + str(self.bubbles["bub-position"]) + "'.")
        log.debug("Game.main", "__name__ variable is '" + str(__name__) + "'.")
        log.debug("Game.main", "'Lives' variable is '" + str(self.stats["lives"]) + "'.")
        log.debug("Game.main", "Score       =" + str(self.stats["score"]))
        log.debug("Game.main", "HiScore     =" + str(self.stats["hiscore"]))
        log.debug("Game.main", "Ship ID's are '" + str(self.ship["id1"]) + "' and '" + str(
            self.ship["id2"]) + "'. (Default = 1 and 2)")
        log.debug("Game.main", "TimeBreak=" + str(self.stats["timebreak"]))
        log.debug("Game.main", "StateTime=" + str(self.stats["timebreak-time"]))
        log.debug("Game.main", "S. Time  =" + str(int(self.stats["timebreak-time"] - time())))

        # old_start()
        if len(self.bubbles["bub-id"]) == 0:
            log.warning("Game.main", "Bubbel-ID lijst is gelijk aan lengte nul.")

        if len(self.bubbles["bub-action"]) == 0:
            log.warning("Game.main", "Bubble-actie lijst is gelijk aan lengte nul.")

        if len(self.bubbles["bub-speed"]) == 0:
            log.warning("Game.main", "Bubbel-snelheid lijst is gelijk aan lengte nul.")

        self.ammo["retime"] = time()

        stats = self.stats

        if stats["scorestate-time"] <= time():
            stats["scorestate"] = 1
            stats["scorestate-time"] = time()
        if stats["secure-time"] <= time():
            stats["secure"] = False
            stats["secure-time"] = time()
        if stats["slowmotion-time"] <= time():
            stats["slowmotion"] = False
            stats["slowmotion-time"] = time()
        if stats["timebreak-time"] <= time():
            stats["timebreak"] = False
            stats["timebreak-time"] = time()
        if stats["confusion-time"] <= time():
            stats["confusion"] = False
            stats["confusion-time"] = time()
        if stats["speedboost-time"] <= time():
            stats["speedboost"] = False
            stats["speedboost-time"] = time()
        if stats["paralis-time"] <= time():
            stats["paralis"] = False
            stats["paralis-time"] = time()
        if stats["shotspeed-time"] <= time():
            stats["shotspeed"] = 0.1
            stats["shotspeed-time"] = time()
        if stats["special-level-time"] <= time():
            stats["special-level"] = False
            stats["special-level-time"] = time()
        if stats["score"] < 0:
            log.error("Game.main", "The 'Score' variable under zero.")
            stats["score"] = 0
        if stats["score"] > stats["hiscore"]:
            stats["hiscore"] = stats["score"]
        if stats["confusion"] and not stats["secure"]:
            shuffling(self.bubbles)

        # self.fore["game-id"] = c.create_image(0, 0, anchor=NW, image=self.fore["game"])
        # self.fore["gloss-id"] = c.create_image(0, 0, anchor=NW, image=self.fore["gloss"])

        start(self.bubbles, self.save_name, self.stats, self.config, self.bub, self.modes, self.canvas)

        global Mainloop
        Mainloop = False

        self.stats = stats

        if len(self.bubbles["bub-id"]) <= 1:
            r_start(self.bubbles, self.stats, self.config, self.bub, self.canvas, self.modes)

        # Thread(None, lambda: Threads().move_bubbles()).start()

        # if 1:

        try:
            if __name__ == '__main__':
                while True:
                    # Mainloop = True
                    self.stats = self.cfg.auto_restore(self.save_name)
                    # GameActive = True
                    while self.stats["lives"] > 0:
                        if not self.modes["pause"]:
                            if not self.stats["timebreak"]:
                                if len(self.bubbles["bub-id"]) < (self.config["width"] - 105 - 72) / 10:
                                    if not self.stats["special-level"]:
                                        Thread(None,
                                               lambda: create_bubble(self.stats, self.config, self.bub, self.canvas,
                                                                     self.bubbles, self.modes, len(self.bubbles["bub-id"]))).start()
                                    else:
                                        Thread(None, lambda: SpecialMode().create_bubble(self.canvas, self.config,
                                                                                         self.bubbles, self.stats,
                                                                                         self.bub)).start()

                                Collision().check_collision(self.root, self.commands, self.bubbles, self.config,
                                                            self.stats,
                                                            self.ammo,
                                                            self.ship, self.canvas, log, self.back,
                                                            self.texts)
                                # Thread(None, lambda: move_ammo(self.canvas, log, self.root, self.ammo)).start()
                            if self.commands["present"] is True:
                                # noinspection PyTypeChecker
                                self.commands["present"] = Present(self.canvas, self.stats, self.temp, self.modes,
                                                                   self.config, self.icons, self.fore, self.log)
                            if self.commands["special-mode"] is True:
                                State.set_state(self.canvas, log, self.stats, "SpecialLevel", self.back)
                                self.commands["special-mode"] = False
                            Thread(None, lambda: refresh(self.stats, self.config, self.bubbles, self.bub, self.canvas,
                                                         self.back, self.texts, self.modes)).start()
                            Thread(None,
                                   lambda: Maintance().auto_save(self.save_name, self.stats, self.bubbles)).start()
                        self.root.update()
                        self.root.update_idletasks()
                        # sleep(0.001)
                    self.root.update()
                    g1 = c.create_text(mid_x, mid_y, text='GAME OVER', fill='Red', font=('Helvetica', 60, "bold"))
                    g2 = c.create_text(mid_x, mid_y + 60, text='Score: ' + str(self.stats["score"]), fill='white',
                                       font=('Helvetica', 30))
                    g3 = c.create_text(mid_x, mid_y + 90, text='Level: ' + str(self.stats["level"]), fill='white',
                                       font=('Helvetica', 30))
                    log.info("Game.main", "Game Over!")
                    self.root.update()
                    sleep(4)
                    c.delete(g1)
                    c.delete(g2)
                    c.delete(g3)
                    del g1, g2, g3
                    Maintance().reset(self.save_name)
                    self.return_main()
                    # clean_all(self.bubbles, self.canvas)
                    # if len(self.bubbles["bub-id"]) != 0:
                    #     log.fatal("Game.main", "Na schoonmaken van speelvlak zijn er nog steeds bubbels overgebleven. " +
                    #               "Vraag de eigenaar voor hulp en ondersteuning.")
                    #     sys.exit(1)
                    #
                    # self.cfg.reset(self.save_name)
        except TclError as e:
            if self.returnmain:
                pass
            else:
                if e.args[0] == 'can\'t invoke "update" command: application has been destroyed':
                    log.info('<root>', "Exit...")
                    sys.exit(0)
                elif e.args[0] == 'can\'t invoke "update_idletasks" command: application has been destroyed':
                    log.info('<root>', "Exit...")
                    sys.exit(0)
                elif e.args[0] == 'invalid command name ".!canvas"':
                    log.info('<root>', "Exit...")
                    sys.exit(0)
                elif e.args[0] == 'invalid command name ".!canvas"':
                    log.info('<root>', "Exit...")
                    sys.exit(0)
                else:
                    log.fatal('Game.main', 'TclError: ' + e.args[0] + "Line: " + str(e.__traceback__.tb_next.tb_lineno))
                    sys.exit(1)
        except AttributeError as e:
            if self.returnmain:
                pass
            else:
                if e.args[0] == "self.tk_widget is None. Not hooked into a Tk instance.":
                    sys.exit(0)
                else:
                    raise AttributeError(e.args[0])


if __name__ == "__main__":
    Game(time())