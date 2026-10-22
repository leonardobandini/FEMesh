# SAP2000 Quad Mesher V2 2.0.46 — tabelle SAP e Full-Quad

## Correzioni

- **Import FAST senza errori accettati:** i triangoli mantengono `NumJoints=3` e usano una quarta voce di connettività valida nella tabella SAP. Import e ripristino FAST richiedono ora zero errori, zero avvisi e zero errori fatali; le identità dei nodi coincidenti ma scollegati restano distinte.
- **Full-Quad 2/3:** Gmsh richiede un numero pari di intervalli sulle curve-guida della mesh delle aree prima di dimezzarle. La preparazione delle curve evita l'errore `1D mesh cannot be divided by 2`. Non vengono tagliati, eliminati o rinominati oggetti frame SAP2000. Bordi selezionati dichiarati immutabili e discretizzazioni manuali dispari restano protetti, con un messaggio esplicito se non compatibili.
- **BAMG:** se restituisce triangoli quasi collineari, il plugin non importa shell incomplete in SAP2000 e mostra un avviso breve, in italiano o inglese, indicando di scegliere un altro algoritmo (per esempio Frontal-Delaunay for Quads 8). La selezione dell'utente non viene cambiata di nascosto. È un limite di questa geometria con BAMG, non un rilascio della tolleranza agli errori d'importazione.
- Verifica immediata delle shell create tramite l'API SAP2000 e pulizia delle sole righe orfane nelle procedure di progetto, preservando i record relativi ad aree reali.

## Riprove

Sulle copie dei modelli originali in `examples/bug17/models/`:

| Selezione | Risultato SAP2000 27.1 |
| --- | --- |
| Circular, 7/BAMG, Simple, 0,3 m (configurazione segnalata) | Rifiuto prima dell'import: triangolo quasi collineare, con indicazione di un altro algoritmo. Nessuna shell incompleta inserita. |
| Circular, 6/Frontal-Delaunay, Simple Full-Quad, 0,4 m | 1.710 quad, 0 triangoli, 104 frame originali, 0 errori d'import. Avvisi di qualità riportati. |
| Multiple, 6/Frontal-Delaunay, Blossom Full-Quad, 0,7 m | 1.390 quad, 0 triangoli, 75 frame originali, 0 errori d'import. Qualità approvata. |
| Multiple, 8/Frontal-Delaunay for Quads, Simple, 0,6 m (configurazione segnalata) | 544 elementi (464 quad, 80 triangoli), 75 frame, 0 errori d'import. Il report qualità segnala elementi oltre la dimensione nominale; **non blocca** la generazione. |

La suite Gmsh comprende anche geometrie e impostazioni reali dei due modelli, la verifica che un fallimento BAMG non produca traceback nell'interfaccia e la prova O-grid con Full-Quad. I 36 esempi SAP2000 V2 sono stati verificati in tre processi isolati. I risultati con opzioni ulteriori e le catture diagnostiche sono in `reports/BUG17_2026-10-14.md` e nella cartella `17_bug` sul Desktop.

La versione COM rimane `1.0.0.0`; l'installer V2 sostituisce l'installazione precedente e mantiene la voce Tools. L'installazione richiede SAP2000 chiuso. La qualità e le assegnazioni del modello FEM finale devono essere controllate sul progetto specifico.
