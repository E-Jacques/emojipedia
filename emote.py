from tkinter import Frame, Label

class Emote():

    def __init__(self, emote: str, id: int, keywords=[]):
        self.emote: str = emote
        self.id = id
        self.keywords: list[str] = keywords

    def getLabel(self, master: Frame, fz=12) -> Label:
        label = Label(master, text=self.emote, font=("Arial", fz))
        return label

    def addKeyword(self, k: str):
        self.keywords.append(k)

    def containsKey(self, k: str) -> bool:
        for key in self.keywords:
            if (k.lower() in key.lower()):
                return True

        return False 