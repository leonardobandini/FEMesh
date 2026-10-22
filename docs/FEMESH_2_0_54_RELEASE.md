# FEMesh 2.0.54 — SAP2000 e CSiBridge

Il plugin si chiama **FEMesh** nella finestra e nel menu **Tools** di SAP2000 27 e CSiBridge 27. La vecchia identità COM, il percorso tecnico dell'installazione e il nome del repository GitHub restano invariati per consentire l'aggiornamento delle versioni installate. La guida bilingue e i testi delle due interfacce usano il nuovo nome.

Quando FEMesh viene aperto senza aree selezionate, le scelte FAST e backup restano memorizzate anche se temporaneamente disabilitate; selezionando una shell dopo l'apertura i due controlli tornano disponibili senza perdere la spunta. Il testo esplicativo del backup si disabilita e si riabilita con la casella. Il resto della meshatura e delle assegnazioni conserva i controlli della 2.0.53.

**SAP2000 27.1:** 36/36 esempi atomici PASS in due sessioni SAP persistenti in parallelo (24+12 modelli aperti in serie nella rispettiva sessione). Preview→Annulla Standard e FAST PASS.

**CSiBridge 27.1:** 36/36 esempi atomici PASS in una sessione Bridge persistente. I modelli SDB sono stati aperti su copie, salvati come BDB, meshati, salvati e riaperti. Due prove mirate di Annulla ripristinano le aree originali e producono BDB riapribili. Sono state verificate sia la build con la sola API di Bridge sia la migrazione della voce Tools su copie del profilo. La prova del menu Tools nella GUI Bridge resta prevista per la verifica manuale dell'utente.

La verifica strutturale e delle assegnazioni sul modello di progetto resta necessaria; il plugin non salva automaticamente il modello in uso. Per risultati, limiti e percorsi locali delle prove consultare `docs/FEMESH_MULTI_HOST_2_0_54_LOCAL.md`.
