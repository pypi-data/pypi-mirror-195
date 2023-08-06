#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó

"""Pomocný modul pro nastavování hladiny kontrolních tisků,
kontrolní tisky a případné další služby spojené s laděním.¤
Protože jsou funkce spojené s laděním, nemají dlouhé
samovysvětlující názvy, ale byla dána přednost krátkým
zkratkovým názvům, přičemž v dokumentačních komentářích
funkcí je podoba názvu vždy vysvětlena.

Definované proměnné:
    DBG     - Nastavení hladiny kontrolních tisků
    TST     - Indikace testovacího režimu
    PKG_DOC - Zda se bude u balíčků tisknout celý dokumentační komentář
              Uplatní se pouze u tisků na samostatný řádek
    CWD     - Zda se bude za zmínkou o importu tohoto modulu
              tisknout i current working directory
    INPUTS  - N-tice stringů s uloženými očekávanými vstupy z klávesnice
              pro ladění komunikace programu s uživatelem prostřednictvím
              funkce input()
    input_index - Index vstupu, který má být následně použit
    dbg_level   - Hladiny DBG, od níž se začnou tisknout úvodní a závěrečné
                  tisky i pro tento modul
    print_cwd   - Zda má být součástí úvodních tisků i informace
                  o aktuální pracovní složce

"""
DBG = 0     # Nastavení hladiny kontrolních tisků
TST = 0     # Indikace testovacího režimu True/False pro funkci input
PKG_DOC = 1 # Zda se bude u balíčků tisknout celý dokumentační komentář
            # Uplatní se pouze u tisků na samostatný řádek

#Proměnná INPUTS slouží k uložení očekávaných vstupů z klávesnice
#Zadávané vstupy vloží testovaný program jako stringy oddělené čárkami
INPUTS = ()
input_index = 0

# Nastavení hladiny pro tisk kontrolních tisků tohoto modulu
dbg_level = 2   # Hladina DBG, při jejímž dosažení či překročení se tiskne
                # zpráva o vlastním zavedení
print_cwd = 1   # Zda se bude za zmínkou o zavádění tohoto modulu
                # tisknout i current working directory

# from dbg import *
if DBG >= dbg_level:
    print(f'===== Modul {__name__} ===== START')
    if print_cwd: import os; print(f'      {os.getcwd()}')
###########################################################################q

def input(prompt: str) -> str:
    """Náhražka zabudované funkce input() umožňující
    testování konverzace s uživatelem prostřednictvím konzoly.
    """
    if TST:
        global input_index, INPUTS
        prDB(2, f'===== dbg: Požadován vstup z klávesnice:\n'
                f'   {input_index = }\n'
                f'   {INPUTS = }')
        print(prompt, end='')
        if input_index >= len(INPUTS):
            msg = ('Bylo zadáno málo vstupních textů - požadován text '
                  f's indexem {input_index}\n{INPUTS = }')
            raise Exception(msg)
        result = INPUTS[input_index]
        print(result)
        input_index += 1
        return result
    else:
        import builtins
        return builtins.input(prompt)


def END(name: str) -> None:
    """Funkce volaná na závěr aplikací komunikujících s uživatelem.
    prostřednictvím klávesnice.
    Očekává argument se jménem volajícího modulu
    """
    import builtins
    return builtins.input(f'===== KONEC APLIKACE V MODULU {name} =====')


def refer_inputs() -> None:
    """Vytiskne načtená vstupy a aktuální index.
    """
    print(f'Aktuální stav emulátoru klávesnice: {input_index = }\n'
           f'        {INPUTS = }')


def confirm(msg:str) -> None:
    """Vypíše zadanou zprávu a požádá o potvrzení pokračování.
    """
    answer = input(f'{msg} - Pokračovat?')
    if answer != '':
        raise Exception('Zažádáno o ukončení')



###########################################################################q

def first_max(max_chars:int=70, text:str='') -> str:
    """Vrátí první řádek zadaného textu, ale nejvýše max znaků.
    Je-li první řádek prázdný, pracuje s druhým řádkem.
    """
    line_end = text.find('\n')
    if (line_end == 0) and (len(text)>1): #První řádek je prázdný
        text     = text[1:]     # Začneme od druhého
        line_end = text.find('\n')
    chars = min(max_chars, line_end if line_end>0 else len(text))
    return text[:chars]


def start_pkg(level: int, name: str, doc: str = '',
              new_line=True, end_char='¤') -> None:
    """Funkce vytiskne informaci o zavádění balíčku spolu s textem
    zadaným v argumentu doc, kam se většinou zadává __doc__.
    Argument new_line určuje, bude-li se tento řádek tisknou
    na samostatném řádku (True) nebo hned za názvem balíčku (False).
    Argument end_char definuje znak ukončující text k tisku.
    Implicitní hodnotou je znak ¤.
    """
    def indented_lines(start:str, txt:str, end_char='¤') -> str:
        """Vrátí zadaný text, přičemž každý řádek bude začínat
        zadaným separátorem.
        """
        index = txt.find(end_char)
        if index > 0: txt = txt[:index]
        lines = txt.splitlines()
        if lines[0].strip() == '': lines.pop(0)
        result = ''.join(start + line for line in lines)
        return result

    if doc == '':
        msg = ''
    else:
        if new_line:
            sep   = '\n      '
            if PKG_DOC:
                msg = indented_lines(sep, doc, end_char)
            else:
                msg = f' - {first_max(72, doc)}'
            chars = 72
        else:
            msg = f' - {first_max(61 - len(name), doc)}'
    prDB(level, f'##### Balíček {name}{msg}')


def stop_pkg(level: int, name: str, txt:str='') -> None:
    """Funkce vytiskne informaci o ukončení zavádění initoru balíčku.
    """
    prDB(level, f'===== Balíček {name} ===== STOP {txt}')


def start_mod(level: int, name: str, txt:str='') -> None:
    """Funkce vytiskne informaci o počátku zavádění modulu.
    """
    prDB(level, f'+++++ Modul {name} ===== START {txt}')


def stop_mod(level: int, name: str, txt:str='') -> None:
    """Funkce vytiskne informaci o ukončení zavádění modulu.
    """
    prDB(level, f'===== Modul {name} ===== STOP {txt}')



###########################################################################q

def nsan(lst:list[str]) -> list[str]:
    """Očekává seznam názvů atributů a vrátí seznam těch,
    které nezačínají a nekončí dvojicí podtržítek.
    Název je zkratkou z Not System Attribute Names
    """
    l = [s for s in lst if len(s)<=4
                        or (s[:2]  != '__'  and  s[-2:] != '__')]
    return l


def prDB(level, *args, sep=' ', end='\n', file=None) -> None:
    """Realizuje pomocné tisky při ladění pouze v případě,
    když je počáteční argument větší nebo rovna hodnotě DBG.
    Ostatní argumenty odpovídají standardní funkci print()"""
    if DBG >= level:
        print(*args, sep=sep, end=end, file=file)


def prSE(level:int, se:bool, caller:str, msg:str= '') -> str:
    """Vytiskne oznámení o startu, resp. konci provádění funkce,
    která ji zavolala.
       level  = hodnota DBG, od níž se bude tisknout
       se     = příznak tisku startu (True) či ukončení (False) těla metody
       caller = Identifikace volajícího - většinou metody či funkce
       msg    = Případná zpráva za vlastním oznámením
       Vrací doporučený odsazovací string pro následující tisky
    Mnemonika: print at Start and End
    """
    if DBG < level:   return prSE.indent    # ==========>
    if not se:
        prSE.level -= 1  # Trasovaná metoda končí, zmenšuji odsazení
        prSE.indent = prSE.level * prSE.inc
    print(f'{prSE.indent}{prSE.start if se else prSE.end}{caller}'
          f'{ " - " + msg if len(msg)>0 else ""}')
    if se:
        prSE.level += 1  # Zvětšuji odsazení pro nižší hladinu
        prSE.indent = prSE.level * prSE.inc
    return prSE.indent
# Definice atributů předchozí funkce
prSE.level = 0      # Hladina vnoření pro nastavení odsazení
prSE.indent= ''     # Aktuální text odsazení pro znázornění hladiny volání
prSE.inc   = '|   ' # Přírůstek odsazení pro zvětšení hloubky vnoření
prSE.start = '==> ' # Indikace volání funkce
prSE.end   = '<== ' # Indikace návratu z funkce


def prIN(level:int, msg:str='', q:bool=False) -> None:
    """Vytiskne zadanou zprávu s odsazením nastaveným funkcí prSE.
    Mnemonika: print inside Start and End.
    Parametr q řídí, jestli se po vytištění zprávy má zobrazit otázka,
    zda se má v programu pokračovat.
    """
    if DBG < level:   return   # ==========>
    lines = msg.splitlines()
    for line in lines:
        print(prSE.indent, line, sep='')
    if q: input('\nPokračovat?')


def prItLn(iter:'iterable', msg=''):
    """Vytiskne prvky iterovatelného objektu každý na samostatný řádek.
    Je-li v parametru msg zadána zpráva, vytiskne ji, za ní vytiskne
    první řádek textu a další řádky odsadí o délku zprávy.
    Mnemonika: print Iterable with new lines
    """
    if len(msg) > 0:
        print(msg, end='')
    indent = ''
    for o in iter:
        print(indent, o, sep='')
        indent = len(msg)*' '


def prIndLim(text:str, data:object,
             shift=1, limit:int=70, end='') -> str:
    """Vrátí zadaný text následovaný uživatelským podpisem objektu data,
    který se pokusí zalomit na hranicích slov tak, aby délka řádku
    nepřesáhla zadaný limit, přičemž případné následující řádky podpisu
    odsazuje tak, aby byly zarovnané pod začátkem prvního.
    V atributu shift lze zadat, o kolik budou následující řádky ještě
    odsazeny, aby se text posunul např. za otevírací závorku kontejneru.
    String v argumentu end je přidán na závěr vygenerovaného textu
    Mnemonika: print with indent and limit
    """
    # prSE(3, 1, 'prIndLim', f'{shift=}, {limit=}, {text=}')
    lst = []    # Seznam tisknutých textů
    def rest(words:list[str], start:int, length:int) -> int:
        """Vezme ze seznamu words postupně další prvky počínaje prvkem
        s indexem start a skládá a přidává je do seznamu lst vnější funkce.
        Zastaví s okamžiku, kdy by po přidání dalšího textu přidal více
        než length znaků. Vrátí index prvního nepřidaného prvku,
        tj. index, od nějž by se mělo příště začít.
        :param words:   seznam tištěných slov
        :param start:   index, od nějž začínáme
        :param length:  délka vytvářeného textu
        :return:        index prvního nepřidaného prvku
        """
        sum = len(words[start])
        while ...:
            nonlocal lst
            lst.append(words[start])
            start += 1
            if start >= len(words):
                return start
            sum += len(words[start]) +1
            if sum > length:
                return start
            lst.append(' ')
    indent = len(text) + shift      # Posun o otevírací závorku kontejneru
    spaces = '\n'  +  indent * ' '  # Zarovnání levého okra dalších řádků
    words  = str(data).split()
    max    = limit - indent         # Počet znaků do konce řádku
    index  = 0
    while ...:
        if index >= len(words):     # Seznam je vyčerpán
            break                   # ---------->
        index = rest(words, index, max) # Přidá další řádek
        if index < len(words):      # Budeme ještě přidávat
            lst.append(spaces)      # Odřádkujeme a odsadíme
    result = text + ''.join(lst) + end
    # prSE(3, 0, 'prIndLim', f'{len(result)=}')
    return result


def prDict(d=None, dict=False, syst=False, msg='', mod=False, prn=True):
    """Vytiskne položky jmenného prostoru zadaného objektu,
    každou na samostatný řádek.
    d    - objekt, jehož atribut __dict__ se bude tisknout,
           resp. slovník, který se bude tisknout
    dict - True oznamuje, že je zadán slovník, False běžný objekt
    syst - budou-li se tisknout i systémové položky.
    msg  - Případná zpráva uvozující celý tisk
    mod  - Je-li zadán, bude se tisknout __dict__ modulu objektu
           zadaného v argumentu d. Ten však musí mít atribut __module__.
    prn  - Zda se bude vytvářený string tisknout
    """
    if not d:
        import __main__
        d = __main__
    elif mod:
        from importlib import import_module
        m = import_module(d.__module__)
        d = m
    if (dict):
        dd = d
        t  = 'Obsah slovníku'
    else:
        dd = d.__dict__
        t  = 'Atributy objektu'
        if msg=='':  msg = str(d)
    result = f'##### {t}: {msg}\n'
    for k, v in dd.items():
        if (syst  or  not k.startswith('__')):
            result += f"{k} = {v}\n"
    if prn: print(result)
    return  result


def prSeq(seq, prn=True) -> str:
    """Vyrobí string s indexovanými položkami zadané posloupnosti
    na jednotlivých řádcích;
    je-li prn=True, tak string vytiskne, poté string vrátí.
    """
    if seq: result = '\n'.join([f'{i}: {item}'
                               for i, item in enumerate(seq)])
    else  : result = (None if seq==None else '<Empty>')
    if prn : print(result)
    return result


def prMatI(msg:str, mat:[[int]], pos:int=3, nl:bool=False):
    """Vytiskne zadaný titulek následovaný položkami zadané celočíselné
    matice přičemž pro tisk čísla vyhradí zadaný počet pozic.
    Argument nl definuje, zda se má za nadpisem odřádkovat.
    Odřádkuje-li se, budou se všechny následující řádky odsazovat o 3 mezery.
    """
    indent = ""
    if msg:
        print(msg, ': ', sep='', end='')
        if nl:
            print()
            indent = "   "
        else:
            indent = (len(msg) + 2)*' '
    first = 1
    for row in mat:
        if first: first = False;  print(indent if nl else '', end='')
        else:     print(indent, end='')
        print([f'{i:{pos}}' for i in row], sep=', ')


def prMatO(msg:str, mat:[[object]]):
    """Vytiskne zadaný titulek následovaný položkami zadané celočíselné
    matice přičemž pro tisk čísla vyhradí zadaný počet pozic.
    Argument nl definuje, zda se má za nadpisem odřádkovat.
    Odřádkuje-li se, budou se všechny následující řádky odsazovat o 3 mezery.
    """
    print(msg)
    for r, row in enumerate(mat):
        print(f'{r=}')
        for c, obj in enumerate(row):
            print(f'   [{r},{c}]:  {obj}')


def prVT(expression: str) -> None:
    """Vytiskne zadaný výraz, jeho hodnotu a typ výsledku.
    Mnemonika: Print Value and Type.
    """
    value = eval(expression)
    print(f'{expression} = {value} # type = {type(value)}')


def str_(lst:list[str]) -> list[str]:
    """Očekává seznam názvů atributů a vrátí seznam těch,
    které nezačínají a nekončí dvojicí podtržítek.
    """
    l = [s for s in lst if len(s)<=4
                        or (s[:2]  != '__'  and  s[-2:] != '__')]
    return l



############################################################################
prDB(dbg_level, f'===== Modul {__name__} ===== STOP')
