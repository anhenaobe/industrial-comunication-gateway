"""Download only public manufacturer evidence; no CAD generation or qualification.

Run from repository root. Failed requests remain in the manifest, never as models.
PDF text/images used during review are temporary, not source-of-truth CAD.
"""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path('hardware/academic_rev1/libraries/sources/passives')
URLS = {
    'XAL40xx.pdf': 'https://www.coilcraft.com/getmedia/6adcb47d-8b55-416c-976e-1e22e0d2848c/xal4000.pdf',
    'TDK_COUT.html': 'https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C3225X7R1C156M250AB',
    'TDK_CIN.html': 'https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C5750X7R2A475K230KA',
}
for part in ['RC0603FR-076K49L', 'RC0603FR-072K49L', 'RC0603FR-07100KL',
             'RC0603FR-0743K2L', 'RC0603FR-0724K9L', 'RC0603FR-0710KL']:
    URLS[part + '.pdf'] = 'https://yageogroup.com/component-documentation/download/specsheet/' + part
for part in ['C0603C202J5GACTU', 'C0603C200J5GACTU']:
    URLS[part + '.pdf'] = 'https://search.kemet.com/component-documentation/download/specsheet/' + part


def acquire(item):
    name, url = item
    result = dict(file=name, url=url)
    try:
        with urllib.request.urlopen(url, timeout=25) as response:
            data = response.read()
            result['resolved_url'] = response.url
        if name.endswith('.pdf') and not data.startswith(b'%PDF'):
            raise ValueError('Response is not a PDF')
        (ROOT / name).write_bytes(data)
        result.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                      status='downloaded_not_CAD_qualified')
    except Exception as error:
        result.update(status='FAILED', error=str(error))
    return result


if __name__ == '__main__':
    ROOT.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(acquire, URLS.items()))
    (ROOT / 'acquisition_manifest_additional.json').write_text(
        json.dumps(results, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(results, indent=2))
