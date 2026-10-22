# Gmsh V2 2.0.28 — comando Ripristina e transizione O-grid

## Interfaccia

La riga inferiore della finestra ha quattro comandi allineati, di larghezza identica: Genera/Applica, Qualità della mesh, Annulla mesh/Annulla generazione, Ripristina default. Quest'ultimo ripristina tutte le opzioni di mesh e trasferimento (anche campi Gmsh, fori, JSON e FAST/backup), mantenendo esattamente i testi inseriti per dimensione minima e massima delle shell. È disabilitato durante la generazione. F1 descrive la funzione in entrambe le lingue. Il reset non salva subito le preferenze: vengono memorizzate al successivo Genera.

## Geometria e verifica

Sul lato esterno dei settori O-grid il backend sfuma il passo verso quello nominale con un campo Distance + Threshold; se è presente un campo dell'utente usa il minimo dei due. Prima dell'import prova uno scambio di diagonale limitato a due triangoli interni adiacenti se migliora entrambi senza spostare nodi o tagliare un frame. Triangoli ancora quasi collineari (angolo <5°, altezza <2% del passo) sono respinti con coordinate e misure prima di toccare SAP2000. Dettagli geometrici: `docs/GMSH_V2_NTEST026_TRIANGLE_DIAGNOSIS.md`.

- Backend Python: 19 test (1 skip); confronto offline della geometria ricostruita del 026: da almeno un triangolo con angolo <5° e altezza <1 mm a zero in quella categoria.
- Build V2 e test UI moderno/Classic: PASS, inclusi i quattro pulsanti uguali, il reset che preserva entrambe le dimensioni, la localizzazione e il JSON inviato al backend. Guida IT/EN verificata.
- SAP2000 27.2 beta su copie isolate: `nTEST026`, `nTEST005`, `nTEST027` **3/3 PASS** nella regressione d'import/connettività in `%TEMP%\opencode\sqm-v228-sap-regression`. Per il 026 sono stati verificati 12 fori con 16 corde libere ciascuno: **908 quad + 188 triangoli = 1.096 shell**, zero invalidi secondo il report. `nTEST027` mantiene le due cuciture a 24 segmenti con nomi nodali coincidenti.
- **Qualità del 026 non approvata:** `quality_passed=false`, 2 eccezioni dimensionali (1,854% della superficie), massimo lato 0,062 m a fronte di 0,05 m nominali; 105 elementi fuori riferimento di forma. Il successo dell'import non è una validazione strutturale della mesh. I modelli originali della regressione non sono stati salvati né sovrascritti.

Il pacchetto installabile comprende Gmsh 4.15.2 congelato e codice sorgente corrispondente; non richiede Python nell'installazione utente. La pubblicazione nel feed V2 e nel feed di aggiornamento V1 avviene solo dopo verifica degli asset e dell'archivio sorgente pubblico.
