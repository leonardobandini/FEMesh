# Third-Party Notices

## SAP2000

La versione V2 del plugin usa l'API di SAP2000/CSiBridge tramite `CSiAPIv1.dll`. Le versioni storiche usavano `SAP2000v1.dll`.

SAP2000, CSiBridge e le loro DLL API sono software proprietari di Computers and Structures, Inc. (CSI). Non fanno parte del pacchetto FEMesh. Gli utenti devono ottenere i programmi e i componenti API direttamente da CSI nel rispetto della licenza applicabile.

Sito: <https://www.csiamerica.com/products/sap2000>

## Gmsh 4.15.2

I backend Python usano Gmsh 4.15.2.

Gmsh e distribuito dagli autori secondo GNU General Public License, versione 2 o successiva, con un'eccezione specifica per le librerie elencate nel testo originale (non per qualunque software esterno). Il pacchetto binario incorpora il binding Python e `gmsh-4.15.dll` dalla wheel ufficiale Windows di Gmsh 4.15.2. Il testo originale e incluso in `licenses/GMSH-LICENSE.txt`. `gmsh-4.15.2-source.tgz` e il sorgente proprio del backend vengono pubblicati come asset separati **nella stessa release pubblica**. Il codice proprio di questo backend e GPL-2.0-or-later; per il binario distribuito insieme a OpenSSL 3 (Apache-2.0) viene scelta l'opzione GPLv3, consentita dalle clausole "o successiva" sia del nostro codice sia di Gmsh. L'ulteriore permesso per il codice C#/SAP2000 non modifica i termini di Gmsh.

Wheel Windows ufficiale: <https://pypi.org/project/gmsh/4.15.2/>. SHA-256 della wheel `gmsh-4.15.2-py2.py3-none-win_amd64.whl`: `7b36083bb410fa27c5d0e052929d1a9844a5b09169d66017b72b41aabd49d711`. SHA-256 della DLL inclusa: `6cac3eefb477265d9fa60bbd869dbbbf7c7ca4cb308c0f8f2b43e91d43de3c1c`. Il binding usato corrisponde byte per byte al `gmsh.py` della medesima wheel, incluso nell'archivio dei sorgenti del plugin.

Sito, licenza e sorgenti: <https://gmsh.info/> e <https://gmsh.info/src/gmsh-4.15.2-source.tgz>

## Python

Il runtime autonomo incorpora CPython 3.12, distribuito secondo la Python Software Foundation License. Il testo applicabile e incluso in `licenses/PYTHON-LICENSE.txt`.

Il runtime incorpora inoltre `libcrypto-3.dll` (OpenSSL 3, Apache-2.0), `libffi-8.dll` (licenza permissiva) e i runtime Visual C++ Microsoft. Le condizioni e gli avvisi OpenSSL/libffi e le condizioni sui binari Windows Microsoft sono riportati anche nella licenza Python inclusa. Questi componenti conservano le proprie licenze: non sono relicenziati sotto GPL dal progetto.

La versione inclusa è CPython **3.12.7** con OpenSSL **3.0.15**. Il codice sorgente CPython è disponibile dalla [release Python 3.12.7](https://www.python.org/downloads/release/python-3127/), OpenSSL dalla [release 3.0.15](https://github.com/openssl/openssl/releases/tag/openssl-3.0.15); il sorgente e le condizioni di libffi sono disponibili presso [libffi](https://github.com/libffi/libffi). Il testo incluso in `licenses/PYTHON-LICENSE.txt` contiene anche le condizioni applicabili di libffi, Apache-2.0 e dei componenti Windows Microsoft. L'eccezione GPL di Gmsh non estende la propria autorizzazione ad altri componenti esterni.

Sito: <https://www.python.org/>

## PyInstaller

Il runtime autonomo e prodotto con PyInstaller 6.16.0. PyInstaller e distribuito secondo GPL-2.0 con una speciale eccezione per la distribuzione dei programmi generati; alcuni suoi file usano Apache-2.0. PyInstaller e uno strumento di build e non viene importato dal plugin a runtime.

Il bootloader PyInstaller nel file eseguibile mantiene i termini e l'eccezione dei suoi autori. Il sorgente dello strumento e il testo dell'eccezione sono disponibili presso [PyInstaller 6.16.0](https://github.com/pyinstaller/pyinstaller/releases/tag/v6.16.0); lo script di configurazione `packaging/SapGmshBackend.spec` è incluso nei sorgenti FEMesh corrispondenti.

Sito e licenza: <https://pyinstaller.org/>

## Microsoft .NET

Il plugin usa .NET Framework 4.8 e Windows Forms. I relativi runtime e strumenti sono distribuiti da Microsoft secondo i rispettivi termini di licenza e non sono inclusi in questo pacchetto. Il plugin non contiene `SAP2000v1.dll`.
