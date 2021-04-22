import random
import itertools
from collections import Counter
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image  #  only non_standard dependency you need to DL
import threading
import queue
import time
from card_class import deck
from player import player
from game import game


def main():




    class App(Tk):
        def __init__(self, *args, **kwargs):
            Tk.__init__(self, *args, **kwargs)
            self.game_object = object

            container = Frame(self)
            container.pack(side="top", fill="both", expand=True)
            container.grid_rowconfigure(0, weight=1)
            container.grid_columnconfigure(0, weight=1)

            self.frames = {}

            list_of_frames = [StartPage, GamePage]

            for F in list_of_frames:
                frame = F(container, self)
                self.frames[F] = frame
                frame.grid(row=0, column=0, sticky="nsew")

            self.fresh = True
            self.show_frame(StartPage)

        def show_frame(self, context):
            frame = self.frames[context]
            print("waiting")
            if not self.fresh:
                time.sleep(0.1)
                frame.update(game_info_q.get())
            self.fresh = False
            frame.tkraise()

    class StartPage(Frame):
        def __init__(self, parent, controller):
            Frame.__init__(self, parent)

            height = 768
            width = 1344
            canvas = Canvas(self, height=height, width=width, bg="midnight blue")
            canvas.pack()

            left_frame = Frame(canvas, bg='midnight blue', bd=5)
            left_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1, anchor='nw')
            name_frame = Frame(left_frame, bg="white", bd=5)
            name_frame.place(relx=0.5, rely=0.17, relwidth=0.9, relheight=0.7, anchor="n")
            self.entry_p0 = Entry(name_frame, font=("Georgia", 18), bd=3)
            self.entry_p0.place(relx= 0,rely=0.2,relwidth=0.5, relheight=0.2)
            self.entry_p1 = Entry(name_frame, font=("Georgia", 18), bd=3)
            self.entry_p1.place(relx=0.51, rely=0.2, relwidth=0.5, relheight=0.2)
            self.entry_p2 = Entry(name_frame, font=("Georgia", 18), bd=3)
            self.entry_p2.place(relx=0, rely=0.45, relwidth=0.5, relheight=0.2)
            self.entry_p3 = Entry(name_frame, font=("Georgia", 18), bd=3)
            self.entry_p3.place(relx=0.51, rely=0.45, relwidth=0.5, relheight=0.2)
            self.entry_p4 = Entry(name_frame, font=("Georgia", 18), bd=3)
            self.entry_p4.place(relx=0.26, rely=0.7, relwidth=0.5, relheight=0.2)
            
            enter_player_label = Label(left_frame, text="Player Names:", font=("Book Antiqua", 18), bd=3)
            enter_player_label.place(relx=0.25, rely=0.07, relwidth=0.5, relheight=0.05)
            # self.entry.bind("<Return>", lambda _: self.button_click(self.entry.get()))

            right_frame = Frame(canvas, bg='midnight blue', bd=5)
            right_frame.place(relx=1, rely=0, relwidth=0.5, relheight=1, anchor='ne')
            self.sc_label = Label(right_frame, text="Starting Chips:", font=("Georgia", 18), bd=3)
            self.sc_label.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.05)
            self.sc_entry = Entry(right_frame, font=("Georgia", 18), bd=3)
            self.sc_entry.place(relx=0.5, rely=0.17, relwidth=0.5, relheight=0.07, anchor="n")

            self.sb_label = Label(right_frame, text="Small-Blind Chips:", font=("Georgia", 18), bd=3)
            self.sb_label.place(relx=0.25, rely=0.33, relwidth=0.5, relheight=0.05)
            self.sb_entry = Entry(right_frame, font=("Georgia", 18), bd=3)
            self.sb_entry.place(relx=0.5, rely=0.4, relwidth=0.5, relheight=0.07, anchor="n")

            self.bb_label = Label(right_frame, text="Big-Blind Chips:", font=("Georgia", 18), bd=3)
            self.bb_label.place(relx=0.25, rely=0.56, relwidth=0.5, relheight=0.05)
            self.bb_entry = Entry(right_frame, font=("Georgia", 18), bd=3)
            self.bb_entry.place(relx=0.5, rely=0.63, relwidth=0.5, relheight=0.07, anchor="n")
            self.bb_entry.bind("<Return>", lambda _: self.button_click(self.entry_p0.get(), self.entry_p1.get(),
                                                                       self.entry_p2.get(), self.entry_p3.get(),
                                                                       self.entry_p4.get(), self.sc_entry.get(),
                                                                       self.sb_entry.get(), self.bb_entry.get(),
                                                                       controller))

            button = Button(right_frame, text="START", font=("Georgia", 18),
                            command=lambda: self.button_click(self.entry_p0.get(), self.entry_p1.get(),
                                                              self.entry_p2.get(), self.entry_p3.get(),
                                                              self.entry_p4.get(), self.sc_entry.get(),
                                                              self.sb_entry.get(), self.bb_entry.get(), controller))
            button.place(relx=0.5, rely=0.9, relwidth=0.3, relheight=0.1, anchor="n")

        def button_click(self, entry0, entry1, entry2, entry3, entry4, entrysc,
                         entrysb, entrybb, controller):
            entry_list = [entry0, entry1, entry2, entry3, entry4, entrysc,
                          entrysb, entrybb]
            player_entry_list = [entry0, entry1, entry2, entry3, entry4]
            print(player_entry_list)
            player_entry_list = list(set(player_entry_list))
            for player in player_entry_list:
                if player == "":
                    player_entry_list.remove(player)
            print(player_entry_list)
            if len(player_entry_list) < 2:
                print("not enough players")
                return
            chip_entry_list = [entrysc, entrysb, entrybb]
            for chips in chip_entry_list:
                try:
                    chips = int(chips)
                except ValueError:
                    print("Value Error")
                    return
                if chips == "" or chips <= 0:
                    print("chip entry error")
                    return
            if not int(entrysc) > int(entrybb) > int(entrysb):
                print("chip entry error2 ")
                return
            setup = {
                "players": player_entry_list,
                "chips": chip_entry_list
            }
            response_q.put(setup)
            game_event.set()
            controller.show_frame(GamePage)

    class GamePage(Frame):
        def __init__(self, parent, controller):
            Frame.__init__(self, parent)

            self.restart = False
            self.responses = []
            self.list_of_button_r = []
            height = 768
            width = 1344
            canvas = Canvas(self, height=height, width=width, bg="forest green")
            canvas.pack()

            frame_1 = Frame(canvas, bg='white', bd=5)
            frame_1.place(relx=0.03, rely=0.6, relwidth=0.25, relheight=0.25, anchor='sw')
            name_frame1 = Frame(frame_1, bg="white", bd=5)
            name_frame1.place(relx=0.5, rely=0.5, relwidth=0.99, relheight=0.99, anchor="c")

            self.frame_p0 = Frame(name_frame1, bd=3, relief="groove")
            self.frame_p0.place(relwidth=1, relheight=1)
            self.name_label_p0 = Label(self.frame_p0, font=("Courier", 14), bd=3)
            self.name_label_p0.place(relx=0, rely=0, relheight=(1 / 3), relwidth=0.38)
            self.chips_label_p0 = Label(self.frame_p0, font=("Courier", 14), bd=3)
            self.chips_label_p0.place(relx=0, rely=(1 / 3), relheight=(1 / 3), relwidth=0.38)
            self.cards_frame_p0 = Frame(self.frame_p0, bd=3, relief="groove")
            self.cards_frame_p0.place(relx=0.38, relheight=1, relwidth=0.62)
            self.card1_p0 = Label(self.cards_frame_p0)
            self.card1_p0.place(relwidth=0.5, relheight=1)
            self.card2_p0 = Label(self.cards_frame_p0)
            self.card2_p0.place(relx=0.5, relwidth=0.5, relheight=1)
            self.stake_label_p0 = Label(self.frame_p0, bd=1, relief="groove")
            self.stake_label_p0.place(relx=0, rely=(2 / 3), relheight=(1 / 3), relwidth=0.38)


            frame_2 = Frame(canvas, bg='red', bd=5)
            frame_2.place(relx=0.05, rely=0.05, relwidth=0.25, relheight=0.25, anchor='nw')
            name_frame2 = Frame(frame_2, bg="white", bd=5)
            name_frame2.place(relx=0.5, rely=0.5, relwidth=0.99, relheight=0.99, anchor="c")

            self.frame_p1 = Frame(name_frame2, bd=3, relief="groove")
            self.frame_p1.place(relwidth=1, relheight=1)
            self.name_label_p1 = Label(self.frame_p1, font=("Courier", 14), bd=3)
            self.name_label_p1.place(relx=0, rely=0, relheight=(1 / 3), relwidth=0.38)
            self.chips_label_p1 = Label(self.frame_p1, font=("Courier", 14), bd=3)
            self.chips_label_p1.place(relx=0, rely=(1 / 3), relheight=(1 / 3), relwidth=0.38)
            self.cards_frame_p1 = Frame(self.frame_p1, bd=3, relief="groove")
            self.cards_frame_p1.place(relx=0.38, relheight=1, relwidth=0.62)
            self.card1_p1 = Label(self.cards_frame_p1)
            self.card1_p1.place(relwidth=0.5, relheight=1)
            self.card2_p1 = Label(self.cards_frame_p1)
            self.card2_p1.place(relx=0.5, relwidth=0.5, relheight=1)
            self.stake_label_p1 = Label(self.frame_p1, bd=1, relief="groove")
            self.stake_label_p1.place(relx=0, rely=(2 / 3), relheight=(1 / 3), relwidth=0.38)


            frame_3 = Frame(canvas, bg='blue', bd=5)
            frame_3.place(relx=0.95, rely=0.05, relwidth=0.25, relheight=0.25, anchor='ne')
            name_frame3 = Frame(frame_3, bg="white", bd=5)
            name_frame3.place(relx=0.5, rely=0.5, relwidth=0.99, relheight=0.99, anchor="c")

            
            self.frame_p2 = Frame(name_frame3, bd=3, relief="groove")
            self.frame_p2.place(relwidth=1, relheight=1)
            self.name_label_p2 = Label(self.frame_p2, font=("Courier", 14), bd=3)
            self.name_label_p2.place(relx=0, rely=0, relheight=(1 / 3), relwidth=0.38)
            self.chips_label_p2 = Label(self.frame_p2, font=("Courier", 14), bd=3)
            self.chips_label_p2.place(relx=0, rely=(1 / 3), relheight=(1 / 3), relwidth=0.38)
            self.cards_frame_p2 = Frame(self.frame_p2, bd=3, relief="groove")
            self.cards_frame_p2.place(relx=0.38, relheight=1, relwidth=0.62)
            self.card1_p2 = Label(self.cards_frame_p2)
            self.card1_p2.place(relwidth=0.5, relheight=1)
            self.card2_p2 = Label(self.cards_frame_p2)
            self.card2_p2.place(relx=0.5, relwidth=0.5, relheight=1)
            self.stake_label_p2 = Label(self.frame_p2, bd=1, relief="groove")
            self.stake_label_p2.place(relx=0, rely=(2 / 3), relheight=(1 / 3), relwidth=0.38)

            frame_4 = Frame(canvas, bg='yellow', bd=5)
            frame_4.place(relx=0.97, rely=0.6, relwidth=0.25, relheight=0.25, anchor='se')
            name_frame4 = Frame(frame_4, bg="white", bd=5)
            name_frame4.place(relx=0.5, rely=0.5, relwidth=0.99, relheight=0.99, anchor="c")


            self.frame_p3 = Frame(name_frame4, bd=3, relief="groove")
            self.frame_p3.place(relwidth=1, relheight=1)
            self.name_label_p3 = Label(self.frame_p3, font=("Courier", 14), bd=3)
            self.name_label_p3.place(relx=0, rely=0, relheight=(1 / 3), relwidth=0.38)
            self.chips_label_p3 = Label(self.frame_p3, font=("Courier", 14), bd=3)
            self.chips_label_p3.place(relx=0, rely=(1 / 3), relheight=(1 / 3), relwidth=0.38)
            self.cards_frame_p3 = Frame(self.frame_p3, bd=3, relief="groove")
            self.cards_frame_p3.place(relx=0.38, relheight=1, relwidth=0.62)
            self.card1_p3 = Label(self.cards_frame_p3)
            self.card1_p3.place(relwidth=0.5, relheight=1)
            self.card2_p3 = Label(self.cards_frame_p3)
            self.card2_p3.place(relx=0.5, relwidth=0.5, relheight=1)
            self.stake_label_p3 = Label(self.frame_p3, bd=1, relief="groove")
            self.stake_label_p3.place(relx=0, rely=(2 / 3), relheight=(1 / 3), relwidth=0.38)

            frame_5 = Frame(canvas, bg='pink', bd=5)
            frame_5.place(relx=0.38, rely=0.95, relwidth=0.25, relheight=0.25, anchor='sw')
            name_frame5 = Frame(frame_5, bg="white", bd=5)
            name_frame5.place(relx=0.5, rely=0.5, relwidth=0.99, relheight=0.99, anchor="c")


            self.frame_p4 = Frame(name_frame5, bd=3, relief="groove")
            self.frame_p4.place(relwidth=1, relheight=1)
            self.name_label_p4 = Label(self.frame_p4, font=("Courier", 14), bd=3)
            self.name_label_p4.place(relx=0, rely=0, relheight=(1 / 3), relwidth=0.38)
            self.chips_label_p4 = Label(self.frame_p4, font=("Courier", 14), bd=3)
            self.chips_label_p4.place(relx=0, rely=(1 / 3), relheight=(1 / 3), relwidth=0.38)
            self.cards_frame_p4 = Frame(self.frame_p4, bd=3, relief="groove")
            self.cards_frame_p4.place(relx=0.38, relheight=1, relwidth=0.62)
            self.card1_p4 = Label(self.cards_frame_p4)
            self.card1_p4.place(relwidth=0.5, relheight=1)
            self.card2_p4 = Label(self.cards_frame_p4)
            self.card2_p4.place(relx=0.5, relwidth=0.5, relheight=1)
            self.stake_label_p4 = Label(self.frame_p4, bd=1, relief="groove")
            self.stake_label_p4.place(relx=0, rely=(2 / 3), relheight=(1 / 3), relwidth=0.38)
            
            frame_d = Frame(canvas, bg='forest green', bd=5)
            frame_d.place(relx=0.375, rely=0.04, relwidth=0.25, relheight=0.35, anchor='nw')
                                 
            self.dealer_frame = Frame(frame_d)
            self.dealer_frame.place(relx=0, rely=0.1, relwidth=1, relheight=1)

            self.dealer = Label(self.dealer_frame, bg="forest green")
            self.dealer.place(relwidth=1, relheight=1)
            dealer_pic = ImageTk.PhotoImage(
                Image.open("cards\dealer.png").resize((400, 250), Image.ANTIALIAS))
            self.dealer.image = dealer_pic
            self.dealer.configure(image=dealer_pic)
            
            frame_anal = Frame(canvas, bg='forest green', bd=5)
            frame_anal.place(relx=0, rely=1, relwidth=0.3, relheight=0.3, anchor='sw')
            name_frameanal = Frame(frame_anal, bg="light green", bd=5)
            name_frameanal.place(relx=0.5, rely=0.5, relwidth=0.99, relheight=1, anchor="c")
            
            
            style = ttk.Style()
            style.theme_use('default')
            style.configure("grey.Horizontal.TProgressbar", background='green')
            
            player_0 = ttk.Progressbar(name_frameanal,style='grey.Horizontal.TProgressbar',orient=HORIZONTAL,length=200,mode='determinate')
            player_0['value'] = 10

            player_0.pack(pady=3)
            
            player_1 = ttk.Progressbar(name_frameanal,style='grey.Horizontal.TProgressbar',orient=HORIZONTAL,length=200,mode='determinate')
            player_1['value'] = 20

            player_1.pack(pady=5)
            
            player_2 = ttk.Progressbar(name_frameanal,style='grey.Horizontal.TProgressbar',orient=HORIZONTAL,length=200,mode='determinate')
            player_2['value'] = 30

            player_2.pack(pady=7)
            
            player_3 = ttk.Progressbar(name_frameanal,style='grey.Horizontal.TProgressbar',orient=HORIZONTAL,length=200,mode='determinate')
            player_3['value'] = 40

            player_3.pack(pady=9)
            
            player_4 = ttk.Progressbar(name_frameanal,style='grey.Horizontal.TProgressbar',orient=HORIZONTAL,length=200,mode='determinate')
            player_4['value'] = 50


            player_4.pack(pady=11)

           
            # self.entry.bind("<Return>", lambda _: self.button_click(self.entry.get()))

            frame_t = Frame(canvas, bg='black', bd=5)
            frame_t.place(relx=0.5, rely=0.5, relwidth=0.4, relheight=0.25, anchor='c')

            self.cc_frame = Frame(frame_t, bd=2, relief="raised")
            self.cc_frame.place(relx=0, rely=0, relwidth=1, relheight=0.9)

            self.cc_1 = Label(self.cc_frame, bg="green")
            self.cc_1.place(relwidth=(.50 / 3), relheight=1)
            card_d1 = ImageTk.PhotoImage(
                Image.open("cards\default0.png").resize((80, 120), Image.ANTIALIAS))
            self.cc_1.image = card_d1
            self.cc_1.configure(image=card_d1)

            self.cc_2 = Label(self.cc_frame, bg="green")
            self.cc_2.place(relx=(.50 / 3), relwidth=(.50 / 3), relheight=1)
            card_d2 = ImageTk.PhotoImage(
                Image.open("cards\default1.png").resize((80, 120), Image.ANTIALIAS))
            self.cc_2.image = card_d2
            self.cc_2.configure(image=card_d2)

            self.cc_3 = Label(self.cc_frame, bg="green")
            self.cc_3.place(relx=(.50 / 3) * 2, relwidth=(.50 / 3), relheight=1)
            card_d3 = ImageTk.PhotoImage(
                Image.open("cards\default1.png").resize((80, 120), Image.ANTIALIAS))
            self.cc_3.image = card_d3
            self.cc_3.configure(image=card_d3)

            self.cc_4 = Label(self.cc_frame, bg="green")
            self.cc_4.place(relx=(.50 / 3) * 3, relwidth=0.25, relheight=1)
            card_d4 = ImageTk.PhotoImage(
                Image.open("cards\default1.png").resize((80, 120), Image.ANTIALIAS))
            self.cc_4.image = card_d4
            self.cc_4.configure(image=card_d4)

            self.cc_5 = Label(self.cc_frame, bg="green")
            self.cc_5.place(relx=((.50 / 3) * 3) + 0.25, relwidth=0.25, relheight=1)
            card_d5 = ImageTk.PhotoImage(
                Image.open("cards\default1.png").resize((80, 120), Image.ANTIALIAS))
            self.cc_5.image = card_d5
            self.cc_5.configure(image=card_d5)

            self.pot_label = Label(frame_t, text="pot: ", font=("Courier", 12), bd=3)
            self.pot_label.place(relx=0.35, rely=0.92, relwidth=0.3, relheight=0.1)

           
            frame_act = Frame(canvas, bg='green', bd=5)
            frame_act.place(relx=1, rely=1, relwidth=0.3, relheight=0.3, anchor='se')

            # self.dealer_label = Label(frame_act, text="dealer: ", font=("Courier", 12), bd=3)
            # self.dealer_label.place(relx=0, rely=0.28, relwidth=0.5, relheight=0.04)

            # self.sb_label = Label(frame_act, text="small-blind: ", font=("Courier", 12), bd=3)
            # self.sb_label.place(relx=0, rely=0.33, relwidth=0.5, relheight=0.04)

            # self.bb_label = Label(frame_act, text="big-blind: ", font=("Courier", 12), bd=3)
            # self.bb_label.place(relx=0, rely=0.38, relwidth=0.5, relheight=0.04)

            self.action_frame = Frame(frame_act, bd=2, relief="raised", bg="green")
            self.action_frame.place(rely=0, relwidth=1, relheight=1)
            self.action_cover_label = Label(self.action_frame, bg="light green")
            self.action_cover_label.place(relx=0, rely=0, relheight=1, relwidth=1)

            self.actor_label = Label(self.action_frame, text="Actor: ", font=("Courier", 12), bd=3)
            self.actor_label.place(relwidth=1, relheight=0.06)

            self.new_round_label = Label(self.action_frame, text="New Round?", font=("Courier", 9), bd=3)
            self.new_round_label.place(relx=0.8, rely=0.05, relheight=0.1, relwidth=0.2)
            self.button_y = Button(self.action_frame, text="Yes", command=lambda: self.action_input("yes"))
            self.button_y.place(relx=0.8, rely=0.15, relheight=0.1, relwidth=0.2)
            self.button_n = Button(self.action_frame, text="No", command=lambda: self.action_input("no"))
            self.button_n.place(relx=0.8, rely=0.25, relheight=0.1, relwidth=0.2)

            self.raise_entry = Entry(self.action_frame, font=("Courier", 9), bd=3)
            self.raise_entry.place(relx=0, rely=1, relheight=0.12, relwidth=0.22, anchor="sw")
            self.raise_button = Button(self.action_frame, text="RAISE", font=("Courier", 9), bd=3, command=lambda: self.action_input(self.raise_entry.get()))
            self.raise_button.place(relx=0.22, rely=1, relheight=0.12, relwidth=0.22, anchor="sw")

            self.winner_label = Label(self.action_frame, font=("Courier", 12), bd=3)
            self.winner_label.place(relx=0, rely=(1/3), relwidth=0.75, relheight=0.3)


        def update(self, game):
            self.new_round_label.lower(self.action_cover_label)
            self.button_y.lower(self.action_cover_label)
            self.button_n.lower(self.action_cover_label)
            self.raise_entry.lower(self.action_cover_label)
            self.raise_button.lower(self.action_cover_label)
            self.winner_label.lower(self.action_cover_label)
            if self.restart:
                card1 = ImageTk.PhotoImage(Image.open(str("cards\default0.png")).resize((80, 120), Image.ANTIALIAS))
                self.cc_1.image = card1
                self.cc_1.configure(image=card1)

                card1 = ImageTk.PhotoImage(Image.open(str("cards\default0.png")).resize((80, 120), Image.ANTIALIAS))
                self.cc_2.image = card1
                self.cc_2.configure(image=card1)

                card1 = ImageTk.PhotoImage(Image.open(str("cards\default0.png")).resize((80, 120), Image.ANTIALIAS))
                self.cc_3.image = card1
                self.cc_3.configure(image=card1)

                card1 = ImageTk.PhotoImage(Image.open(str("cards\default0.png")).resize((80, 120), Image.ANTIALIAS))
                self.cc_4.image = card1
                self.cc_4.configure(image=card1)

                card1 = ImageTk.PhotoImage(Image.open(str("cards\default0.png")).resize((80, 120), Image.ANTIALIAS))
                self.cc_5.image = card1
                self.cc_5.configure(image=card1)
                self.restart = False
            if game.round_ended:
                time.sleep(0.3)
                self.new_round_label.lift(self.action_cover_label)
                self.button_y.lift(self.action_cover_label)
                self.button_n.lift(self.action_cover_label)
                winners = []
                scores = []
                for player in game.list_of_players_not_out:
                    if player.win:
                        winners.append(player)
                        scores.append(player.score)
                print(f"gui thinks winners are: {winners}")
                print(f"and thinks scores are: {scores}")
                if scores == [[]]:
                    self.winner_label["text"] = "Winner: " + str(winners)
                    
                    card1 = ImageTk.PhotoImage(
                        Image.open("cards\\" + str(game.cards[0]) + ".png").resize((80, 120), Image.ANTIALIAS))
                    self.cc_1.image = card1
                    self.cc_1.configure(image=card1)

                    card1 = ImageTk.PhotoImage(
                        Image.open("cards\\" + str(game.cards[1]) + ".png").resize((80, 120), Image.ANTIALIAS))
                    self.cc_2.image = card1
                    self.cc_2.configure(image=card1)

                    card1 = ImageTk.PhotoImage(
                        Image.open("cards\\" + str(game.cards[2]) + ".png").resize((80, 120), Image.ANTIALIAS))
                    self.cc_3.image = card1
                    self.cc_3.configure(image=card1)

                    card1 = ImageTk.PhotoImage(
                        Image.open("cards\\" + str(game.cards[3]) + ".png").resize((80, 120), Image.ANTIALIAS))
                    self.cc_4.image = card1
                    self.cc_4.configure(image=card1)

                    card1 = ImageTk.PhotoImage(
                        Image.open("cards\\" + str(game.cards[4]) + ".png").resize((80, 120), Image.ANTIALIAS))
                    self.cc_5.image = card1
                    self.cc_5.configure(image=card1)
                    
                else:
                    try:
                        for player in game.list_of_players_not_out:
                            if player.win:
                                if player.score == max(scores):
                                    self.winner_label["text"] = "Winner: " + str(winners) + "\n" + score_interpreter(player)
                                    
                                    card1 = ImageTk.PhotoImage(
                                        Image.open("cards\\" + str(game.cards[0]) + ".png").resize((80, 120), Image.ANTIALIAS))
                                    self.cc_1.image = card1
                                    self.cc_1.configure(image=card1)

                                    card1 = ImageTk.PhotoImage(
                                        Image.open("cards\\" + str(game.cards[1]) + ".png").resize((80, 120), Image.ANTIALIAS))
                                    self.cc_2.image = card1
                                    self.cc_2.configure(image=card1)

                                    card1 = ImageTk.PhotoImage(
                                        Image.open("cards\\" + str(game.cards[2]) + ".png").resize((80, 120), Image.ANTIALIAS))
                                    self.cc_3.image = card1
                                    self.cc_3.configure(image=card1)

                                    card1 = ImageTk.PhotoImage(
                                        Image.open("cards\\" + str(game.cards[3]) + ".png").resize((80, 120), Image.ANTIALIAS))
                                    self.cc_4.image = card1
                                    self.cc_4.configure(image=card1)

                                    card1 = ImageTk.PhotoImage(
                                        Image.open("cards\\" + str(game.cards[4]) + ".png").resize((80, 120), Image.ANTIALIAS))
                                    self.cc_5.image = card1
                                    self.cc_5.configure(image=card1)
                                    
                    except IndexError:
                        pass
                self.winner_label.lift(self.action_cover_label)

                self.restart = True

                return
            if game.need_raise_info:
                self.raise_entry.lift(self.action_cover_label)
                self.raise_button.lift(self.action_cover_label)
            try:
                card1 = ImageTk.PhotoImage(
                    Image.open("cards\\" + str(game.cards[0]) + ".png").resize((80, 120), Image.ANTIALIAS))
                self.cc_1.image = card1
                self.cc_1.configure(image=card1)

                card1 = ImageTk.PhotoImage(
                    Image.open("cards\\" + str(game.cards[1]) + ".png").resize((80, 120), Image.ANTIALIAS))
                self.cc_2.image = card1
                self.cc_2.configure(image=card1)

                card1 = ImageTk.PhotoImage(
                    Image.open("cards\\" + str(game.cards[2]) + ".png").resize((80, 120), Image.ANTIALIAS))
                self.cc_3.image = card1
                self.cc_3.configure(image=card1)

                card1 = ImageTk.PhotoImage(
                    Image.open("cards\\" + str(game.cards[3]) + ".png").resize((80, 120), Image.ANTIALIAS))
                self.cc_4.image = card1
                self.cc_4.configure(image=card1)

                card1 = ImageTk.PhotoImage(
                    Image.open("cards\\" + str(game.cards[4]) + ".png").resize((80, 120), Image.ANTIALIAS))
                self.cc_5.image = card1
                self.cc_5.configure(image=card1)
            except IndexError:
                pass
            try:
                self.name_label_p0["text"] = game.list_of_players[0]
                self.name_label_p1["text"] = game.list_of_players[1]
                self.name_label_p2["text"] = game.list_of_players[2]
                self.name_label_p3["text"] = game.list_of_players[3]
                self.name_label_p4["text"] = game.list_of_players[4]
            except IndexError:
                pass
            try:
                self.chips_label_p0["text"] = "Chips:\n" + str(game.list_of_players[0].chips)
                self.chips_label_p1["text"] = "Chips:\n" + str(game.list_of_players[1].chips)
                self.chips_label_p2["text"] = "Chips:\n" + str(game.list_of_players[2].chips)
                self.chips_label_p3["text"] = "Chips:\n" + str(game.list_of_players[3].chips)
                self.chips_label_p4["text"] = "Chips:\n" + str(game.list_of_players[4].chips)
            except IndexError:
                pass
            try:
                card1 = ImageTk.PhotoImage(
                    Image.open("cards\\" + str(game.list_of_players[0].cards[0]) + ".png").resize((85, 125), Image.ANTIALIAS))
                self.card1_p0.image = card1
                self.card1_p0.configure(image=card1)

                card1 = ImageTk.PhotoImage(
                    Image.open("cards\\" + str(game.list_of_players[1].cards[0]) + ".png").resize((80, 125), Image.ANTIALIAS))
                self.card1_p1.image = card1
                self.card1_p1.configure(image=card1)

                card1 = ImageTk.PhotoImage(
                    Image.open("cards\\" + str(game.list_of_players[2].cards[0]) + ".png").resize((80, 125), Image.ANTIALIAS))
                self.card1_p2.image = card1
                self.card1_p2.configure(image=card1)

                card1 = ImageTk.PhotoImage(
                    Image.open("cards\\" + str(game.list_of_players[3].cards[0]) + ".png").resize((80, 125), Image.ANTIALIAS))
                self.card1_p3.image = card1
                self.card1_p3.configure(image=card1)

                card1 = ImageTk.PhotoImage(
                    Image.open("cards\\" + str(game.list_of_players[4].cards[0]) + ".png").resize((80, 125), Image.ANTIALIAS))
                self.card1_p4.image = card1
                self.card1_p4.configure(image=card1)

            except IndexError:
                pass
            try:
                card2 = ImageTk.PhotoImage(
                    Image.open("cards\\" + str(game.list_of_players[0].cards[1]) + ".png").resize((80, 125), Image.ANTIALIAS))
                self.card2_p0.image = card2
                self.card2_p0.configure(image=card2)

                card2 = ImageTk.PhotoImage(
                    Image.open("cards\\" + str(game.list_of_players[1].cards[1]) + ".png").resize((80, 125), Image.ANTIALIAS))
                self.card2_p1.image = card2
                self.card2_p1.configure(image=card2)

                card2 = ImageTk.PhotoImage(
                    Image.open("cards\\" + str(game.list_of_players[2].cards[1]) + ".png").resize((80, 125), Image.ANTIALIAS))
                self.card2_p2.image = card2
                self.card2_p2.configure(image=card2)

                card2 = ImageTk.PhotoImage(
                    Image.open("cards\\" + str(game.list_of_players[3].cards[1]) + ".png").resize((80, 125), Image.ANTIALIAS))
                self.card2_p3.image = card2
                self.card2_p3.configure(image=card2)

                card2 = ImageTk.PhotoImage(
                    Image.open("cards\\" + str(game.list_of_players[4].cards[1]) + ".png").resize((80, 125), Image.ANTIALIAS))
                self.card2_p4.image = card2
                self.card2_p4.configure(image=card2)
            except IndexError:
                pass
            try:
                self.stake_label_p0["text"] = "Stake: " + str(game.list_of_players[0].stake)
                self.stake_label_p1["text"] = "Stake: " + str(game.list_of_players[1].stake)
                self.stake_label_p2["text"] = "Stake: " + str(game.list_of_players[2].stake)
                self.stake_label_p3["text"] = "Stake: " + str(game.list_of_players[3].stake)
                self.stake_label_p4["text"] = "Stake: " + str(game.list_of_players[4].stake)
            except IndexError:
                pass
            self.pot_label["text"] = "Pot: " + str(game.pot)
            if game.game_over:
                self.actor_label["text"] = "Winner!: " + str(game.winner.name)
                return
            print(f"round ended {game.round_ended}")

            self.actor_label["text"] = str(game.acting_player.name)

            variable = StringVar(self.action_frame)
            variable.initialize("ACTION")
            w = OptionMenu(self.action_frame, variable, *game.possible_responses)
            w.place(relx=0, rely=0.05, relheight=0.1, relwidth=0.3)
            button_go = Button(self.action_frame, text="GO", font=("Courier", 10), command=lambda: self.action_input(variable.get()))
            button_go.place(relx=1, rely=1, relheight=0.3, relwidth=0.3, anchor="se")


        def action_input(self, entry0):

            response_q.put(entry0)
            game_event.set()
            time.sleep(0.1)
            if not game_info_q.empty():
                self.update(game_info_q.get())

    def score_interpreter(player):
        list_of_hand_types = ["High Card", "One Pair", "Two Pair", "Three of a Kind", "Straight", "Flush",
                              "Full House",
                              "Four of a Kind", "Straight Flush", "Royal Flush"]
        list_of_values_to_interpret = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
                                       "Jack",
                                       "Queen",
                                       "King", "Ace"]
        hand_type = list_of_hand_types[player.score[0]]
        mod1 = list_of_values_to_interpret[player.score[1]]
        mod2 = list_of_values_to_interpret[player.score[2]]
        mod3 = list_of_values_to_interpret[player.score[3]]
        if player.score[0] == 0:
            return hand_type + ": " + mod3
        if player.score[0] == 1:
            return hand_type + ": " + mod1 + "s"
        if player.score[0] == 2:
            return hand_type + ": " + mod1 + "s" + " and " + mod2 + "s"
        if player.score[0] == 3:
            return hand_type + ": " + mod1 + "s"
        if player.score[0] == 4:
            return hand_type + ": " + mod1 + " High"
        if player.score[0] == 5:
            return hand_type + ": " + mod1 + " High"
        if player.score[0] == 6:
            return hand_type + ": " + mod1 + "s" + " and " + mod2 + "s"
        if player.score[0] == 7:
            return hand_type + ": " + mod1 + "s"
        if player.score[0] == 8:
            return hand_type + ": " + mod1 + " High"
        if player.score[0] == 9:
            return hand_type

    def ask_app(question, game=""):
        print("asking...")
        print(question)
        answer = ""
        if game != "":
            game_info_q.put(game)
        game_event.wait()
        if not response_q.empty():
            answer = response_q.get()
        game_event.clear()

        return answer

    def update_gui(game1):
        print("updating gui...")
        print(game1)

    def play(game):
        game.deck.shuffle()
        game_info_q.put(game)
        update_gui(game)
        game.establish_player_attributes()
        game.deal_hole()
        game.print_round_info()
        game.act_one()
        game.print_round_info()
        if not game.round_ended:
            game.deal_flop()
            game.print_round_info()
        if not game.round_ended:
            game.ask_players()
            game.print_round_info()
        if not game.round_ended:
            game.deal_turn()
            game.print_round_info()
        if not game.round_ended:
            game.ask_players()
            game.print_round_info()
        if not game.round_ended:
            game.deal_river()
            game.print_round_info()
        if not game.round_ended:
            game.ask_players()
            game.print_round_info()
        if not game.round_ended:
            game.score_all()
            game.print_round_info()
        game.find_winners()
        game_info_q.put(game)

        game.print_round_info()
        game.round_ended = True
        print(game.winners, game.winner, [player for player in game.list_of_players_not_out if player.win])
        game.end_round()

    def run_app():
        app = App()
        app.mainloop()

    def run_game_data():
        game0 = Game()
        while True:
            play(game0)

    game_event = threading.Event()
    response_q = queue.Queue()
    game_info_q = queue.Queue()
    end_update = threading.Event()
    t1 = threading.Thread(target=run_app)
    t1.start()
    t2 = threading.Thread(target=run_game_data())
    t2.start()


if __name__ == "__main__":
    main()
