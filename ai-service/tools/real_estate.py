"""Rental listing showcase: sample listings per district plus links to the live sahibinden.com search.

The listings are illustrative examples, not real offers. Every card links to the real sahibinden.com
search for the same district and room layout, where the user sees current listings.
"""
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

from tools.transport import _normalize, find_district

SAHIBINDEN_BASE = "https://www.sahibinden.com/kiralik-daire"
# Room-layout filter codes confirmed on sahibinden.com search pages; other layouts fall back to a text query.
ROOM_FILTER_CODES = {"1+0": "38472", "1+1": "38473", "3+1": "38474"}

DISTRICT_SLUGS = {"beylikduzu": "istanbul-beylikduzu", "kadikoy": "istanbul-kadikoy", "sisli": "istanbul-sisli", "besiktas": "istanbul-besiktas"}
DISTRICT_NAMES = {"beylikduzu": "Beylikdüzü", "kadikoy": "Kadıköy", "sisli": "Şişli", "besiktas": "Beşiktaş"}

# (mahalle, verified sahibinden neighbourhood slug or None, kind, area m², floor, aidat TRY, transit, price factor, features)
LISTINGS = {
    "beylikduzu": [
        ("Adnan Kahveci", None, "Site İçi Daire", 110, "4. Kat", 1200, "Metrobüs · 4 dk yürüme", 0.85, ["Havuz", "Güvenlik", "Otopark"]),
        ("Barış", None, "Rezidans", 120, "7. Kat", 2100, "Metrobüs · 8 dk yürüme", 0.95, ["Güvenlik", "Spor salonu"]),
        ("Yakuplu", None, "Daire", 95, "2. Kat", 450, "Metrobüs · 12 dk yürüme", 0.70, ["Sahile yakın"]),
        ("Cumhuriyet", None, "Site İçi Daire", 75, "Yüksek Giriş", 900, "Metrobüs · 6 dk yürüme", 0.60, ["Eşyalı", "Güvenlik"]),
    ],
    "kadikoy": [
        ("Caferağa (Moda)", "istanbul-kadikoy-caferaga", "Daire", 85, "3. Kat", 600, "M4 Kadıköy · 7 dk yürüme", 0.95, ["Sahile yakın"]),
        ("Göztepe", None, "Site İçi Daire", 105, "5. Kat", 1500, "Marmaray Göztepe · 5 dk yürüme", 0.90, ["Güvenlik", "Otopark"]),
        ("Koşuyolu", None, "Daire", 95, "1. Kat", 500, "M4 Acıbadem · 8 dk yürüme", 0.85, ["Bahçe"]),
        ("Fenerbahçe", None, "Daire", 120, "2. Kat", 800, "Marmaray Feneryolu · 6 dk yürüme", 1.00, ["Balkon", "Asansör"]),
    ],
    "sisli": [
        ("Mecidiyeköy", None, "Rezidans", 75, "12. Kat", 2400, "M2 Şişli-Mecidiyeköy · 4 dk yürüme", 0.90, ["Güvenlik", "Spor salonu"]),
        ("Esentepe", "istanbul-sisli-esentepe", "Rezidans", 90, "9. Kat", 2800, "M2 Gayrettepe · 6 dk yürüme", 0.95, ["Concierge", "Otopark"]),
        ("Fulya", None, "Daire", 85, "3. Kat", 700, "Metrobüs Mecidiyeköy · 10 dk yürüme", 0.85, ["Asansör"]),
        ("Teşvikiye (Nişantaşı)", None, "Daire", 110, "4. Kat", 1100, "M2 Osmanbey · 6 dk yürüme", 1.00, ["Yüksek tavan", "Asansör"]),
    ],
    "besiktas": [
        ("Levent", None, "Rezidans", 80, "15. Kat", 2600, "M2 Levent · 5 dk yürüme", 0.95, ["Güvenlik", "Spor salonu"]),
        ("Etiler", None, "Site İçi Daire", 115, "3. Kat", 1800, "M6 Etiler · 4 dk yürüme", 1.00, ["Otopark", "Güvenlik"]),
        ("Ortaköy", None, "Daire", 90, "2. Kat", 650, "Otobüs · Ortaköy durağı 2 dk", 0.90, ["Boğaz'a yakın"]),
        ("Abbasağa", None, "Daire", 85, "Bahçe Katı", 400, "Beşiktaş iskelesi · 10 dk yürüme", 0.80, ["Bahçe"]),
    ],
}

MAHALLE_ALIASES = {
    "adnan kahveci": "beylikduzu", "yakuplu": "beylikduzu",
    "moda": "kadikoy", "caferaga": "kadikoy", "goztepe": "kadikoy", "kosuyolu": "kadikoy", "fenerbahce": "kadikoy",
    "мода": "kadikoy", "гёзтепе": "kadikoy",
    "mecidiyekoy": "sisli", "esentepe": "sisli", "fulya": "sisli", "nisantasi": "sisli", "tesvikiye": "sisli", "нишанташи": "sisli",
    "levent": "besiktas", "etiler": "besiktas", "ortakoy": "besiktas", "abbasaga": "besiktas", "левент": "besiktas", "этилер": "besiktas",
}

TEXT = {
    "ru": {"period": "/ мес", "ikamet": "Статус mahalle для ВНЖ: проверьте на e-ikamet.goc.gov.tr",
           "source": "Демо-подборка İBB CBS · актуальные объявления на sahibinden.com"},
    "tr": {"period": "/ ay", "ikamet": "İkamet için mahalle durumunu e-ikamet.goc.gov.tr üzerinden kontrol edin",
           "source": "İBB CBS örnek seçki · güncel ilanlar sahibinden.com'da"},
}


def _district_key(location: str) -> Optional[str]:
    normalized = _normalize(location)
    for alias, key in MAHALLE_ALIASES.items():
        if alias in normalized:
            return key
    key = find_district(location)
    return key if key in LISTINGS else None


def _search_url(path: str, rooms: str, extra_text: str = "") -> str:
    params: Dict[str, str] = {}
    if rooms in ROOM_FILTER_CODES:
        params["a20"] = ROOM_FILTER_CODES[rooms]
        if extra_text:
            params["query_text"] = extra_text
    else:
        params["query_text"] = " ".join(part for part in (rooms, extra_text) if part)
    return f"{SAHIBINDEN_BASE}/{path}?{urlencode(params)}"


def _round_price(value: float) -> int:
    return int(round(value / 500.0)) * 500


def search_listings(location: str, max_budget_try: float, rooms: str, language: str = "ru") -> Dict[str, Any]:
    lang = "tr" if language == "tr" else "ru"
    text = TEXT[lang]
    rooms = (rooms or "2+1").strip()
    key = _district_key(location)

    items: List[Dict[str, Any]] = []
    if key:
        district_name = DISTRICT_NAMES[key]
        for index, (mahalle, slug, kind, area, floor, aidat, transit, factor, features) in enumerate(LISTINGS[key], start=1):
            items.append({
                "id": f"demo-{key}-{index:02d}",
                "title": f"{rooms} {kind}, {district_name} {mahalle}",
                "mahalle": mahalle,
                "price": _round_price(max_budget_try * factor),
                "currency": "TRY",
                "period": text["period"],
                "rooms": rooms,
                "area": f"{area} m²",
                "floor": floor,
                "aidat": f"{aidat:,} TRY".replace(",", " "),
                "transit": transit,
                "features": features,
                "ikamet_status": text["ikamet"],
                "url": _search_url(slug, rooms) if slug else _search_url(DISTRICT_SLUGS[key], rooms, mahalle.split(" (")[0]),
                "sample": True,
            })
        search_url = _search_url(DISTRICT_SLUGS[key], rooms)
        location_name = district_name
    else:
        location_name = location.strip().title()
        search_url = _search_url("istanbul", rooms, location_name)

    return {
        "location": location_name,
        "rooms": rooms,
        "items": items,
        "searchUrl": search_url,
        "source": text["source"],
    }
