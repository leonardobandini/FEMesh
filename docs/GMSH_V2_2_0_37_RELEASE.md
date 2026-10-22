# SAP2000 Quad Mesher V2 2.0.37 — scheda Opzioni aggiuntive compatta

La casella **Preferisci mesh regolari allineate alla griglia (se possibile)** si trova ora in cima a **Additional Options / Opzioni aggiuntive**, seguita da simmetria, fori e aperture. La scheda contiene tutti i controlli senza richiedere lo scorrimento nella finestra standard, sia in inglese sia in italiano. I testi di aiuto sono stati resi più brevi mantenendo le spiegazioni complete nella guida offline.

La preferenza rimane inizialmente disattivata; la sua modalità Gmsh, il JSON inviato, Reset e le preferenze salvate funzionano come nella 2.0.36. La transfinite automatica è una preferenza per le superfici compatibili: **non forza una griglia lungo gli assi globali o locali**. Simmetria esatta resta un controllo distinto.

Verifica: build net48 senza avvisi, test UI EN/IT della visibilità integrale della scheda senza barre, default OFF, JSON, reset e ripristino; guida bilingue validata, test backend e prove di installazione standalone. Restano disponibili gli esempi SAP verificati nella 2.0.36. Installare con SAP2000 chiuso e riavviarlo prima della prova.
