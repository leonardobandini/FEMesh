# SAP2000 Quad Mesher V2 2.0.21

Release ZIP autonomo per Windows x64, .NET Framework 4.8 e SAP2000 27.1.0 o 27.2.0 beta con i limiti documentati. Il runtime Gmsh e incluso e non serve installare Python. Chiudere SAP2000, estrarre tutto lo ZIP, eseguire `install_plugin.cmd`, riavviare SAP2000 e verificare la versione `2.0.21` nella finestra del plugin.

## Joint pattern e spessore

- I valori joint pattern dei nodi sorgente restano esatti. I bordi sono interpolati linearmente e le shell a quattro nodi usano coordinate naturali bilineari inverse.
- Nei poligoni con piu di quattro nodi, i joint pattern interni usano un interpolante thin-plate affine-preserving e vengono limitati all'intervallo minimo/massimo dei vertici sorgente.
- Gli override nodali di spessore usano coordinate bilineari sui quadrilateri e mean-value sui poligoni; i figli triangolari ricevono il formato a quattro valori richiesto da SAP2000.
- Ogni valore scritto viene riletto tramite xAPI. Un errore interrompe la mesh e attiva il rollback.

Le regole sono approssimazioni geometriche validate, non una replica esatta dell'algoritmo interno non documentato di SAP2000. Sui tre casi disponibili, la differenza sul volume totale equivalente e compresa fra 0,074% e 1,373%; la differenza simmetrica locale arriva al 15,33% nel caso irregolare. Se joint pattern o thickness overwrite sono determinanti per il progetto, controllarli e preferibilmente reintrodurli direttamente in SAP2000 sul modello gia meshato dal plugin.

## Trasferimento e compatibilita

- FAST usa snapshot e ripristino tabellare del modello completo, con verifica di geometria, GUID, coordinate, sezioni e assegnazioni. I poligoni che SAP non ricostruisce da righe di continuazione usano una stretta eccezione tramite API a oggetti.
- Standard conserva il percorso per singolo oggetto. Entrambi trasferiscono la stessa mesh Gmsh.
- La compatibilita mirata con SAP2000 27.2.0 beta recupera FieldKey vuoti dove verificato ed esclude soltanto tabelle globali non modificate dalla mesh. Non costituisce certificazione completa della beta.
- Joint offset nodali e overwrite di progetto non leggibili restano non supportati. Usare backup numerato e controllo manuale a valle.

## Verifiche

- Build plugin e installer senza warning o errori.
- Guida offline italiana/inglese e 24 esempi validati.
- Test di sostituzione da V1 1.0.120 e V2 2.0.13 riusciti.
- Fixture SAP a quattro e otto nodi: joint pattern e thickness override scritti e riletti con esito PASS, inclusi figli triangolari.
- Otto pattern-base SAP indipendenti: errore RMS dei pesi ridotto da 0,06708 a 0,05727 rispetto alle coordinate mean-value.

Il manifest pubblico V2 viene aggiornato solo dopo la verifica online dello ZIP e del relativo SHA-256. Il feed V1 resta separato.
