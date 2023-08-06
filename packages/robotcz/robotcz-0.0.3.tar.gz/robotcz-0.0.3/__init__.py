#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
#P:/70_INP/robotcz/__init__.py
"""Realizuje svět robota Karla.¤
Je určen jako vyučovací pomůcka pro výklad
algoritmických konstrukcí a základů OOP.
Verze 1.00.8885_2022-01-22
"""
import dbg; dbg.start_pkg(2, __name__, __doc__, new_line=False)
###########################################################################q

# Konstanta určující hlavní paradigma - to ovlivňuje,
# zda budou na konci modulu exportovány třídy nebo funkce.
OO_PARADIGM = False


###########################################################################q

from enum   import IntEnum
from .      import IO



###########################################################################q

class Color(IntEnum):
    """Výčtový typ definující 8 základních RGB barev.
    Lze je zadat jak plným, tak jednoznakovým názvem.
    """
    BLACK   = 0
    BLUE    = 1
    RED     = 2
    MAGENTA = 3
    GREEN   = 4
    CYAN    = 5
    YELLOW  = 6
    WHITE   = 7

# Implicitní barva přidávaného robota.
DEFAULT_COLOR = Color.BLUE



###########################################################################q

class Direction4(IntEnum):
    """Výčtový typ definující 4 hlavní světové strany.
    Lze je zadat jak plným, tak jednoznakovým názvem.
    """
    EAST  = 0   # Východ - doprava
    NORTH = 1   # Sever  - nahoru
    WEST  = 2   # Západ  - doleva
    SOUTH = 3   # Jih    - dolů

    @property
    def dx(self):
        """Vrátí vodorovný přírůstek při přesunu v daném směru."""
        return Direction4._dx[self.value]

    @property
    def dy(self):
        """Vrátí svislý přírůstek při přesunu v daném směru. """
        return Direction4._dy[self.value]

    def turn_left(self) -> 'Direction4':
        """Vrátí směr po otočení o 90°vlevo."""
        return Direction4((self.value + 1) & 0b11)

    def turn_right(self) -> 'Direction4':
        """Vrátí směr po otočení o 90°vpravo."""
        return Direction4((self.value + 3) & 0b11)

    def turn_about(self) -> 'Direction4':
        """Vrátí směr po otočení o 180°."""
        return Direction4((self.value + 2) & 0b11)

# Aby se atributy staly běžnými atributy, musí se dodat dodatečně
Direction4._dx = [1,  0, -1, 0]
Direction4._dy = [0, -1,  0, 1]

# Implicitní směr natočení přidávaného robota
DEFAULT_DIR = Direction4.EAST



###########################################################################q
IKarel:type = None
from typing import Protocol, runtime_checkable

@runtime_checkable
class IKarel(Protocol):
    """Třída definuje protokol pro minimální verzi robota Karla.
    """
    def pick(self) -> IKarel:       """Zvedne značku."""
    def put(self)  -> IKarel:       """Položí značku."""
    def step(self) -> IKarel:       """Posune se na další políčko"""
    def turn_left(self) -> IKarel:  """Otočí se o 90° vlevo."""
    def is_east(self) -> bool:      """Prozradí, je-li otočen na východ."""
    def is_marker(self) -> bool:    """Prozradí, je-li pod ním značka."""
    def is_wall(self) -> bool:      """Prozradí, je-li před ním zeď."""
    def robot_before(self)-> IKarel:"""Vrátí odkaz na robota před ním."""
    def hide(self) -> True:         """Skryje robota a zrychlí."""
    def unhide(self) -> int:        """Vrátí úroveň zobrazování robota."""



###########################################################################q
class Karel():
    """Definuje minimální verzi robota Karla implementující protokol IKarel.
    """
    def __init__(self, row:int =-1,  col:int = 0,
                       dir4 :Direction4 = DEFAULT_DIR,
                       color:Color      = DEFAULT_COLOR,
                       add:bool         = True):
        """Vytvoří roboty s rodným číslem.
        """
        if not active_world():
            raise Exception(
                '\nNelze vytvořit robota - není dostupný svět robotů')
        if add:
            active_world().add_robot(self, row, col, dir4, color)

    def __repr__(self):
        """Vrátí systémový podpis robota zobrazující jeho souřadnice,
        směr natočení, barvu a je-li skryt, tak i úroveň skrytí.
        """
        return active_world().repr(self)

    def pick(self) -> 'Karel':
        """Zvedne značku z políčka, na němž stojí.
        Není-li již na daném políčku žádná značka, ohlásí chybu.
        """
        active_world().pick(self)
        return self

    def put(self) -> 'Karel':
        """Položí značku na políčko, na němž stojí.
        Je-li již na něm maximální povolený počet značek, ohlásí chybu.
        """
        active_world().put(self)
        return self

    def step(self) -> 'Karel':
        """Posune robota na další políčko ve směru, do nějž je natočen.
        Je-li na daném políčku robot nebo zeď, ohlásí chybu.
        """
        active_world().step(self)
        return self

    def turn_left(self) -> 'Karel':
        """Otočí robotem o 90° vlevo.
        """
        active_world().turn_left(self)
        return self

    def is_east(self) -> bool:
        """Vrátí informaci o tom,
        je-li robot otočen na východ.
        """
        return active_world().is_east(self)

    def is_marker(self) -> bool:
        """Vrátí informaci o tom,
        je-li na políčku pod robotem nějaká značka.
        """
        return active_world().is_marker(self)

    def is_wall(self) -> bool:
        """Vrátí informaci o tom,
        je-li na políčku před robotem zeď.
        """
        return active_world().is_wall(self)

    def robot_before(self) -> 'Karel':
        """Je-li na políčku před robotem jiný robot, vrátí odkaz na něj,
        jinak vrátí prázdný odkaz.
        """
        return active_world().robot_before(self)

    def hide(self) -> True:
        """Přestane robota zobrazovat, čímž jeho činnost výrazně zrychlí,
        a vrátí hodnotu True, aby jej bylo možno použít jako podmínku
        v podmíněném příkazu iniciujícím odsazení.
        """
        return active_world().hide(self)

    def unhide(self) -> int:
        """Vrátí úroveň zobrazování do stavy před posledním skrytím.
        Byl-li proto již tehdy skrytý (a tím pádem i zrychlený),
        zůstane skrytý (a zrychlený) i nadále.
        Byl-li zobrazovaný, začne se opět zobrazovat.
        Vrátí aktuální hloubku potlačování zobrazení.
        """
        return active_world().unhide(self)



###########################################################################q
# Veřejné metody modulu

def new_world(*fields:[int|str]):
    """Případnou existující aktivní instanci světa robotů nejprve deaktivuje.
    Poté vytvoří nový šachovnicový svět.
    Jsou-li zadány celočíselné argumenty, je vytvořen prázdný svět
    se zadaným počtem řádků (první argument) a sloupců (druhý argument).
    Jsou-li zadány stringy, reprezentují jejich znaky jednotlivá políčka.
    Číslo na políčku udává počet značek, znak # označuje zeď.
    Není-li zadán žádný argument, chová se jako po zavolání new_world(10,10).
    """
    # dbg.prSE(0, 1, 'new_world', f'{fields = }')
    if active_world(): active_world().destroy()

    if len(fields)==0:
        # dbg.prSE(0, 0, 'new_world', f'len(fields)==0')
        return new_world(10, 10)    # Rekurzivní volání
    elif isinstance(fields[0], int):
        from .robotworld  import new_empty_world
        new_empty_world(fields[0], fields[1])
    elif isinstance(fields[0], str):
        fields = [fields]
        from .robotworld import new_world as new_rw
        new_rw(*fields)
    else:
        # dbg.prSE(0, 0, 'new_world', f'EXCEPTION'
        #               f'{type(fields[0])=},{fields=} ')
        raise Exception(f'\nNeplatné argumenty volání funkce: '
                        f'new_word{fields}')
    result = active_world()
    from .robotwindow import RobotWindow
    RobotWindow(active_world())
    # dbg.prSE(0, 0, 'new_world', f'{fields = }')
    return result


def active_world() ->'RobotWorld':
    """Vrátí odkaz na aktuálně používaný svět robotů.
    """
    from .robotworld import active_world
    return active_world



###########################################################################q
# Globální atributy



###########################################################################q
# Exportované atributy
if OO_PARADIGM:
    __all__ = ('dbg', 'IO',
               'active_world', 'new_world', 'IKarel', 'Karel',
               'Color', 'Direction4', 'DEFAULT_COLOR', 'DEFAULT_DIR',
              #'RobotWorld', 'RobotWindow', 'IRobotWorldListener',
              #'get_world', 'new_empty_world', 'new_world',
              )
else:
    # Odkazy na hodnoty třídy Color
    BLACK   = Color.BLACK
    BLUE    = Color.BLUE
    RED     = Color.RED
    MAGENTA = Color.MAGENTA
    GREEN   = Color.GREEN
    CYAN    = Color.CYAN
    YELLOW  = Color.YELLOW
    WHITE   = Color.WHITE

    # Odkazy na hodnoty třídy Direction4
    EAST  = Direction4.EAST
    NORTH = Direction4.NORTH
    WEST  = Direction4.WEST
    SOUTH = Direction4.SOUTH

    # Odkazy na metody třídy Karel
    pick         = Karel.pick
    put          = Karel.put
    step         = Karel.step
    turn_left    = Karel.turn_left
    is_east      = Karel.is_east
    is_marker    = Karel.is_marker
    is_wall      = Karel.is_wall
    robot_before = Karel.robot_before
    hide         = Karel.hide
    unhide       = Karel.unhide

    # Definice exportovaných proměnných
    __all__ = ('dbg', 'IO',
        'active_world', 'new_world', 'IKarel', 'Karel',
        'BLACK', 'BLUE', 'RED', 'MAGENTA', 'GREEN', 'CYAN', 'YELLOW', 'WHITE',
        'DEFAULT_COLOR', 'DEFAULT_DIR',
        'EAST', 'NORTH', 'WEST', 'SOUTH',
        'pick', 'put', 'step', 'turn_left',
        'is_east', 'is_marker', 'is_wall', 'robot_before',
        'hide', 'unhide',
    )



###########################################################################q
dbg.stop_pkg(2, __name__)
