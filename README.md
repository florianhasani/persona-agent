# Persona Marketing Agent

Der **Persona Marketing Agent** ist eine KI-gestützte Marketing-Anwendung auf Basis des **Google Agent Development Kit (ADK)** und einer benutzerfreundlichen Oberfläche mit **Gradio**.  

Die Anwendung erstellt automatisch drei differenzierte Marketing-Personas und generiert darauf abgestimmtes Messaging (Value Proposition, Call-to-Action und Werbetext).  


## Projektziel

Ziel dieses Projekts ist die praktische Anwendung generativer KI im Marketingkontext durch den Einsatz des Google ADK.  

Im Fokus stehen:

- Entwicklung eines funktionsfähigen Multi-Agent-Systems  
- Strukturierte Aufgabendelegation zwischen spezialisierten Agenten  
- Umsetzung einer benutzerfreundlichen Web-Oberfläche  
- Integration von Fehlerbehandlung und robustem Systemverhalten  

Die Anwendung demonstriert, wie spezialisierte KI-Agenten koordiniert zusammenarbeiten können, um komplexere Marketingaufgaben modular zu lösen.


## Funktionsumfang

### Eingaben

Der Nutzer kann folgende Informationen angeben:

- Produkt oder Thema  
- Zielgruppe  
- Marketingziel (z. B. Leads, Kaufabschlüsse, Anmeldungen)  
- Tonalität (z. B. professionell, motivierend, emotional)  
- Zusatzinformationen  
- Sprache (Deutsch oder Englisch)

### Ausgaben

Die Anwendung erzeugt:

**1. Drei differenzierte Personas**, jeweils mit:
- Name  
- Alter  
- Rolle oder Lebenssituation  
- Ziel  
- Schmerzpunkt  
- Kauftrigger  
- Bevorzugte Kommunikationskanäle  

**2. Passendes Messaging je Persona**, bestehend aus:
- Value Proposition  
- Call-to-Action (CTA)  
- Werbetext (Ad Copy)  
- Optional: Keywords  

### Verfeinerung

Zusätzlich kann das generierte Ergebnis durch natürliche Sprache weiter angepasst werden.  
So wird eine iterative Optimierung des Outputs ermöglicht.

## Verwendung der Anwendung

1. Produkt oder Thema eingeben  
2. Zielgruppe definieren  
3. Marketingziel auswählen  
4. Ton festlegen  
5. Optional Zusatzinformationen ergänzen  
6. Auf „Generieren“ klicken  

Die Anwendung erstellt daraufhin automatisch Personas und passendes Messaging.

### Fehlerbehandlung

API-Fehler (z. B. Quota-Limits oder Netzwerkprobleme) werden abgefangen und transparent angezeigt.  
Die Anwendung bleibt dadurch technisch nachvollziehbar und robust.


## Agenten-Architektur

Die Anwendung basiert auf einer klar strukturierten Multi-Agent-Architektur:

- **root_agent**  
  Koordiniert den gesamten Workflow und delegiert Aufgaben an spezialisierte Sub-Agenten.

- **persona_agent**  
  Generiert drei klar unterscheidbare Marketing-Personas auf Basis der Nutzereingaben.

- **messaging_agent**  
  Erstellt strategisch abgestimmtes Messaging je Persona.

### Ablauf

1. Der Root-Agent analysiert die Nutzereingabe.  
2. Die Persona-Erstellung wird an den persona_agent delegiert.  
3. Die generierten Personas werden zusammen mit den Marketinginformationen an den messaging_agent übergeben.  
4. Die Ergebnisse werden strukturiert zusammengeführt und ausgegeben.  

Dieses Design demonstriert das Delegationsprinzip innerhalb des Google ADK.


## Installation und Ausführung

### Voraussetzungen

- Python 3.11 oder höher  
- Optional: `uv` als Paketmanager  

### Projekt einrichten

```bash
git clone <DEIN-REPO-URL>
cd marketing-agent
uv sync
```

Alternativ mit pip:

```bash
pip install -e .
```

### Anwendung starten

```bash
uv run python app.py
```

oder

```bash
python app.py
```

Anschließend im Browser öffnen:

```
http://localhost:7860
```


## Technologiestack

- Google ADK (Agent Development Kit)  
- Gemini-Modell (über Google API)  
- Gradio (Web-Oberfläche)  
- Python 3.11  


## Lernziele und Erkenntnisse

Durch die Umsetzung des Projekts wurden folgende Kompetenzen vertieft:

- Konzeption und Implementierung von Multi-Agent-Systemen  
- Strukturierung komplexer Marketingaufgaben in modulare KI-Komponenten  
- Prompt-Design für spezialisierte Agenten  
- Integration asynchroner Prozesse in eine Webanwendung  
- Gestaltung einer nutzerfreundlichen KI-Oberfläche  


## Beispielausgabe

Beispiel-Eingabe:

Produkt: Nachhaltige Sneakers  
Zielgruppe: Umweltbewusste Millennials  
Marketingziel: Leads generieren  
Ton: Informativ  

Beispiel-Ausgabe (gekürzt):

PERSONA 1  
Name: Laura  
Alter: 27  
Rolle: Nachhaltigkeitsbewusste Berufseinsteigerin  
Ziel: Umweltfreundliche Kaufentscheidung treffen  
Schmerzpunkt: Unsicherheit bei Greenwashing  
Trigger: Transparente Produktion, Zertifikate  

MESSAGING  
Value Proposition: Nachhaltige Sneakers mit transparenter Lieferkette und umweltfreundlichen Materialien.  
CTA: Jetzt mehr erfahren und nachhaltige Mode entdecken.  
Ad Copy: Unsere Sneakers verbinden Stil mit Verantwortung...

## Reflexion und Lernerfahrungen

Die Entwicklung des Persona Marketing Agenten hat gezeigt, wie leistungsfähig Multi-Agent-Systeme im Marketingkontext eingesetzt werden können. Besonders deutlich wurde, dass die Qualität der Ergebnisse stark von der klaren Aufgabenverteilung zwischen spezialisierten Agenten abhängt.

### Herausforderungen

Eine zentrale Herausforderung war das Verständnis der Agenten-Architektur im Google ADK. Insbesondere das Zusammenspiel zwischen Root-Agent und Sub-Agenten erforderte eine präzise Strukturierung der Instruktionen, damit Delegation und Ausgabeformat korrekt funktionieren.

Ein weiterer wichtiger Lernpunkt war das Prompt-Design. Kleine Änderungen in der Formulierung der Agent-Instruktionen führten zu deutlich unterschiedlichen Ergebnissen. Dadurch wurde deutlich, wie entscheidend präzise und strukturierte Anweisungen für konsistente Outputs sind.

Auch die Integration asynchroner Prozesse (async/await) in eine Webanwendung stellte eine technische Herausforderung dar. Die Kombination aus Google ADK und Gradio erforderte ein sauberes Handling von Sessions und Event-Loops.

Zusätzlich musste berücksichtigt werden, dass API-Limits oder Quota-Probleme auftreten können. Eine transparente Fehlerbehandlung war daher notwendig, um die Robustheit der Anwendung sicherzustellen.

### Erkenntnisse

Durch das Projekt wurde deutlich:

- Multi-Agent-Systeme ermöglichen eine klare Modularisierung komplexer Aufgaben.
- Spezialisierte Sub-Agenten liefern qualitativ bessere Ergebnisse als ein einzelner Generalist-Agent.
- Eine saubere Trennung von Koordination (Root-Agent) und Ausführung (Sub-Agenten) erhöht die Wartbarkeit des Systems.
- Benutzerfreundliche Oberflächen sind entscheidend, um KI-Anwendungen praxisnah einsetzbar zu machen.

Insgesamt hat das Projekt ein tieferes Verständnis für generative KI, Agenten-Architekturen und deren praktische Anwendung im Marketing vermittelt.