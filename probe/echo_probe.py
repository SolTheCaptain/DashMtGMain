# Временная проба EchoMTG: ищем готовые муверы + свежая история 4 сетов
import json, time, urllib.request, urllib.error

BASE = "https://api.echomtg.com/api/"
def raw(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        return 0, repr(e)
def get(path):
    for _ in range(3):
        c, b = raw(path)
        try: return json.loads(b)
        except Exception: time.sleep(2)
    return {}

out = {"guesses": {}, "items": []}
for p in ["data/top_movers/", "data/topmovers/", "data/market_movers/", "data/gainers/", "data/losers/",
          "data/price_changes/", "data/changes/", "data/popular/", "data/hot/", "data/biggest_movers/",
          "market/movers/", "data/item_movers/", "data/set_movers/?set_code=FRA", "data/spikes/",
          "data/watchlist/", "data/trending_items/", "data/most_valuable/"]:
    c, b = raw(p)
    out["guesses"][p] = [c, b[:400]]
for code in ("FRA", "FRC", "MSH", "MSC"):
    for it in get("data/set/?set_code=" + code).get("set", {}).get("items", []):
        h = get("data/item_history/?emid=%s" % it["emid"]).get("data") or {}
        out["items"].append({"set": code, "emid": it["emid"], "name": it["name"],
                             "date": h.get("date"), "regular": h.get("regular"), "foil": h.get("foil")})
        time.sleep(0.15)
with open("probe/result.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False)
# КОНЕЦ ФАЙЛА
