# Concrete_Barrier: perdita delle procedure di progetto dopo Show Tables

## Stato

Riprodotto con SAP2000 27.1 e plugin installato 2.0.50. La candidata **2.0.51 locale, non pubblicata** ammette soltanto la perdita verificata della procedura Concrete Shell Design con conferma obbligatoria prima di Applica. La matrice a quattro processi e la pubblicazione attendono la prova manuale dell'utente.

## Sequenza e diagnostica

1. Sul modello `Concrete_Barrier(0.3m).sdb` (21 aree, 68 joint) selezionare tutto, Genera con dimensione massima 0,5 m, Applica.
2. `Display > Show Tables > Connectivity Data > Joint Coordinates`, scorrere fino in fondo, chiudere la tabella.
3. Riaprire lo stesso SDB senza salvare, selezionare tutto, Genera con le stesse impostazioni.
4. Errore alla fine dell'inserimento: `Area design procedure was not transferred to 1.` Il rollback mantiene le 21 aree originali. SHA-256 dell'SDB su disco prima/dopo: `28C89B148BF93826FF97E930465645BDF1E400218859200B51D559AFBC2509BF`.

Sulla sessione reale PID 100376, la stessa operazione via xAPI esterna e con timeout riproduce il difetto. Il batch `Area Design Procedures` registra **546/546 record letti, 0 errori**, ma `GetTableForEditingArray` subito dopo restituisce **zero righe** e `GetTableForDisplayArray` restituisce 546 righe con **`No Design`** per il figlio `1`, mentre la madre richiede **`Concrete Shell Design`**. Il controllo del plugin evita di applicare definitivamente una mesh con assegnazioni perse. Log `%LOCALAPPDATA%\SAP2000QuadMesher\plugin-errors.log`.

La copia isolata dell'SDB in `%TEMP%\opencode\concrete-barrier-two-cycle-20261019` completa due cicli con la lettura delle coordinate tramite API, ma questo **non** riproduce l'apertura della tabella nella GUI. Tentativi sulla sessione già interessata: annullamento preventivo delle modifiche tabellari, lettura nel gruppo `All`, reimport identico, import con sezioni complete e import CSV: nessuno ha ripristinato le procedure. Gli esperimenti sono stati rimossi dal sorgente; la DLL installata resta 2.0.50.

## Prossima verifica

Il fallback è passato sul modello aperto: 525 shell applicate con consenso esplicito nell'automazione, **525/525 `No Design` dichiarati**, hash SDB originale invariato. Dopo nuova apertura senza salvataggio, Genera→Annulla ha ripristinato **21/21 procedure `Concrete Shell Design`**, 21 aree originali e hash immutato. Verificare manualmente il flusso GUI sulla build locale 2.0.51. Solo dopo il riscontro manuale, eseguire la matrice a quattro processi e valutare una release.

DLL 2.0.51 locale installata dopo la chiusura di SAP2000: SHA-256 `5E3D74E768D372A8B2539101FA5F91BC8F5CC557522B1D94044D63316D58B8EE`. Installer, pacchetto precedente e registrazione COM verificati. Rollback completo della 2.0.50: `%TEMP%\opencode\barrier-v250-before-v251-manual-20261019`. Release e feed pubblici restano alla 2.0.50.

## Lettura diretta nella nuova sessione aperta

PID 42968, file originale invariato (21 aree, SHA-256 `28C89B148BF93826FF97E930465645BDF1E400218859200B51D559AFBC2509BF`), nessuna selezione. La **prima** chiamata xAPI `GetTableForEditingArray("Area Design Procedures", "")` ha restituito `code=0`, campi `Area|DesignProc`, **0 record**. Senza cambiare modello, `GetTableForDisplayArray` ha restituito `code=0`, **21 record**, tutti `Concrete Shell Design`. Dopo questa chiamata, anche la riflessione su `cPlugin.ReadEditableTable` della DLL installata 2.0.51 ha restituito **21 record**; `cPlugin.ReadDisplayTable` ne ha restituiti 21. Il getter editabile è quindi dipendente dallo stato/transitorio dell'editor SAP, non prova che la procedura originale sia `No Design`.

`Area Section Property Design Parameters` ha 5 record leggibili da entrambi i getter (fra cui `Barriera`, armatura `B450C`). La tabella `Overwrites - Concrete Shell Design - ACI 350-20` è segnalata vuota da `GetAllTables`; non equivale a `Area Design Procedures`. La correzione locale recupera l'acquisizione delle procedure dal getter di visualizzazione quando l'editabile omette aree selezionate, e impedisce che lo snapshot tralasci tacitamente 21 procedure leggibili.

**2.0.52 locale installata per il test manuale** con SAP2000 chiuso: DLL SHA-256 `472E1A402C349FBA91FBD0E35DB41831EC4CCAE659661CFBBE788BEA4197D7B2`. Su una copia di `Concrete_Barrier` a 0,5 m, 21 aree/68 nodi selezionati → 525 aree applicate; smoke FAST `nTEST014` PASS; build .NET e 30 test Python PASS (1 skip). Pacchetto, registrazione COM e rollback della precedente 2.0.51 verificati: `%TEMP%\opencode\barrier-v251-before-v252-manual-20261019`. Al momento dell'installazione locale, il ciclo GUI e la matrice erano ancora da verificare; la release pubblica era la 2.0.50.

## Riscontro manuale e regressione successiva

L'utente ha confermato che la 2.0.52 non riproduce l'errore nella sequenza GUI; non compare l'avviso di perdita quando le procedure sono effettivamente trasferite. Matrice su DLL installata SHA-256 `472E1A402C349FBA91FBD0E35DB41831EC4CCAE659661CFBBE788BEA4197D7B2`: quattro sessioni SAP2000 27.1 avviate in parallelo con nove casi ciascuna. Gruppi 2–4 **27/27 PASS**; `nTEST005` nel gruppo 1 ha superato il timeout di apertura modello SAP *prima dell'ingresso nel plugin*, lasciando una sessione isolata senza modello, che è stata chiusa. Tutto il gruppo 1 è stato rieseguito su un'altra sessione isolata: **9/9 PASS** incluso `nTEST005`. Totale riconciliato: **36 ID distinti, 36 PASS**. Log: `%TEMP%\opencode\v252-full36-fourworkers-20261019` e `%TEMP%\opencode\v252-group1-retry-20261019`. Preview→Annulla Standard (`nTEST004`) e FAST (`nTEST028`): PASS. L'SDB originale `Concrete_Barrier` conserva SHA-256 `28C89B148BF93826FF97E930465645BDF1E400218859200B51D559AFBC2509BF`.
