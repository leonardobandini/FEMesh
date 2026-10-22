# SAP2000 Quad Mesher V2 2.0.36

## Novità

- Nuova preferenza **Preferisci mesh regolari allineate alla griglia (se possibile)** nella scheda generale Gmsh. È inizialmente disattivata; quando attiva richiede a Gmsh superfici transfinite automatiche dove compatibili. È salvata nelle preferenze e Reset la disattiva.
- La guida offline EN/IT descrive i quattro gruppi Gmsh, le finestre Impostazioni MeshAdapt/BAMG/QuadQS, le opzioni aggiuntive e di trasferimento, il campo per le opzioni numeriche e i parametri backend fissi; contiene configurazioni guidate e confronti SAP con opzione OFF/ON.
- Rispetto alla 2.0.32 pubblica, sono incluse le migliorie locali già verificate nelle 2.0.33–2.0.35: selezione dinamica durante l'apertura del plugin, opzioni di simmetria in cima alla relativa scheda e correzioni del flusso di anteprima.

## Verifica

- Build .NET net48 senza errori né avvisi; test UI/JSON/reset/persistenza e 20 test backend Python (1 escluso).
- Prove SAP su copie dei modelli: nTEST001 rettangolo OFF 50 quad / ON 55 quad; nTEST002 trapezio OFF 61 quad + 11 triangoli / ON 77 quad; nTEST003 triangolo, nTEST010 bordi vincolati, nTEST014 bordi condivisi, nTEST012 frame e nTEST005 foro O-grid completati con preferenza ON.
- Nove prove SAP isolate delle opzioni avanzate: MeshAdapt e RefineSteps, BAMG e i suoi due parametri, Blossom Full-Quad, Relocate2D, QuadQuasiStructured e due mappe, fallback algoritmo OFF. La preferenza regolare non garantisce quad ovunque: esaminare l'anteprima e il report qualità sul proprio modello.

## Distribuzione

Il pacchetto standalone contiene plugin, backend Gmsh 4.15.2, installer, guida offline bilingue, licenze e sorgenti corrispondenti nel relativo archivio. Installare con SAP2000 chiuso; la release non modifica i modelli sorgente.
