"""
    TODO:
        find text in text area using ctrl + f, set cursor position at found match.
        add date time string.

        easter-egg : encryption, decryption
"""
from darkpad import DarkPad

path = str(__file__)
pl = path.split('\\')
pl[-1] = 'img\\Darkpad.ico'
icon = "\\".join(pl)

darkpad = DarkPad(geometry="1200x700",icon=icon)
darkpad.mainloop()