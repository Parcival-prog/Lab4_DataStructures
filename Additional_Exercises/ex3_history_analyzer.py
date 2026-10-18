from collections import Counter, defaultdict

LAST_NAME, SEED_NUM, ARTIST = "CANALES", 7, "BRYANADAMS"
CUSTOMERS = [f"{LAST_NAME}_C{i}" for i in range(1, 6)]
PRICES = {"NOTEBOOK": 50, "PEN": 15, "USB": 350, "HEADPHONES": 800, "CALCULATOR": 600}
PRODUCTS = list(PRICES)

# 1. Generate transactions: (customer, product, quantity, price)
def qty(i, j):
    return (SEED_NUM * (i + 1) + ord(ARTIST[(i + j) % len(ARTIST)]) * (j + 1)) % 9 + 1

records = [(c, PRODUCTS[j % 5], qty(i, j), PRICES[PRODUCTS[j % 5]])
           for i, c in enumerate(CUSTOMERS) for j in (i, i + 1)]
records.append(records[0])            # repeated customer-product purchase

print("1. GENERATED TRANSACTION RECORDS")
for r in records: print(r)

# 2. Organize by customer and product
data = defaultdict(list)
for c, p, q, pr in records: data[c].append((p, q, q * pr))
print("\n2. ORGANIZED TRANSACTION DATA")
for c, t in data.items(): print(c, t)

# 4 (values). Total value per record and overall
values = [q * pr for _, _, q, pr in records]
total = sum(values)

# 3. Repeated / distinct
pairs = Counter((c, p) for c, p, _, _ in records)
print("\n3. REPEATED/DISTINCT TRANSACTIONS")
print("Repeated purchases :", [k for k, n in pairs.items() if n > 1])
print("Distinct customers :", len({r[0] for r in records}))
print("Distinct products  :", len({r[1] for r in records}))
print("Distinct purchases :", len(pairs))

print("\n4. TRANSACTION VALUES")
for r, v in zip(records, values): print(r[0], r[1], "value:", v)
print("Overall value:", total)

# 5 & 6. Summaries
by_c, by_p = defaultdict(lambda: [0, 0]), defaultdict(lambda: [0, 0])
for c, p, q, pr in records:
    for d, k in ((by_c, c), (by_p, p)):
        d[k][0] += q; d[k][1] += q * pr
print("\n5. CUSTOMER SUMMARIES (quantity, value)")
for c, v in by_c.items(): print(c, v)
print("\n6. PRODUCT SUMMARIES (quantity, value)")
for p, v in by_p.items(): print(p, v)

# 7. Ordered results
print("\n7. ORDERED RESULTS")
print("Customers by value:", sorted(((v[1], c) for c, v in by_c.items()), reverse=True))
print("Products by value :", sorted(((v[1], p) for p, v in by_p.items()), reverse=True))

# 8. Overall summary
top_c = max(by_c, key=lambda c: by_c[c][1])
top_p = max(by_p, key=lambda p: by_p[p][1])
print("\n8. FINAL CONSOLIDATED TRANSACTION REPORT")
print("Total transactions:", len(records), "| Repeated:", len(records) - len(pairs))
print("Total quantity:", sum(r[2] for r in records), "| Total value:", total)
print("Top customer:", top_c, "| Top product:", top_p)
print("Average transaction value:", round(total / len(records), 2))