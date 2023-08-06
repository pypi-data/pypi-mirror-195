#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
#
"""Modul definující sadu metod pro jednoduchý vstup a výstup
prostřednictvím dialogových oken
spolu s metodou zastavující běh programu na zadaný počet milisekund.

@author  Jan Lampa
@version 2021-Summer
"""

import tkinter as tk

from tkinter        import messagebox, simpledialog, Tk
from tkinter.ttk    import Combobox


window_location = "+300+300"


def enter(prompt, default_value):
    """
    Zobrazí dialogové okno s výzvou k zadání reálné hodnoty
    při zavření okna zavíracím tlačítkem ukončí aplikaci.
    :param prompt: Text výzvy oznamující uživateli, co má zadat
    :param default_value: Implicitní hodnota.
    :return: Uživatelem zadaná hodnota, resp. potvrzená implicitní hodnota.
    """
    application_window = Tk()
    application_window.withdraw()
    if isinstance(default_value, str):
        sd = simpledialog.askstring("Input", prompt,
                                    parent=application_window,
                                    initialvalue=default_value)
    elif isinstance(default_value, int):
        sd = simpledialog.askinteger("Input", prompt,
                                     parent=application_window,
                                     initialvalue=default_value)
    elif isinstance(default_value, float):
        sd = simpledialog.askfloat("Input", prompt,
                                   parent=application_window,
                                   initialvalue=default_value)
    else:
        raise Exception("Atribut default value must be integer,string or float")
    return sd


def choose(question, *buttons):
    """
    Zobrazí dialogové okno se otázkou, na níž má uživatel odpovědět stiskem
    některého z tlačítek, jejichž popisky naznačují možné odpovědi.
    Vrátí pořadí stisknutého tlačítka.
    Pokud uživatel neodpoví a zavře dialog, metoda ukončí program.
    :param question: Zobrazovaný text otázky
    :param buttons: Popisky na tlačítcích
    :return: Pořadí stisknutého tlačítka, přičemž první tlačítko zleva
    na pořadí 0
    """
    application_window = Tk()
    application_window.withdraw()

    def command(string):
        global result
        result = string
        tl.destroy()
        application_window.destroy()

    def on_closing():
        tl.destroy()
        application_window.destroy()

    global result
    result = -1
    tl = tk.Toplevel()
    tl.geometry(window_location)
    tl.protocol("WM_DELETE_WINDOW", on_closing)
    label = tk.Label(tl, text=question)
    label.pack(padx=5, pady=5)
    for button_text in buttons:
        button = tk.Button(tl, text=button_text, command=lambda: command(button_text))
        button.pack(side=tk.LEFT, padx=5, pady=5)

    application_window.mainloop()
    return result


def confirm(question) -> bool:
    """
    Zobrazí dialogové okno se zprávou a umožní uživateli odpovědět
    <b>ANO</b> nebo <b>NE</b>. Vrátí informaci o tom, jak uživatel odpověděl.
    Neodpoví-li a zavře dialog, ukončí program.
    :param question: Zobrazovaný text otázky.
    :return:<b>{@code true}</b> Odpověděl-li uživatel <b>ANO</b>,
            <b>{@code false}</b> odpověděl-li <b>NE</b>
    """
    application_window = Tk()
    application_window.withdraw()
    return messagebox.askyesno("Question", question)


def inform(text) -> None:
    """
    Zobrazí dialogové okno se zprávou a počká,
    až uživatel stiskne tlačítko OK;
    při zavření okna zavíracím tlačítkem ukončí celou aplikaci.
    :param text: Zobrazovaný text
    """
    application_window = Tk()
    application_window.withdraw()
    application_window.geometry(window_location)

    mb = messagebox.showinfo("Information", text)


def select(prompt, *options):
    """
    Zobrazí dialogové okno s výzvou k zadání
    některého z textů v rozbalovacím seznamu;
    při zavření okna nebo stisku tlačítka Cancel
    se celá aplikace ukončí.
    :param prompt: Text výzvy oznamující uživateli, co má zadat
    :param options: Texty, z nichž si může uživatel vybrat
    :return: Uživatelem zadaná hodnota
    """
    application_window = Tk()
    application_window.withdraw()

    def command():
        global result
        result = combo.get()
        tl.destroy()
        application_window.destroy()

    def on_closing():
        tl.destroy()
        application_window.destroy()

    global result
    result = -1
    tl = tk.Toplevel()
    tl.geometry(window_location)
    tl.protocol("WM_DELETE_WINDOW", on_closing)
    label = tk.Label(tl, text=prompt)
    label.pack(padx=5, pady=5)
    combo = Combobox(tl, values=options)
    combo.set(options[0])
    combo.pack(padx=5, pady=5)
    combo['state'] = 'readonly'
    button = tk.Button(tl, text="Submit", command=command)
    button.pack(padx=5, pady=5)
    application_window.mainloop()
    return result


def set_dialog_position(x: int, y: int):
    """
    Nastaví pozici příštího dialogového okna.
    :param x: Vodorovná souřadnice
    :param y: Svislá souřadnice
    """
    global window_location
    window_location = '+%d+%d' % (x, y)


def pause(miliseconds: int):
    """
     Počká zadaný počet milisekund.
    :param miliseconds: Počet milisekund, po něž se má čekat
    """
    from time import sleep
    sleep(float(miliseconds / 1000))

