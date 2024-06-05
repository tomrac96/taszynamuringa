class Turing:
  
  def __init__(self, instrukcje, tasma):
    self.tasma = tasma
    self.koniec = None 
    self.instrukcje = instrukcje 
    self.dict_instrukcje = None
    self.glowica = None 
    self.ruch_glowica = 0
    self.tasma_conv = []
    self.stan = None

  def odczyt_pliku(self):
    inst = {}
    zp = ""
    with open(self.instrukcje, 'r') as plik:
      for wiersz in plik:
        if wiersz[0] == '!':
          if wiersz.split()[1] == "input":
            self.tasma = wiersz.split()[2]
            continue
          if wiersz.split()[1] == "start_state":
            self.stan =  wiersz.split()[2]
            continue
          if wiersz.split()[1] == 'Koniec':
            self.koniec = wiersz.split()[2]
            continue
        if wiersz[0] == '%':
          zp = wiersz.split()[1]
          inst[zp] ={}
          tmp = {}
          inst[zp]=tmp
          continue
        try:
          ob_znak, zapis, kierunek, stan = wiersz.split()
        except:
          continue
        tmp[ob_znak] = (zapis, kierunek, stan)
    plik.close()
    self.dict_instrukcje = inst

  def modif_tasma(self, extend):
    tasma_extend = ["$"] * extend
    tmp = tasma_extend + list(self.tasma) + tasma_extend
    self.tasma = tmp

  def ruch_tasma(self, ob_znak):
    zapis, kierunek, stan = self.dict_instrukcje[self.stan][ob_znak]
    if kierunek == "R":
      self.ruch_glowica += 1
    elif kierunek == "L":
      self.ruch_glowica -= 1
    return self.ruch_glowica

  def konwersja_tasma(self):
    self.tasma = list(self.tasma)

  def konwersja_tasma_bis(self):
    self.tasma = "".join([elem for elem in self.tasma if elem != "$"])
    
  def odczyt_tasma(self):
    self.odczyt_pliku()
    self.konwersja_tasma()
    self.modif_tasma(15)
    while self.stan != self.koniec:
        self.glowica = self.tasma[self.ruch_glowica]

        zapis, kierunek, stan = self.dict_instrukcje[self.stan][self.glowica]
        self.tasma[self.ruch_glowica] = zapis
        self.ruch_glowica = self.ruch_tasma(self.glowica)
        self.stan = stan

        print(f"Aktualny stan glowicy: {self.glowica}")
        print(f"Aktualna wartość ruchu: {self.ruch_glowica}")
        print(f"Aktualny stan: {self.stan}")
        print(f"Taśma: {''.join([elem for elem in self.tasma if elem != '$'])}")
        print("\n")

    self.konwersja_tasma_bis()
    print("Taśma koniec: ", self.tasma)
    return

# Przykładowa taśma
tasma = "1010"

# Tworzenie instancji i uruchomienie maszyny Turinga
t = Turing("tr00jboj.txt", tasma)
t.odczyt_tasma()
