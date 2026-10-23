# FEMesh

FEMesh è un plugin open source per generare mesh di elementi shell prevalentemente quadrangolari in **SAP2000 e CSiBridge 27+**, usando Gmsh. L'installer registra **Tools → FEMesh** negli host già inizializzati. Windows x64 e .NET Framework 4.8 sono necessari per il plugin; Python e Gmsh sono inclusi nello ZIP installabile.

## Distribuzione corrente

- [Release FEMesh v2.0.64](https://github.com/leonardobandini/FEMesh/releases/tag/v2.0.64) · [ZIP, sorgenti e checksum](packaging/SOURCE.template.md).
- Prerequisito esterno: installa il [Microsoft Visual C++ Redistributable x64 ufficiale](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist), versione **14.42.34226.3 o successiva compatibile**. Le DLL runtime Visual C++ Microsoft non sono incluse nello ZIP FEMesh.
- Per installare: dopo il prerequisito, estrai lo ZIP, chiudi SAP2000 e CSiBridge, esegui `install_plugin.cmd` e riapri l'host.
- [Guida FEMesh in italiano](docs/help-gmsh-v2/index-it.html) · [English help](docs/help-gmsh-v2/index-en.html).
- [Build dai sorgenti](packaging/SOURCE_BUILD.md) · [licenze e termini](LICENSE-APPLICATION.md) · [componenti di terzi](THIRD_PARTY_NOTICES.md).

La candidata **2.0.64** contiene `SOURCE.md` con i riferimenti ai sorgenti corrispondenti pubblicabili esclusivamente come asset della stessa release. La verifica di ogni modello ingegneristico risultante resta a carico dell'utilizzatore.

Il codice originale FEMesh è **GPL-2.0-or-later**; Gmsh 4.15.2 è **GPL-2.0-or-later** dei suoi titolari. Per il backend binario combinato con OpenSSL 3 (Apache-2.0) viene scelta **GPLv3** secondo le clausole «or later». Le licenze degli altri componenti e l'eccezione limitata di Gmsh restano invariate. SAP2000, CSiBridge e `CSiAPIv1.dll` non sono inclusi nel pacchetto.

Il controllo aggiornamenti integrato è disattivato. Le future versioni saranno distribuite tramite le [release FEMesh](https://github.com/leonardobandini/FEMesh/releases).
