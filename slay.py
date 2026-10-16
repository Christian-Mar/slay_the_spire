# Importeer de module 'random' zodat we kaarten kunnen schudden
import random


# Definieer de klasse Player: dit is de blauwdruk voor een speler
class Player:
    # Klasse-constante: hoeveel kaarten de speler bij elke beurt trekt
    HAND_SIZE = 5

    # De constructor: wordt automatisch uitgevoerd bij Player(name)
    def __init__(self, name: str) -> None:
        # Bewaar de naam van de speler in het object
        self.name = name
        # Maak de startstapel: 5 keer 'Strike' en 5 keer 'Block' (10 kaarten)
        self.draw_pile: list[str] = ["Strike"] * 5 + ["Block"] * 5
        # Schud de draw pile zodat de kaarten in willekeurige volgorde liggen
        random.shuffle(self.draw_pile)
        # De hand van de speler is bij de start nog leeg
        self.hand: list[str] = []
        # De discard pile (aflegstapel) is bij de start ook leeg
        self.discard_pile: list[str] = []
        # Teller voor het beurtnummer; we beginnen op 0, start_turn maakt er 1 van
        self.turn = 0

    # Methode die één kaart van de draw pile naar de hand verplaatst
    def draw_card(self) -> None:
        # Controleer of de draw pile leeg is
        if not self.draw_pile:
            # Leg alle kaarten van de discard pile terug op de draw pile
            self.draw_pile.extend(self.discard_pile)
            # Maak de discard pile leeg (de kaarten zitten nu in de draw pile)
            self.discard_pile.clear()
            # Schud de draw pile opnieuw
            random.shuffle(self.draw_pile)
        # Als er nog steeds geen kaarten zijn (alles zit al in de hand), stop dan
        if not self.draw_pile:
            # Verlaat de methode zonder een kaart te trekken
            return
        # Neem de bovenste (laatste) kaart van de draw pile en steek ze in de hand
        self.hand.append(self.draw_pile.pop())

    # Methode die een nieuwe beurt start
    def start_turn(self) -> None:
        # Verhoog het beurtnummer met 1
        self.turn += 1
        # Herhaal HAND_SIZE (5) keer
        for _ in range(self.HAND_SIZE):
            # Trek telkens één kaart
            self.draw_card()
        # Sorteer de hand alfabetisch zodat ze netjes getoond wordt
        self.hand.sort()

    # Methode die een beurt afsluit
    def end_turn(self) -> None:
        # Alle overgebleven kaarten uit de hand gaan naar de discard pile
        self.discard_pile.extend(self.hand)
        # Maak de hand leeg
        self.hand.clear()

    # Methode die een kaart speelt
    def play_card(self, card: str) -> None:
        # Controleer of de gevraagde kaart wel in de hand zit
        if card not in self.hand:
            # Zo niet: toon een foutmelding
            print(f"You don't have the card {card} in your hand")
            # En stop de methode hier
            return
        # Toon welke kaart gespeeld wordt
        print(f"Playing card {card}")
        # Verwijder (één exemplaar van) de kaart uit de hand
        self.hand.remove(card)
        # Leg de gespeelde kaart op de discard pile
        self.discard_pile.append(card)

    # Methode die de huidige toestand op het scherm toont
    def show_status(self) -> None:
        # Toon de kopregel met de naam van de speler en het beurtnummer
        print(f"===========player {self.name} / (turn {self.turn})")
        # Toon de kaarten in de hand (een lijst wordt getoond als ['...', ...])
        print(f"hand: {self.hand}")

    # Hoofdmethode die het volledige spel laat lopen
    def play_game(self) -> None:
        # Start de eerste beurt
        self.start_turn()
        # Oneindige lus: het spel loopt tot de speler 'quit' typt
        while True:
            # Toon de status (naam, beurt en hand)
            self.show_status()
            # Vraag wat de speler wil doen en verwijder spaties voor/achter
            action = input("What do you want to do?").strip()
            # Als de speler 'quit' typt...
            if action == "quit":
                # ...dan verlaten we de lus en is het spel gedaan
                break
            # Als de speler 'end' typt...
            elif action == "end":
                # ...dan wordt de huidige beurt afgesloten
                self.end_turn()
                # ...en meteen een nieuwe beurt gestart
                self.start_turn()
            # In alle andere gevallen beschouwen we de invoer als een kaartnaam
            else:
                # Probeer die kaart te spelen
                self.play_card(action)


# Deze code wordt alleen uitgevoerd als je dit bestand rechtstreeks start
if __name__ == '__main__':
    # Vraag de naam van de speler
    name = input("Hello, what is your name? ")
    # Maak een nieuw Player-object met die naam
    p = Player(name)
    # Start het spel
    p.play_game()
