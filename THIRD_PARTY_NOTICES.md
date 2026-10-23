# Third-Party Notices

## SAP2000

La versione distribuita del plugin usa l'API di SAP2000/CSiBridge tramite `CSiAPIv1.dll`.

SAP2000, CSiBridge e le loro DLL API sono software proprietari di Computers and Structures, Inc. (CSI). Non fanno parte del pacchetto FEMesh. Gli utenti devono ottenere i programmi e i componenti API direttamente da CSI nel rispetto della licenza applicabile.

Sito: <https://www.csiamerica.com/products/sap2000>

## Componenti del backend binario 2.0.65

Il codice originale FEMesh è GPL-2.0-or-later. Per il backend binario
combinato con OpenSSL 3 (Apache-2.0) viene esercitata l'opzione GPLv3
consentita dalle clausole «or later» del codice originale e di Gmsh. Questa
scelta non modifica la licenza di alcun componente di terzi.

| Componente | Licenza | Ruolo e riferimenti |
| --- | --- | --- |
| Gmsh 4.15.2 e binding Python | GPL-2.0-or-later con eccezione limitata dei titolari | Libreria di mesh nel backend; `licenses/GMSH-LICENSE.txt`, binding nel sorgente FEMesh e `gmsh-4.15.2-source.tgz` tra gli asset della stessa release. |
| CPython 3.12.7 | Python Software Foundation License | Runtime autonomo; `licenses/PYTHON-LICENSE.txt`, [sorgente CPython](https://www.python.org/downloads/release/python-3127/). |
| OpenSSL 3.0.15 (`libcrypto-3.dll`) | Apache-2.0 | Componente del runtime Python; avviso nel testo Python e [sorgente OpenSSL](https://github.com/openssl/openssl/releases/tag/openssl-3.0.15). |
| libffi (`libffi-8.dll`, versione puntuale da verificare) | Licenza permissiva libffi | Supporto FFI; avviso nel testo Python e [sorgente upstream](https://github.com/libffi/libffi). |
| PyInstaller 6.16.0 (bootloader) | GPL-2.0 con eccezione per i programmi generati; alcuni file Apache-2.0 | Bootloader nel backend eseguibile; [sorgente e termini](https://github.com/pyinstaller/pyinstaller/releases/tag/v6.16.0). |

## Prerequisito Microsoft esterno

FEMesh 2.0.65 **non include** `VCRUNTIME140.dll`, `VCRUNTIME140_1.dll` né
altre DLL separate del runtime Visual C++ Microsoft. Prima dell'installazione
occorre installare separatamente il
[Microsoft Visual C++ Redistributable x64 ufficiale](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist)
in versione **14.42.34226.3 o successiva compatibile**. La prova del
prerequisito su una macchina Windows pulita rimane da effettuare.

L'additional permission del codice C# verso `CSiAPIv1.dll` non si applica a
Gmsh o agli altri componenti di terzi. Ogni release binaria distribuita deve
rendere disponibili gli archivi dei sorgenti corrispondenti FEMesh/backend e
Gmsh 4.15.2 come asset della medesima release, con versione e checksum.

## Gmsh 4.15.2

I backend Python usano Gmsh 4.15.2.

Gmsh è distribuito dai suoi titolari secondo GNU GPL versione 2 o successiva, con un'eccezione specifica per i componenti elencati nel testo originale. Il pacchetto binario contiene il binding Python e `gmsh-4.15.dll` dalla wheel ufficiale Windows di Gmsh 4.15.2. Il testo originale è incluso in `licenses/GMSH-LICENSE.txt`. L'archivio sorgente Gmsh e quello FEMesh/backend devono accompagnare il binario nella medesima release, con i rispettivi checksum. La scelta GPLv3 per il backend combinato con OpenSSL 3 non modifica la licenza originale o l'eccezione di Gmsh.

Wheel Windows ufficiale: <https://pypi.org/project/gmsh/4.15.2/>. SHA-256 della wheel `gmsh-4.15.2-py2.py3-none-win_amd64.whl`: `7b36083bb410fa27c5d0e052929d1a9844a5b09169d66017b72b41aabd49d711`. SHA-256 della DLL inclusa: `6cac3eefb477265d9fa60bbd869dbbbf7c7ca4cb308c0f8f2b43e91d43de3c1c`. Il binding usato corrisponde byte per byte al `gmsh.py` della medesima wheel, incluso nell'archivio dei sorgenti del plugin.

Sito, licenza e sorgenti: <https://gmsh.info/> e <https://gmsh.info/src/gmsh-4.15.2-source.tgz>

## Python

Il runtime autonomo incorpora CPython 3.12, distribuito secondo la Python Software Foundation License. Il testo applicabile e incluso in `licenses/PYTHON-LICENSE.txt`.

Il pacchetto binario incorpora `libcrypto-3.dll` (OpenSSL 3, Apache-2.0) e `libffi-8.dll` (licenza permissiva). `licenses/PYTHON-LICENSE.txt` riporta anche condizioni relative a codice Microsoft incorporato nella build Python; non significa che FEMesh distribuisca separatamente DLL del runtime Visual C++. I componenti conservano le rispettive licenze: non sono relicenziati sotto GPL dal progetto.

La versione inclusa è CPython **3.12.7** con OpenSSL **3.0.15**. Il codice sorgente CPython è disponibile dalla [release Python 3.12.7](https://www.python.org/downloads/release/python-3127/), OpenSSL dalla [release 3.0.15](https://github.com/openssl/openssl/releases/tag/openssl-3.0.15); il sorgente e le condizioni di libffi sono disponibili presso [libffi](https://github.com/libffi/libffi). `licenses/PYTHON-LICENSE.txt` riporta anche avvisi libffi e Apache-2.0 e condizioni sul codice Microsoft incorporato in Python; le DLL Visual C++ restano un prerequisito esterno. L'eccezione GPL di Gmsh non estende la propria autorizzazione ad altri componenti esterni.

Sito: <https://www.python.org/>

## PyInstaller

Il runtime autonomo e prodotto con PyInstaller 6.16.0. PyInstaller e distribuito secondo GPL-2.0 con una speciale eccezione per la distribuzione dei programmi generati; alcuni suoi file usano Apache-2.0. PyInstaller e uno strumento di build e non viene importato dal plugin a runtime.

Il bootloader PyInstaller nel file eseguibile mantiene i termini e l'eccezione dei suoi autori. Il sorgente dello strumento e il testo dell'eccezione sono disponibili presso [PyInstaller 6.16.0](https://github.com/pyinstaller/pyinstaller/releases/tag/v6.16.0); lo script di configurazione `packaging/SapGmshBackend.spec` è incluso nei sorgenti FEMesh corrispondenti.

Sito e licenza: <https://pyinstaller.org/>

## Microsoft .NET

Il plugin usa .NET Framework 4.8 e Windows Forms. I relativi runtime e strumenti sono distribuiti da Microsoft secondo i rispettivi termini di licenza e non sono inclusi in questo pacchetto. Il plugin non contiene `SAP2000v1.dll`.
