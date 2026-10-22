# SAP2000 Quad Mesher V2 2.0.38 — guida tecnica bilingue

La guida offline è stata rivista confrontandola con i controlli effettivi delle quattro schede. Nuove schermate numerate EN/IT sono acquisite direttamente dalla finestra 2.0.38. La descrizione del flusso operativo adotta una sequenza strutturata e distingue le aree SAP2000 sorgenti dagli elementi shell generati e dalle loro assegnazioni.

I campi di lunghezza accettano valori nell'unità corrente mostrata accanto al campo oppure numeri con suffisso `m`, `cm`, `mm`, `ft` o `in`; in quest'ultimo caso il plugin converte il valore automaticamente. La vecchia opzione Tolleranza non compare nell'interfaccia corrente: i criteri dimensionali del report qualità sono fissi e non sono presentati come controlli di meshing. Non vengono presentate opzioni di configurazione manuale delle superfici strutturate o dei campi dimensionali, assenti dalla UI.

Questa release modifica documentazione e numero di versione, senza alterare l'algoritmo Gmsh, il trasferimento SAP2000 o i valori iniziali. Sono inclusi installer standalone, sorgenti corrispondenti e guida bilingue. La regressione completa su 36 copie isolate dei modelli SAP viene rieseguita sul pacchetto finale prima della pubblicazione.
