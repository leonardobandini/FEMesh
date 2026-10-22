# SAP2000 Quad Mesher V2 2.0.22

Release ZIP autonomo per Windows x64, .NET Framework 4.8 e SAP2000 27.1.0 o 27.2.0 beta con i limiti documentati. Il runtime Gmsh e incluso e non serve installare Python. Chiudere SAP2000, estrarre tutto lo ZIP, eseguire `install_plugin.cmd`, riavviare SAP2000 e verificare la versione `2.0.22` nella finestra del plugin.

## Joint offset delle aree

- Gli offset di tipo `1` conservano il nome del joint pattern e il fattore di scala. Il pattern viene propagato ai nuovi joint prima di assegnare l'offset alle aree figlie.
- Gli offset espliciti di tipo `2` conservano i valori sui vertici sorgente, usano interpolazione lineare sui bordi, coordinate bilineari nei quadrilateri e coordinate mean-value nei poligoni generali.
- I figli triangolari ricevono il formato a quattro valori richiesto da SAP2000.
- Ogni offset scritto viene riletto tramite API. Una differenza interrompe l'operazione e attiva il rollback.
- Un pattern definito senza una riga esplicita su un joint usa il valore effettivo zero restituito semanticamente da SAP2000; gli altri codici API non nulli restano errori.

Le regole sono approssimazioni geometriche validate, non una replica dell'algoritmo interno non documentato di SAP2000. Gli eventuali tipi offset futuri diversi da `0`, `1` e `2` vengono rifiutati esplicitamente. Se i joint offset sono determinanti per il progetto, controllarli a valle sul modello meshato.

## Diagnostica e limiti

- Gli errori recuperabili di Gmsh, API SAP2000, trasferimento e verifica vengono registrati in `plugin-errors.log` prima del rollback e della localizzazione del messaggio.
- La cancellazione richiesta dall'utente resta un percorso normale e non viene registrata come guasto.
- Gli overwrite di progetto non leggibili, inclusi quelli osservati per Concrete Design Italian NTC 2008, richiedono ancora revisione e replica manuale sui figli.
- Il backup contiene l'ultimo SDB salvato, non eventuali modifiche non salvate.

## Verifiche

- Build plugin senza warning o errori.
- Guida offline italiana/inglese e 24 esempi validati.
- Fixture SAP a quattro nodi: joint pattern, thickness override e offset espliciti di tipo `2` scritti e riletti con esito PASS.
- Fixture SAP a otto nodi: pattern definito senza righe esplicite, thickness override e offset di tipo `1` scritti e riletti con esito PASS.
- Prova Standard end-to-end sul modello circolare: 8 aree sorgente trasformate in 1747 aree figlie, 176 frame conservati, proprieta `slab` conservata e 241 figli verificati con offset tipo `1`, pattern `Default` e scala `0.5`.
- Il trasferimento delle proprieta ai figli e stato inoltre controllato nel modello risultante dall'utente.

Il manifest pubblico V2 viene aggiornato solo dopo la verifica online dello ZIP e del relativo SHA-256. Il feed V1 resta separato.
