# Importeer de oorspronkelijke klasse Player uit slay.py, zodat we daarop kunnen verderbouwen
from slay import Player


# ANSI-kleurcode voor rood (werkt in de meeste terminals, ook in VS Code)
ROOD = "\033[91m"
# ANSI-kleurcode voor blauw
BLAUW = "\033[94m"
# ANSI-kleurcode voor geel
GEEL = "\033[93m"
# ANSI-kleurcode voor grijs
GRIJS = "\033[90m"
# ANSI-code voor vetgedrukte tekst
VET = "\033[1m"
# ANSI-code die alle opmaak weer uitzet
RESET = "\033[0m"

# Woordenboek dat bij elke kaartnaam een kleur hoort: Strike = rood, Block = blauw
KAART_KLEUR = {"Strike": ROOD, "Block": BLAUW}


# Hulpfunctie die één kaart als gekleurd blokje teruggeeft, bv. [Strike]
def toon_kaart(kaart: str) -> str:
    # Zoek de kleur van de kaart op (onbekende kaart = geen kleur) en zet haakjes errond
    return f"{KAART_KLEUR.get(kaart, '')}[{kaart}]{RESET}"


# Hulpfunctie die een hele lijst kaarten als één regel tekst teruggeeft
def toon_kaarten(kaarten: list[str]) -> str:
    # Als de lijst leeg is, tonen we het woord 'leeg' in grijs
    if not kaarten:
        # Geef de grijze tekst '(leeg)' terug
        return f"{GRIJS}(leeg){RESET}"
    # Zet elke kaart om naar een gekleurd blokje en plak ze aan elkaar met een spatie
    return " ".join(toon_kaart(k) for k in kaarten)


# Nieuwe klasse die alles van Player erft, maar extra uitleg en visualisatie toont
class VisualPlayer(Player):

    # Overschrijf draw_card zodat we tonen wat er bij het trekken gebeurt
    def draw_card(self) -> None:
        # Controleer of de draw pile leeg is vóór we trekken
        if not self.draw_pile and self.discard_pile:
            # Leg uit wat er nu gaat gebeuren
            print(f"{GEEL}♻️  De draw pile is leeg! De {len(self.discard_pile)} kaarten "
                  # Tweede deel van dezelfde zin (Python plakt beide stukken tekst aan elkaar)
                  f"uit de discard pile worden teruggelegd en geschud.{RESET}")
        # Onthoud hoeveel kaarten er in de hand zitten vóór het trekken
        aantal_voor = len(self.hand)
        # Laat de oorspronkelijke methode van Player het echte werk doen
        super().draw_card()
        # Als de hand gegroeid is, werd er effectief een kaart getrokken
        if len(self.hand) > aantal_voor:
            # Toon welke kaart (de laatst toegevoegde) van de draw pile naar de hand ging
            print(f"   🃏 Je trekt {toon_kaart(self.hand[-1])}  draw pile ➜ hand")

    # Overschrijf start_turn zodat we een duidelijke titel tonen
    def start_turn(self) -> None:
        # Toon een lege regel en een titel voor de nieuwe beurt (beurtnummer + 1, want het wordt zo verhoogd)
        print(f"\n{VET}▶ Beurt {self.turn + 1} begint: je trekt {self.HAND_SIZE} kaarten{RESET}")
        # Laat de oorspronkelijke methode van Player de beurt starten
        super().start_turn()

    # Overschrijf end_turn zodat we tonen welke kaarten afgelegd worden
    def end_turn(self) -> None:
        # Toon welke kaarten uit de hand naar de discard pile gaan
        print(f"\n{VET}■ Einde beurt:{RESET} {toon_kaarten(self.hand)}  hand ➜ discard pile")
        # Laat de oorspronkelijke methode van Player de hand afleggen
        super().end_turn()

    # Overschrijf play_card zodat ook kleine letters werken en we uitleg tonen
    def play_card(self, card: str) -> None:
        # Maak van de invoer een nette kaartnaam, bv. 'strike' wordt 'Strike'
        card = card.capitalize()
        # Laat de oorspronkelijke methode van Player de kaart spelen
        super().play_card(card)
        # Als de kaart echt gespeeld werd, ligt ze nu bovenaan de discard pile
        if self.discard_pile and self.discard_pile[-1] == card:
            # Leg uit waar de kaart naartoe ging
            print(f"   {toon_kaart(card)}  hand ➜ discard pile")

    # Overschrijf show_status zodat de drie stapels visueel getoond worden
    def show_status(self) -> None:
        # Bereken het totaal aantal kaarten over de drie stapels (moet altijd 10 zijn)
        totaal = len(self.draw_pile) + len(self.hand) + len(self.discard_pile)
        # Toon een kopregel met de naam en het beurtnummer
        print(f"\n{VET}=========== Speler {self.name} / beurt {self.turn} ==========={RESET}")
        # Toon de draw pile als verborgen kaarten (■), want je weet de volgorde niet
        print(f"📦 Draw pile    ({len(self.draw_pile):2}): {GRIJS}{'■ ' * len(self.draw_pile) or '(leeg)'}{RESET}")
        # Toon de kaarten in de hand, met kleur
        print(f"✋ Hand         ({len(self.hand):2}): {toon_kaarten(self.hand)}")
        # Toon de kaarten in de discard pile, met kleur
        print(f"🗑️  Discard pile ({len(self.discard_pile):2}): {toon_kaarten(self.discard_pile)}")
        # Toon het totaal, zodat je ziet dat kaarten enkel verschuiven en nooit verdwijnen
        print(f"{GRIJS}   Totaal: {totaal} kaarten (ze verhuizen alleen tussen de stapels){RESET}")
        # Toon welke acties mogelijk zijn
        print(f"{GRIJS}   Typ een kaartnaam (Strike/Block), 'end' of 'quit'{RESET}")

    # Overschrijf play_game zodat we eerst de spelregels tonen
    def play_game(self) -> None:
        # Toon een titel
        print(f"\n{VET}{GEEL}*** Welkom bij Slay the Spire (mini-versie) ***{RESET}")
        # Regel 1: hoe een beurt start
        print("• Bij elke beurt trek je 5 kaarten van de draw pile naar je hand.")
        # Regel 2: wat er met gespeelde kaarten gebeurt
        print("• Een gespeelde kaart gaat van je hand naar de discard pile.")
        # Regel 3: wat er op het einde van de beurt gebeurt
        print("• Typ 'end': de rest van je hand gaat ook naar de discard pile.")
        # Regel 4: wat er gebeurt als de draw pile leeg is
        print("• Is de draw pile leeg? Dan wordt de discard pile geschud en wordt ze je nieuwe draw pile.")
        # Laat de oorspronkelijke spellus van Player het spel spelen
        super().play_game()
        # Toon een afscheidsboodschap nadat de speler 'quit' typte
        print(f"\n{GEEL}Bedankt voor het spelen, {self.name}!{RESET}")


# Deze code wordt alleen uitgevoerd als je dit bestand rechtstreeks start
if __name__ == '__main__':
    # Vraag de naam van de speler
    name = input("Hello, what is your name? ")
    # Maak een VisualPlayer in plaats van een gewone Player
    p = VisualPlayer(name)
    # Start het spel
    p.play_game()
