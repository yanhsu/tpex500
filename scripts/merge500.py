import json
FIELDS = ['code','name','industry','q1_gm','q1_om','q1_nm','q2_gm','q2_om','q2_nm','q1_eps','h1_eps','q2_eps','per','dividend','price']
def parse_num(s):
    s = s.strip()
    if s == '': return None
    try: return float(s)
    except ValueError: return None
seed_rows = {}
with open('/tmp/seed500.txt', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip('\n')
        if not line.strip(): continue
        parts = line.split('|')
        if len(parts) < len(FIELDS): parts = parts + [''] * (len(FIELDS) - len(parts))
        elif len(parts) > len(FIELDS): parts = parts[:len(FIELDS)]
        row = {}
        for k, v in zip(FIELDS, parts):
            row[k] = v if k in ('code','name','industry') else parse_num(v)
        seed_rows[row['code']] = row
fresh_prices = {}
try:
    with open('/tmp/fresh_prices.txt', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or '|' not in line: continue
            code, price_s = line.split('|', 1)
            p = parse_num(price_s)
            if p is not None: fresh_prices[code.strip()] = p
except FileNotFoundError: pass
refreshed = 0; fallback = 0; out = []
for code, row in seed_rows.items():
    price = fresh_prices.get(code)
    if price is not None: refreshed += 1
    else: price = row.get('price'); fallback += 1
    dividend = row.get('dividend')
    yield_pct = round(dividend / price * 100, 2) if (dividend is not None and price is not None and price > 0) else None
    def growth(k1, k2):
        v1, v2 = row.get(k1), row.get(k2)
        return round(v2 - v1, 2) if (v1 is not None and v2 is not None) else None
    out.append({'code': row['code'], 'name': row['name'], 'industry': row['industry'],
        'q1_gm': row['q1_gm'], 'q1_om': row['q1_om'], 'q1_nm': row['q1_nm'],
        'q2_gm': row['q2_gm'], 'q2_om': row['q2_om'], 'q2_nm': row['q2_nm'],
        'g_gm': growth('q1_gm','q2_gm'), 'g_om': growth('q1_om','q2_om'), 'g_nm': growth('q1_nm','q2_nm'),
        'q1_eps': row['q1_eps'], 'h1_eps': row['h1_eps'], 'q2_eps': row['q2_eps'],
        'per': row['per'], 'dividend': dividend, 'price': price, 'yield': yield_pct})
out.sort(key=lambda r: r['code'])
with open('/tmp/final_results_500.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False)
print(f'rows={len(out)} refreshed_price={refreshed} fallback_to_seed={fallback}')
