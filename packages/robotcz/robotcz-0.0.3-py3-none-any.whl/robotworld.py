#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
#R:/PGM_PYT/p1_00_00a_Module_template.py
"""
Modul definující svět robotů.
Umožňuje přihlášení posluchačů, kteří jej budou zobrazovat,
přičemž na vlastní způsob zobrazení nejsou kladeny žádné požadavky.
"""
import dbg; dbg.start_mod(2, __name__);   MyDBG=0
###########################################################################q

from abc    import ABC, abstractmethod
from typing import Protocol, runtime_checkable

from . import IO
from . import Color
from . import Direction4
from . import IKarel
from . import DEFAULT_COLOR
from . import DEFAULT_DIR



###########################################################################q
# Konstanty modulu:

# Délka čekání po kroku a otočce.
PAUSE = 300

# Implicitní velikost světa robotů = implicitní počet řádků a sloupců.
DEFAULT_SIZE = 10

# Maximální povolený počet značek na jednom políčku světa robotů.
MAX_MARKERS = 19

# Znak reprezentující zeď při zadávání světa stringy.
WALL_CHAR = '#'

# Číslo reprezentující přítomnost zdi na daném políčku.
WALL = MAX_MARKERS + 1

# Základ číselné soustavy pro převod znaků na čísla představující
# počet značek na daném políčku.
RADIX = 36



###########################################################################q
# Proměnné modulu:

# Aktuální (a současně jediná platná) instance světa.
# Není-li, tak prázdný odkaz.
active_world:'RobotWorld' = None



###########################################################################q

@runtime_checkable
class IRobotWorldListener(Protocol):
    """Třída definuje protokol, jenž mají splňovat posluchači událostí
    ve světě robotů, kteří následně zobrazují jeho aktuální stav.
    """

    def repaint(self, fields:[[int]], robots:['WRobot']) -> None:
        """Hlášení o změně ve světě robota vyžadující jeho překreslení.
        """

    def release(self):
        """Oznámení o konci světa robota a z toho plynoucí povinnosti
        uvolnit blokované zdroje.
        """



###########################################################################q
class WRobot:
    """Instance slouží jako zástupci jednotlivých robotů v robotím světě.
    Pamatují si svoje charakteristiky: pozici, směr, barvu a hladinu skrytí.
    """
    count = 0

    def __init__(self, world:'RobotWorld', robot:IKarel,
                 row:int, col:int, dir4:Direction4, color:Color):
        """Vytvoří zástupce robota zadané barvy umístěného na zadaném místě
        a otočeného do zadaného směru.
        """
        WRobot.count += 1
        self.ID = WRobot.count  # Pořadí přihlášeného robota
        self._robot  = robot    # Zastupovaný robot
        self._hidden = 0        # Hladina skrytí
        self._world  = world    # Svět, v němž se robot pohybuje
        # Dále se iniciují běžné a zobrazované charakteristiky
        self._row    = self._vrow  = row    # Řádek
        self._col    = self._vcol  = col    # Sloupec
        self._dir4   = self._vdir4 = dir4   # Směr natočení
        self._color  = color                # Barva - ta se nemůže změnit

    @property
    def color(self) -> Color:
        """Vrátí barvu zadaného robota.
        """
        return self._color

    @property
    def dir4(self) -> Direction4:
        """Vrátí aktuální směr natočení zadaného robota.
        """
        return self._dir4

    @property
    def col(self):
        """Vrátí sloupec v němž se daný robot aktuálně nachází.
        """
        return self._col

    @property
    def row(self):
        """Vrátí řádek v němž se daný robot aktuálně nachází.
        """
        return self._row

    @property
    def vdir4(self) -> Direction4:
        """Vrátí aktuálně zobrazovaný směr natočení zadaného robota.
        """
        return self._vdir4

    @property
    def vcol(self):
        """Vrátí sloupec v němž se daný robot aktuálně zobrazuje.
        """
        return self._vcol

    @property
    def vrow(self):
        """Vrátí řádek v němž se daný robot aktuálně zobrazuje.
        """
        return self._vrow

    def show(self):
        """Nastaví zobrazovací parametry zadaného robota,
        a zobrazí aktuální stav světa robotů.
        """
        if self._hidden == 0:
            self._vcol  = self._col
            self._vrow  = self._row
            self._vdir4 = self._dir4
            self._world.repaint()
            IO.pause(PAUSE)

    def __repr__(self):
        """Vrátí textový podpis identifikující zastupovaného robota.
        """
        hidden = f', hidden={self._hidden}' if self._hidden else ''
        result = (f'{self._robot.__class__.__name__}_{self.ID}('
                  f'row={self._row}, col={self._col}, '
                  f'dir4={self._dir4.name}, color={self._color.name}'
                  f'{hidden})')
        return result



###########################################################################q
class RWError(Exception):
    """Výjimka informující o chybě ve světě robotů.
    Jejíž initor nejprve zobrazí dialogové okno se zprávou, a teprve pak
    dotvoří objekt klasické výjimky se zápisem na standardní výstup.
    Zobrazení dialogového okna je možno ovlivnit.
    """
    show_dialog = True

    def __init__(self, message:str):
        """Má-li to povoleno, zobrazí dialogové okno se zprávou,
        a poté vyhodí standardní výjimku s toutéž zprávou.
        """
        message = '\n' + message
        if RobotError.show_dialog:
            IO.inform(f'Vyhozena výjimka!{message}')
        super().__init__(message)



###########################################################################q
class RobotError(RWError):
    """Výjimka informuje o stavu robota, který ji vyvolal.
    """

    def __init__(self, robot:WRobot, message:str):
        msg = f'{robot}\n{message}'
        super().__init__(msg)



###########################################################################q
class RobotWorld:
    """Instance třídy {@code RobotWorld} reprezentuje svět robotů
    koncipovaný jako šachovnice, na jejíž pole je možno pokládat značky.
    Svět si pamatuje roboty, kteří se v něm vyskytují,
    spolu s jejich pozicemi a natočeními
    a dokáže je prostřednictvím přihlášených posluchačů zobrazit.
    """

    counter:int = 0

    def __init__(self, fields:[[int]]):
        """Vytvoří nový svět s velikostí a počtem značek
        na jednotlivých polích definovaným argumentem fields.
        """
        RobotWorld.counter = RobotWorld.counter+1
        self.ID      = RobotWorld.counter
        self._fields = fields       # Počty značek na jednotlivých políčcích
        self._rows   = len(fields)  # Počet řádků dvorku
        self._cols   = len(fields[0])#Počet sloupců dvorku
        self._robots    = {}        # Mapa robotů na jejich zástupce
        self._listeners = []        # Posluchači událostí ve světě robotů

    def __repr__(self):
        """Podepíše svět jeho rozměrem, počtem uchovávaných robotů
        a informací o jeho živosti.
        """
        global active_world
        active = active_world is self
        r = (f'RobotWorld(ID={self.ID}, '
             f'rows={self._rows}, cols={self._cols}, ' 
             f'robots={len(self._robots)}{"" if active else ", NEAKTIVNÍ"})'
            )
        return r

    @property
    def cols(self) -> int:
        """Počet sloupců světa (dvorku).
        """
        self._check_world_alive()
        return self._cols

    @property
    def rows(self) -> int:
        """Počet řádků světa (dvorku).
        """
        self._check_world_alive()
        return self._rows

    @property
    def fields(self) -> [[int]]:
        """Matice s počty značek, resp. příznaky zdi na jednotlivých polích.
        """
        self._check_world_alive()
        return [row[:] for row in self._fields]

    @property
    def robots(self) -> [WRobot]:
        """Pole zástupců robotů přítomných ve světě.
        """
        self._check_world_alive()
        return list(self._robots.values())

    def repr(self, robot:IKarel) -> str:
        """Vrátí systémový podpis wrobota reprezentujícího zadaného robota.
        """
        self._check_world_alive()
        if (wr := self._robots.get(robot)):
            return wr.__repr__()
        else:
            return (f'Robot {id(robot)} není přítomen v aktuálním světě' 
                    f' - nejde tedy podepsat')

    def add_listener(self, listener:IRobotWorldListener) -> None:
        """Přidá zadaného posluchače.
        """
        if isinstance(listener, IRobotWorldListener):
            self._check_world_alive()
            self._listeners.append(listener)
        else:
            RWError(f'Zadaný posluchač neimplementuje protokol '
                    f'IRobotWorldListener\n     {listener = }')

    def remove_listener(self, listener:IRobotWorldListener) -> None:
        """Odebere zadaného posluchače.
        """
        self._check_world_alive()
        self._listeners.remove(listener)

    def add_robot(self, robot:IKarel, row:int=-1, col:int=0,
                        dir4:Direction4 = DEFAULT_DIR,
                        color:Color     = DEFAULT_COLOR) -> None:
        """Přidá zadaného robota mezi spravované a zobrazované,
        umístí jej a natočí.
        """
        # dbg.prSE(MyDBG, 1, 'add_robot')
        if not isinstance(robot, IKarel):
            RWError(f'Přidávaný robot neimplementuje protokol IKarel'
                    f'     {robot = }')
        msg = lambda arg, type: f'\nArgument {arg} není typu {type}'
        assert isinstance(robot, IKarel), \
               "\nTyp argumentu robot neimplementuje protokol IKarel"
        assert isinstance(row,   int),          msg('row',   int)
        assert isinstance(col,   int),          msg('col',   int)
        assert isinstance(dir4,  Direction4),   msg('dir4',  Direction4)
        assert isinstance(color, Color),        msg('color', Color)
        self._check_world_alive()
        if self._robots.get(robot):
            raise RobotError(self._robots.get(robot),
                  "Zadaný robot je již přítomen")
        if row<0:  row = self._rows + row
        if col<0:  col = self._cols + col
        if self._is_field_free(row, col):
            wrobot = WRobot(active_world, robot, row, col, dir4, color)
            self._robots[robot] = wrobot
            wrobot.show()
        else:
            block = "ZEĎ" if self._fields[row][col] == WALL \
                        else self._robot_on(row, col)

            IO.inform(f'Nelze přidat zadaného robota\n'
                      f'na poli [{row}, {col}] je {block}')
        # dbg.prSE(MyDBG, 0, 'add_robot')

    def remove_robot(self, robot:IKarel) -> None:
        """Odebere zadaného robota z množiny spravovaných a zobrazovaných.
        """
        self._check_world_alive()
        if self._robots.get(robot):
            del self._robots[robot]
        else:
            msg = f'Robot není přítomen, takže nejde odebrat: {robot}'
            raise RWError(msg)

    def destroy(self) -> None:
        """Je-li daný svět aktuálním světem, umrtví jej.
        V opačném případě neudělá nic, protože svět je již umrtven.
        """
        if active_world == self:
            destroy_world(self)

    def is_east(self, robot:IKarel) -> bool:
        """Vrátí informaci o tom, je-li robot otočen na východ.
        """
        self._check_world_alive()
        wrobot = self._robots[robot]
        result = (wrobot._dir4 == Direction4.EAST)
        return result

    def is_marker(self, robot:IKarel) -> bool:
        """Vrátí informaci o tom, je-li na políčku pod robotem značka.
        """
        self._check_world_alive()
        wrobot = self._robots[robot]
        result = self._fields[wrobot._row][wrobot._col]
        return result > 0

    def is_wall(self, robot:IKarel) -> bool:
        """Vrátí informaci o tom, je-li na políčku před robotem zeď.
        """
        self._check_world_alive()
        wrobot = self._robots[robot]
        col    = wrobot._col + wrobot._dir4.dx
        row    = wrobot._row + wrobot._dir4.dy
        result = ((col < 0)  or  (col >= self._cols)
               or (row < 0)  or  (row >= self._rows)
               or (self._fields[row][col] == WALL) )
        return result

    def robot_before(self, robot:IKarel) -> IKarel:
        """Je-li na políčku před robotem jiný robot, vrátí odkaz na něj,
        jinak vrátí prázdný odkaz.
        """
        # dbg.prSE(MyDBG,1, 'RobotWorld.robot_before', f'({robot})')
        # Součástí testu na zeď je i kontrola živosti světa robotů
        if self.is_wall(robot):
            # dbg.prSE(MyDBG,0, 'RobotWorld.robot_before', f'None - Je tam zeď')
            return None
        wrobot = self._robots[robot]
        col    = wrobot._col + wrobot._dir4.dx
        row    = wrobot._row + wrobot._dir4.dy
        result = self._robot_on(row, col)
        # dbg.prSE(MyDBG,0, 'RobotWorld.robot_before', f'{result = }')
        return result

    def pick(self, robot:IKarel) -> None:
        """Je-li na políčku robota alespoň jedna značka, zvedne ji,
        není-li tam, vyhodí výjimku.
        """
        self._check_world_alive()
        wrobot = self._robots[robot]
        markers = self._fields[wrobot._row][wrobot._col]
        if markers > 0:
            self._fields[wrobot._row][wrobot._col] -= 1
        else:
            raise RobotError(wrobot,
                             "\nNa poli nejsou žádné značky")

    def put(self, robot:IKarel) -> None:
        """Položí na políčko  pod zadaným robotem značku.
        Je-li tam již plno, vyhodí výjimku.
        """
        self._check_world_alive()
        wrobot = self._robots[robot]
        markers = self._fields[wrobot._row][wrobot._col]
        if markers < MAX_MARKERS:
            self._fields[wrobot._row][wrobot._col] += 1
        else:
            raise RobotError(wrobot,
                             "\nNa pole již nelze přidat další značku.")

    def step(self, robot:IKarel) -> None:
        """Přesune zadaného robota o políčko vpřed.
        """
        # dbg.prSE(MyDBG, 1, 'RobotWorld.step', f'{self._robots[robot]}')
        wrobot = self._robots[robot]
        col = wrobot._col + wrobot._dir4.dx
        row = wrobot._row + wrobot._dir4.dy
        self._move_to(row, col, wrobot)
        # dbg.prSE(MyDBG, 0, 'RobotWindow.step', f'{self._robots[robot]}')

    def turn_left(self, robot:IKarel) -> None:
        """Otočí zadaného robota o 90° vlevo.
        """
        # dbg.prSE(MyDBG, 1, 'RobotWorld.turn_left', f'{self._robots[robot]}')
        wrobot       = self._robots[robot]
        wrobot._dir4 = wrobot._dir4.turn_left()
        wrobot.show()
        # dbg.prSE(MyDBG, 0, 'RobotWindow.turn_left', f'{self._robots[robot]}')

    def hide(self, robot:IKarel) -> True:
        """Přestane robota zobrazovat, čímž jeho činnost výrazně zrychlí,
        a vrátí hodnotu True, abz jej bylo možno použít jako podmínku
        v podmíněném příkazu iniciujícím odsazení.
        """
        wrobot = self._robots[robot]
        wrobot._hidden += 1
        return True

    def unhide(self, robot:IKarel) -> int:
        """Vrátí úroveň zobrazování do stavy před posledním skrytím.
        Byl-li proto již tehdy skrytý (a tím pádem i zrychlený),
        zůstane skrytý (a zrychlený) i nadále.
        Byl-li zobrazovaný, začne se opět zobrazovat.
        Vrátí aktuální hloubku potlačování zobrazení..
        """
        wrobot = self._robots[robot]
        wrobot._hidden -= 1
        if wrobot._hidden < 0:
            raise RobotError(wrobot,
                  '\nZadanému odkrytí neodpovídá žádné zakrytí.')
        if wrobot._hidden == 0:
            wrobot.show()
        return wrobot._hidden

    def repaint(self):
        """Oznámí všem přihlášeným posluchačům, že se svět změnil,
        a je proto třeba jej překreslit.
        """
        for l in self._listeners:
            l.repaint(self._fields, list(self._robots.values()))


    ### nezveřejňované metody ##############################################

    def _checkInside(self, row:int, col:int) -> None:
        """Prověří, že daný svět je aktivní
        a že zadaná souřadnice je uvnitř něj.
        """
        self._check_world_alive()
        if (col<0  or  row<0  or  col>=self._cols  or  row>=self._rows):
            msg = f'Pozice [{row}, {col}] není uvnitř světa robotů'
            raise RWError(msg)

    def _check_world_alive(self) -> None:
        """Prověří, je-li daný svět tím aktuálním.
        """
        if active_world != self:
            msg = "Daný svět robotů byl již odstraněn"
            raise RWError(msg)

    def _is_field_free(self, row:int, col:int) -> bool:
        """Vrátí informaci o tom, je-li možno na pole dosadit robota.
        """
        # dbg.prSE(MyDBG, 1, '_is_field_free', f'{row=}, {col=}')
        # dbg.prMatI('_fields', self._fields)
        self._check_world_alive()
        self._checkInside(row, col)
        result = (not ((self._fields[row][col] == WALL)  or
                       (self._robot_on(row, col)      )  ))
        # dbg.prSE(MyDBG, 0, '_is_field_free',  f'{result=}')
        return result

    def _move_to(self, row:int, col:int, wrobot:WRobot):
        """Přesune zadaného robota na zadanou pozici.
        """
        # dbg.prSE(MyDBG, 1, 'RobotWorld._move_to', f'{wrobot}')
        if not self._is_field_free(row, col):
            object = ('zeď' if self._fields[row][col] == WALL
                            else 'jiný robot')
            raise RWError(f'Na pole [{row}, {col}] nelze vstoupit, '
                          f'je na něm {object}.')
        wrobot._row = row
        wrobot._col = col
        wrobot.show()
        # dbg.prSE(MyDBG, 0, 'RobotWorld._move_to', f'{wrobot}')

    def _robot_on(self, row:int, col:int) -> IKarel:
        """Vrátí robota na zadaném poli; není-li tam žádný, vrátí None.
        """
        # dbg.prSE(MyDBG,1, 'WRobot._robot_on', f'({row=}, {col=})')
        # dbg.prIN(MyDBG, dbg.prSeq(self._robots.values(),prn=False))
        self._checkInside(row, col)
        for robot, wrobot in self._robots.items():
            if wrobot._row==row  and  wrobot._col==col:
                # dbg.prSE(MyDBG,0, 'WRobot._robot_on', f'= {robot}')
                return robot        #==========>
        # dbg.prSE(MyDBG,0, 'WRobot._robot_on', f'None - Žádný tam není')
        return None



###########################################################################q
# Veřejné metody modulu

def get_world() -> 'RobotWorld':
    """Vrátí aktuální instanci světa robotů;
    pokud žádná neexistuje, vrátí None.
    """
    return active_world


def new_empty_world(rows:int, cols:int) -> 'RobotWorld':
    """Pokud žádná aktivní instance světa robotů neexistuje, vytvoří
    svět se zadaným počtem řádků a sloupců s políčky bez značek.
    Počet řádků i sloupců musí být kladný.
    """
    return create_world(
           [[0 for c in range(cols)] for r in range(rows)])


def new_world(world:[str]) -> 'RobotWorld':
    """Pokud žádná aktivní instance světa robotů neexistuje, vytvoří
    šachovnicový svět, obsah jehož políček je definován znaky
    ve strinzích ze zadaného seznamu.
    Seznam nesmí být prázdný a délky stringů musejí být shodné
    """
    result = create_world(
             [[c2i(chr) for chr in row] for row in world])
    return result


def destroy_world(world:RobotWorld):
    """Zruší aktuální svět, aby bylo možno vytvořit nový.
    Při té příležitosti oznámí všem posluchačům, že se svět ruší
    a že mají uvolnit všechny blokované zdroje.
    Pokud žádný aktuální svět neexistuje, neudělá nic.
    """
    global active_world
    if active_world == None:   return
    if active_world != world:
        raise RWError('Pokus o zrušení jiného než aktivního světa')
    active_world._robots = {}
    for listener in active_world._listeners:
        listener.release()
    active_world = None



###########################################################################q
# Neveřejné metody modulu

def c2i(c:str) -> int:
    """Převede znak reprezentující počet značek nebo zeď
    na odpovídající celé číslo.
    """
    if c == WALL_CHAR:
        m = WALL
    else:
        try:
            if   c == ' ' :    c = '0'
            elif c == '.' :    c = '1'
            elif c == ':' :    c = '2'
            elif c == '…' :    c = '3'  # '\u2026' - Alt+0133
            elif c == '∷' :    c = '4'  # '\u2237' - Alt+08759
            m = int(c, RADIX)
        except Exception as ex:
            code = ('není pouhý znak'
                    if (not isinstance(c,str))  or  (len(c) != 1)
                    else f's kódem {hex(ord(c))}')
            msg = f'\nNečekaný argument "{c}" {code}'
            raise RWError(msg)
    return m


def create_world(fields:[[int]]) -> 'RobotWorld':
    """Pokud žádná aktivní instance světa robotů neexistuje,
    vytvoří svět s definovaným obsahem.
    Pokud aktivní svět existuje, vyhodí výjimku.
    """
    # dbg.prSE(MyDBG, 1, 'robotworld.create_world', f'{fields = }')
    global active_world
    if active_world:
        msg = ("Aktivní svět robotů již existuje a smí být jen jeden.\n"
               "Před vytvořením nového musíte zrušit ten původní")
        raise RWError(msg)
    active_world = RobotWorld(fields)
    # dbg.prSE(MyDBG, 0, 'robotworld.create_world', f'{active_world=}')
    return active_world


import typing
###########################################################################q
dbg.stop_mod(2, __name__)
