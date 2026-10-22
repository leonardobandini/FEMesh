# Backlog assegnazioni V2 dopo 2.0.18

Questo documento registra il lavoro da riprendere **dopo la revisione dell'interfaccia**. Solo al termine dell'implementazione e delle verifiche sotto elencate andra riscritta e riallineata la guida offline italiana/inglese. Non aggiornare l'help in anticipo sulla base della sola presenza del codice.

Riferimento dello stato gia verificato: `docs/GMSH_V2_TRANSFER_MATRIX_2_0_18.md`.

## Requisiti obbligatori per il prossimo aggiornamento della guida

Questi contenuti devono essere inseriti nella guida offline italiana e inglese quando verra aggiornata, anche se la richiesta di aggiornamento non li menzionera espressamente.

### Joint pattern e sovrascritture nodali di spessore

- Spiegare che la V2 2.0.21 conserva i valori esatti sui joint sorgente e usa interpolazione lineare sui bordi della shell padre.
- Per una shell padre a quattro joint, spiegare che i joint interni usano coordinate naturali bilineari inverse.
- Per una shell padre con piu di quattro joint, spiegare che i joint pattern interni usano un interpolante thin-plate che conserva i campi affini; il risultato e limitato al minimo e massimo dei valori sui joint sorgente.
- Per le sovrascritture nodali di spessore, spiegare che i quadrilateri usano le stesse coordinate bilineari, mentre i poligoni con piu di quattro joint usano coordinate mean-value non negative. I figli triangolari vengono assegnati nel formato a quattro valori richiesto dall'API SAP2000.
- Precisare che ogni valore assegnato viene riletto tramite API e che un errore interrompe la mesh e attiva il rollback.
- Dichiarare senza ambiguita che queste regole sono approssimazioni geometriche validate, ma non riproducono esattamente in ogni punto l'algoritmo interno non documentato di SAP2000. Le differenze locali possono essere maggiori della differenza sul volume totale.
- Raccomandare, quando joint pattern o sovrascritture di spessore sono determinanti per il progetto, di controllarli e preferibilmente reintrodurli direttamente in SAP2000 sul modello gia meshato dal plugin, quindi **a valle della meshatura**. Questa raccomandazione deve comparire sia nella descrizione del trasferimento sia nel flusso operativo consigliato.

### Inventario delle proprieta shell

- Aggiungere una sezione autonoma che descriva, una per una, tutte le proprieta, assegnazioni, carichi e overwrite applicabili alle shell in SAP2000.
- Per ogni voce indicare: significato fisico, dove si assegna in SAP2000, comportamento padre -> figli, comportamento Apply -> Undo, supporto Standard, supporto FAST, eventuale interpolazione e limiti verificati.
- L'inventario deve comprendere almeno: sezione shell e materiale, tipo di comportamento, assi locali, massa, modificatori, edge constraint, molle di area e di bordo, gruppi, joint pattern, thickness overwrite, joint offset, carichi uniformi e non uniformi, pressioni di superficie e di bordo, temperatura, deformazione, poropressione, gravita, vento, procedure e overwrite di progetto.
- Le voci non leggibili o non riproducibili tramite API devono essere marcate esplicitamente come non supportate, con la procedura manuale consigliata dopo la meshatura. Non presentare come trasferita una proprieta verificata soltanto per presenza o conteggio.

## Parziali o non verificati: da implementare e verificare

- **Pressione e molla su bordo, Standard Undo**: aggiungere una fixture dedicata `padre -> figli -> padre` e confrontare bordo, faccia, proprieta, intensita, load pattern e copertura geometrica prima/dopo.
- **Procedura di progetto dell'area, FAST e Standard**: creare almeno una fixture con valore esplicito non predefinito; verificare sia `padre -> figli` sia `padre -> figli -> padre` nei due percorsi. Gestire e testare separatamente tabella leggibile, vuota e illeggibile.
- **Carichi d'area non ancora provati singolarmente**: gravita, poropressione costante, rotazione, deformazione costante, temperatura costante e vento. Per ogni tipo verificare tutti i parametri SAP sui figli FAST/Standard e sul padre dopo Undo FAST/Standard.
- **Overwrite shell diversi da EC2, incluso ACI350**: verificare getter/setter e tabelle su fixture reali; implementare il trasferimento e l'Undo soltanto per i codici che SAP rende leggibili e scrivibili senza errori.
- **Carichi e assegnazioni dei joint riutilizzati**: aggiungere fixture Gmsh end-to-end dedicate per carichi, molle, restraint, constraint e joint pattern; distinguere chiaramente i joint originali riutilizzati dai nuovi joint.
- **Nuovi joint della mesh**: joint pattern implementati con la regola 2.0.21 sopra descritta; completare la verifica end-to-end sulle mesh Gmsh effettive e mantenere distinta ogni altra assegnazione dei joint.
- **Spessore/offset e carichi governati da joint pattern**: thickness override, joint offset di tipo 1/2 e carichi governati da joint pattern sono implementati e riletti via API. Le fixture mirate coprono offset espliciti a quattro nodi e offset da pattern non assegnato a otto nodi; `Circular_Floor` copre Standard end-to-end. Resta da aggiungere una fixture FAST end-to-end dedicata ai joint offset.
- **Carico area -> frame**: progettare una ripartizione che conservi risultante e distribuzione sui frame; implementare solo dopo confronto numerico padre/figli e verifica Undo.
- **Assi locali avanzati e altre assegnazioni senza lettura affidabile**: inventariare le API SAP disponibili, aggiungere fixture specifiche e mantenere il blocco quando la fedelta non e dimostrabile.
- **Overwrite shell EC2**: riesaminare con versioni SAP/API successive. Nella 27.1 getter e setter restituiscono codice `1`; non dichiarare supporto finche una fixture reale non passa lettura, trasferimento e Undo.

## Non applicabili nello stato attuale

- **Undo di una mesh bloccata prima della generazione**: non applicabile perche non esistono figli e il modello non viene sostituito. Verificare comunque che il fallimento lasci modello, selezione e assegnazioni invariati.
- **Propagazione automatica ai nuovi joint di dati senza una regola fisica definita**: non applicabile finche non esiste una strategia di interpolazione/ripartizione validata.
- **Ripristino tramite Undo di dati che SAP non rende leggibili**: non garantibile; resta necessario l'avviso e il backup numerato dell'ultimo SDB salvato.

## Criteri di completamento

- Ogni voce supportata deve avere fixture reale SAP2000 27.1 o successiva, non solo test sintetici del codice.
- Verificare separatamente FAST/tabellare e Standard/API a oggetti.
- Verificare separatamente `padre -> figli` e `padre -> figli -> padre` con Apply e Undo.
- Confrontare tutti i campi significativi, non soltanto presenza e conteggio dei record.
- FAST deve mantenere `fatal=0`, `errors=0`, `warnings=0`; nessuna whitelist di errori SAP.
- Registrare versione SAP, modello, input, risultati e limiti residui.
- Aggiornare la matrice tecnica solo dopo il passaggio delle fixture interessate.

## Sequenza concordata

1. Rivedere l'interfaccia e il modo in cui presenta modalita, limiti, avvisi e stato delle assegnazioni.
2. Implementare e verificare tutte le voci parziali/non verificate sopra elencate.
3. Riclassificare esplicitamente le voci ancora non supportate o non applicabili.
4. Riscrivere in un'unica fase l'help IT/EN e la matrice utente, coerenti con la nuova interfaccia e con le sole prove realmente superate.
