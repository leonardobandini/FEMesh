# SAP2000 Quad Mesher V2 2.0.17 — release per prove collaborative

Release ZIP autonomo per Windows x64 / SAP2000 27.1.0 / .NET Framework 4.8. Il runtime Gmsh è incluso; non è richiesta un'installazione Python. Chiudere SAP2000, estrarre l'intero ZIP, eseguire `install_plugin.cmd` e riaprire il programma. Aprire **Tools > SAP2000 Quad Mesher** e controllare `2.0.17` nel titolo. Usare copie dei modelli durante le prove; salvare manualmente il risultato solo dopo la verifica tecnica.

## Migrazione xAPI e assegnazioni

- Contratto plugin, accesso al modello, importazione tabelle e snapshot usano `CSiAPIv1` (xAPI). La V2 non distribuisce DLL CSI proprietarie.
- L'area padre trasferisce ai figli sezione, assi locali semplici, massa, edge constraint, modificatori, materiale, temperatura materiale, gruppi, carichi e molle/pressioni superficiali. Pressioni e molle assegnate a un bordo vengono trasferite solo ai corrispondenti bordi figli, con verifica della lunghezza totale. I tipi di carico non provati individualmente sono distinti nella guida.
- Annulla dopo Applica ricostruisce le aree poligonali con la lista completa dei nodi e ripristina le tabelle delle assegnazioni agli oggetti. I load pattern usati per leggere quelle tabelle sono selezionati temporaneamente e il filtro precedente viene ripristinato. Carichi, molle, restraint, vincoli e joint pattern dei nodi originali sono stati verificati nella fixture di ripristino.
- La guida offline italiana/inglese (F1 o ?) include una **matrice a tre colonne**: proprietà padre, trasferimento ai figli, ripristino del padre con Annulla. 🟢 significa prova riuscita; 🟡 significa limite o prova non conclusa; 🔴 indica l'errore xAPI osservato.

## Sovrascritture di progetto shell: limite dichiarato

Le sovrascritture specifiche di progetto delle shell **non sono trasferite automaticamente** in questa release. Nella prova SAP2000 27.1.0 il getter e il setter EC2 hanno restituito codice `1`. Se SAP segnala una tabella di sovrascritture/procedura non vuota ma illeggibile tramite API, il preflight non blocca più per questa sola ragione: il plugin avverte di **replicare manualmente l'impostazione sui figli**. Con copia numerata disattivata consiglia di attivarla e rigenerare; con copia attiva comunica il percorso reale del backup creato prima di meshare. Il backup contiene l'**ultimo `.sdb` salvato**, non le modifiche SAP non salvate. Annulla non garantisce il recupero di un overwrite inaccessibile.

La release è stata provata su SAP2000 27.1.0, **non** risolve né certifica il comportamento delle tabelle nella beta 27.2.0. Carichi area→frame e valori legati a joint pattern/spessore/offset sui nuovi joint non sono ripartiti senza una regola fisica validata: la mesh si ferma in questi casi. La propagazione dei joint pattern ai nodi nuovi resta oggetto di studio.

## Verifiche di regressione

- FAST `nTEST002`: 77 shell figlie e fixture padre→figli per gruppi, sezione, materiale, modificatori, assi, massa, edge constraint, carico/pressione/molla. Standard `nTEST003`: 61 shell, fixture equivalente. Pressione e molla di bordo: copertura 2,2 m e 2,0 m, uguale ai rispettivi bordi padre. FAST e Standard Applica→Annulla PASS su copie.
- Prova atomica del percorso di warning EC2 illeggibile: mesh e Annulla completati sia con backup spento sia con backup attivo; controllati testo e file numerato. Il valore EC2 esplicito resta **non verificabile** tramite l'API che ha restituito codice `1`; la prova del warning usa una simulazione controllata, non un overwrite realmente imposto.
- Guida offline IT/EN, 24 esempi e backend congelato validati. Test installer su pacchetto estratto e aggiornamento da V1 / V2 precedente eseguiti durante la build della release.

Il manifest pubblico V2 viene aggiornato soltanto dopo che ZIP e checksum caricati nella release sono verificati. Il manifest V1 resta separato. Il pacchetto sorgenti corrispondente e i sorgenti Gmsh sono disponibili negli asset della stessa release.
