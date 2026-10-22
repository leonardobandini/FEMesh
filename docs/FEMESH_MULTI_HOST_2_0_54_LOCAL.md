# FEMesh 2.0.54: candidata locale SAP2000 / CSiBridge

FEMesh è il nome visibile della finestra e della voce Tools. L'identità COM `SapQuadTransitionPlugin.cPlugin`, il CLSID, il nome fisico della DLL e la cartella tecnica dell'installazione precedente sono conservati per aggiornare le installazioni esistenti senza cambiare il nome del repository GitHub. L'installer per utente aggiorna i menu di **SAP2000 27 e CSiBridge 27**, conservando le altre voci. La build V2 seleziona `CSiAPIv1.dll` da SAP2000 oppure, se SAP2000 non è installato, da CSiBridge; non richiede `SAP2000v1.dll` per il plugin V2 e l'installer.

La selezione dinamica mantiene lo stato dei checkbox: quando la finestra si apre senza aree, FAST e backup sono disabilitati ma non deselezionati; selezionando successivamente una shell diventano nuovamente disponibili con le scelte precedenti. Anche la spiegazione del backup si disabilita/riabilita insieme al checkbox.

## CSiBridge 27.1

Su copie dei modelli atomici SDB, aperte con CSiBridge e salvate come BDB:

| Copia | Applica FEMesh | Annulla FEMesh |
|---|---:|---:|
| `nTEST001` | 1 → 8 aree; BDB riaperto | 1 → 1 area; BDB riaperto |
| `nTEST014` | 2 → 142 aree; BDB riaperto | 2 → 2 aree; BDB riaperto |

Le prove di Applica sono in `%TEMP%\opencode\femesh-v254-bridge-reopen-20261021`; quelle di Annulla in `%TEMP%\opencode\femesh-v254-bridge-undo-20261021`. Sono state eseguite tramite xAPI sulla DLL compilata usando **soltanto** la CSiAPI di Bridge. Non modificano né salvano gli SDB originali. L'apertura dal menu Tools nel processo Bridge resta da verificare dopo l'installazione locale.

La matrice completa è **36/36 PASS** sulla build finale Bridge-only, in una singola sessione CSiBridge persistente. Ogni SDB originale è stato copiato, aperto in Bridge, salvato come BDB, meshato con i parametri del catalogo atomico, salvato e riaperto; il checksum di ogni SDB originale coincide con la copia pre-mesh. I BDB verificati e il riepilogo sono in `%TEMP%\opencode\femesh-v254-bridge-matrix-final-retest-20261021`. Il totale delle aree può restare invariato quando alcune aree vengono sostituite da altrettante: la verifica richiede elementi generati positivi e inventario finale riaperto, non un aumento artificioso del conteggio.

SAP2000 27.1: **36/36 PASS** su due sessioni persistenti in parallelo, 24 e 12 modelli aperti in sequenza; riepilogo in `%TEMP%\opencode\femesh-v254-sap-matrix-20261021\summary.csv`. Preview→Annulla Standard e FAST: PASS.

Queste verifiche sono state eseguite sulla candidata installata localmente prima del rilascio. Il plugin non salva automaticamente il modello aperto; la verifica del FEM finale sul modello di progetto spetta all'utilizzatore.
