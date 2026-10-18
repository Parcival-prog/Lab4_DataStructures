"""Engineering Test Data Organizer"""
from collections import Counter, defaultdict

CATEGORIES = ["TEMPERATURE", "VOLTAGE", "CURRENT", "PRESSURE", "SPEED"]

LAST_NAME = "CANALES"
SEED_NUM = 7
FAVORITE_ARTIST = "BRYAN_ADAMS"

SOURCES = [f"{LAST_NAME}_T{i}" for i in range(1, 6)]


def make_value(s_idx, c_idx, k=0):
    """Value from SEED_NUM and the character position/code of FAVORITE_ARTIST."""
    pos = (s_idx + c_idx + k) % len(FAVORITE_ARTIST)
    ch = FAVORITE_ARTIST[pos]
    raw = SEED_NUM * (s_idx + 1) + ord(ch) * (c_idx + 1) + (pos + 1) * (k + 1)
    return round(raw % 100 + (pos + 1) / 10, 2)


records = [(src, cat, make_value(i, j))
           for i, src in enumerate(SOURCES) for j, cat in enumerate(CATEGORIES)]
records.append(records[0])                      
for i, src in enumerate(SOURCES[:3]):           
    for j in (0, 1):                             
        for k in (1, 2):
            records.append((src, CATEGORIES[j], make_value(i, j, k)))

organized = defaultdict(lambda: defaultdict(list))
for src, cat, val in records:
    organized[src][cat].append(val)

pair_counts = Counter((s, c) for s, c, _ in records)
repeated_pairs = {p: n for p, n in pair_counts.items() if n > 1}
record_counts = Counter(records)
repeated_records = {r: n for r, n in record_counts.items() if n > 1}
distinct_records = set(records)
distinct_values = sorted({v for _, _, v in records})

by_cat = defaultdict(list)
for _, cat, val in records:
    by_cat[cat].append(val)
cat_summary = {c: {"count": len(v), "min": min(v), "max": max(v),
                   "mean": round(sum(v) / len(v), 2), "total": round(sum(v), 2)}
               for c, v in by_cat.items()}
src_summary = {s: {"count": sum(len(v) for v in cats.values()),
                   "total": round(sum(sum(v) for v in cats.values()), 2)}
               for s, cats in organized.items()}

cats_by_mean = sorted(cat_summary.items(), key=lambda x: x[1]["mean"], reverse=True)
srcs_by_total = sorted(src_summary.items(), key=lambda x: x[1]["total"], reverse=True)
sorted_records = sorted(records, key=lambda r: (r[0], r[1], r[2]))


def line(title):
    print("\n" + "=" * 60 + f"\n{title}\n" + "=" * 60)


line("1. GENERATED TEST DATA")
print(f"{'No.':<5}{'SOURCE':<18}{'CATEGORY':<14}VALUE")
for n, (s, c, v) in enumerate(records, 1):
    print(f"{n:<5}{s:<18}{c:<14}{v}")

line("2. ORGANIZED TEST DATA (by source and category)")
for s in SOURCES:
    print(s)
    for c, vals in organized[s].items():
        print(f"   {c:<14}{vals}")

line("3. REPEATED / DISTINCT DATA")
print("Repeated source/category pairs:")
for (s, c), n in repeated_pairs.items():
    print(f"   {s} - {c}: {n} records")
print("Exact repeated records:")
for (s, c, v), n in repeated_records.items():
    print(f"   {s}, {c}, {v}: appears {n} times")
print(f"Total records: {len(records)} | Distinct records: {len(distinct_records)}")
print(f"Distinct sources: {len({r[0] for r in records})} | "
      f"Distinct categories: {len({r[1] for r in records})}")
print(f"Distinct values ({len(distinct_values)}): {distinct_values}")

line("4. NUMERICAL AND CATEGORICAL SUMMARIES")
print(f"{'CATEGORY':<14}{'COUNT':<7}{'MIN':<8}{'MAX':<8}{'MEAN':<8}TOTAL")
for c in CATEGORIES:
    d = cat_summary[c]
    print(f"{c:<14}{d['count']:<7}{d['min']:<8}{d['max']:<8}{d['mean']:<8}{d['total']}")
print(f"\n{'SOURCE':<18}{'COUNT':<7}TOTAL")
for s in SOURCES:
    print(f"{s:<18}{src_summary[s]['count']:<7}{src_summary[s]['total']}")

line("5. PROCESSED RESULTS")
print("Highest value :", max(records, key=lambda r: r[2]))
print("Lowest value  :", min(records, key=lambda r: r[2]))
print("Overall mean  :", round(sum(r[2] for r in records) / len(records), 2))
multi = [(s, c) for s, cats in organized.items() for c, v in cats.items() if len(v) > 1]
print("Categories with multiple measurements:", sorted({c for _, c in multi}))

line("6. ORDERED RESULTS")
print("Categories ranked by mean (high to low):")
for rank, (c, d) in enumerate(cats_by_mean, 1):
    print(f"   {rank}. {c:<14}{d['mean']}")
print("Sources ranked by total (high to low):")
for rank, (s, d) in enumerate(srcs_by_total, 1):
    print(f"   {rank}. {s:<18}{d['total']}")
print("Records sorted by source, category, value:")
for s, c, v in sorted_records:
    print(f"   {s:<18}{c:<14}{v}")

line("7. FINAL SUMMARY")
print(f"Student inputs  : {LAST_NAME}, seed {SEED_NUM}, artist {FAVORITE_ARTIST}")
print(f"Sources         : {len(SOURCES)} | Categories: {len(CATEGORIES)}")
print(f"Total records   : {len(records)} ({len(distinct_records)} distinct, "
      f"{len(records) - len(distinct_records)} repeated)")
print(f"Top category    : {cats_by_mean[0][0]} (mean {cats_by_mean[0][1]['mean']})")
print(f"Top source      : {srcs_by_total[0][0]} (total {srcs_by_total[0][1]['total']})")
print(f"Value range     : {distinct_values[0]} to {distinct_values[-1]}")