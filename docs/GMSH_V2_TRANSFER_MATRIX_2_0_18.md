# Matrice V2 2.0.18 - assegnazioni padre, figli e Undo

Stato del candidato locale 2.0.18 su SAP2000 27.1.0. Le regressioni `Apply -> Undo` passano su tutti i 36 modelli atomici sia in FAST sia in Standard. FAST riporta `csv-undo-method=tabular`; Standard riporta `csv-undo-method=legacy-object`. Verde significa verificato su copia SAP, giallo implementato ma non verificato con una fixture dedicata per ogni variante, rosso indica una API SAP non funzionante nel caso provato.

| Proprieta / assegnazione del padre | FAST: padre -> figli (tabelle) | Standard: padre -> figli (singoli oggetti) | FAST: figli -> padre con Undo | Standard: figli -> padre con Undo |
| --- | --- | --- | --- | --- |
| Geometria, nome e GUID area | Verde: nodi e shell creati in blocco con `Joint Coordinates` e `Connectivity - Area`; conteggi e connettivita verificati. | Verde: nodi e shell creati con `AddCartesian` e `AddByPoint`. Una mesh identica al padre conserva direttamente l'oggetto, evitando duplicati coincidenti. | Verde: cancellazione per omissione e ripristino tabellare. Eccezione mirata per poligoni con piu di 4 nodi: `AddCartesian`/`AddByPoint`, poi verifica di nome, GUID e ordine completo dei nodi. | Verde: shell generate eliminate e aree originali ricreate per oggetto; connettivita completa verificata. |
| Sezione shell; assi locali semplici; massa; edge constraint | Verde: sezione nella tabella primaria; altre proprieta applicate e confrontate su ogni figlio. | Verde: setter SAP applicati e confrontati su ogni figlio. | Verde: sezione e tabelle di assegnazione originali confrontate dopo Undo. | Verde: proprieta del padre ripristinate dalla snapshot e verificate. |
| Modificatori, materiale sovrascritto, temperatura materiale | Verde: valori espliciti F11=0,72, materiale e 26,5 C verificati sui figli. | Verde: stessa fixture verificata sui figli. | Verde: tabelle oggetto originali ripristinate e confrontate. | Verde: valori riapplicati al padre ricostruito e confrontati. |
| Carico uniforme, pressione e molla superficiali | Verde: intensita, pattern, faccia e molla verificati sui figli. | Verde: stessa fixture verificata tramite API oggetti. | Verde: tabelle oggetto prima/dopo identiche con tutti i load pattern temporaneamente visibili. | Verde: carichi e molle del padre ripristinati dalla snapshot. |
| Pressione e molla su bordo | Verde: solo sui bordi figli corrispondenti; copertura totale uguale al bordo padre. | Verde: stesso controllo geometrico di copertura. | Verde: fixture FAST `Apply -> Undo` verificata. | Giallo: percorso di ripristino presente; non ripetuta una fixture Standard dedicata al solo carico di bordo. |
| Gruppi area | Verde: gruppo esplicito su ciascun figlio; `ALL` resta automatico. | Verde: assegnazione per oggetto su ciascun figlio. | Verde: tabella gruppi originale confrontata dopo Undo. | Verde: gruppi del padre riapplicati e verificati. |
| Procedura di progetto area | Giallo: copiata quando SAP espone il record; prova focalizzata `No Design`. | Giallo: stessa informazione applicata quando leggibile, senza fixture Gmsh non predefinita completa. | Giallo: preservazione tabellare predisposta; avviso se la tabella e illeggibile. | Giallo: ripristino predisposto quando la API espone il valore. |
| Overwrite shell EC2 | Rosso: getter/setter xAPI restituiscono codice 1; replica manuale richiesta. | Rosso: stesso limite xAPI. | Rosso: non garantito se la tabella e illeggibile; usare il backup numerato. | Rosso: stesso limite; usare il backup numerato. |
| Altri carichi area: gravita, poropressione, rotazione, strain, temperatura, vento | Giallo: cattura e trasferimento implementati, non ogni tipo ha una fixture dedicata. | Giallo: setter presenti, non ogni tipo ha una fixture dedicata. | Giallo: tabelle oggetto preservate, senza prova separata per ogni tipo. | Giallo: snapshot e ripristino per oggetto presenti, senza prova separata per ogni tipo. |
| Joint pattern sui nuovi joint; thickness overwrite nodale | Verde in 2.0.21: bordi lineari, quadrilateri bilineari, pattern thin-plate e spessori mean-value sui poligoni; valori scritti riletti via API. | Verde: stessa regola e verifica per oggetto. | Verde: fixture originali ripristinate; per valori determinanti resta consigliato il controllo manuale a valle. | Verde: proprieta del padre ripristinate. |
| Carico area -> frame; joint offset nodali | Rosso: non esiste ancora una ripartizione/interpolazione validata; la mesh viene bloccata. | Rosso: stesso blocco preventivo. | Giallo: nessun Undo pertinente per una mesh bloccata. | Giallo: nessun Undo pertinente per una mesh bloccata. |
| Carichi, molle, restraint e constraint dei joint originali | Giallo: restano sui joint riutilizzati; non vengono inventati sui nuovi nodi. | Giallo: stesso comportamento. | Verde: fixture con 13 tabelle di assegnazioni area/joint identiche prima e dopo. | Verde: joint originali e relative assegnazioni ripristinati e verificati. |

## Evidenza di regressione

- FAST: 36/36 `Apply -> Undo`, metodo tracciato `tabular`, import SAP accettati soltanto con `fatal=0`, `errors=0`, `warnings=0`.
- Standard: 36/36 `Apply -> Undo`, metodo tracciato `legacy-object`.
- Poligoni FAST verificati esplicitamente: `nTEST004`, `nTEST022`, `nTEST032`; ulteriori poligoni sono passati nella matrice completa.
- Mesh Standard identica al padre verificata in `nTEST029`: nessuna shell coincidente viene creata e tutte le assegnazioni restano sull'oggetto originale.

## SAP2000 27.2.0 beta compatibility status

The matrix above is the verified SAP2000 27.1.0 baseline. The following table records the narrower set of tests completed on SAP2000 27.2.0 build 3919 beta and installed locally as the 2.0.19 compatibility candidate. It must not be read as a complete 27.2 certification.

| Capability on SAP2000 27.2.0 beta | FAST | Standard | Current evidence |
| --- | --- | --- | --- |
| Read the three primary geometry tables | Green | Green | Blank editing-array FieldKeys are recovered from CSV headers and validated against metadata and row values. |
| Generate and Undo `Circular_Floor` (8 areas, 281 joints, 176 frames selected) | Green | Green | Both modes returned to 8 areas and 281 joints with the original names; the source SDB hash was unchanged. |
| Parent-to-child section, axes, mass, edge constraint, modifiers, material, material temperature, groups, loads, pressure and springs | Green for a 50-quad fixture | Green for a 49-quad + 12-triangle fixture | `PARENT_CHILD_ASSIGNMENTS_PASS` and `PARENT_EDGE_ASSIGNMENTS_PASS`. |
| Apply-to-Undo with explicit parent/edge fixture | Green for a full-quad fixture | Green for a mixed fixture | FAST reports `csv-undo-method=tabular verified=true`; Standard reports `csv-undo-method=legacy-object verified=true`. |
| Area material temperature | Green | Green | Restored through `AreaObj.SetMatTemp`; table replay incorrectly converted 26.5 C to -3.0556 C in the tested beta. |
| FAST mixed quad/triangle import | Yellow / open | Not applicable | The 27.1 repeated-`Joint3` triangle padding is rejected by 27.2 in the focused mixed FAST case; the revised trial did not complete within the timeout. |
| `Area Design Procedures` | Yellow / manual review | Yellow / manual review | The tested 27.2 schema lacks the expected `Area` identity field. No non-default procedure is claimed as preserved. |
| EC2 shell overwrites | Red | Red | Existing xAPI getter/setter limitation remains; use backup and manual review. |

Observed 27.2 schema differences and the exact test record are documented in `SAP2000_27_2_BETA_COMPATIBILITY_REPORT.md`.
