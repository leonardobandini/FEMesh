# V2 2.0.29: valutazione della dimensione massima

La 2.0.29 **non altera la mesh**, il valore richiesto a Gmsh, la dimensione minima o la tolleranza di automerge SAP2000. Cambia solo il giudizio di qualità nella V2; la V1 conserva il proprio criterio.

Per ciascuna shell di area positiva, `h_K` è il lato libero più lungo (escludendo soltanto i segmenti originali espressamente protetti); `A_K` è la superficie e `h_t = h_nominale × 1,20` è il riferimento con la tolleranza già esistente. Le shell con `h_K > h_t × 1,001` restano contate come **Size exceptions** e la loro quota di superficie resta visibile. La nuova misura supplementare è

`e_A = Σ A_K × max(0, h_K / h_t − 1) / Σ A_K`,

applicata soltanto alle shell effettivamente fuori misura. Un eccesso piccolo in poche shell non domina quindi l'intero risultato, mentre un eccesso esteso o consistente aumenta `e_A`.

Il giudizio dimensionale passa se valgono **tutti** questi limiti di progetto, non soglie universali della letteratura: `e_A ≤ 2%`, quota di superficie fuori misura `≤ 10%`, e nessun lato libero maggiore di `1,5 × h_nominale` (con il margine numerico `× 1,001`). Il massimo, la percentuale fuori misura, la nuova media dell'eccesso e il massimo dei tratti originali protetti restano leggibili nel report. Nessuna eccezione è concessa agli elementi invertiti o degeneri; la qualità media della forma deve restare almeno 0,5.

Nella prova SAP2000 isolata `nTEST026` sulla DLL locale 2.0.29 (`%TEMP%\opencode\sqm-local-v229-quality-regression\nTEST026`), la mesh conserva **1.096 shell** e dodici fori integri. `h_nominale=0,05 m`, `h_t=0,06 m`, massimo lato libero `0,062 m`, 1,854% di area fuori misura e **0,064% di eccesso medio pesato**: `quality_passed=True`, con punteggio di forma invariato 0,793/1 e **2 Size exceptions ancora dichiarate** nel report. L'esito positivo riflette la nuova politica di valutazione, non una correzione geometrica aggiuntiva. La prova `tools/TestGmshSizeQuality.ps1` verifica anche casi con sforamento diffuso o un lato gravemente fuori misura che devono fallire.
