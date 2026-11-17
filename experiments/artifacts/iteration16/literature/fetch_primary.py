import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent
PAPERS = [('2609.14858', 'v2'), ('2609.24972', 'v3'), ('2602.14670', 'v2'), ('2602.12670', 'v4')]

def fetch(item):
    identifier, version, kind = item
    url = f'https://arxiv.org/{kind}/{identifier}{version if kind == "html" else ""}'
    record = {'url': url, 'requested_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (primary-source research audit)'})
        with urllib.request.urlopen(request, timeout=35) as response:
            body = response.read()
            filename = f'{identifier}{version if kind == "html" else ""}_{kind}.html'
            (ROOT / filename).write_bytes(body)
            record.update(status=response.status, final_url=response.url, content_type=response.headers.get('Content-Type'), bytes=len(body), sha256=hashlib.sha256(body).hexdigest(), file=filename, response_headers=dict(response.headers))
    except Exception as error:
        record.update(error_type=type(error).__name__, error=str(error), saved_source=False)
    return record

if __name__ == '__main__':
    items = [(identifier, version, kind) for identifier, version in PAPERS for kind in ['abs', 'html']]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        records = list(executor.map(fetch, items))
    (ROOT / 'raw_fetch_receipts.json').write_text(json.dumps({'purpose': '原始响应归档尝试；HTTP成功不自动证明内容身份或完整性', 'records': records}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(records, ensure_ascii=False, indent=2))
