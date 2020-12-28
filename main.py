#!/usr/bin/env python3
import teamgen
import tkinter as tk
from tkinter import ttk


class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg='#313131')
        self.master = master
        self.initUI()

    def initUI(self):
        self.master.title('RWBY Team Name Generator')

        self.character_boxes = []
        for char in range(4):
            frame = tk.Frame(self.master, relief=tk.RAISED, borderwidth=2)
            tk.Label(frame, text=f'Character {char+1}').grid(row=0, column=0, columnspan=3)
            tk.Label(frame, text='First Name').grid(row=1, column=0)
            tk.Label(frame, text='Last Name').grid(row=1, column=1)

            data = {
                'first': tk.Entry(frame),
                'last': tk.Entry(frame)
            }

            data['first'].grid(row=2, column=0)
            data['last'].grid(row=2, column=1)

            if char == 0:
                tk.Label(frame, text='Force Leader?').grid(row=1, column=2)
                var = data['leader'] = tk.IntVar()
                tk.Checkbutton(frame, variable=var).grid(row=2, column=2)

            self.character_boxes.append(data)

            # arrange in 2x2 grid
            row, col = divmod(char, 2)
            frame.grid(row=row, column=col, sticky='w', padx=10, pady=10)

        button = tk.Button(self.master, text='Generate!', command=self.generate)
        button.grid(row=2, column=0, columnspan=2, sticky='nsew', pady=20)

        self.result = ScrollableFrame(self.master)
        self.result.grid(row=3, column=0, columnspan=2, sticky='nsew')

        # menu bar
        menu = tk.Menu(self.master)
        menu.add_command(label='About/Help', command=self.about)
        self.master.config(menu=menu)

    def generate(self):
        c1, c2, c3, c4 = [
            {char['first'].get()[:1].upper(), char['last'].get()[:1].upper()} - {''}
            for char in self.character_boxes
        ]
        force_leader = self.character_boxes[0]['leader'].get()

        if len(c1 | c2 | c3 | c4) == 0:
            # no names given, simply return a few random choices
            options_nosub = set(teamgen.get_random_teams(10))
            options_withsub = set()
        else:
            # otherwise, use the names that were given
            options_nosub = set(teamgen.teamgen(c1, c2, c3, c4, allow_subs=False, fix_leader=bool(force_leader)))
            options_withsub = set(teamgen.teamgen(c1, c2, c3, c4, fix_leader=bool(force_leader))) - options_nosub

        # clear any previous run's information
        for w in self.result.scrollable_frame.winfo_children():
            w.destroy()

        # and now the new information
        frame = self.result.scrollable_frame

        f1 = tk.Frame(frame)
        tk.Label(f1, text='Options without letter substitutions:').grid(row=0, column=0, columnspan=3, sticky='nsew')
        for i, (abbr, name, color) in enumerate(options_nosub, start=1):
            tk.Label(f1, text=abbr).grid(row=i, column=0, sticky='nsew', padx=8)
            tk.Label(f1, text=name).grid(row=i, column=1, sticky='nsew', padx=8)
            tk.Button(f1, bg=color, state=tk.DISABLED, width=10).grid(row=i, column=2, sticky='nsew', padx=8)

        f2 = tk.Frame(frame)
        tk.Label(f2, text='Options with letter substitutions:').grid(row=0, column=0, columnspan=3, sticky='nsew')
        for i, (abbr, name, color) in enumerate(options_withsub, start=1):
            tk.Label(f2, text=abbr).grid(row=i, column=0, sticky='nsew', padx=8)
            tk.Label(f2, text=name).grid(row=i, column=1, sticky='nsew', padx=8)
            tk.Button(f2, bg=color, state=tk.DISABLED, width=10).grid(row=i, column=2, sticky='nsew', padx=8)

        f1.grid(row=0, column=0, sticky='nsew', padx=10)
        f2.grid(row=0, column=1, sticky='nsew', padx=10)

    def about(self):
        text = '''RWBY is an animated series created by Rooster Teeth. In its universe, characters are assigned a team of four, and the team is
    - a color/associated with a color/reminds you of a color
    - formed using the first letters of the first (sometimes last) names of the characters

For example, Ruby Rose, Weiss Schnee, Blake Belladonna, and Yang Xiao Long form Team RWBY ("Ruby"). From this we can also see that substitutions are allowed. From JNPR, CRDL, and BRNZ, we also learn that last names are allowed to be used in place of first names.

All known team names (as of V6):
    - RWBY ("Ruby"): Ruby Rose, Weiss Schnee, Blake Belladonna, Yang Xiao Long
    - JNPR ("Juniper"): Jaune Arc, Nora Valkerie, Pyrrha Nikos, Lie Ren
    - CRDL ("Cardinal"): Cardin Winchester, Russel Thrush, Dove Bronzewing, Sky Lark
    - CFVY ("Coffee"): Coco Adel, Fox Alistair, Velvet Scarletina, Yatsuhashi Dashi
    - SSSN ("Sun"): Sun Wukong, Scarlet David, Sage Ayana, Neptune Vasilias
    - ABRN ("Auburn"): Arslan Altan, Bolin Hori, Reese Chloris, Nadir Shiko
    - BRNZ ("Bronze"): Brawnz Ni, Roy Stallion, Nolan Porfrio, May Zedong
    - FNKI ("Funky"): Flynt Coal, Neon Katt (other members unknown)
    - STRQ ("Stark"): Summer Rose, Taiyang Xiao Long, Raven Branwen, Qrow Branwen

Penny's Team (Penny Polendina and Ciel Soleil) and Cinder's team (Cinder Fall, Mercury Black, Emerald Sustrai, Neo Politan) are not given names in the show, though the latter is sometimes referred to as "CMNE" (Carmine) or "CMSN" (Crimson) by the fans.

In this program, you can generate a list of possible team names given a list of characters. If you only want to use first names, leave the last name boxes blank. To simply generate a handful of random team names, leave all boxes blank. (In other cases, *all* matches are returned.) The order of the characters is irrelevant: this program will generate names using all possible team orderings. To force one character to be the leader, enter his or her name in the "Character 1" box and select the "Force Leader?" option.

Any returned color is guaranteed to contain all of the letters of the team name, but it's definitely not guaranteed to be pronounced the way you'd expect. Nor are these results comprehensive.

The following substitutions are being checked:
    F «» V
    I «» Y
    U «» W
    X «» Z

Color data taken from this API: https://github.com/meodai/color-names.
'''
        win = tk.Toplevel(self.master)
        container = tk.Text(win, width=120, wrap=tk.WORD, height=50)
        container.insert(1.0, text)
        container.config(state=tk.DISABLED)
        container.pack(fill=tk.BOTH)


if __name__ == '__main__':
    root = tk.Tk()
    Application(master=root).mainloop()
