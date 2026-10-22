# nTEST026 — triangolo respinto da SAP2000

Diagnosi del caso V2 sulla beta SAP2000 27.2 (10 ottobre 2026). Il modello sorgente e i risultati precedenti restano intatti.

## Evidenza

La traccia isolata `%TEMP%\opencode\sqm-nTEST026-geometry-diagnostic-31c8529da67f40f6b35b46d3174690c9\nTEST026\failure.txt` identifica il figlio 294 dell'area sorgente 1 (nome restituito `296`), con tag Gmsh `689|37|253` e nodi SAP `365|53|169`. Coordinate in metri nel piano Z=0:

| Nodo | X | Y |
| --- | ---: | ---: |
| 365 | 0.24135810346126813 | 0.058497880869927507 |
| 53 | 0.23772792206135787 | 0.057272077938642148 |
| 169 | 0.23136396103067894 | 0.05463603896932108 |

Il centro del foro sorgente vicino è (0.225, 0.070) m; i vertici distano rispettivamente 19.997, 18.000 e 16.630 mm dal centro: la cella è nella fascia esterna di raccordo O-grid, non all'interno del foro di raggio 10 mm.

- Lati: **3.832, 6.888, 10.714 mm**; area planare positiva **0.884 mm²**. I tre nomi dei nodi sono distinti, e SAP2000 ne legge le coordinate attese: non è una coincidenza di nodi o un triangolo invertito.
- Angoli: **2.469°, 176.158°, 1.373°**. Altezza rispetto al lato maggiore: **0.165 mm**. È un triangolo quasi collineare: il difetto è la forma/degenerazione, non semplicemente un lato corto.
- Il triangolo precedente, figlio 293 / area `295`, condivide il lato `53–365`, resta leggibile (`GetPoints=0`) e ha area **9.936 mm²**. La diagnostica non ha trovato triangoli precedenti più piccoli o identici. `AddByPoint` del figlio 294 restituisce codice 0 e nome `296`, ma `GetPoints(296)` restituisce 1 e `296` non compare nell'elenco delle aree; fallisce la successiva assegnazione dei modificatori. SAP2000 ha quindi scartato l'area durante la creazione; il codice 1 dei modificatori è un effetto, non la causa.
- Il file di input `examples/atomic/models/nTEST026.$2k` riporta `MergeTol=0.001` m (**1 mm**), maggiore dell'altezza 0.165 mm. Questo rende plausibile un rigetto geometrico da parte di SAP, pur con distanze tra i tre vertici maggiori di 1 mm; la regola interna esatta con cui SAP scarta l'area non è documentata da questa prova.

Nella prova isolata `%TEMP%\opencode\sqm-nTEST026-merge0p1mm-cf2becd9e6484556afd49e075a93499b\nTEST026\completed.txt` la generazione/importazione con tolleranza ridotta **0.1 mm** completa: **742 shell (576 quad, 166 triangoli), 0 elementi invalidi** secondo il report del plugin. La verifica automatica si interrompeva dopo l'importazione sul primo triangolo (`nTEST026 non-quadrilateral 195`), perché il controllo dei fori assumeva ancora esclusivamente quad V1; `run_test01_fast.cs` ora accetta triangoli nella modalità V2 e controlla tutti i loro lati. Questo risultato precedente **non prova ancora** che tutte le 12 aperture e le cuciture superino la verifica aggiornata: occorre rieseguire la prova isolata.

La tolleranza ridotta non è una correzione della qualità: il report della prova completata indica `quality_passed=False`, **216 elementi fuori riferimento di forma**, **9 eccezioni dimensionali**, lato massimo **0.064 m** rispetto a 0.05 m nominali. Prima di considerare risolto nTEST026 bisogna eliminare/rimeshare i triangoli quasi collineari nella fascia O-grid, conservando il contorno dei fori e la congruenza fra le tre aree, e ripetere il controllo dei 12 fori sulla mesh importata.

## Prototipo di transizione e riparazione locale

Nel backend `sap_gmsh_mesher.py` il lato esterno dei settori O-grid alimenta ora un campo `Distance + Threshold`: la taglia parte da quella dei segmenti dell'anello esterno e raggiunge gradualmente la taglia massima nello spazio circostante. Se è presente un campo utente, viene applicato il minimo fra i due. Dopo la generazione, un triangolo quasi collineare può essere riparato cambiando la diagonale **soltanto** di due triangoli adiacenti dello stesso output, con controllo di convessità, area, orientazione, lato e qualità di entrambi; gli spigoli sui frame non si cambiano. Un triangolo rimasto con angolo <5° e altezza <2% del passo viene rifiutato prima del trasferimento SAP, con coordinate e misura nel messaggio.

Il test offline `test_nTEST026_ogrid_transition_avoids_near_collinear_triangles` ricostruisce le tre aree e i dodici fori (20 mm, passo 50 mm), includendo ottimizzazione Laplace2D: con il campo uniforme precedente contiene almeno un triangolo sotto 5° e 1 mm di altezza; con la transizione e la riparazione nuove ne contiene **zero**, senza nodi nell'interno dei fori. La suite backend passa (19 test, 1 skip).

**Aggiornamento 2.0.28:** la regressione SAP2000 su copia isolata del modello originale ha completato l'import e la verifica di tutte le 12 aperture (`%TEMP%\opencode\sqm-v228-sap-regression\nTEST026`). Sono state create 1.096 shell, zero elementi invalidi; il report qualità **non** passa per 2 eccezioni dimensionali (massimo 0,062 m, obiettivo 0,05 m).
