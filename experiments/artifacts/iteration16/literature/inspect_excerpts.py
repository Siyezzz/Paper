"""Produce bounded primary-source excerpts; not a complete paper or code audit."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json

class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
    def handle_data(self, data):
        self.parts.append(data)

root = Path(__file__).resolve().parent
terms = {
    '2609.14858v2_html.html': ['simulator', 'limitation'],
    '2609.24972v3_html.html': ['DomainGuard', 'cost gate'],
    '2602.14670v2_html.html': ['forbidden regions', 'admission'],
    '2602.12670v4_html.html': ['task.md', 'applicability', 'allowed_hosts'],
}
records = []
for filename, queries in terms.items():
    raw = (root / filename).read_bytes()
    parser = Text()
    parser.feed(raw.decode('utf-8'))
    text = ' '.join(' '.join(parser.parts).split())
    excerpts = []
    for query in queries:
        start = text.lower().find(query.lower())
        excerpts.append({'query': query, 'found': start >= 0,
                         'excerpt': text[max(0, start-220):start+1200] if start >= 0 else None})
    records.append({'file': filename, 'sha256': hashlib.sha256(raw).hexdigest(), 'excerpts': excerpts})
output = {'scope': 'First-match bounded excerpts, not exhaustive absence checks', 'records': records}
(root / 'inspected_excerpts.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
print(json.dumps(output, indent=2))
