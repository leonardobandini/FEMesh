# FEMesh — versione distribuita

## 2.0.66 — candidata locale, non pubblicata

- Corretto il riconoscimento dei bordi di un'apertura quando frame del gruppo si sovrappongono a frame selezionati non appartenenti al gruppo: i tratti comuni mantengono l'appartenenza geometrica al contorno dopo la suddivisione.
- Durante ogni Genera, backup numerato opzionale prima del salvataggio obbligatorio dello stato corrente; lo snapshot di Annulla segue il salvataggio. Documentati gli effetti su Applica e Annulla mesh.
- Un modello mai salvato mostra un avviso all'apertura del plugin: guida e schede restano consultabili ma le operazioni sono disattivate finché il modello non viene salvato nell'host.
- L'installer verifica la versione del Visual C++ Redistributable x64 e, se necessario, scarica da Microsoft il prerequisito firmato e ne avvia il setup interattivo prima di installare FEMesh.
- Nuovo installer grafico bilingue con lingua Windows rilevata automaticamente, selezione manuale IT/EN e stato delle fasi fino alla registrazione nei menu SAP2000/CSiBridge.
- Il modello resta bloccato mentre FEMesh è aperto; le modifiche del plugin sbloccano temporaneamente il modello con la finestra SAP2000/CSiBridge non interattiva. Corretta la riabilitazione della finestra dell'host alla chiusura.

## 2.0.65 — 23 ottobre 2026

- Ripristinato il controllo aggiornamenti della V2, con la medesima UI e gli stessi messaggi; consulta esclusivamente l'ultima release stabile pubblica di FEMesh.
- Il download avviene soltanto su scelta esplicita dell'utente tramite browser; nessuna installazione automatica.
- Lo ZIP dell'ultima release usa il nome stabile `FEMesh-latest.zip`.

## 2.0.64 — 23 ottobre 2026

- `SOURCE.md` identifica esclusivamente binario, sorgenti e checksum della medesima release FEMesh.
- Disattivato il controllo aggiornamenti integrato e rimosso il relativo collegamento al feed; le future versioni saranno annunciate tramite le release FEMesh.
- Nessuna modifica prevista all'algoritmo di mesh.

## 2.0.63 — 22 ottobre 2026

- Distribuzione del medesimo motore di mesh verificato nella precedente matrice atomica: 36/36 su SAP2000, 36/36 su CSiBridge.
- Installer pubblico `FEMesh-2.0.63.zip` e collegamento stabile `FEMesh-latest.zip`, mantenendo gli alias tecnici necessari ai client degli aggiornamenti esistenti.
- Licenze e sorgenti corrispondenti verificati; il binario combinato usa GPLv3, mentre il codice originale FEMesh e Gmsh conservano GPL-2.0-or-later. L'installer include `SOURCE.md`; la build dal solo archivio sorgenti è stata provata.
