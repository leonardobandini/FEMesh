# SAP2000 Quad Mesher V2 2.0.50

Questa versione riunisce le modifiche locali successive alla 2.0.46: compatibilità FAST con le chiavi geometriche di SAP2000 27.2 beta, controllo dei nodi originali coincidenti e riuso delle identità SAP, trasferimento mirato dei modificatori di rigidezza, anteprima bloccata contro modifiche accidentali, backup prima di Genera e conferma separata prima di Applica.

Durante **Applica** e **Annulla mesh** la finestra di attesa, centrata sulla finestra SAP2000 aperta, avverte che il programma può sembrare bloccato e chiede di non chiuderlo né arrestarlo. Non presenta OK e si chiude automaticamente al termine. Compare prima del ripristino della vista; dopo Genera un avviso analogo precede il nascondimento delle aree originali. I comandi Vista di SAP2000 possono apparire brevemente perché non esiste un'API di visibilità per singolo oggetto nella sola vista attiva.

La regressione SAP2000 27.1 sul pacchetto completo: **36/36 PASS** in quattro sessioni indipendenti (nove esempi per sessione). Risultati e modelli di prova isolati in `%TEMP%\opencode\v250-full36-fourworkers-package-20261016`; gli SDB sorgenti non sono stati salvati dal test.
