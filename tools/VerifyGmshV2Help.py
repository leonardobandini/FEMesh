"""Check both shipped help languages, local links and V2-verified examples."""
import json
import re
import hashlib
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELP = ROOT / 'docs' / 'help-gmsh-v2'


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get('id'):
            self.ids.add(values['id'])
        for name in ('href', 'src'):
            if values.get(name):
                self.links.append(values[name])


def main():
    for diagram in HELP.rglob('*.svg'):
        if re.search(r'\bSAP\b(?!2000)', diagram.read_text(encoding='utf-8-sig')):
            raise ValueError('Visible diagram uses SAP instead of SAP2000: ' + diagram.name)
    current = json.loads((HELP / 'assets' / 'new-ui-examples.json').read_text(encoding='utf-8'))
    if len(current) != 23 or len({item['id'] for item in current}) != 23:
        raise ValueError('Missing or duplicate SAP-verified New UI example')
    if any('runFolder' in item for item in current):
        raise ValueError('Public help examples must not expose local run folders')
    for item in current:
        options = item['settings']
        if (options.get('previewMode') is not True or options.get('algorithm') == 9 or
                item['generated']['areas'] != item['generated']['quads'] + item['generated']['triangles'] or
                'Size exceptions:' not in item['qualitySummary'] or
                not all((HELP / 'assets' / item[key]).is_file() for key in
                        ('screenshot', 'sourceSvg', 'resultSvg', 'backendSettings'))):
            raise ValueError('New UI SAP example/settings missing or inconsistent: ' + item['id'])
        saved = json.loads((HELP / 'assets' / item['backendSettings']).read_text(encoding='utf-8-sig'))
        if saved != options:
            raise ValueError('New UI effective Gmsh settings differ from archived JSON: ' + item['id'])
    regular = json.loads((HELP / 'assets' / 'regular-grid-sap-settings.json').read_text(encoding='utf-8'))
    original = json.loads((HELP / 'assets' / 'new-ui-nTEST001-settings.json').read_text(encoding='utf-8-sig'))
    if regular['structured']['mode'] != 'automatic':
        raise ValueError('Regular-grid SAP settings must enable automatic grid preference')
    original['structured']['mode'] = 'automatic'
    if regular != original:
        raise ValueError('Grid comparison changes additional options besides structured.mode')
    documented_options = ('Mesh.Smoothing', 'Mesh.RefineSteps', 'Mesh.AnisoMax', 'Mesh.SmoothRatio',
                          'Mesh.RecombineMinimumQuality', 'Mesh.RecombineOptimizeTopology',
                          'Mesh.RecombineNodeRepositioning', 'Mesh.QuadqsSizemapMethod',
                          'Mesh.QuadqsTopologyOptimizationMethods', 'Mesh.QuadqsRemeshingBoldness',
                           'Mesh.QuadqsScalingOnTriangulation', 'Mesh.AlgorithmSwitchOnFailure')
    for name in ('index-it.html', 'index-en.html'):
        parser = Links()
        parser.feed((HELP / name).read_text(encoding='utf-8'))
        for url in parser.links:
            if url.startswith('#'):
                if url[1:] not in parser.ids:
                    raise FileNotFoundError(name + ': missing section ' + url)
            elif '://' not in url and not (HELP / url).is_file():
                raise FileNotFoundError(name + ': missing local resource ' + url)
        text = (HELP / name).read_text(encoding='utf-8')
        if 'ETABS' in text.upper():
            raise ValueError(name + ': excluded host mentioned in the public help')
        additional = text.split('<section id="aggiuntive">', 1)[1].split('</section>', 1)[0]
        gmsh_tab = text.split('<section id="gmsh">', 1)[1].split('</section>', 1)[0]
        grid_name = 'Prefer regular (grid-aligned) mesh when possible' if name.endswith('-en.html') else 'Preferisci mesh regolari allineate alla griglia'
        if (any(option not in text for option in documented_options) or
                any('<section id="' + section + '">' not in text for section in
                    ('transazione', 'unita', 'interfaccia', 'bordi', 'ricette', 'griglia-esempi')) or
                grid_name not in additional or grid_name in gmsh_tab or
                'preserveSelectedEdges=true' not in text.split('<section id="bordi">', 1)[1].split('</section>', 1)[0] or
                '<section id="storico">' in text or 'legacy-' in text):
            raise ValueError(name + ': incomplete or stale current-interface help')
        language = 'en' if name.endswith('-en.html') else 'it'
        if ('<section id="json">' in text or 'interface-v244-' in text or
                re.search(r'\bSAP\b(?!2000)', text) or
                re.search(r'new-ui-[^"<> ]+-(?:options|additional|transfer|symmetry|json)\.png', text)):
            raise ValueError(name + ': obsolete host wording or interface image is still displayed')
        for tab in ('gmsh', 'additional', 'transfer'):
            image = HELP / 'assets' / f'interface-v261-{language}-{tab}.png'
            raw = image.read_bytes()
            old_image = HELP / 'assets' / f'interface-v244-{language}-{tab}.png'
            if (text.count(image.name) != 2 or raw[:8] != b'\x89PNG\r\n\x1a\n' or
                     int.from_bytes(raw[16:20], 'big') < 550 or
                     int.from_bytes(raw[20:24], 'big') < 760 or
                     hashlib.sha256(raw).digest() == hashlib.sha256(old_image.read_bytes()).digest()):
                raise ValueError(name + ': missing or invalid current-interface screenshot ' + tab)
        for marker in ((('FEMesh version · 2.0.68' if name.endswith('-en.html') else 'Versione FEMesh · 2.0.68'), 'leonardo@csi-italia.eu', 'Mesh.MeshSizeMin', 'Mesh.Smoothing', 'Mesh.AlgorithmSwitchOnFailure',
                          'https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist',
                          'https://gmsh.info/', 'C. Geuzaine', 'J.-F. Remacle',
                          'Gmsh attribution.' if name.endswith('-en.html') else 'Attribuzione Gmsh.',
                          '14.42.34226.3',
                          'Microsoft Visual C++ runtime DLLs are not included' if name.endswith('-en.html') else 'Le DLL runtime Visual C++ Microsoft non sono incluse',
                          'Mesh.QuadqsSizemapMethod', 'Mesh.RecombineNodeRepositioning',
                          'Mesh.RecombineOptimizeTopology',
                          'Prefer regular (grid-aligned) mesh when possible' if name.endswith('-en.html') else 'Preferisci mesh regolari allineate alla griglia',
                                'October 25, 2026' if name.endswith('-en.html') else '25 ottobre 2026',
                          'Additional options' if name.endswith('-en.html') else 'Opzioni aggiuntive',
                          'Transfer options' if name.endswith('-en.html') else 'Opzioni di trasferimento',
                          'Do not show this backup warning again' if name.endswith('-en.html') else 'Non mostrare più questo avviso sul backup',
                          'Do not show this Apply confirmation again' if name.endswith('-en.html') else 'Non mostrare più questa conferma di Applica',
                           'source areas remain visible' if name.endswith('-en.html') else 'aree originali restano visibili')
                        ):
            if marker not in text:
                raise ValueError(name + ': undocumented feature ' + marker)
        if any(item['id'] not in text for item in current):
            raise ValueError(name + ': missing documented example')
    print('GMSH_V2_HELP=PASS LANGUAGES=2 CURRENT_EXAMPLES=' + str(len(current)))


if __name__ == '__main__':
    main()
