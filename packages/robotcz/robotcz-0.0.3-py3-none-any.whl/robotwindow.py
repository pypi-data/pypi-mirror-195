#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
#R:/PGM_PYT/robot/robotwindow.py
"""
Modul definující posluchače světa robotů,
který je schopen zobrazit tento svět v okně knihovny tkinter.
"""
import dbg; dbg.start_mod(2, __name__);   MyDBG=0
###########################################################################q

import tkinter as tk

from .robotworld import (IRobotWorldListener, RobotWorld, WRobot,
                         WALL_CHAR, )



###########################################################################q
class RobotWindow ():   # Implements IRobotWorldListener
    """Třída zodpovědná za zobrazení robotího dvorku a jednotlivých robotů.
    Zobrazovaní roboti musejí být instancemi třídy {@link RobotWorld.WRobot}.
    Při vytváření zobrazovací instance se nejprve vytvoří instance světa
    robotů, u které se pak zobrazovací instance zaregistruje jako posluchač.
    """

    def __init__(self, world:RobotWorld):
        """Vytvoří základní okno definované zadaným rodičovským oknem
        a maticí s počty značek na jednotlivých políčkách.
        """
        # dbg.prSE(MyDBG, 1, 'RobotWindow.__init__', f'{world=}')
        # self.root  = tk.Tk()    # Rodičovské okno
        self.frame = tk.Frame()
        self.world = world
        import os
        self.frame.master.protocol("WM_DELETE_WINDOW",
                                   lambda: os._exit(0))
        # Pole s nesmyslnými počty značek, aby se ikony musely měnit
        self.fields = [[MARKERS for _ in range(world.cols)]
                                for _ in range(world.rows)]
        self.labels = []      # Matice návěští s ikonami
        # Připraví se prázdná návěští bez ikon
        for r, row in enumerate(self.fields):
            row_labels = []
            for c, markers in enumerate(row):
                label = tk.Label(self.frame, borderwidth=0)
                label.grid(row=r, column=c)
                row_labels.append(label)
            self.labels.append(row_labels)
        # dbg.prIN(MyDBG, "Před překreslením", q=1)
        self.repaint(world.fields, world.robots)
        # dbg.prIN(MyDBG, "Po překreslení", q=1)
        world.add_listener(self)
        # dbg.prSE(MyDBG, 0, 'RobotWindow.__init__')

    def repaint(self, fields:[[int]], robots:['WRobot']) -> None:
        """Překreslení svět robota v reakci na hlášení o jeho změně.
        V argumentech je zadán počet značek na jednotlivých polích
        a pozice, barva a směr natočení jednotlivých robotů.
        """
        # dbg.prSE(MyDBG, 1, 'RobotWindow.repaint')
        # Zkopíruju obsah jednotlivých polí
        world = [[c for c in row] for row in fields]
        # Přepíšu obsah polí, na nichž stojí roboti, záporným pořadím
        # ikony daného robota v poli ikon robotů posunutým o jedničku,
        # protože nulu potřebuji pro pole bez značek
        for r in robots:
            # Pořadí barvy dělím dvěma
            color_num = r.color.value  *  DIRECTIONS
            robot_num = -(color_num  +  r.vdir4.value) - 1
            world[r.vrow][r.vcol] = robot_num
            # dbg.prIN(MyDBG, f'{robot_num=:3}: {r}')
        # U polí, jejichž obsah se změnil, vyměním ikonu v návěští
        # a zapamatuji si nový stav
        for r, row in enumerate(fields):
            for c in range(len(row)):
                if world[r][c] != self.fields[r][c]:
                    self.fields[r][c] = num = world[r][c]
                    # dbg.prSeq(FIELD_LOOKS)
                    if num>=0:
                        self.labels[r][c]["image"] = FIELD_LOOKS[num]
                    else:
                        # dbg.prIN(MyDBG, f'{r=}, {c=}, {(-num-1)=}, '
                        #                 f'{ROBOT_LOOKS[-num-1].file}')
                        self.labels[r][c]["image"] = ROBOT_LOOKS[-num-1]
                    # self.labels[r][c]["image"] = (FIELD_LOOKS[num] if num>=0
                    #                         else  ROBOT_LOOKS[-num-1])
        self.frame.update()
        self.frame.pack()
        # dbg.prSE(MyDBG, 0, 'RobotWindow.repaint')

    def release(self):
        """Oznámení o konci světa robota a z toho plynoucí povinnosti
        uvolnit blokované zdroje.
        """
        self.frame.destroy()



###########################################################################q
class Icon (tk.PhotoImage):
    """Potomek určený pouze pro ladění,
    aby prozrazoval soubor, z nějž převzal obrázek.
    """
    def __init__(self, file):
        tk.PhotoImage.__init__(self, file=file)
        self._file = file

    @property
    def file(self):
        return self._file


###########################################################################q
# Veřejné metody modulu

def create_window_for(world:RobotWorld) -> RobotWorld:
    """Vytvoří okno reprezentující zadaný svět robotů
    a přihlásí se u tohoto světa jako jeho posluchač.
    """
    global window
    window = RobotWindow(world)
    return window.world



###########################################################################q
# Veřejné metody modulu



###########################################################################q
# Proměnné modulu:
window:RobotWindow


###########################################################################q
# Konstanty modulu:

# Kořenové okno
_ROOT = tk.Tk()

# Cesta k rodičovskému balíčku
import os as _os
_robot_dir = _os.getcwd() + '/robotcz/'

# Složka se soubory ikon robotů
ROBOTS_ICON_DIRECTORY = _robot_dir + 'IMGR/'
dbg.prDB(2, f'=== {ROBOTS_ICON_DIRECTORY = }')
# Znaky charakterizující jednotlivé barvy robotů
ROBOTS_COLOR_CHARS = [
    "K",  # 000 = Black
    "B",  # 001 = Blue
    "R",  # 010 = Red
    "M",  # 011 = Magenta
    "G",  # 100 = Green
    "C",  # 101 = Cyan
    "Y",  # 110 = Yellow
    "W"   # 111 = White
]
# Koncovky názvů souborů s ikonami robotů natočených do daných směrů
DIRECTION_EXTENSIONS = [
    "_EAST.gif",   "_NORTH.gif",   "_WEST.gif",   "_SOUTH.gif"
]
# Ikony reprezentující různě natočené roboty různých barev
ROBOT_LOOKS = [#tk.PhotoImage()
               Icon(ROBOTS_ICON_DIRECTORY + col + dir)
               for col in ROBOTS_COLOR_CHARS
               for dir in DIRECTION_EXTENSIONS ]
# for i, f in enumerate(ROBOT_LOOKS): print(f'{i:2}: {f.file}')

# Složka se soubory ikon polí se zdí či různými počty značek
FIELDS_ICON_DIRECTORY = _robot_dir + 'IMGF/'
# Názvy souborů s ikonami polí se zdí či různými počty značek
MARKER_ICON_FILENAMES = [
     "0.gif",  "1.gif",  "2.gif",  "3.gif",  "4.gif",
     "5.gif",  "6.gif",  "7.gif",  "8.gif",  "9.gif",
    "C0.gif", "C1.gif", "C2.gif", "C3.gif", "C4.gif",
    "C5.gif", "C6.gif", "C7.gif", "C8.gif", "C9.gif",
    "BrickWall.gif"
]
# Ikony reprezentující pole se zdí či různými počty značek
FIELD_FILES = [FIELDS_ICON_DIRECTORY + texture
               for texture in MARKER_ICON_FILENAMES]
FIELD_LOOKS = [tk.PhotoImage(file=FIELDS_ICON_DIRECTORY + texture)
               for texture in MARKER_ICON_FILENAMES ]

# Počet možných barev robotů (každá barva má dva reprezentanty)
COLORS = len(ROBOTS_COLOR_CHARS)

# Počet možných směrů natočení robotů (každý směr má dva reprezentanty)
DIRECTIONS = len(DIRECTION_EXTENSIONS)

# Počet souborů s ikonami polí s různými počty značek a zdí
MARKERS = len(MARKER_ICON_FILENAMES)

# Index názvu souboru s ikonou reprezentující zeď
WALL_INDEX = MARKERS -1

title = "World of robots"


# Exportované atributy
__all__ = ['RobotWindow', 'MARKERS',
           'create_window_for'
           ]


###########################################################################q
dbg.stop_mod(2, __name__)
