# FEMesh

## FEMesh per SAP2000 e CSiBridge

FEMesh è un plugin gratuito e open source per generare mesh di elementi shell prevalentemente quadrangolari in SAP2000 e CSiBridge tramite Gmsh. L'installer rileva gli host 27 e successivi che espongono `CSiAPIv1.dll` e registra **Tools → FEMesh** nei profili già inizializzati. La vecchia identità COM resta invariata per aggiornare le installazioni esistenti. Mesh e trasferimento sono stati verificati su SAP2000 e CSiBridge 27; la beta SAP2000 27.2.0 è stata provata, mentre la release finale 28 non è installata sul PC di prova.

- **[Scarica sempre l'ultimo pacchetto di installazione](https://github.com/leonardobandini/FEMesh/releases/latest/download/FEMesher-latest.zip)** · [Release e sorgenti corrispondenti](https://github.com/leonardobandini/FEMesh/releases/latest).
- **Installazione:** estrai lo ZIP, chiudi SAP2000/CSiBridge, esegui `install_plugin.cmd` e riavvia l'host. La [guida FEMesh](docs/help-gmsh-v2/index-it.html) comprende opzioni, limiti e esempi; [English help](docs/help-gmsh-v2/index-en.html).
- **Sorgenti:** questo repository contiene il codice del progetto e la sua cronologia; la release include il relativo `-source.zip` e i sorgenti Gmsh upstream. [Build dai sorgenti](packaging/SOURCE_BUILD.md) · [Licenze](LICENSE-APPLICATION.md).
- **Aggiornamenti delle installazioni precedenti:** il [feed storico](https://github.com/leonardobandini/sap2000-quad-mesher-updates) rimane attivo e pubblica lo stesso ZIP verificato sotto il nome compatibile `Sap2000QuadMesher-<versione>.zip`.

La **2.0.62** mantiene tutti i nodi dei bordi O-grid sul raggio specificato usando archi circolari. La matrice atomica su copie dei modelli è **36/36 PASS** su SAP2000 e **36/36 PASS** su CSiBridge; l'help bilingue e il pacchetto installabile sono stati verificati. [Changelog](CHANGELOG.md).

La **2.0.54** estende FEMesh a CSiBridge, con installazione nella voce Tools di entrambi gli host, e conserva le spunte FAST/backup quando la selezione cambia dopo l'apertura della finestra. Le matrici atomiche hanno dato **36/36 PASS** su SAP2000 e **36/36 PASS** su CSiBridge con BDB salvati e riaperti. [Note di rilascio](docs/FEMESH_2_0_54_RELEASE.md).

La V2 distribuita usa [`SapGmshReplacement.csproj`](SapQuadTransitionPlugin/SapGmshReplacement.csproj) e il sorgente dedicato `PluginV2.cs`; il progetto V1 storico continua a compilare `Plugin.cs` senza trascinare la vecchia interfaccia nella V2. Funzioni, limiti e istruzioni di build/installazione sono in [`README-GMSH-V2.md`](SapQuadTransitionPlugin/README-GMSH-V2.md).

La **V2 2.0.42** espone i passaggi di smoothing, applica la ricomposizione Simple e Blossom alla stessa triangolazione completata e presenta barra/area nella finestra di generazione. Chiudere con la X un'anteprima non applicata ripristina il modello come Annulla mesh; dopo Applica la mesh resta. Dettagli e verifiche: [`note di rilascio 2.0.42`](docs/GMSH_V2_2_0_42_RELEASE.md).

La **V2 2.0.43** richiede una scelta fra **Annulla mesh** e **Applica mesh** quando si chiude un'anteprima non ancora confermata; la finestra indica l'operazione fino al termine. L'interfaccia mostra tre schede: il JSON resta nei tracciati diagnostici, senza editor nascosti attivi. Testi e disposizione di Additional options e Transfer options sono stati rivisti. [Note di rilascio 2.0.43](docs/GMSH_V2_2_0_43_RELEASE.md).

La **V2 2.0.44** ignora nodi/frame selezionati estranei alle aree da suddividere e rispetta l'identità dei nodi SAP2000 anche se più nodi hanno le stesse coordinate: preserva le disconnessioni intenzionali e riusa le stazioni di una cucitura realmente connessa. [Note di rilascio 2.0.44](docs/GMSH_V2_2_0_44_RELEASE.md).

La **V2 2.0.45** aggiorna la guida bilingue con introduzione, procedura operativa, limiti del backup, verifica del modello FEM meshato e modalità di segnalazione dei problemi. [Note di rilascio 2.0.45](docs/GMSH_V2_2_0_45_RELEASE.md).

La **V2 2.0.46** corregge l'import FAST con triangoli e metodi Full-Quad su geometrie molto vincolate; i frame SAP restano integri. Se BAMG produce elementi quasi collineari, un messaggio breve suggerisce di selezionare un altro algoritmo prima di riprovare, senza importare elementi invalidi. [Note di rilascio 2.0.46](docs/GMSH_V2_2_0_46_RELEASE.md).

La build locale 2.0.47 ha aggiunto la compatibilità FAST con le chiavi tabellari vuote di SAP2000 27.2.0 beta e uniformato i checkbox dei fori alle altre opzioni; queste modifiche sono incluse nella 2.0.50 dopo la verifica con SAP2000 27.1.0 stable.

La **V2 2.0.50** include le modifiche locali 2.0.47–2.0.49 e mostra un avviso di attesa centrato sulla finestra SAP2000 durante Applica, Annulla e l'aggiornamento della vista dopo Genera. [Note di rilascio 2.0.50](docs/GMSH_V2_2_0_50_RELEASE.md).

La **V2 2.0.52** recupera le procedure di progetto delle aree dalla tabella di visualizzazione quando l'API editabile ne restituisce temporaneamente zero, senza scambiarle per assenza di assegnazioni. Se un import perde davvero Concrete Shell Design sulle nuove shell, prima di Applica è richiesto il consenso esplicito. [Note di rilascio 2.0.52](docs/GMSH_V2_2_0_52_RELEASE.md).

La **V2 2.0.53** allinea il checkbox e il testo del backup nella scheda Opzioni di trasferimento; cliccando il testo si alterna la spunta. [Note di rilascio 2.0.53](docs/GMSH_V2_2_0_53_RELEASE.md).

Il [censimento Gmsh 4.15.2 per la progettazione della V2](docs/GMSH_V2_INVENTARIO.md) distingue algoritmi 1D/2D/3D, mesh strutturate, quadrangolazione, sizing fields e compatibilità con gli elementi SAP2000. La build 2.0 attualmente installabile è un **prototipo parziale**, non l'interfaccia completa prevista dal censimento.

Per la soletta del modello `Circular_Floor.sdb`, la [guida ai metodi con confronto visivo Midas/Dlubal e prove Gmsh offline](docs/CIRCULAR_FLOOR_GMSH_V2_GUIDA.md) spiega perché una mesh a fasce richiede anche la corretta partizione delle superfici, oltre alla scelta dell'algoritmo 2D.

Lo scopo principale di questo progetto e **mostrare, con un esempio funzionante, come integrare SAP2000 con altri programmi per rendere piu efficace il proprio lavoro**. Il plugin collega C#/.NET, l'API di SAP2000 e Python/Gmsh per automatizzare la creazione di mesh quad-dominant su aree piane. Illustra metodi, procedure e potenzialita dell'integrazione tra software di terze parti: il suo valore prevalente e didattico.

La **1.0.79 è stata la prima versione destinata agli utenti**; la 1.0.80 ha introdotto la congruenza dei bordi raffittiti e un solo import FAST multi-area, la 1.0.81 ha corretto i fallback regolari e i piccoli fori condivisi, e la 1.0.82 ha aggiunto annullamento e misure con suffissi `m`, `cm`, `mm`, `ft`, `in`. Dalla 1.0.83 FAST e preselezionato ma facoltativo; la 1.0.84 aggiunge automaticamente la voce del plugin nel menu Tools di SAP2000 27 durante l'installazione. La 1.0.85 corregge l'import FAST nei modelli con triangoli o shell poligonali preesistenti. La **1.0.87** aggiunge nodi congruenti sul bordo di mesh adiacenti, gestione FAST dei triangoli generati e candidati Gmsh multicore con numero di worker configurabile. La **1.0.88** evita maglie oblunghe su aree nulle sovrapposte; la **1.0.89** corregge Undo FAST per poligoni, aggiunge backup numerati e riduce il sovra-raffittimento della mesh su geometrie triangolari e poligonali. Le versioni prima della 1.0.79 erano build di sviluppo e di prova, anche quando temporaneamente scaricabili su GitHub. Il plugin è utilizzabile, ma risultati e modelli devono essere verificati dall'utente nel proprio contesto tecnico. Il progetto principale e in [`SapQuadTransitionPlugin`](SapQuadTransitionPlugin/README.md).

## Stato del progetto

La **1.0.97** mostra l'aggiornamento disponibile su due righe centrate nella finestra del plugin. La 1.0.96 ripristina l'opzione della dimensione massima vincolante dopo «Annulla mesh»; la 1.0.95 ha introdotto la fascia globale fitta sulle solette radiali, la memoria delle ultime opzioni e l'anteprima con SAP2000 utilizzabile. Il riconoscimento si basa sulla geometria, non sul nome del modello; la tolleranza esplicita sugli spigoli nuovi rimane configurabile. Tutti i 36 esempi di regressione SAP2000 sono passati nella build 1.0.95.

La **1.0.101** corregge le mesh di solette radiali a 60 e 70 cm, anche con dimensione massima vincolante. Rende selezionabile la mesh regolare nel profilo Acciaio: su `Nodo_2` produce 128 quadrilateri cartesiani di 10 cm, oppure 1.653 quadrilateri con passo vincolante di 30 mm, senza nodi sospesi sulle intersezioni ortogonali.

La build locale di prova **1.0.102** dispone tre comandi nella finestra: Genera/Applica, Qualita della mesh e Annulla mesh. Applica mantiene la finestra aperta per ispezionare o ingrandire la mesh in SAP2000 e consente di annullarla finche la finestra resta aperta.

La build locale di prova **1.0.103** applica subito la mesh eliminando gli originali dal modello in memoria; uno snapshot CSV locale conserva coordinate e assegnazioni per consentire **Annulla mesh** anche dopo Applica, mentre lo zoom SAP2000 rimane utilizzabile.

La build locale di prova **1.0.104** protegge la congruenza dei lati condivisi nelle mesh di `Multiple_Silo_Slab` a 0,5 m, mantenendo le stazioni prodotte dalle aree gia elaborate durante le transizioni rettangolari e le mesh con telai. La proposta di organizzazione delle opzioni e del report di qualita e in `docs/PROPOSTA_INTERFACCIA_E_QUALITA_MESH.md`; non modifica ancora l'interfaccia.

La build locale di prova **1.0.105** riordina le opzioni in **Mesh | Fori | Avanzate** con riepilogo della selezione e tre modalita radio esclusive. Se occorre confrontarla con la schermata precedente, il layout classico resta disponibile impostando `SAP_QUAD_OPTIONS_LAYOUT=legacy` prima dell'avvio di SAP2000. La proposta di report globale non e ancora applicata.

La build locale di prova **1.0.106** prova automaticamente strategie alternative quando quella richiesta non produce una mesh, preservando nodi, telai, fori e dimensione massima. Confronta numero di elementi, triangoli e qualita; dopo la generazione indica le opzioni effettivamente utilizzate e gli eventuali avvisi di qualita. Il modello SAP2000 aperto non viene modificato durante il confronto dei candidati.

La build locale di prova **1.0.107** estende la simmetria esatta alle strategie non regolari su selezioni di piu aree e presenta una qualita complessiva mediata per superficie su tutti gli elementi generati, lasciando dimensione e orientamento come controlli vincolanti. Le schede si chiamano **Opzioni della mesh | Fori e Aperture | Opzioni Avanzate** (con traduzioni inglesi). I testi italiani correnti da revisionare sono in [`docs/CATALOGO_OPZIONI_E_TOOLTIP_IT.md`](docs/CATALOGO_OPZIONI_E_TOOLTIP_IT.md); il criterio tecnico della qualita e in [`docs/QUALITA_MESH_AGGREGATA.md`](docs/QUALITA_MESH_AGGREGATA.md). Il profilo materiale conserva per ora il comportamento esistente.

La build locale di prova **1.0.108** applica alla finestra le correzioni italiane dell'autore registrate in [`docs/CATALOGO_OPZIONI_E_TOOLTIP_IT.md`](docs/CATALOGO_OPZIONI_E_TOOLTIP_IT.md) e aggiorna le etichette e i tooltip inglesi. Nell'interfaccia italiana gli oggetti frame sono chiamati "Frame"; le descrizioni delle strategie, della simmetria e della suddivisione degli spigoli con nodi selezionati sono piu esplicite.

La build locale di prova **1.0.109** aggiunge un **Report sugli elementi creati** con i totali effettivi del modello dopo la mesh: aree e tipo di area, frame, link e nodi. I conteggi dell'anteprima escludono gli originali conservati per Annulla; dopo Applica sono aggiornati e dopo Annulla torna la selezione iniziale.

Nella build locale **1.0.110** il report sostituisce la selezione nel medesimo riquadro, senza ridurre lo spazio delle schede. Il recupero automatico prova prima l'inserimento di nodi sugli spigoli con nodi selezionati e mostra l'opzione effettivamente utilizzata. Gli errori del generatore rispettano la lingua selezionata.

La build locale **1.0.111** rende la finestra del plugin richiamabile dalla barra delle applicazioni e prova a riabilitare la finestra SAP2000 durante l'anteprima; la navigazione SAP2000 restava comunque bloccata finché il comando del plugin era in corso. La raccolta locale dei modelli usati per i test si crea sul Desktop con `tools/CollectRegressionModels.ps1`.

La build locale **1.0.112** restituisce a SAP2000 il controllo del comando del plugin mentre l'anteprima resta aperta: questo consente al viewport di elaborare realmente zoom, pan e cambi di vista prima di Applica.

La build locale **1.0.113** mantiene la finestra del plugin in primo piano mentre si naviga nel viewport SAP2000 visibile intorno alla finestra, con l'anteprima ancora da confermare.

La build locale **1.0.114** chiude automaticamente il solo avviso nativo SAP2000 «Plugin completed successfully.» emesso quando il plugin restituisce il controllo al viewport, lasciando aperta l'anteprima della mesh.

La **1.0.115** distribuisce le modifiche verificate delle build locali 1.0.102–1.0.114 e rimuove i link esterni CUBIT e COMSOL dal report della qualita della mesh, mantenendo metriche e intervalli di riferimento.

La build locale di prova **1.0.116** abilita Annulla generazione appena parte l'operazione, anche prima dello snapshot, e offre un comando di annullamento indipendente e reattivo nelle elaborazioni multi-area lunghe.

La build locale di prova **1.0.117** aggiunge una guida offline illustrata in italiano e inglese: F1 o il pulsante ? della finestra aprono la lingua selezionata. La guida include schermate delle tre schede ed esempi SAP2000 prima/dopo in SVG con nodi e frame vincolanti evidenziati. Il plugin mostra un'icona Quad Mesher dedicata nella barra delle applicazioni.

La **1.0.118** recepisce le revisioni dell'autore alla guida italiana, le riporta nella guida inglese e allinea verticalmente i testi del piè di pagina del plugin. Le etichette e i documenti correnti mostrano solo il numero di versione.

La build locale di prova **1.0.119** migliora la chiusura dell'avviso nativo SAP2000 e centra la finestra Annulla generazione sul plugin. La tolleranza iniziale è 20%; una preparazione meno fitta dei candidati simmetrici con frame limita il sovraraffinamento lontano dai vincoli.

La **1.0.120** sostituisce il callback nativo dell'avviso SAP2000 che poteva provocare un crash durante l'interazione con il plugin. Il messaggio di completamento viene chiuso con un controllo periodico protetto; gli errori della finestra vengono registrati localmente senza interrompere il processo SAP2000.

Questa e la copia di progetto ripulita del workspace storico. Contiene il plugin, utility sperimentali, modelli SAP2000, fixture e risultati di test; build, cache e release storiche sono escluse dal controllo versione. Le fixture SAP2000 sono gestite con Git LFS.

Documentazione di continuita:

- [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md): stato funzionale e tecnico verificato.
- [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md): ambiente, build e strategia di test.
- [`docs/MIGRATION_AND_RELEASE.md`](docs/MIGRATION_AND_RELEASE.md): trasferimento, GitHub e packaging.
- [`docs/UPDATES.md`](docs/UPDATES.md): manifest GitHub, notifica aggiornamenti e procedura di pubblicazione.
- [`docs/MULTICORE_PERFORMANCE_1_0_87.md`](docs/MULTICORE_PERFORMANCE_1_0_87.md): 36 regressioni v1.0.87 e confronto controllato del backend multicore.
- [`SapQuadTransitionPlugin/README.md`](SapQuadTransitionPlugin/README.md): uso del plugin e comportamento delle mesh.

## Verifica rapida

Dal root del progetto:

```cmd
dotnet build SapQuadTransitionPlugin\SapQuadTransitionPlugin.csproj -c Release
python -c "import gmsh; print(gmsh.__version__)"
```

Verifica storica della fase di sviluppo, eseguita il 24 settembre 2026:

- compilazione Release completata con 0 warning e 0 errori;
- Python 3.12.7;
- Gmsh 4.15.2;
- SAP2000 27 interop disponibile localmente.

Il pacchetto binario include un runtime Python 3.12 privato e Gmsh 4.15.2. L'utente finale non deve installare Python, Gmsh o pacchetti `pip`.

## Avvertenza

`SAP2000v1.dll` non fa parte del progetto e non deve essere pubblicata o inclusa nei pacchetti. Le fixture SAP2000 presenti sono state dichiarate pubblicabili dal loro autore, ma sono escluse dal pacchetto binario del plugin.

## Licenza

Il [codice originale](LICENSE-APPLICATION.md) e GPL-2.0-or-later (`SPDX-License-Identifier: GPL-2.0-or-later`). `LICENSE` contiene GPLv2, `GPL-3.0.txt` GPLv3; per il backend binario combinato con OpenSSL 3 si sceglie l'opzione GPLv3. [Questa nota](SAP2000-LINKING-EXCEPTION.md) riguarda esclusivamente il codice C# dell'autore, **non concede diritti sull'API SAP2000 o su Gmsh**: i termini dei terzi sono in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md). Gli archivi sorgenti sono allegati alla [release corrente](https://github.com/leonardobandini/sap2000-quad-mesher-updates/releases/latest) e conservati nell'[archivio pubblico dei sorgenti](https://github.com/leonardobandini/sap2000-quad-mesher-updates/tree/source-archive) dopo la sostituzione delle release di prova.
