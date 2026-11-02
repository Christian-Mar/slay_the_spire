# Importeer 'os' om de poort uit de omgeving te kunnen lezen
import os

# Importeer NiceGUI: het framework waarmee we een webinterface in pure Python bouwen
from nicegui import ui

# Importeer de oorspronkelijke klasse Player; de spellogica blijft dus ongewijzigd
from slay import Player

# Per kaartnaam: icoon, kleurverloop en een korte beschrijving
KAARTEN = {
    "Strike": {"icoon": "⚔️", "kleur": "linear-gradient(160deg, #ef4444, #7f1d1d)", "tekst": "Deal 6 damage"},
    "Block": {"icoon": "🛡️", "kleur": "linear-gradient(160deg, #3b82f6, #1e3a8a)", "tekst": "Gain 5 block"},
}

# CSS voor de kaarten, de stapels en de animaties
CSS = """
body { background: radial-gradient(circle at 50% 0%, #2a2140, #0f0c1a 70%); color: #eee; }
.kaart {
    width: 120px; height: 170px; border-radius: 12px; padding: 8px;
    border: 3px solid #fcd34d; color: white; cursor: pointer;
    display: flex; flex-direction: column; align-items: center; justify-content: space-between;
    box-shadow: 0 6px 14px rgba(0,0,0,.5);
    transition: transform .2s, box-shadow .2s;
    
}
.kaart.nieuw { animation: delen .45s ease-out backwards; }
.kaart:hover { transform: translateY(-22px) scale(1.12) rotate(-2deg); box-shadow: 0 16px 24px rgba(0,0,0,.7); z-index: 5; }
.kaart .naam { font-weight: bold; letter-spacing: 1px; }
.kaart .icoon { font-size: 54px; }
.kaart .tekst { font-size: 12px; text-align: center; opacity: .9; }
@keyframes delen {
    from { transform: translate(-300px, -80px) rotate(-25deg); opacity: 0; }
    to { transform: none; opacity: 1; }
}
.rug {
    width: 56px; height: 80px; border-radius: 8px; border: 2px solid #a78bfa;
    background: repeating-linear-gradient(45deg, #4c1d95, #4c1d95 6px, #5b21b6 6px, #5b21b6 12px);
    box-shadow: 0 2px 6px rgba(0,0,0,.5);
}
.mini { width: 56px; height: 80px; border-radius: 8px; border: 2px solid #fcd34d;
        display: flex; align-items: center; justify-content: center; font-size: 28px; }
.arena { width: 100%; max-width: 760px; display: flex; justify-content: space-between; align-items: flex-end;
         padding: 20px 40px; border-radius: 16px; background: linear-gradient(#1e1b3a, #2d2552 70%, #3b2f2f 70%); }
.figuur { display: flex; flex-direction: column; align-items: center; gap: 4px; position: relative; width: 170px; }
.sprite { font-size: 90px; line-height: 1; filter: drop-shadow(0 8px 6px rgba(0,0,0,.6)); }
.balk { width: 150px; height: 14px; background: #3f3f46; border-radius: 7px; overflow: hidden; border: 1px solid #000; }
.balk > div { height: 100%; transition: width .5s; }
.intentie { background: #7f1d1d; padding: 2px 10px; border-radius: 10px; font-size: 13px; }
.valt-aan-rechts { animation: stoot-rechts .5s ease-in-out; }
.valt-aan-links { animation: stoot-links .5s ease-in-out; }
.geraakt { animation: schok .45s; }
.dood { transform: rotate(90deg) translateY(30px); opacity: .3; transition: all .6s; }
.getal { position: absolute; top: 0; font-size: 34px; font-weight: 900; text-shadow: 0 2px 4px #000;
         animation: zweef 1.1s ease-out forwards; pointer-events: none; }
@keyframes stoot-rechts { 50% { transform: translateX(150px) rotate(8deg); } }
@keyframes stoot-links { 50% { transform: translateX(-150px) rotate(-8deg); } }
@keyframes schok { 0%,100% { transform: none; filter: none; } 20%,60% { transform: translateX(-12px); filter: brightness(2) sepia(1) hue-rotate(-40deg) saturate(6); } 40%,80% { transform: translateX(12px); } }
@keyframes zweef { from { transform: translateY(0); opacity: 1; } to { transform: translateY(-80px); opacity: 0; } }
.stapel-titel { font-weight: bold; letter-spacing: 2px; opacity: .8; }
"""


# Eén browser-sessie = één speler; de pagina wordt per bezoeker opgebouwd
@ui.page("/")
def hoofdpagina() -> None:
    # Voeg de CSS toe aan de pagina
    ui.add_css(CSS)
    # Maak een speler voor deze bezoeker en start meteen de eerste beurt
    speler = Player("Held")
    speler.start_turn()
    # Vijanden die na elkaar opduiken: naam, sprite, levenspunten en schade per beurt
    vijanden = [("Slijm", "🟢", 20, 5), ("Goblin", "👺", 30, 7), ("Demon", "👹", 40, 9)]
    # Toestand van het gevecht
    st = {"hp": 50, "block": 0, "vijand": 0, "vhp": vijanden[0][2], "anim": {}, "nieuw": True,
          "tekst": "Een nieuwe beurt begint: je trekt 5 kaarten.", "einde": ""}

    # Geeft (naam, sprite, max hp, schade) van de huidige vijand
    def vijand():
        return vijanden[min(st["vijand"], len(vijanden) - 1)]

    # Kaart van de hand spelen: verplaatst ze naar de discard pile en heeft een effect
    def speel(kaart: str) -> None:
        if st["einde"]:
            return
        speler.play_card(kaart)
        st["nieuw"] = False
        st["anim"] = {}
        if kaart == "Strike":
            st["vhp"] = max(0, st["vhp"] - 6)
            st["anim"] = {"speler": "valt-aan-rechts", "vijand": "geraakt", "getal_vijand": ("-6", "#f87171")}
            st["tekst"] = f"Je speelde Strike: {vijand()[0]} verliest 6 HP."
            if st["vhp"] == 0:
                st["anim"]["dood"] = True
                st["tekst"] = f"{vijand()[0]} is verslagen! Beëindig je beurt voor de volgende vijand."
        else:
            st["block"] += 5
            st["anim"] = {"getal_speler": ("+5 🛡️", "#60a5fa")}
            st["tekst"] = "Je speelde Block: +5 block."
        scherm.refresh()

    # Beurt beëindigen: de vijand slaat terug, daarna begint een nieuwe beurt
    def einde_beurt() -> None:
        if st["einde"]:
            return
        speler.end_turn()
        st["anim"] = {}
        naam, _, _, schade = vijand()
        if st["vhp"] == 0:
            # Vijand dood: de volgende komt
            st["vijand"] += 1
            if st["vijand"] >= len(vijanden):
                st["einde"] = "🏆 Overwinning! Alle vijanden zijn verslagen."
            else:
                st["vhp"] = vijand()[2]
                st["tekst"] = f"Een nieuwe vijand verschijnt: {vijand()[0]}!"
        else:
            # Block vangt eerst de schade op, de rest gaat van je HP af
            opgevangen = min(st["block"], schade)
            echt = schade - opgevangen
            st["hp"] = max(0, st["hp"] - echt)
            st["anim"] = {"vijand": "valt-aan-links", "speler": "geraakt",
                          "getal_speler": (f"-{echt}" if echt else "geblokt 🛡️", "#f87171" if echt else "#60a5fa")}
            st["tekst"] = f"{naam} valt aan voor {schade}: {opgevangen} geblokt, {echt} schade."
            if st["hp"] == 0:
                st["einde"] = "💀 Je bent verslagen."
                st["anim"]["dood_speler"] = True
        st["block"] = 0
        if not st["einde"]:
            speler.start_turn()
            st["nieuw"] = True
        scherm.refresh()

    # Alles opnieuw beginnen
    def herstart() -> None:
        nonlocal speler
        speler = Player("Held")
        speler.start_turn()
        st.update(hp=50, block=0, vijand=0, vhp=vijanden[0][2], anim={}, nieuw=True, einde="",
                  tekst="Nieuw spel gestart.")
        scherm.refresh()

    # Tekent één figuur (soldaat of vijand) met sprite, levensbalk en eventueel zwevend getal
    def teken_figuur(sprite: str, naam: str, hp: int, max_hp: int, klasse: str, kleur: str,
                     getal, dood: bool, flip: bool, extra: str = "") -> None:
        with ui.element("div").classes("figuur"):
            if getal:
                ui.html(f'<span class="getal" style="color:{getal[1]}">{getal[0]}</span>')
            if extra:
                ui.html(extra)
            stijl = "transform:scaleX(-1);" if flip else ""
            # Binnenste div krijgt de animatie, de buitenste de spiegeling
            ui.html(f'<div style="{stijl}"><div class="sprite {klasse} {"dood" if dood else ""}">{sprite}</div></div>')
            with ui.element("div").classes("balk"):
                ui.element("div").style(f"width:{100 * hp / max_hp}%;background:{kleur}")
            ui.label(f"{naam}  {hp}/{max_hp}").classes("text-sm")

    # Het gevechtsveld met soldaat links en vijand rechts
    def teken_arena() -> None:
        a = st["anim"]
        naam, sprite, max_vhp, schade = vijand()
        with ui.element("div").classes("arena"):
            blok = f'<div class="intentie" style="background:#1e3a8a">🛡️ {st["block"]}</div>' if st["block"] else ""
            teken_figuur("🤺", "Soldaat", st["hp"], 50, a.get("speler", ""), "#22c55e",
                         a.get("getal_speler"), st["hp"] == 0, False, blok)
            intentie = "" if st["vhp"] == 0 else f'<div class="intentie">⚔️ valt aan voor {schade}</div>'
            teken_figuur(sprite, naam, st["vhp"], max_vhp, a.get("vijand", ""), "#ef4444",
                         a.get("getal_vijand"), st["vhp"] == 0, False, intentie)

    # Tekent een stapel verborgen kaarten (draw pile)
    def teken_rug(aantal: int) -> None:
        with ui.column().classes("items-center gap-1"):
            ui.label(f"DRAW PILE ({aantal})").classes("stapel-titel")
            with ui.row().classes("gap-0 w-40 flex-wrap justify-center").style("min-height:90px"):
                for _ in range(aantal):
                    ui.element("div").classes("rug").style("margin-left:-40px")

    # Tekent een stapel zichtbare minikaarten (discard pile)
    def teken_discard(kaarten: list[str]) -> None:
        with ui.column().classes("items-center gap-1"):
            ui.label(f"DISCARD PILE ({len(kaarten)})").classes("stapel-titel")
            with ui.row().classes("gap-0 w-40 flex-wrap justify-center").style("min-height:90px"):
                for k in kaarten:
                    ui.html(f'<div class="mini" style="background:{KAARTEN[k]["kleur"]};margin-left:-34px">'
                            f'{KAARTEN[k]["icoon"]}</div>')

    # Het volledige scherm; refresh() tekent het opnieuw na elke actie
    @ui.refreshable
    def scherm() -> None:
        ui.label(f"Beurt {speler.turn}").classes("text-2xl font-bold")
        teken_arena()
        ui.label(st["einde"] or st["tekst"]).classes("text-amber-300 text-lg")
        # Draw pile links, discard pile rechts
        with ui.row().classes("w-full justify-around items-start mt-4"):
            teken_rug(len(speler.draw_pile))
            teken_discard(speler.discard_pile)
        # De hand: klik op een kaart om ze te spelen
        ui.label("HAND (klik om te spelen)").classes("stapel-titel mt-6")
        with ui.row().classes("gap-2 justify-center").style("min-height:190px"):
            if not speler.hand:
                ui.label("(lege hand, beëindig je beurt)").classes("text-gray-400 self-center")
            for i, k in enumerate(speler.hand):
                # animation-delay laat de kaarten één voor één binnenvliegen
                kaart = ui.html(
                    f'<div class="naam">{k}</div><div class="icoon">{KAARTEN[k]["icoon"]}</div>'
                    f'<div class="tekst">{KAARTEN[k]["tekst"]}</div>'
                ).classes("kaart nieuw" if st["nieuw"] else "kaart").style(f'background:{KAARTEN[k]["kleur"]};animation-delay:{i * 0.08}s')
                kaart.on("click", lambda _, k=k: speel(k))
        with ui.row().classes("gap-4 mt-4"):
            ui.button("End turn", icon="skip_next", on_click=einde_beurt).props("color=amber text-color=black")
            ui.button("Restart", icon="restart_alt", on_click=herstart).props("flat color=white")
        totaal = len(speler.draw_pile) + len(speler.hand) + len(speler.discard_pile)
        ui.label(f"Totaal: {totaal} kaarten (ze verhuizen alleen tussen de stapels)").classes("text-xs text-gray-500")

    with ui.column().classes("w-full items-center p-6"):
        ui.label("Slay the Spire (mini)").classes("text-4xl font-bold text-amber-300")
        scherm()


# Start de server (lokaal op http://localhost:8080); PORT laat hosting-platformen de poort bepalen
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Slay mini", port=int(os.environ.get("PORT", "8080")), reload=False, show=False)
