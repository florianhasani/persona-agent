# Agent-Architektur: Persona Marketing Agent

## Ueberblick

Die Anwendung ist ein Multi-Agent-System mit Google ADK:
- root_agent koordiniert den Ablauf
- persona_agent erstellt 3 Personas
- messaging_agent erstellt pro Persona Messaging (Value Proposition, CTA, Ad Copy)

## Architektur

Nutzerinput
|
v
root_agent
|–> persona_agent (3 Personas)
|–> messaging_agent (Messaging je Persona)
v
Ausgabe: PERSONAS + MESSAGING

## Komponenten

### root_agent
- Extrahiert aus dem Input: Produkt, Zielgruppe, Marketingziel, Ton, Zusatzinfos, Sprache
- Delegiert Persona-Erstellung an persona_agent
- Delegiert Messaging-Erstellung an messaging_agent
- Formatiert die Ausgabe in zwei Sektionen: PERSONAS und MESSAGING

### persona_agent
- Liefert 3 unterscheidbare Personas
- Jede Persona enthaelt Ziel, Schmerzpunkt, Trigger und bevorzugte Kanaele

### messaging_agent
- Erzeugt pro Persona:
  - Value Proposition
  - CTA
  - Ad Copy (3 bis 5 Saetze)
  - Optional Keywords

## Fehlerbehandlung

API-Fehler (z. B. Quota-Limits oder Netzwerkprobleme) werden auf Anwendungsebene abgefangen und transparent an den Nutzer weitergegeben.  
Die Anwendung maskiert keine externen API-Fehler, sondern stellt eine klare Fehlermeldung dar. Dadurch bleibt die Systemarchitektur nachvollziehbar und technisch sauber.