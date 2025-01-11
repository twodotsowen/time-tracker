#!/bin/python3

import tkinter as tk
from tkinter import simpledialog
from datetime import datetime, timedelta

def rgb_to_hex(rgb):
    r, g, b = rgb
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def write_one_event(letter, start_time, end_time, note):
    current_date = datetime.now()
    monday_of_week = current_date - timedelta(days=current_date.weekday())
    month_name = monday_of_week.strftime('%B')
    day = monday_of_week.day
    with open(f"week_of_{month_name}_{day}.txt", "a") as file:
        date_str = end_time.strftime('%Y/%m/%d')
        start_str = start_time.strftime('%H:%M')
        end_str = end_time.strftime('%H:%M')
        note_str = " # " + note if len(note) else ""
        file.write(f"{letter} {date_str} {start_str}-{end_str}{note_str}\n")


class TimeTracker(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.current_char = None
        self.current_subcat_index = None
        self.current_start_time = None
        self.current_note = ""

        # UI Elements
        self.geometry("500x460")
        self.title("Time Tracker")
        # label
        self.label = tk.Label(self, text="Press a letter", font=("Arial", 32))
        self.label.pack(padx=0, pady=0)
        # note prompt
        self.note_prompt = tk.Label(self, text="", font=("Arial", 15),
                                    fg="#888888", bg="#333333", anchor='n')
        self.note_prompt.pack(fill=tk.BOTH, expand=True)

        # first column of labels
        self.frame1 = tk.Frame(self)
        self.frame1.pack(side=tk.LEFT, ipadx=25, fill=tk.X, expand=True)
        # and init second
        self.frame2 = tk.Frame(self, bg="#aaaaaa")
        
        # categories
        self.legend = {}
        with open('legend', 'r') as f:
            for line in f:
                if len(line.strip()) == 0:
                    continue
                parts = line.strip().split(':')
                self.legend[parts[0].lower()] = (parts[1], tuple(map(int, parts[2].split(','))))
                # add legend to top of tkinter
                hex_color = "#{:02x}{:02x}{:02x}".format(*map(int, parts[2].split(',')))
                label = tk.Label(self.frame1, text=f"{parts[0]}: {parts[1]}",
                                 bg=hex_color, padx=10, pady=5,
                                 justify=tk.RIGHT, anchor="w",
                                 relief=tk.RAISED)
                label.pack(pady=0, fill=tk.X)

        self.load_subcats()
        self.bind('<KeyPress>', self.handle_press)


    def load_subcats(self):
        f = open('subcategories', 'r')
        self.subcats = {}
        for line in f:
            line = line.strip()
            if not len(line):
                continue
            cat, subs = line.split(':')
            self.subcats[cat.lower()] = subs.split(',')
        f.close()
            
            
    def write_subcats(self):
        f = open('subcategories', 'w')
        for c in self.subcats.keys():
            line = c + ':' + ','.join(self.subcats[c]) + '\n'
            f.write(line)
        f.close()
        

    def update_note_prompt(self):
        text = "Press a number to pick a subcategory"
        color = "#999999"
        if self.current_subcat_index != None:
            subcat = self.subcats[self.current_char][self.current_subcat_index]
            if len(subcat):
                self.current_note = subcat
                text = subcat
                color = "#ffffff"
            else:
                text = "Press ENTER to edit subcategory"
        self.note_prompt.config(text=text, fg=color)

        
    def handle_press(self, event):
        if event.keysym == "Return" and self.current_subcat_index != None:
            self.edit_note()
        elif event.char.isnumeric():
            self.current_subcat_index = (int(event.char)+9)%10
            self.update_note_prompt()
            self.set_subcategory_list()
        else:
            char = event.char.lower()
            if char in self.legend:
                self.current_subcat_index = None
                self.start_event(char)

                
    def edit_note(self):
        result = simpledialog.askstring("Input", self.current_note)
        if result is not None:
            self.current_note = result.lower()
            self.subcats[self.current_char][self.current_subcat_index] = self.current_note
        self.update_note_prompt()
        self.set_subcategory_list()
        self.write_subcats()

        
    def start_event(self, char):
        self.end_last_event()
        current_time = datetime.now()
        self.current_char = char
        self.current_start_time = current_time
        self.current_note = ""
        self.update_note_prompt()
        self.label.config(text=self.legend[self.current_char][0])
        color_nums = self.legend[self.current_char][1]
        color = rgb_to_hex(color_nums)
        self.configure(bg=color)
        self.label.config(bg=color)
        self.set_subcategory_list()

        
    def set_subcategory_list(self):
        # squish category list
        self.frame1.pack_forget()
        self.frame1.pack(side=tk.LEFT, ipadx=30, fill=tk.X)
        
        # second column of labels
        self.frame2.pack_forget()
        self.frame2 = tk.Frame(self, bg="#aaaaaa")
        self.frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # sub category labels
        for i in range(10):
            subcat = self.subcats[self.current_char][i] if i < len(self.subcats[self.current_char]) else None
            msg, color = (subcat, '#000000') if subcat else ("Add Sub-Category", '#444444')
            bg_color = '#eeeeee' if i == self.current_subcat_index else '#aaaaaa'
            label = tk.Label(self.frame2, text=f"{(i+1)%10}: {msg}",
                             bg=bg_color, fg=color, padx=8, pady=6,
                             anchor="w",
                             relief=tk.RAISED)
            label.pack(fill=tk.X)
        panel = tk.Frame(self.frame2, bg="#777777")
        panel.pack(fill=tk.BOTH, expand=True)

        
    def end_last_event(self):
        if not self.current_char:
            return
        self.add_event_span(self.current_char, self.current_start_time, datetime.now())

        
    def add_event_span(self, event_char, start_time, end_time):
        if start_time.date() != end_time.date():
            # split up the timespan into two: one ending midnight yesterday and one starting midnight
            end_of_day = datetime.combine(start_time.date(), datetime.max.time())
            start_of_next_day = datetime.combine(end_time.date(), datetime.min.time())
            write_one_event(event_char, start_time, end_of_day, self.current_note)
            write_one_event(event_char, start_of_next_day, end_time, self.current_note)
        else:
            write_one_event(event_char, start_time, end_time, self.current_note)

            
    def on_closing(self):
        self.end_last_event()
        self.destroy()

        
if __name__ == "__main__":
    app = TimeTracker()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
