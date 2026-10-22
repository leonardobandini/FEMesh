# SAP2000 Quad Mesher 2.0.40 — candidato locale, non pubblicato

La finestra rimane utilizzabile dopo Applica: una nuova selezione, nello stesso SDB o in un SDB diverso aperto nella stessa sessione SAP2000, riabilita Genera solo dopo aver concluso e liberato lo snapshot della mesh precedente. Una nuova operazione acquisisce il proprio snapshot dal modello corrente. Gruppi, simmetria disponibile e valori di lunghezza vengono aggiornati quando cambia modello o unità SAP2000.

**Semantica di conferma:** Annulla mesh è disponibile soltanto mentre la mesh è in anteprima. Applica conferma la transazione, elimina lo snapshot temporaneo e disabilita Annulla; il backup numerato dell'ultimo SDB salvato è indipendente da tale snapshot. In presenza di dati non salvati, la conferma non salva automaticamente il modello SAP2000 su disco.

La prova di integrazione su copie isolate verifica `Genera → Applica → cambia SDB → seleziona → Genera → Applica` nella stessa finestra, nonché un secondo ciclo nello stesso modello e il passaggio fra unità di misura. Nessuno dei due SDB sorgenti dei test viene modificato. La distribuzione pubblica e il feed restano alla versione 2.0.39 fino a una richiesta successiva.
