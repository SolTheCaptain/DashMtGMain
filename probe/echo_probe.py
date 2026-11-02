# Временная проба: муверы рынка Cardmarket, фойл/нефойл отдельно, с названием сета
import json, re, time, urllib.request, urllib.error

S3 = "https://downloads.s3.cardmarket.com/productCatalog/"
def get(u):
    with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "DashMtG/1.0", "Accept": "application/json"}), timeout=180) as r:
        return json.loads(r.read())
pg = get(S3 + "priceGuide/price_guide_1.json")
names = {p["idProduct"]: p["name"] for p in get(S3 + "productList/products_singles_1.json")["products"]}
BAD = re.compile(r"Token|Art Series|Filler|Emblem|Checklist|Oversized|^(Island|Swamp|Forest|Mountain|Plains)( |$)")

def movers(suf, up, n=10, mn=3):
    best = {}
    for g in pg["priceGuides"]:
        nm = names.get(g["idProduct"])
        if not nm or BAD.search(nm): continue
        a1, a7, a30, tr = (g.get(k + suf) for k in ("avg1", "avg7", "avg30", "trend"))
        if not (a1 and a7 and a30 and tr): continue
        if max(a30, tr) < mn or min(a30, a7, tr) < 0.25: continue
        x, y = a7 / a30, tr / a30
        v = min(x, y) if up else max(x, y)
        if (up and v <= 1) or (not up and v >= 1): continue
        if nm not in best or (v > best[nm]["v"] if up else v < best[nm]["v"]):
            best[nm] = {"v": v, "id": g["idProduct"], "name": nm, "avg30": a30, "avg7": a7, "trend": tr}
    return sorted(best.values(), key=lambda r: -r["v"] if up else r["v"])[:n]

out = {"createdAt": pg["createdAt"]}
for key, suf, up in (("up", "", True), ("down", "", False), ("up_foil", "-foil", True), ("down_foil", "-foil", False)):
    rows = movers(suf, up)
    for r in rows:
        try:
            c = get("https://api.scryfall.com/cards/cardmarket/%d" % r["id"])
            r["set"], r["set_code"] = c.get("set_name"), c.get("set", "").upper()
        except Exception as e:
            r["set"] = None
        time.sleep(0.12)
    out[key] = rows
with open("probe/result.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
# КОНЕЦ ФАЙЛА
