from collections import Counter, defaultdict

LAST_NAME, SEED_NUM, ARTIST = "CANALES", 7, "BRYANADAMS"
SUBJECTS = ["PROGRAMMING", "MATHEMATICS", "ELECTRONICS", "PHYSICS", "ENGLISH"]
STUDENTS = [f"{LAST_NAME}_S{i}" for i in range(1, 6)]

def category(s):
    return "Excellent" if s >= 90 else "Good" if s >= 80 else "Fair" if s >= 75 else "Poor"

records = [[st, sub, (SEED_NUM * (i + 1) + ord(ARTIST[(i + j) % len(ARTIST)]) * (j + 1)) % 51 + 50]
           for i, st in enumerate(STUDENTS) for j, sub in enumerate(SUBJECTS)]
records.append(list(records[0]))      
records[-2][2] = None                 

print("1. GENERATED RECORDS")
for r in records: print(r)
data = defaultdict(dict)
for st, sub, sc in records: data[st][sub] = sc
print("\n2. ORGANIZED DATA")
for st, subs in data.items(): print(st, subs)

print("\n3. REPEATED/INCOMPLETE")
print("Repeated  :", [k for k, n in Counter(map(tuple, records)).items() if n > 1])
print("Incomplete:", [r for r in records if r[2] is None])

valid = [r for r in records if r[2] is not None]
print("\n4. PERFORMANCE CATEGORIES")
for st, sub, sc in valid: print(st, sub, sc, category(sc))

unique = {(st, sub): sc for st, sub, sc in valid}
by_st, by_sub = defaultdict(list), defaultdict(list)
for (st, sub), sc in unique.items():
    by_st[st].append(sc); by_sub[sub].append(sc)
avg = lambda v: round(sum(v) / len(v), 2)
print("\n5. SUMMARIES")
for st, v in by_st.items(): print(st, "avg:", avg(v), "highest:", max(v), "lowest:", min(v))
for sub, v in by_sub.items(): print(sub, "avg:", avg(v), "highest:", max(v), "lowest:", min(v))

print("\n6. ORDERED RESULTS")
print("Students by average:", sorted(((avg(v), s) for s, v in by_st.items()), reverse=True))
print("Subjects by average:", sorted(((avg(v), s) for s, v in by_sub.items()), reverse=True))

cats = Counter(category(sc) for sc in unique.values())
print("\n7. FINAL STUDENT PERFORMANCE REPORT")
print("Total records:", len(records), "| Valid unique:", len(unique), "| Repeated: 1 | Incomplete: 1")
print("Category counts:", dict(cats))
print("Class average:", avg(list(unique.values())))