import threading
import time
import rubrica


# Consumatore Thread Class
class Consumatore(threading.Thread):
    def __init__(self, rub, i):
        super().__init__(name="Consumatore " + str(i))
        self.c = rub

    def run(self):
        self.c.modifica("gigi", "rossi", 11111111)

        time.sleep(2)

        self.c.cancella("Alberto", "Alberti")

        time.sleep(2)

        self.c.inserisci("Rossano", "Rosso", 3478999)
        self.c.modifica("mario romualdo", "rossi", 2222222)
        self.c.inserisci("Alberto", "Alberti", 3475599)

        time.sleep(2)

        self.c.inserisci("Carlo", "Carli", 3475591)
        self.c.inserisci("Ubaldo", "Ubaldi", 3475511)

        time.sleep(3)

        self.c.cancella("Alberto", "Alberti")
        self.c.cancella("Ubaldo", "Ubaldi")
        time.sleep(1)

        items_produced = 0
        while items_produced < 10:
            self.c.suggerimento()
            items_produced += 1

        # Il metodo .ordina() restituisce una stringa, non modifica self.rub.
        # Ho quindi sostituito i comandi:

        # self.c.ordina(crescente=False))
        # print(self.c)

        # con:

        print(self.c.ordina(crescente=False))

        # ------------------------------ Test Aggiuntivi --------------------------------

        time.sleep(2)

        q = rubrica.Rubrica()
        q.inserisci("Mario", "Biondi", 3345562)
        print("==========> Consumatore testa uguaglianza:", self.c == q)

        time.sleep(2)

        q.load("___testfile2")
        q.load("___testfile1")
        q.cancella("Gigi", "Biondi")
        print("==========> Consumatore testa uguaglianza:", self.c == q)
        print("==========> Consumatore: FINE TEST")
















