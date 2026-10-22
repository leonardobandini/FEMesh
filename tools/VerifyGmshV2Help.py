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
    entries = json.loads((HELP / 'assets' / 'examples.json').read_text(encoding='utf-8'))
    current = json.loads((HELP / 'assets' / 'new-ui-examples.json').read_text(encoding='utf-8'))
    if len(entries) != 24 or any(item['generated']['areas'] !=
                                item['generated']['quads'] + item['generated']['triangles'] for item in entries):
        raise ValueError('Missing or inconsistent historical Classic example metadata')
    if len(current) != 23 or len({item['id'] for item in current}) != 23:
        raise ValueError('Missing or duplicate SAP-verified New UI example')
    expected = {'nTEST001': True, 'nTEST003': False, 'nTEST010': True,
                'nTEST011': False, 'nTEST012': True, 'nTEST014': True, 'nTEST010-locked': False,
                'nTEST005': False, 'nTEST017': False, 'nTEST024': True,
                'nTEST007': True, 'nTEST008': True, 'nTEST013': False,
                'nTEST018': False, 'nTEST019': True, 'nTEST020': True,
                 'nTEST028': False, 'nTEST035': False,
                 'nTEST005-ogrid': True, 'nTEST006-ogrid': True,
                 'nTEST015-symmetry': True, 'nTEST025-ogrid': True,
                 'nTEST027-ogrid': True, 'nTEST034-symmetry': False}
    for item in entries:
        settings = item['actualGmshSettings']
        if (item['id'] not in expected or item['qualityPassed'] != expected[item['id']] or
                 settings['qualityTolerancePercent'] != 20 or
                 settings['preserveSelectedEdges'] != (item['id'] == 'nTEST010-locked') or
                 abs(settings['options']['Mesh.MeshSizeMin'] - item['maximumSize'] * .8) > 1e-8):
            raise ValueError('Incorrect quality report, minimum percentage or edge-lock setting: ' + item['id'])
        if item['id'].endswith(('-ogrid', '-symmetry')):
            if (item['oGrid'] != item['id'].endswith('-ogrid') or
                    item['exactSymmetry'] != item['id'].startswith(('nTEST006', 'nTEST015', 'nTEST025', 'nTEST027', 'nTEST034')) or
                    item['oGrid'] != bool(settings['oGrid']) or
                    item['exactSymmetry'] != bool(settings['exactSymmetry'])):
                raise ValueError('Feature flags differ from effective Gmsh settings: ' + item['id'])
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
    for name in ('index-it.html', 'index-en.html', 'legacy-it.html', 'legacy-en.html'):
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
        if name.startswith('index-'):
            additional = text.split('<section id="aggiuntive">', 1)[1].split('</section>', 1)[0]
            gmsh_tab = text.split('<section id="gmsh">', 1)[1].split('</section>', 1)[0]
            grid_name = 'Prefer regular (grid-aligned) mesh when possible' if name.endswith('-en.html') else 'Preferisci mesh regolari allineate alla griglia'
            if (any(option not in text for option in documented_options) or
                    any('<section id="' + section + '">' not in text for section in
                        ('transazione', 'unita', 'interfaccia', 'bordi', 'ricette', 'griglia-esempi')) or
                    grid_name not in additional or grid_name in gmsh_tab or
                    'preserveSelectedEdges=true' not in text.split('<section id="bordi">', 1)[1].split('</section>', 1)[0] or
                    'not exposed by New' in text or 'non è esposta dalla nuova UI' in text or
                    '2.0.26 · ' in text or '2.0.37 · ' in text):
                raise ValueError(name + ': incomplete or stale current-interface help')
            language = 'en' if name.endswith('-en.html') else 'it'
            if ('<section id="json">' in text or 'interface-v244-' in text or
                    re.search(r'SAP2000(?!/CSiBridge)', text) or
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
        for marker in ((('FEMesh version · 2.0.63' if name.endswith('-en.html') else 'Versione FEMesh · 2.0.63'), 'leonardo@csi-italia.eu', 'Mesh.MeshSizeMin', 'Mesh.Smoothing', 'Mesh.AlgorithmSwitchOnFailure',
                          'Mesh.QuadqsSizemapMethod', 'Mesh.RecombineNodeRepositioning',
                          'Mesh.RecombineOptimizeTopology',
                          'Prefer regular (grid-aligned) mesh when possible' if name.endswith('-en.html') else 'Preferisci mesh regolari allineate alla griglia',
                              'October 22, 2026' if name.endswith('-en.html') else '22 ottobre 2026',
                          'Additional options' if name.endswith('-en.html') else 'Opzioni aggiuntive',
                          'Transfer options' if name.endswith('-en.html') else 'Opzioni di trasferimento',
                          'Do not show this backup warning again' if name.endswith('-en.html') else 'Non mostrare più questo avviso sul backup',
                          'Do not show this Apply confirmation again' if name.endswith('-en.html') else 'Non mostrare più questa conferma di Applica',
                           'source areas remain visible' if name.endswith('-en.html') else 'aree originali restano visibili')
                       if name.startswith('index-') else
                       ('id="simmetria"', 'id="esempi-simmetria"', 'Mesh.MeshSizeMin',
                        'Distance', 'Threshold', 'FAST', 'Standard', 'O-grid', '🟢', '🟡', '🔴')):
            if marker not in text:
                raise ValueError(name + ': undocumented feature ' + marker)
        expected_cases = current if name.startswith('index-') else entries
        if any(item['id'] not in text for item in expected_cases):
            raise ValueError(name + ': missing documented example')
    print('GMSH_V2_HELP=PASS LANGUAGES=2 NEW_EXAMPLES=' + str(len(current)) +
          ' HISTORICAL_EXAMPLES=' + str(len(entries)))


if __name__ == '__main__':
    main()
