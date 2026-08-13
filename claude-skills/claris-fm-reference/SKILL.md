---
name: claris-fm-reference
description: >
  Nachschlagewerk für Claris FileMaker: Funktionen, Script Steps und deren
  deutsche/englische Namen. Immer verwenden, wenn es um FileMaker-Funktionen,
  Kalkulationen, Formeln, Script Steps, Scriptschritte, Get()-/Hole()-Funktionen,
  Fehlercodes oder FileMaker-Syntax geht — auch wenn der Name nur auf Deutsch
  genannt wird (z.B. "SetzeVar", "Gehe zu Layout", "Hole(LetzterFehler)") oder
  die Frage beiläufig wirkt. Niemals FileMaker-Signaturen oder Parameternamen
  aus dem Gedächtnis beantworten — zuerst hier den Slug nachschlagen und die
  Doku-Seite live fetchen.
---

# Claris FileMaker Reference

Zweck: FileMaker-Fragen mit der offiziellen Claris-Doku beantworten statt aus
dem (lückenhaften, ggf. veralteten) Modellwissen.

## Workflow

1. **Namen auflösen.** Deutscher Name genannt? → `references/mapping-de-en.md`
   lesen (Format: `Deutsch | English | slug`). Englischer Name? → Slug in
   `references/functions.md` bzw. `references/script-steps.md` nachschlagen
   (Format: `Name | slug`).
2. **Doku-Seite fetchen.**
   `https://help.claris.com/markdown/en/pro-help/<slug>.md`
   Für deutsche Antworten/Zitate wahlweise `markdown/de/` — gleiche Slugs.
   Diese Seiten enthalten Signatur, Parameter, Kompatibilität und Beispiele.
3. **Antworten.** Signaturen und Parameternamen wörtlich aus der Doku
   übernehmen, nicht rekonstruieren. In FileMaker-Code: kein Leerzeichen vor
   Semikolon.

## Weitere Doku (außerhalb Funktionen/Steps)

Gleiches URL-Schema, andere Guides:
`https://help.claris.com/markdown/en/<guide>/<slug>.md` mit guide ∈
`pro-help`, `data-api-guide`, `admin-api-guide`, `odata-guide`,
`server-help`, `fms-installation-guide`. Slug unbekannt? Index fetchen:
`https://help.claris.com/llms.txt` (kuratiert) oder gezielt per Web-Suche
`site-unabhängig: "help.claris.com" <Thema>`.

Nützliche Direktlinks: Fehlercodes → `pro-help/error-codes.md`,
cURL-Optionen → `pro-help/curl-options.md`,
Script-Trigger → `pro-help/script-triggers-reference.md`.

## Aktualität

Die gebündelten Referenzdateien sind Snapshots (Generierungsdatum steht im
Header jeder Datei). Bei Fragen nach vollständigen oder aktuellen Listen
(alle Funktionen einer Kategorie, Neuerungen einer Version) nicht die
Indizes zitieren, sondern die Kategorie-Seite live fetchen (z.B.
`pro-help/text-functions.md`) — die Indizes dienen der Slug-Auflösung.

## Wartung

`python3 scripts/update.py` regeneriert alle drei Referenzdateien aus der
Navigations-TOC der Claris-Hilfe (MadCap, Data/Tocs/main_toc*.js) —
Indizes aus der en-TOC, Mapping als de/en-Join über den Slug. Nach jedem FileMaker-Release einmal ausführen. Fehlt
`mapping-de-en.md`, ebenfalls dieses Script ausführen.
