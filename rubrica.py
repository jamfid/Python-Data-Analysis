# Assegnamento 2  aa 2021-22 622AA modulo programmazione 9 crediti
# Studente: Giacomo Fidone, Matricola: 531668
# Mail: g.fidone1@studenti.unipi.it, Cellulare: +39 331 998 2455

import threading
from queue import Queue
import logging
import random


class Rubrica:
    """ Costruttore: crea una rubrica vuota rappresentata come
        dizionario di contatti vuoto """
    def __init__(self):
        """ crea una nuova rubrica vuota """
        self.rub = {}
        self.queue = Queue()
        self.cond = threading.Condition()
        logging.basicConfig(format="%(message)s", level=logging.DEBUG)
        self.logger = logging.getLogger()

    def __str__(self):
        """ Serializza una rubrica attraverso una stringa
        con opportuna codifica (a scelta dello studente) """
        self.cond.acquire()
        self.logger.debug("\n" + threading.current_thread().getName() + " acquisisce il lock per \"__str__\".")
        rub_str = ""
        for record in self.rub:
            rub_str += record[0] + " " + record[1] + " : " + str(self.rub[record]) + "\n"
        self.logger.debug(threading.current_thread().getName() + " serializza la rubrica e rilascia.")
        self.cond.notifyAll()
        self.cond.release()
        return rub_str

    def __eq__(self, r):
        """stabilisce se due rubriche contengono
        esattamente le stesse chiavi con gli stessi dati"""
        # Il metodo è un po' diverso rispetto a quello del primo assegnamento: i comandi di return sono stati sostituiti
        # da aggiornamenti della variabile "result" con lo scopo di snellire il codice – si evita infatti di ripetere
        # prima di ogni return la stampa terminale del logger e l'invocazione dei metodi .notifyAll() e .release(). Lo
        # stesso viene fatto nei metodi "modifica" e "cancella".
        self.cond.acquire()
        self.logger.debug("\n" + threading.current_thread().getName() + " acquisisce il lock per \"__eq__\".")
        try:
            result = True
            if len(self.rub) == len(r.rub):
                for record in self.rub:
                    if record not in r.rub or self.rub[record] != r.rub[record]:
                        result = False
            else:
                result = False
            self.logger.debug(threading.current_thread().getName() + " verifica l'uguaglianza e rilascia.")
            self.cond.notifyAll()
            self.cond.release()
            return result
        except AttributeError:
            self.logger.debug(f"{r} non è una Rubrica." + threading.current_thread().getName() + "rilascia il lock per "
                                                                                                 "\"__eq__\".")
            self.cond.notifyAll()
            self.cond.release()

    def __add__(self, r):
        """crea una nuova rubrica unendone due (elimina i duplicati)
        e la restituisce come risultato --
        se ci sono contatti con la stessa chiave nelle due rubriche
        ne riporta uno solo """
        self.cond.acquire()
        self.logger.debug("\n" + threading.current_thread().getName() + " acquisisce il lock per \"__add__\".")
        try:
            new_r = Rubrica()
            new_r.rub = self.rub.copy()
            for record in r.rub:
                if record not in self.rub:
                    new_r.rub[record] = r.rub[record]
            self.logger.debug(threading.current_thread().getName() + f" unisce {self.rub} e {r} e rilascia")
            self.cond.notifyAll()
            self.cond.release()
            return new_r
        except AttributeError:
            self.logger.debug(f"{r} non è una Rubrica. " + threading.current_thread().getName() + " rilascia il lock "
                                                                                                  "per \"__add__\".")
            self.cond.notifyAll()
            self.cond.release()

    def load(self, nomefile):
        """ carica da file una rubrica eliminando il
        precedente contenuto di self """
        self.cond.acquire()
        self.logger.debug("\n" + threading.current_thread().getName() + " acquisisce il lock per \"load\".")
        try:
            with open(nomefile, "r") as file:
                self.rub.clear()
                line = file.readline()
                while line:
                    values = line.split(":")
                    self.inserisci(values[0], values[1], int(values[2]))
                    line = file.readline()
            self.logger.debug(threading.current_thread().getName() + f" effettua il load di {nomefile} e rilascia.")
            self.cond.notifyAll()
            self.cond.release()
        except FileNotFoundError:
            self.logger.debug(f"Il file {nomefile} non esiste. Load non eseguito. " + threading.current_thread().getName() +
                              " rilascia il lock per \"load\".")
            self.cond.notifyAll()
            self.cond.release()
            print()

    def inserisci(self, nome, cognome, dati):
        """ inserisce un nuovo contatto con chiave (nome,cognome)
        restituisce "True" se l'inserimento Ã¨ andato a buon fine e "False"
        altrimenti (es chiave replicata) -- case insensitive """
        # Il "check_type" è un metodo che ho definito per semplificare il controllo del tipo di valori in ingresso.
        # Assumo che due contatti diversi possano essere inseriti con gli stessi dati.
        # Si esegue qui una semplificazione analoga a quella proposta in "__eq__". In aggiunta, il controllo case
        # insensitive è eseguito da un metodo a parte – .record_exists(). Lo stesso viene fatto nel metodo "cerca".
        self.cond.acquire()
        result = False
        if self.check_type(nome, cognome, dati):
            self.logger.debug("\n" + threading.current_thread().getName() + " acquisisce il lock per \"inserisci\".")
            if self.record_exists(nome, cognome):
                msg = f" rilascia il lock: il contatto \"{nome} {cognome}\" è esistente."
            else:
                msg = f" inserisce il contatto \"{nome} {cognome}\" e rilascia."
                self.rub[(nome, cognome)] = dati
                result = True
        else:
            msg = " rilascia il lock: i dati inseriti non sono corretti."
        self.logger.debug(threading.current_thread().getName() + msg)
        self.cond.notifyAll()
        self.cond.release()
        return result

    def modifica(self, nome, cognome, newdati):
        """ modifica i dati relativi al contatto con chiave (nome,cognome)
        sostituendole con "newdati" -- restituisce "True" se la modifica
        Ã¨ stata effettuata e "False" altrimenti (es: la chiave non Ã¨ presente )"""
        self.cond.acquire()
        result = False
        if self.check_type(nome, cognome, newdati):
            self.logger.debug("\n" + threading.current_thread().getName() + " acquisisce il lock per \"modifica\".")
            if (nome, cognome) in self.rub:
                self.rub[(nome, cognome)] = newdati
                msg = f" modifica il contatto \"{nome} {cognome}\" e rilascia."
                result = True
            else:
                msg = f" non modifica il contatto \"{nome} {cognome}\" e rilascia."
        else:
            msg = f" rilascia il lock: i dati inseriti non sono corretti."
        self.logger.debug(threading.current_thread().getName() + msg)
        self.cond.notifyAll()
        self.cond.release()
        return result

    def cancella(self, nome, cognome):
        """ il contatto con chiave (nome,cognome) esiste lo elimina
        insieme ai dati relativi e restituisce True -- altrimenti
        restituisce False """
        self.cond.acquire()
        result = False
        if self.check_type(nome=nome, cognome=cognome):
            self.logger.debug("\n" + threading.current_thread().getName() + " acquisisce la lock per \"cancella\".")
            if (nome, cognome) in self.rub:
                del self.rub[(nome, cognome)]
                msg = f" cancella l'elemento \"{nome} {cognome}\" e rilascia."
                result = True
            else:
                msg = f" non trova l'elemento \"{nome} {cognome}\" e rilascia."
        else:
            msg = " rilascia il lock: i dati inseriti non sono corretti."
        self.logger.debug(threading.current_thread().getName() + msg)
        self.cond.notifyAll()
        self.cond.release()
        return result

    def cerca(self, nome, cognome):
        """ restitusce i dati del contatto se la chiave e' presente
        nella rubrica e "None" altrimenti -- case insensitive """
        self.cond.acquire()
        result = None
        if self.check_type(nome=nome, cognome=cognome):
            self.logger.debug("\n" + threading.current_thread().getName() + " acquisisce il lock per \"cerca\".")
            if self.record_exists(nome, cognome):
                msg = f" trova il valore di \"{nome} {cognome}\" e rilascia."
                result = self.rub[self.record_exists(nome, cognome)]
            else:
                msg = f" non trova il valore di \"{nome} {cognome}\" e rilascia."
        else:
            msg = f" rilascia il lock: i dati inseriti non sono corretti."
        self.logger.debug(threading.current_thread().getName() + msg)
        self.cond.notifyAll()
        self.cond.release()
        return result

    def store(self, nomefile):
        """ salva su file il contenuto della rubrica secondo
        un opportuno formato (a scelta dello studente)"""
        # Il formato da me scelto prevede un contatto per linea nome:cognome:telefono\n
        self.cond.acquire()
        self.logger.debug("\n" + threading.current_thread().getName() + " acquisisce il lock per \"store\".")
        with open(nomefile, "w") as file:
            for record in self.rub:
                file.write(record[0] + ":" + record[1] + ":" + str(self.rub[record]) + "\n")
        self.logger.debug(threading.current_thread().getName() + " esegue lo store e rilascia.")
        self.cond.notifyAll()
        self.cond.release()

    def ordina(self, crescente=True):
        """ serializza su stringa il contenuto della rubrica come in
            Nannipieri Felice 32255599\n
            Neri Paolo 347555776\n
            Rossi Mario 3478999\n
            Rossi Mario Romualdo 3475599\n
            Tazzini Tazzetti Gianna 33368999\n
            le chiavi ordinate lessicograficamente per Cognome -- Nome
            in modo crescente (True) o decrescente (False)
            Fra nome, cognome e telefono seve essere presente ESATTAMENTE uno spazio
            Restituisce la stringa prodotta """
        # La normalizzazione dei nomi (ad es. "FELICE nannipieri" in "Felice Nannipieri") è eseguita
        # dal metodo aggiuntivo "normalize".
        self.cond.acquire()
        self.logger.debug("\n" + threading.current_thread().getName() + " acquisisce il lock per \"ordina\".")
        ordered_r = {}
        for record in self.rub:
            ordered_r[self.normalize(record[1]), self.normalize(record[0])] = self.rub[record]
        if crescente:
            records = sorted(ordered_r)
        else:
            records = sorted(ordered_r, reverse=True)
        result = ""
        for record in records:
            result += record[0] + " " + record[1] + " " + str(ordered_r[record]) + "\n"
        self.logger.debug("\n" + threading.current_thread().getName() + " serializza la rubrica e rilascia.")
        self.cond.notifyAll()
        self.cond.release()
        return result

    def suggerisci(self, nome, cognome):
        """Il metodo suggerisci viene invocato da un thread per
        effettuare un suggerimento di un contatto nella rubrica.
        Prende come parametro il nome ed il cognome del contatto e
        lo inserisce in una coda (di lunghezza massima 3).
        Non si puo' inserire un elemento nella coda se la coda e' piena.
        """
        #self.cond.acquire()
        self.logger.debug("\n" + threading.current_thread().getName() + " acquisisce il lock per \"suggerisci\".")
        while self.queue.full():
            self.logger.debug(threading.current_thread().getName() + " entra in attesa: coda piena.")
            self.cond.wait()
        self.queue.put((nome, cognome))
        self.logger.debug(threading.current_thread().getName() + f" inserisce \"{nome} {cognome}\" nella coda e "
                                                                 f"rilascia.")
        #self.cond.notifyAll()
        #self.cond.release()

    def suggerimento(self):
        """Il metodo suggerimento viene invocato da un thread per
        ottenere un suggerimento recuperato dalla rubrica.
        Il thread legge gli elementi presenti in una coda
        di lunghezza 3. Se la coda è vuota, attende l'inserimento di
        un elemento, altrimenti prende il primo elemento della
        coda e lo stampa."""
        #self.cond.acquire()
        self.logger.debug("\n" + threading.current_thread().getName() + " acquisisce il lock per \"suggerimento\".")
        while self.queue.empty():
            self.logger.debug(threading.current_thread().getName() + " entra in attesa: coda vuota.")
            self.cond.wait()
        record = self.queue.get()
        self.logger.debug(threading.current_thread().getName() + f" preleva \"{record}\" dalla coda.")
        self.inserisci(record[0], record[1], random.randint(3311111, 3391111))
        self.queue.task_done()
        #self.cond.notifyAll()
        #self.cond.release()

        # ––––––------––––––––––––––––----–––- Metodi aggiuntivi –––––––––––––––––––------––––––––– :

    @staticmethod
    def check_type(nome="", cognome="", dati=0):
        """ Restituisce "True" se il tipo dei dati è quello atteso,
        "False" altrimenti."""
        if type(nome) == str and type(cognome) == str and type(dati) == int:
            return True
        return False

    @staticmethod
    def normalize(text):
        """ Prende in input una stringa e la normalizza con iniziali maiuscole (ad es.
        "tazzini tazzetti" in "Tazzini Tazzetti"). Restituisce la stringa prodotta."""
        words = text.split()
        capitalized_words = [word.capitalize() for word in words]
        result = capitalized_words[0]
        for word in capitalized_words[1:]:
            result += " " + word
        return result

    def record_exists(self, nome, cognome):
        for record in self.rub:
            if (record[0].lower(), record[1].lower()) == (nome.lower(), cognome.lower()):
                return record[0], record[1]
        return False
