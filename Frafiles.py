# generate_dummy_claims.py
import json, os

# Hardcoded 12 demo villagers (3 for each of 4 villages)
villagers = [
    {"name": "Ramesh", "village": "Arepally", "lat": 17.941, "lng": 79.589, "area_ha": 1.8, "status": "pending", "doc": "docs/ramesh_arepally.pdf"},
    {"name": "Lakshmi", "village": "Arepally", "lat": 17.943, "lng": 79.591, "area_ha": 2.2, "status": "verified", "doc": "docs/lakshmi_arepally.pdf"},
    {"name": "Sita", "village": "Arepally", "lat": 17.945, "lng": 79.593, "area_ha": 1.5, "status": "rejected", "doc": "docs/sita_arepally.pdf"},

    {"name": "Arjun", "village": "Damera", "lat": 17.999, "lng": 79.567, "area_ha": 2.9, "status": "verified", "doc": "docs/arjun_damera.pdf"},
    {"name": "Bheema", "village": "Damera", "lat": 18.003, "lng": 79.562, "area_ha": 1.2, "status": "pending", "doc": "docs/bheema_damera.pdf"},
    {"name": "Sundari", "village": "Damera", "lat": 18.005, "lng": 79.565, "area_ha": 3.5, "status": "rejected", "doc": "docs/sundari_damera.pdf"},

    {"name": "Raju", "village": "Oglapur", "lat": 17.971, "lng": 79.710, "area_ha": 2.1, "status": "verified", "doc": "docs/raju_oglapur.pdf"},
    {"name": "Kavya", "village": "Oglapur", "lat": 17.975, "lng": 79.711, "area_ha": 2.4, "status": "pending", "doc": "docs/kavya_oglapur.pdf"},
    {"name": "Lalitha", "village": "Oglapur", "lat": 17.973, "lng": 79.709, "area_ha": 1.7, "status": "rejected", "doc": "docs/lalitha_oglapur.pdf"},

    {"name": "Bheema Rao", "village": "Oorugonda", "lat": 18.047, "lng": 79.628, "area_ha": 2.0, "status": "pending", "doc": "docs/bheemarao_oorugonda.pdf"},
    {"name": "Sita Bai", "village": "Oorugonda", "lat": 18.048, "lng": 79.627, "area_ha": 3.3, "status": "verified", "doc": "docs/sitabai_oorugonda.pdf"},
    {"name": "Ramesh Koya", "village": "Oorugonda", "lat": 18.046, "lng": 79.629, "area_ha": 1.9, "status": "rejected", "doc": "docs/rameshkoya_oorugonda.pdf"},
]

claims = []
for v in villagers:
    claims.append({
        "person_name": v["name"],
        "village": v["village"],
        "state": "Telangana",
        "coordinates": {"lat": v["lat"], "lng": v["lng"]},
        "area_ha": v["area_ha"],
        "status": v["status"],
        "doc": v["doc"]
    })

# Save JSON file
os.makedirs("data", exist_ok=True)
with open("data/sample_claims.json", "w", encoding="utf-8") as f:
    json.dump(claims, f, ensure_ascii=False, indent=2)

print("✅ sample_claims.json created with 12 villagers (area in hectares) in data/")
