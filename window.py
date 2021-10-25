from tkinter import *
from tkinter.ttk import *
from string import ascii_lowercase, ascii_uppercase
from emote import Emote
from os import chdir
import json

chdir("/home/emilien/Documents/Dev/Projet/emojipedia")

class MainFrame(Frame):
    def __init__(self, master: Tk):
        super().__init__(master)
        super().grid(row=0, column=0, sticky="we")
        master.bind("<Key>", self.moveArrow)
        self.master = master
        self.query: str = ""
        self.input = Entry(master)
        self.emotes: list[Emote] = []
        self.emoteFrame = Frame(master)
        self.emoteFrameColNum = 6
        self.selected: list[int, int] = [-1, -1]
        self.lastUsed: list[int] = []

        self.setupFrame()
        self.loadEmotes("data.json")
        self.loadLastUsed("lastused.json")
        self.displayEmotes()

    def setupFrame(self):
        self.input.bind("<Key>", self.displayEmotes)
        self.input.grid(row=0, column=0, sticky="nwe", padx=2, pady=2)
        self.emoteFrame.grid(row=1, column=0, padx=2, pady=2, sticky="wes")

    def getEmoteById(self, id: int) -> Emote:
        for e in self.emotes:
            if e.id == id:
                return e

        return None

    def moveArrow(self, ev: Event):
        maxLen = len(self.getFilteredEmotes(self.query)) if self.query != "" else len(self.lastUsed)
        if ev.keysym == "Down":
            self.selected[0] = max(0, self.selected[0])
            if (self.selected[1] + 1) * self.emoteFrameColNum  + self.selected[0] < maxLen:
                self.selected[1] += 1
        elif ev.keysym == "Up":
            self.selected[0] = max(0, self.selected[0])
            self.selected[1] = max(0, self.selected[1] - 1)
        elif ev.keysym == "Right":
            if self.selected[1] * self.emoteFrameColNum  + self.selected[0] + 1 < maxLen:
                self.selected[0] += 1
                self.selected[1] = max(0, self.selected[1])

                if self.selected[0] // self.emoteFrameColNum > 0:
                    self.selected[0] = 0
                    self.selected[1] += 1
        elif ev.keysym == "Left":
            if self.selected[0] == 0 and self.selected[1] > 0:
                self.selected[0] = self.emoteFrameColNum - 1
                self.selected[1] = max(0, self.selected[1] - 1)
            else:
                self.selected[0] = max(0, self.selected[0] - 1)
                self.selected[1] = max(0, self.selected[1])
        elif ev.keysym == "Escape":
            super().destroy()
            self.saveLastUsed("lastused.json")
            self.master.withdraw()
            self.master.destroy()
        elif ev.keysym in ["Return", "KP_Enter"]:
            idx = self.selected[1] * self.emoteFrameColNum  + self.selected[0]
            if self.query != "":
                self.writeEmote(self.getFilteredEmotes(self.query)[idx])
            else:
                self.writeEmote(self.getEmoteById(self.lastUsed[idx]))
        elif str(self.master.focus_get()) != str(self.input):
            self.input.insert(len(self.input.get()), ev.char)
            self.input.focus()

        if ev.keysym in ["Down", "Up", "Right", "Left", "Return", "KP_Enter"]:
            self.displayEmotes()    

    def writeEmote(self, emote: Emote):
        if (self.lastUsed.count(emote.id) > 0):
            self.lastUsed.remove(emote.id)
        self.lastUsed = [emote.id] + self.lastUsed

        self.master.clipboard_clear()
        self.master.clipboard_append(emote.emote)
        self.master.update()

    def loadEmotes(self, path: str):
        with open(path, "r") as f:
            rawData = f.read()
            data = json.loads(rawData)

        for d in data:
            self.emotes.append(Emote(emote=d["emote"], id=d["id"], keywords=d["keywords"]))

    def loadLastUsed(self, path:str):
        with open(path, "r") as f:
            rawData = f.read()
            data = json.loads(rawData)

        self.lastUsed = data

    def saveLastUsed(self, path: str):
        with open(path, "w") as f:
            f.write(json.dumps(self.lastUsed))

    def getFilteredEmotes(self, q="") -> 'list[Emote]':
        l = [e for e in self.emotes if e.containsKey(q) or q == ""]
        return l
    
    def displayEmotes(self, entry: Event=None):
        value = self.query
        if entry and entry.keysym not in ["Down", "Up", "Right", "Left", "Escape", "Return", "KP_Enter"]:
            value=self.input.get()
            if entry.char in ascii_lowercase + ascii_uppercase:
                value += entry.char
            self.selected = [-1, -1]
        elif entry:
            super().focus()

        self.query = value  

        for widget in self.emoteFrame.winfo_children():
            widget.destroy()

        emotes = [self.getEmoteById(id) for id in self.lastUsed]
        if value != "":
            emotes = self.getFilteredEmotes(value)

        for idx, emote in enumerate(emotes):
            emoteLabel = emote.getLabel(self.emoteFrame, fz=16)
            if self.selected[0] == idx%self.emoteFrameColNum  and self.selected[1] == idx//self.emoteFrameColNum :
                emoteLabel.config(bg="lightblue")

            emoteLabel.grid(row=idx//self.emoteFrameColNum , column=idx%self.emoteFrameColNum , padx=5, pady=5)
            
