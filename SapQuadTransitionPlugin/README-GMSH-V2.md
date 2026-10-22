# FEMesh 2.0.63 — SAP2000 e CSiBridge

FEMesh suddivide aree selezionate in elementi shell prevalentemente quadrangolari con Gmsh. La voce del menu è **Tools → FEMesh**. Il nome tecnico della DLL e l'identità COM restano compatibili con le installazioni esistenti.

## Uso

1. Apri un modello salvato in SAP2000 o CSiBridge 27+, seleziona le aree e, quando occorre, i nodi e i frame che devono vincolare la geometria.
2. In FEMesh imposta le dimensioni della mesh e le opzioni Gmsh. Con **Genera**, controlla l'anteprima e il report di qualità prima di scegliere **Applica** oppure **Annulla mesh**.
3. **Applica** conferma la sostituzione delle aree sorgenti nel modello aperto; **Annulla mesh** ripristina la geometria acquisita prima dell'operazione. Per conservare il risultato salva esplicitamente il modello nell'host. Controlla comunque assegnazioni, connettività, vincoli e comportamento strutturale.

La guida offline dettagliata è in `docs/help-gmsh-v2/index-it.html` (italiano) e `docs/help-gmsh-v2/index-en.html` (English); è raggiungibile anche con **F1** dalla finestra del plugin. Il backup numerato contiene l'ultimo file SDB/BDB *salvato*, non le modifiche ancora in memoria. FAST importa la mesh attraverso le tabelle editabili quando disponibile; la modalità Standard usa le API degli oggetti. I fori O-grid usano archi circolari e mantengono i nodi del bordo al raggio richiesto.

## Scaricare e compilare

- [ZIP d'installazione FEMesh corrente](https://github.com/leonardobandini/FEMesh/releases/latest/download/FEMesh-latest.zip).
- `SOURCE.md`, incluso nello ZIP, rimanda ai sorgenti FEMesh e Gmsh corrispondenti alla versione distribuita. Le istruzioni di build sono nell'archivio sorgenti, `packaging/SOURCE_BUILD.md`.
- Il codice originale FEMesh e Gmsh sono GPL-2.0-or-later. Il binario combinato con OpenSSL 3 elegge GPLv3; leggi `LICENSE-APPLICATION.md`, `GPL-3.0.txt`, `THIRD_PARTY_NOTICES.md` e `licenses/`. Non è inclusa alcuna DLL CSI.

Le versioni precedenti erano usate per sviluppo e debug. La presente guida riguarda solo la distribuzione corrente.
