class MaszynaTuringa:
    def __init__(self, sciezka_pliku):
        self.tasma = []
        self.glowica = 0
        self.stan = ''
        self.stan_koncowy = ''
        self.przejscia = {}
        self.zaladuj_maszyne_turinga(sciezka_pliku)

    def zaladuj_maszyne_turinga(self, sciezka_pliku):
        with open(sciezka_pliku, 'r') as plik:
            linie = plik.readlines()

        liczba_wejsciowa = ''
        aktualny_stan = None
        for linia in linie:
            if linia.startswith('! input'):
                liczba_wejsciowa = linia.split()[2]
            elif linia.startswith('! start_state'):
                self.stan = linia.split()[2]
            elif linia.startswith('! Koniec'):
                self.stan_koncowy = linia.split()[2]
            elif linia.startswith('%'):
                aktualny_stan = linia.split()[1]
            else:
                czesci = linia.split()
                if len(czesci) >= 4 and aktualny_stan is not None:
                    symbol_odczytu = czesci[0]
                    symbol_zapisu = czesci[1]
                    kierunek = czesci[2]
                    nastepny_stan = czesci[3]
                    self.przejscia[(aktualny_stan, symbol_odczytu)] = (symbol_zapisu, kierunek, nastepny_stan)
                else:
                    print(f'Niepoprawna linia: {linia}')

        self.tasma = list(liczba_wejsciowa)

    def krok(self):
        if self.glowica < 0 or self.glowica >= len(self.tasma):
            #print('Głowica wykracza poza granice tasmy lub tasma jest pusta.')
            self.stan = self.stan_koncowy
            return

        aktualny_symbol = self.tasma[self.glowica]
        if (self.stan, aktualny_symbol) in self.przejscia:
            nowy_symbol, kierunek, nowy_stan = self.przejscia[(self.stan, aktualny_symbol)]
            self.tasma[self.glowica] = nowy_symbol
            self.stan = nowy_stan
            if kierunek == 'R':
                self.glowica += 1
            elif kierunek == 'L':
                self.glowica -= 1
        else:
            print(f'Brak przejścia dla stanu {self.stan} i symbolu {aktualny_symbol}.')
            self.stan = self.stan_koncowy

    def uruchom(self):
        krok_licznik = 0
        while self.stan != self.stan_koncowy:
            self.krok()
            krok_licznik += 1
            if krok_licznik > 10000:  # Przerwanie w przypadku nieskończonej pętli
                print('Przekroczono limit kroków. Prawdopodobnie nieskończona pętla.')
                break

    def wyswietl_wynik(self):
        print('Finalna tasma:', ''.join(self.tasma))
        print('Finalny stan:', self.stan)

    @classmethod
    def uruchom_program(cls, sciezka_pliku):
        maszyna = cls(sciezka_pliku)
        maszyna.uruchom()
        maszyna.wyswietl_wynik()

        # Sprawdzenie, czy liczba jest podzielna przez 3
        ostatni_stan = maszyna.stan
        if ostatni_stan == 'podzielna':
            liczba = ''.join(maszyna.tasma)
            liczba = liczba.rstrip('_')  # Usunięcie '_' z końca liczby
            try:
                liczba_int = int(liczba)
                if liczba_int % 3 == 0:
                    print('Werdykt: Tak, liczba jest podzielna przez 3.')
                else:
                    print('Werdykt: Nie, liczba nie jest podzielna przez 3.')
            except ValueError:
                print(f'Nieprawidłowy format liczby na taśmie: {liczba}')
        else:
            print('Werdykt: Nie, liczba nie jest podzielna przez 3.')

# Uruchomienie programu
if __name__ == '__main__':
    MaszynaTuringa.uruchom_program('saxony.txt')
