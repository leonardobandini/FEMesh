# FEMesh

FEMesh è un plugin open source per generare mesh di elementi shell prevalentemente quadrangolari in **SAP2000 e CSiBridge 27+**, usando Gmsh. L'installer registra **Tools → FEMesh** negli host già inizializzati. Windows x64 e .NET Framework 4.8 sono necessari per il plugin; Python e Gmsh sono inclusi nello ZIP installabile.

## Distribuzione corrente

- **[Scarica lo ZIP d'installazione FEMesh più recente](https://github.com/leonardobandini/FEMesh/releases/latest/download/FEMesh-latest.zip)** · [Release e checksum](https://github.com/leonardobandini/FEMesh/releases/latest).
- Per installare: estrai lo ZIP, chiudi SAP2000 e CSiBridge, esegui `install_plugin.cmd` e riapri l'host.
- [Guida FEMesh in italiano](docs/help-gmsh-v2/index-it.html) · [English help](docs/help-gmsh-v2/index-en.html).
- [Codice sorgente della release](https://github.com/leonardobandini/FEMesh/releases/latest) · [build dai sorgenti](packaging/SOURCE_BUILD.md) · [licenze e termini](LICENSE-APPLICATION.md) · [componenti di terzi](THIRD_PARTY_NOTICES.md).

La release **2.0.63** distribuisce gli stessi algoritmi di mesh verificati nella 2.0.62 e include nello ZIP `SOURCE.md` per raggiungere i sorgenti corrispondenti. La matrice sulle copie dei modelli ha dato **36/36 PASS in SAP2000** e **36/36 PASS in CSiBridge**; l'help bilingue, il pacchetto installabile e una build eseguita dal solo archivio sorgenti sono stati verificati. Ogni modello ingegneristico risultante richiede comunque la verifica delle assegnazioni e dei risultati da parte dell'utilizzatore.

Il codice originale FEMesh e Gmsh 4.15.2 sono **GPL-2.0-or-later**; il binario combinato con OpenSSL 3 (Apache-2.0) sceglie **GPLv3**. Le licenze degli altri componenti rimangono quelle dei rispettivi titolari. Il programma CSI e la sua DLL API non sono inclusi nella distribuzione.

Le versioni precedenti erano build di **sviluppo e debug**, utilizzate per le prove: questa pagina descrive solo la distribuzione corrente. I sorgenti corrispondenti alle copie precedentemente rese scaricabili rimangono archiviati; i diritti già concessi ai loro destinatari non vengono revocati. Il [feed degli aggiornamenti esistenti](https://github.com/leonardobandini/sap2000-quad-mesher-updates) conserva i nomi tecnici compatibili con i client installati.
