# slay_the_spire

Advanced Python - dagelijks werk 1 (vervaldatum: 9 november 2026 23:59, meerdere inzendingen toegestaan)

## Opdracht

```python
# Het spel "Slay the Spire" is een kaartspel waar de SPELER
# monsters verslaat door kaarten te spelen.

# De speler heeft drie stapels kaarten:
#  - de draw pile waaruit nieuwe kaarten getrokken worden
#  - zijn "hand"
#  - de discard pile waar gespeelde kaarten terecht komen

# Bij de start van elke beurt trekt de speler 5 kaarten uit zijn
# draw pile naar zijn "hand".
# De speler kan daarna zoveel kaarten spelen als hij wil.
# Gespeelde kaarten gaan naar de "discard pile"
# Aan het einde van de beurt gaan de overgebleven kaarten uit de hand
# ook naar de discard pile.

# Als er geen kaarten meer zijn in de draw pile, wordt de discard pile
# terug toegevoegd aan de drawpile en de kaarten worden geschud.

class Player:
    ...


if __name__ == '__main__':
    name = input("Hello, what is your name? ")
    p = Player(name)
    p.play_game()
```

### Verwachte output

```
Hello, what is your name? X
===========player X / (turn 1)
hand: ['Block', 'Block', 'Block', 'Block', 'Strike']
What do you want to do?Block
Playing card Block
===========player X / (turn 1)
hand: ['Block', 'Block', 'Block', 'Strike']
What do you want to do?Strike
Playing card Strike
===========player X / (turn 1)
hand: ['Block', 'Block', 'Block']
What do you want to do?end
===========player X / (turn 2)
hand: ['Block', 'Strike', 'Strike', 'Strike', 'Strike']
What do you want to do?Strike
Playing card Strike
===========player X / (turn 2)
hand: ['Block', 'Strike', 'Strike', 'Strike']
What do you want to do?Block
Playing card Block
===========player X / (turn 2)
hand: ['Strike', 'Strike', 'Strike']
What do you want to do?end
===========player X / (turn 3)
hand: ['Block', 'Block', 'Block', 'Strike', 'Strike']
What do you want to do?Block
Playing card Block
===========player X / (turn 3)
hand: ['Block', 'Block', 'Strike', 'Strike']
What do you want to do?Block
Playing card Block
===========player X / (turn 3)
hand: ['Block', 'Strike', 'Strike']
What do you want to do?Block
Playing card Block
===========player X / (turn 3)
hand: ['Strike', 'Strike']
What do you want to do?quit
```

(De getrokken kaarten verschillen per spel, want de draw pile wordt willekeurig geschud.)

## Bestanden

| Bestand | Wat het is |
| --- | --- |
| `slay.py` | De opdracht zelf: klasse `Player` met tekstspel in de terminal |
| `slay_visueel.py` | Terminalversie met kleuren en uitleg over waar kaarten naartoe gaan |
| `slay_nicegui.py` | Grafische webversie (NiceGUI) met kaarten, soldaat en vijanden |

De spelregels uit de opdracht zitten alleen in `slay.py`. De twee andere versies bouwen erop voort.
Het gevecht (HP, schade, block, vijanden) in `slay_nicegui.py` is een eigen toevoeging en staat niet in de opdracht.

## Starten

Python 3.10 of hoger is nodig.

### 1. Opdrachtversie (terminal)

```bash
cd /Users/christianmarginet/Documents/slay
python3 slay.py
```

### 2. Visuele terminalversie

```bash
cd /Users/christianmarginet/Documents/slay
python3 slay_visueel.py
```

### 3. Webversie met NiceGUI

Eenmalig de omgeving klaarzetten:

```bash
cd /Users/christianmarginet/Documents/slay
python3 -m venv .venv
.venv/bin/pip install nicegui
```

Starten op poort 8765 (verander het getal als die poort bezet is):

```bash
cd /Users/christianmarginet/Documents/slay && PORT=8765 .venv/bin/python slay_nicegui.py
```

Open daarna http://localhost:8765 in de browser. Stoppen kan met `Ctrl+C` in de terminal.
Zonder `PORT=...` gebruikt de server poort 8080.

## Spelen

### Terminal (`slay.py` en `slay_visueel.py`)

Na het opstarten vul je je naam in. Daarna kun je telkens een van deze dingen typen:

| Invoer | Effect |
| --- | --- |
| `Strike` of `Block` | Speelt die kaart: ze gaat van je hand naar de discard pile |
| `end` | Beëindigt de beurt: de rest van je hand gaat naar de discard pile en je trekt 5 nieuwe kaarten |
| `quit` | Stopt het spel |

Is de draw pile leeg bij het trekken, dan worden de discard pile en eventuele resterende kaarten teruggelegd en geschud.
Je mag zoveel kaarten spelen als je wilt in een beurt.

### Web (`slay_nicegui.py`)

- Klik op een kaart in je hand om ze te spelen.
- Klik op **End turn** om je beurt te beëindigen. De vijand valt dan aan.
- **Strike** doet 6 schade aan de vijand, **Block** geeft 5 block. Block vangt de volgende aanval van de vijand op.
- Verslaat de soldaat alle drie de vijanden (Slijm, Goblin, Demon), dan win je. Zakt je HP naar 0, dan verlies je.
- Met **Restart** begin je opnieuw.

Net als in de opdracht mag je zoveel kaarten spelen als je wilt, want er is geen energie. Daardoor is het spel vrij makkelijk.

## Kaarten

De startstapel bestaat uit 10 kaarten: 5× `Strike` en 5× `Block`.
Deze kaarten verhuizen alleen tussen de drie stapels en verdwijnen nooit.
