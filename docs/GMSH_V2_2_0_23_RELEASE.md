# SAP2000 Quad Mesher V2 2.0.23

Release correttiva per Windows x64, .NET Framework 4.8 e SAP2000 27.1.0 o 27.2.0 beta con i limiti documentati. Il runtime Gmsh e incluso e non serve installare Python. Chiudere SAP2000, estrarre tutto lo ZIP, eseguire `install_plugin.cmd`, riavviare SAP2000 e verificare la versione `2.0.23` nella finestra del plugin.

## Compatibilita SAP2000 27.2 beta

- Il recupero dello schema CSV riallinea in modo univoco i valori contenenti virgole non quotate, inclusi i nomi dei materiali, senza ignorare tabelle dal modello snapshot.
- FAST rileva gli schemi tabellari incompleti esposti dalla beta e usa automaticamente l'inserimento tramite API oggetti. Lo stesso percorso sicuro viene usato quando la mesh contiene triangoli.
- Undo ricrea connettivita, sezione e procedura di progetto nella stessa transazione SAP, preservando `Concrete Shell Design` sulle aree ricostruite.
- I GUID generati obbligatoriamente da SAP sono accettati soltanto quando il modello originale non specificava alcun GUID; i GUID originali valorizzati restano verificati esattamente.

## Trasferimento proprieta

- Restano attivi il trasferimento e la rilettura dei joint pattern, dei thickness override e dei joint offset di tipo `1` e `2` introdotti nelle versioni precedenti.
- Gli overwrite di progetto non leggibili, inclusi quelli osservati per Concrete Design Italian NTC 2008, richiedono ancora revisione e replica manuale sui figli.
- Il backup contiene l'ultimo SDB salvato, non eventuali modifiche non salvate.

## Verifiche

- Matrice Apply-to-Undo FAST: `36/36 PASS`.
- Matrice Apply-to-Undo Standard: `36/36 PASS`.
- Fixture SAP a quattro nodi: pattern, thickness override e offset espliciti di tipo `2` PASS.
- Fixture SAP a otto nodi: pattern, thickness override e offset di tipo `1` PASS.
- Preflight snapshot completo di `Multiple_Silo_Slab.sdb`: PASS senza salvataggio del modello.

Il manifest pubblico V2 viene aggiornato solo dopo la verifica online dello ZIP e del relativo SHA-256. Il feed V1 resta separato.
