# FEMesh 2.0.65 — SAP2000 e CSiBridge

FEMesh suddivide aree selezionate in elementi shell prevalentemente quadrangolari con Gmsh. La voce del menu è **Tools → FEMesh**. Il nome tecnico della DLL e l'identità COM restano compatibili con le installazioni esistenti.

## Uso

1. Apri un modello salvato in SAP2000 o CSiBridge 27+, seleziona le aree e, quando occorre, i nodi e i frame che devono vincolare la geometria.
2. In FEMesh imposta le dimensioni della mesh e le opzioni Gmsh. Con **Genera**, controlla l'anteprima e il report di qualità prima di scegliere **Applica** oppure **Annulla mesh**.
3. **Applica** conferma la sostituzione delle aree sorgenti nel modello aperto; **Annulla mesh** ripristina la geometria acquisita prima dell'operazione. Per conservare il risultato salva esplicitamente il modello nell'host. Controlla comunque assegnazioni, connettività, vincoli e comportamento strutturale.

La guida offline dettagliata è in `docs/help-gmsh-v2/index-it.html` (italiano) e `docs/help-gmsh-v2/index-en.html` (English); è raggiungibile anche con **F1** dalla finestra del plugin. Il backup numerato contiene l'ultimo file SDB/BDB *salvato*, non le modifiche ancora in memoria. FAST importa la mesh attraverso le tabelle editabili quando disponibile; la modalità Standard usa le API degli oggetti. I fori O-grid usano archi circolari e mantengono i nodi del bordo al raggio richiesto.

## Scaricare e compilare

- Prima di installare FEMesh, installa il [Microsoft Visual C++ Redistributable x64 ufficiale](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist), versione **14.42.34226.3 o successiva compatibile**. Le DLL runtime Visual C++ Microsoft non sono incluse nello ZIP.
- [Pagina delle release FEMesh](https://github.com/leonardobandini/FEMesh/releases): il controllo aggiornamenti nel piè di pagina avvisa quando esiste una nuova release stabile. Solo **Scarica** apre nel browser lo [ZIP dell'ultima release](https://github.com/leonardobandini/FEMesh/releases/latest/download/FEMesh-latest.zip); l'installazione resta manuale.
- `SOURCE.md`, incluso nello ZIP, identifica gli asset FEMesh/backend e Gmsh della medesima release e i relativi checksum. Le istruzioni di build sono nell'archivio sorgenti, `packaging/SOURCE_BUILD.md`.
- Il codice originale FEMesh è GPL-2.0-or-later; Gmsh 4.15.2 è GPL-2.0-or-later dei suoi titolari. Il backend binario combinato con OpenSSL 3 (Apache-2.0) esercita l'opzione GPLv3. Le licenze degli altri componenti e l'eccezione limitata di Gmsh restano invariate: vedi `LICENSE-APPLICATION.md`, `GPL-3.0.txt`, `THIRD_PARTY_NOTICES.md` e `licenses/`. Non è inclusa alcuna DLL CSI.

FEMesh usa **Gmsh 4.15.2** e il binding Python. Gmsh è copyright © **C. Geuzaine e J.-F. Remacle**, GPL-2.0-or-later con la propria eccezione limitata: [sito ufficiale Gmsh](https://gmsh.info/). Il pacchetto contiene `licenses/GMSH-LICENSE.txt` e gli avvisi; vedi `THIRD_PARTY_NOTICES.md` e il sorgente Gmsh fra gli asset della stessa release FEMesh. La scelta GPLv3 del backend combinato non modifica la licenza originale di Gmsh.
