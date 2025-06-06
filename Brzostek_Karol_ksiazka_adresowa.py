import tkinter as tk
import json
from collections import Counter
from tkinter import Scrollbar, scrolledtext
from faker import Faker
from tkinter import OptionMenu, ttk, messagebox
import sys
import unicodedata


# Otwarcie pliku JSON i pobranie jego zawartości.
def pobierz_plik(nazwa_pliku="dane.json"):
    try:
        with open(nazwa_pliku, "r", encoding="utf-8") as file:
            dane=json.load(file)
            return dane if dane else []
    except:
        return []

# Zapisywanie nowych danych do JSON.
def zapisz_plik(dane_zapisywane, nazwa_pliku="dane.json"):
    try: 
        with open(nazwa_pliku, "w", encoding="utf-8") as file:
            json.dump(dane_zapisywane, file, ensure_ascii=False, indent=4)
    except:
        messagebox.showerror("Błąd!", "Wystąpił błąd poczas zapisu pliku JSON.")

# Wyświetlenie wszystkich wpisów, istniejących w pliku JSON.
def wczytaj_dane():

    dane=pobierz_plik()
    
    for row in table.get_children():
        table.delete(row)

        
    for adres in dane:
        table.insert('', 'end', values=(
            adres.get("imie", ""),
            adres.get("nazwisko", ""),
            adres.get("numer telefonu", ""),
            adres.get("ulica", ""),
            adres.get("numer domu", ""),
            adres.get("miejscowosc", ""),
        ))

# Dodawanie nowego wpisu do pliku JSON
def zatwierdz_dane():
    imie=entry_imie.get().strip()
    nazwisko=entry_nazwisko.get().strip()
    numer_telefonu=entry_numer_telefonu.get().strip()
    ulica=entry_ulica.get().strip()
    numer_domu=entry_numer_domu.get().strip()
    miejscowosc=entry_miejscowosc.get().strip()

    if not all([imie, nazwisko, ulica, numer_domu, miejscowosc, numer_telefonu]):
        messagebox.showerror("Błąd!", "Wszystkie dane muszą być wprowadzone i nie mogą być wyłącznie znakami białymi!")
        return

    if any(char.isdigit() for char in imie+nazwisko+miejscowosc):
        messagebox.showwarning("Błąd!", "W imieniu, nazwisku oraz nazwie miasta nie może znajdować się żadna cyfra!")
        return

    if not any(char.isdigit() for char in numer_domu):
        messagebox.showwarning("Błąd!", "Numer domu musi zawierać przynajmniej jedną cyfrę!")
        return

    if not all(znak.isdigit() or znak in " -+" for znak in numer_telefonu):
        messagebox.showwarning("Błąd!", "Numer telefonu może zawierać jedynie cyfry, spacje oraz znaki - i +!")
        return

    adres={
        "imie": imie,
        "nazwisko": nazwisko,
        "numer telefonu": numer_telefonu,
        "ulica": ulica,
        "numer domu": numer_domu,
        "miejscowosc": miejscowosc
    }

    dane=pobierz_plik()
    
    # Sprawdzenie, czy wpis już istnieje w pliku JSON.
    for wpis in dane:
        if (wpis["imie"].lower()==imie.lower() and
            wpis["nazwisko"].lower()==nazwisko.lower() and
            oczysc_numer(wpis["numer telefonu"])==oczysc_numer((numer_telefonu))):
            messagebox.showwarning("Duplikat!", "Podany adres już istnieje w bazie danych!")
            wyczysc_pola_wprowadzania()
            return
    
    dane.append(adres)

    zapisz_plik(dane)

    messagebox.showinfo("Sukces!", "Pomyślnie dodano nowe dane.")

    table.insert('', 'end', values=(imie, nazwisko, numer_telefonu, ulica, numer_domu, miejscowosc))

    wyczysc_pola_wprowadzania()

# Usuwanie wszystkich danych z pliku.
def wyczysc_dane():

    if not messagebox.askyesno("Potwierdź.", "Czy na pewno chcesz wyczyścić wszystkie dane z tabeli?"):
        return

    zapisz_plik([])

    for row in table.get_children():
            table.delete(row)

    messagebox.showinfo("Sukces!", "Dane zostały wyczyszczone.")

# Usuwanie pojedynczego wpisu z pliku.
def usun_wpis():

    zaznaczony=table.selection()
    if not zaznaczony:
        messagebox.showwarning("Brak zaznaczenia.", "Wybierz wpis, który chcesz usunąć.")
        return

    indeks=zaznaczony[0]
    wartosci=table.item(indeks, "values")

    if not messagebox.askyesno("Usuwanie wpisu.", "Czy na pewno chcesz usunąć zaznaczony wpis?"):
        return

    dane=pobierz_plik()

    dane = [adres for adres in dane if not(
        adres.get("imie", "")==wartosci[0] and
        adres.get("nazwisko", "")==wartosci[1] and
        oczysc_numer(adres.get("numer telefonu", ""))==oczysc_numer(wartosci[2]) and
        adres.get("ulica", "")==wartosci[3] and
        adres.get("numer domu", "")==wartosci[4] and
        adres.get("miejscowosc", "")==wartosci[5]

        )]

    zapisz_plik(dane)
    
    table.delete(indeks)
    messagebox.showinfo("Sukces!", "Pomyślnie usunięto zaznaczony wpis.")

# Uzupełnienie pliku JSON losowymi danymi (Faker).
def uzupelnij_danymi():
    
    if not messagebox.askyesno("Dodawanie nowych danych.", "Czy na pewno chcesz dodać 20 nowych, losowych wpisów do pliku?"):
        return

    fake=Faker('pl_PL')
    adresy=[]

    dane=pobierz_plik()

    adresy.extend(dane)

    # Stworzenie wymyślonych danych.
    for _ in range(20):
        adres={
        "imie": fake.first_name(),
        "nazwisko": fake.last_name(),
        "numer telefonu": fake.phone_number(),
        "ulica": fake.street_name(),
        "numer domu": fake.building_number(),
        "miejscowosc": fake.city()
        }
        adresy.append(adres)

    zapisz_plik(adresy)

    for row in table.get_children():
        table.delete(row)
    
    # Wstawienie danych do tabeli.
    for adres in adresy:
        table.insert('', 'end', values=(
            adres.get("imie", ""),
            adres.get("nazwisko", ""),
            adres.get("numer telefonu", ""),
            adres.get("ulica", ""),
            adres.get("numer domu", ""),
            adres.get("miejscowosc", "")
        ))

    messagebox.showinfo("Sukces!", "Pomyślnie uzupełniono plik wymyślonymi danymi.")

# Oczyszczenie numeru ze spacji, "-" i "+".
def oczysc_numer(nr):
    return ''.join(filter(str.isdigit, nr))

# Wyszukiwanie wpisów.
def wyszukaj_dane():
    pole=kryterium.get()
    wartosc=entry_szukaj.get().strip().lower()

    if not wartosc.strip():
        messagebox.showerror("Błąd!", "Nie wprowadzono wartości!")
        entry_szukaj.delete(0, tk.END)
        return

    dane=pobierz_plik()

    table.delete(*table.get_children())

    if pole=="numer telefonu":
        wartosc=oczysc_numer(wartosc)

    znalezione=[]

    for adres in dane:
        wartosc_z_pliku=adres.get(pole, "").strip().lower()

        if pole=="numer telefonu":
            wartosc_z_pliku=oczysc_numer(wartosc_z_pliku)

        if wartosc in wartosc_z_pliku:
            znalezione.append(adres)
    # Błąd, jeśli nie znaleziono szukanego wpisu.
    if not znalezione:
        wczytaj_dane()
        messagebox.showinfo("Brak wyników.", "Nie znaleziono w bazie szukanych wartości.")

    else:
        for adres in znalezione:
            table.insert('', 'end', values=(
            adres.get("imie", ""),
            adres.get("nazwisko", ""),
            adres.get("numer telefonu", ""),
            adres.get("ulica", ""),
            adres.get("numer domu", ""),
            adres.get("miejscowosc", "")
            ))

    entry_szukaj.delete(0, tk.END)

# Czyszczenie pól ręcznego wprowadzania nowego wpisu.
def wyczysc_pola_wprowadzania():
    entry_imie.delete(0, tk.END)
    entry_nazwisko.delete(0, tk.END)
    entry_numer_telefonu.delete(0, tk.END)
    entry_ulica.delete(0, tk.END)
    entry_numer_domu.delete(0, tk.END)
    entry_miejscowosc.delete(0, tk.END)

# Wyświetlanie statystyk miast.
def pokaz_statystyki():
    dane=pobierz_plik()
    if not dane:
        messagebox.showwarning("Brak danych!", "Brak danych w bazie.")
        return

    miejscowosci=[adres.get("miejscowosc", "").strip().lower() for adres in dane]
    statystyki = Counter(miejscowosci)

    posortowane=sorted(statystyki.items())

    stat_okno=tk.Toplevel(root)
    stat_okno.title("Statystyki miejscowości")
    stat_okno.geometry("400x400")
    stat_okno.resizable(True, False)

    canvas=tk.Canvas(stat_okno)
    scrollbar=tk.Scrollbar(stat_okno, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    frame=tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    for miasto, liczba in posortowane:
        tekst=f"{miasto.title()}: {liczba}"
        tk.Label(frame, text=tekst, anchor="w").pack(fill="x", padx=10, pady=2)

    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def zamknij_program():
   if not messagebox.askyesno("Opuść program.", "Czy na pewno chcesz opuścić program?"):
       return
   else:
        sys.exit()

root = tk.Tk()
root.title("Formularz adresowy")

#Tworzenie etykiet i pol tekstowych dla kazdego pola danych
tk.Label(root, text="Imię:").grid(row=0, column=0, sticky="w")
entry_imie=tk.Entry(root)
entry_imie.grid(row=0, column=1, sticky="w")

tk.Label(root, text="Nazwisko:").grid(row=1, column=0, sticky="w")
entry_nazwisko=tk.Entry(root)
entry_nazwisko.grid(row=1, column=1, sticky="w")

tk.Label(root, text="Numer telefonu:").grid(row=2, column=0, sticky="w")
entry_numer_telefonu=tk.Entry(root)
entry_numer_telefonu.grid(row=2, column=1, sticky="w")

tk.Label(root, text="Ulica: ").grid(row=3, column=0, sticky="w")
entry_ulica=tk.Entry(root)
entry_ulica.grid(row=3, column=1, sticky="w")

tk.Label(root, text="Numer domu:").grid(row=4, column=0, sticky="w")
entry_numer_domu=tk.Entry(root)
entry_numer_domu.grid(row=4, column=1, sticky="w")

tk.Label(root, text="Miejscowość:").grid(row=5, column=0, sticky="w")
entry_miejscowosc=tk.Entry(root)
entry_miejscowosc.grid(row=5, column=1, sticky="w")
kolumny = ("Imię", "Nazwisko", "Numer telefonu", "Ulica", "Numer domu", "Miejscowość")

# Przycisk ręcznego dodawania danych.
tk.Button(root, text="Zatwierdź", background="#89e98f", command=zatwierdz_dane).grid(row=0, rowspan=6, column=1)

# Przycisk automatycznego dodawania danych.
tk.Button(root, text="Uzupełnij losowymi danymi (20 nowych wpisów)", command=uzupelnij_danymi).grid(row=6, columnspan=2)

tk.Button(root, text="Wyświetl wszystkie wpisy.", command=wczytaj_dane).grid(row=7, columnspan=2)

# Wyszukiwanie wpisów.
tk.Label(root, text="Wybierz, po jakiej wartości chcesz przeszukać dane:").grid(row=8, column=0, sticky="w")
kryterium=tk.StringVar(value="imie")
opcje_kryterium=["imie", "nazwisko", "numer telefonu", "ulica", "miejscowosc"]
opcje_menu=tk.OptionMenu(root, kryterium, *opcje_kryterium)
opcje_menu.grid(row=8, column=1, sticky="w")

tk.Label(root, text="Wpisz wartość, jaka ma zostać wyszukana: ").grid(row=9, column=0, sticky="w")
entry_szukaj=tk.Entry(root)
entry_szukaj.grid(row=9, column=1, sticky="w")

tk.Button(root, text="Wyszukaj", command=wyszukaj_dane).grid(row=8, rowspan=2, column=1)



# Tabela wyświetlająca wpisy istniejące w JSON.
table=ttk.Treeview(root, columns=kolumny, show="headings")
for col in kolumny:
    table.heading(col, text=col)
table.grid(row=10, columnspan=2)

tk.Button(root, text="Statystyki miast", command=pokaz_statystyki).grid(row=11, column=0, sticky="nw")

wczytaj_dane()


tk.Button(root, text="Usuń zaznaczony wpis.", command=usun_wpis).grid(row=12, columnspan=2)

tk.Button(root, text="Wyczyść wszystkie dane z pliku", command=wyczysc_dane).grid(row=13, columnspan=2)

tk.Button(root, text="Zamknij program.", background="#fc4c4c", command=zamknij_program).grid(row=14, columnspan=2)

root.mainloop()


