"""
    TODO:
        find text in text area using ctrl + f, set cursor position at found match.
        add date time string.

        easter-egg : encryption, decryption
"""
from darkpad import DarkPad

path = str(__file__)
plist = path.split('\\')
plist[-1] = 'img/DarkPad.ico'
icon_path = "\\".join(plist)

darkpad = DarkPad(geometry="1200x700",icon=icon_path)
darkpad.mainloop()