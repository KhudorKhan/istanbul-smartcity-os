"""Multimodal route planner: public transport, car/taxi and ferry options between Istanbul districts."""
import math
from typing import Any, Dict, List, Optional

from tools.route_geometry import car_geometry, ferry_geometry, transit_geometry

# Car and taxi estimates. Indicative values for 2026; update from the current UKOME taxi tariff and fuel prices.
ROAD_FACTOR = 1.35          # straight-line distance -> road distance
BOSPHORUS_DETOUR_KM = 6     # extra distance to reach a bridge or the tunnel
CITY_TRIP_KM = 10           # shorter trips use city streets instead of motorways
SPEED_FREE_KMH = 55         # free-flowing traffic
SPEED_PEAK_KMH = 24         # typical rush hour on D-100 / TEM
FUEL_L_PER_100KM = 7.5
FUEL_PRICE_TRY = 50.0
TAXI_START_TRY = 40.0
TAXI_PER_KM_TRY = 50.0

TRANSIT_FARE = {"ru": "27.50 TRY (с учетом aktarma)", "tr": "27.50 TRY (aktarma dahil)"}
MINUTES = {"ru": "мин", "tr": "dk"}

DISTRICTS = {
    "beylikduzu": {"name": "Beylikdüzü", "lat": 41.0015, "lon": 28.6419, "side": "eu", "aliases": ("beylikduzu", "бейликдюзю", "бейликдюзу")},
    "haramidere": {"name": "Haramidere", "lat": 41.0062, "lon": 28.6837, "side": "eu", "aliases": ("haramidere", "харамидере")},
    "esenyurt": {"name": "Esenyurt", "lat": 41.0343, "lon": 28.6801, "side": "eu", "aliases": ("esenyurt", "эсеньюрт", "есеньюрт")},
    "avcilar": {"name": "Avcılar", "lat": 40.9796, "lon": 28.7214, "side": "eu", "aliases": ("avcilar", "авджылар", "авджилар")},
    "bakirkoy": {"name": "Bakırköy", "lat": 40.9819, "lon": 28.8772, "side": "eu", "aliases": ("bakirkoy", "бакыркёй", "бакыркей")},
    "basaksehir": {"name": "Başakşehir", "lat": 41.0931, "lon": 28.8020, "side": "eu", "aliases": ("basaksehir", "башакшехир")},
    "eminonu": {"name": "Eminönü / Sultanahmet", "lat": 41.0170, "lon": 28.9700, "side": "eu",
                "aliases": ("eminonu", "sultanahmet", "fatih", "эминёню", "эминеню", "султанахмет", "фатих")},
    "karakoy": {"name": "Karaköy", "lat": 41.0256, "lon": 28.9744, "side": "eu", "aliases": ("karakoy", "каракёй", "каракей", "каракой")},
    "taksim": {"name": "Taksim", "lat": 41.0370, "lon": 28.9850, "side": "eu", "aliases": ("taksim", "beyoglu", "таксим", "бейоглу")},
    "sisli": {"name": "Şişli", "lat": 41.0602, "lon": 28.9877, "side": "eu", "aliases": ("sisli", "mecidiyekoy", "шишли", "меджидиекёй")},
    "besiktas": {"name": "Beşiktaş", "lat": 41.0422, "lon": 29.0067, "side": "eu", "aliases": ("besiktas", "бешикташ")},
    "airport": {"name": "İstanbul Havalimanı", "lat": 41.2620, "lon": 28.7420, "side": "eu",
                "aliases": ("havaliman", "airport", "аэропорт")},
    "kadikoy": {"name": "Kadıköy", "lat": 40.9910, "lon": 29.0270, "side": "as", "aliases": ("kadikoy", "кадыкёй", "кадикей", "кадыкей")},
    "uskudar": {"name": "Üsküdar", "lat": 41.0226, "lon": 29.0150, "side": "as", "aliases": ("uskudar", "ускюдар")},
    "atasehir": {"name": "Ataşehir", "lat": 40.9923, "lon": 29.1244, "side": "as", "aliases": ("atasehir", "аташехир")},
}

# Hand-checked public transport plans from the western districts along the Metrobüs line.
WEST_ORIGIN_OFFSET_MIN = {"beylikduzu": 0, "esenyurt": 5, "haramidere": -10, "avcilar": -15}
WEST_TRANSIT = {
    "taksim": {"minutes": 85, "legs": [("metrobus", "metrobus", "@entry", "mb_mecidiyekoy"), ("m2", "m2", "m2_sisli", "m2_taksim")], "steps": {
        "ru": ["Метробус от {origin} до Mecidiyeköy", "Пересадка на линию M2 на станции Şişli-Mecidiyeköy", "M2 до станции Taksim"],
        "tr": ["Metrobüs ile {origin} → Mecidiyeköy", "Şişli-Mecidiyeköy'de M2 hattına aktarma", "M2 ile Taksim istasyonuna"]}},
    "sisli": {"minutes": 75, "legs": [("metrobus", "metrobus", "@entry", "mb_mecidiyekoy")], "steps": {
        "ru": ["Метробус от {origin} до Mecidiyeköy без пересадок"],
        "tr": ["Metrobüs ile aktarmasız {origin} → Mecidiyeköy"]}},
    "karakoy": {"minutes": 85, "legs": [("metrobus", "metrobus", "@entry", "mb_cevizlibag"), ("t1", "t1", "t1_cevizlibag", "t1_karakoy")], "steps": {
        "ru": ["Метробус от {origin} до Cevizlibağ", "Пересадка на трамвай T1 (Kabataş – Bağcılar)", "T1 до остановки Karaköy через Sultanahmet и Eminönü"],
        "tr": ["Metrobüs ile {origin} → Cevizlibağ", "T1 tramvay hattına (Kabataş – Bağcılar) aktarma", "T1 ile Sultanahmet ve Eminönü üzerinden Karaköy durağına"]}},
    "eminonu": {"minutes": 80, "legs": [("metrobus", "metrobus", "@entry", "mb_zeytinburnu"), ("t1", "t1", "t1_zeytinburnu", "t1_eminonu")], "steps": {
        "ru": ["Метробус от {origin} до Zeytinburnu", "Пересадка на трамвай T1 (Kabataş – Bağcılar)", "T1 до остановок Sultanahmet / Eminönü"],
        "tr": ["Metrobüs ile {origin} → Zeytinburnu", "T1 tramvay hattına (Kabataş – Bağcılar) aktarma", "T1 ile Sultanahmet / Eminönü duraklarına"]}},
    "besiktas": {"minutes": 90, "legs": [("metrobus", "metrobus", "@entry", "mb_zincirlikuyu"), ("bus", "bus", "mb_zincirlikuyu", "bus_besiktas")], "steps": {
        "ru": ["Метробус от {origin} до Zincirlikuyu", "Автобус от Zincirlikuyu до Beşiktaş (около 15 мин)"],
        "tr": ["Metrobüs ile {origin} → Zincirlikuyu", "Zincirlikuyu'dan otobüsle Beşiktaş'a (yaklaşık 15 dk)"]}},
    "kadikoy": {"minutes": 105, "legs": [("metrobus", "metrobus", "@entry", "mb_sogutlucesme")], "steps": {
        "ru": ["Метробус от {origin} до конечной Söğütlüçeşme (через мост 15 Temmuz Şehitler)", "Söğütlüçeşme → центр Kadıköy: 10–15 мин пешком или автобусом"],
        "tr": ["Metrobüs ile {origin} → Söğütlüçeşme son durağı (15 Temmuz Şehitler Köprüsü üzerinden)", "Söğütlüçeşme → Kadıköy merkez: 10–15 dk yürüyüş veya otobüs"]}},
    "uskudar": {"minutes": 95, "legs": [("metrobus", "metrobus", "@entry", "mb_zeytinburnu"), ("t1", "t1", "t1_zeytinburnu", "t1_sirkeci"), ("marmaray", "marmaray", "mr_sirkeci", "mr_uskudar")], "steps": {
        "ru": ["Метробус от {origin} до Zeytinburnu", "Трамвай T1 до Sirkeci", "Marmaray от Sirkeci под Босфором до Üsküdar (1 станция)"],
        "tr": ["Metrobüs ile {origin} → Zeytinburnu", "T1 tramvay ile Sirkeci'ye", "Marmaray ile Sirkeci'den Boğaz altından Üsküdar'a (1 durak)"]}},
    "airport": {"minutes": 120, "legs": [("metrobus", "metrobus", "@entry", "mb_mecidiyekoy"), ("m2", "m2", "m2_sisli", "m2_gayrettepe"), ("m11", "m11", "m2_gayrettepe", "m11_airport")], "fare": {"ru": "27.50 TRY + доплата M11 по расстоянию", "tr": "27.50 TRY + mesafeye göre M11 farkı"}, "steps": {
        "ru": ["Метробус от {origin} до Mecidiyeköy", "M2 одна станция до Gayrettepe", "M11 Gayrettepe – İstanbul Havalimanı"],
        "tr": ["Metrobüs ile {origin} → Mecidiyeköy", "M2 ile bir durak Gayrettepe'ye", "M11 Gayrettepe – İstanbul Havalimanı"]}},
}

TEXT = {
    "ru": {
        "generic_steps": ["Метро, Метробус или трамвай по оптимальной схеме İBB с одной пересадкой",
                          "Точная схема и расписание — в приложении İstanbul Senin"],
        "generic_bosphorus": "Босфор пересекается на Marmaray или пароме",
        "roads_bosphorus": "D-100 (E-5) через мост 15 Temmuz Şehitler или TEM (O-2) через мост Fatih Sultan Mehmet",
        "roads_airport": "TEM (O-3) или платная O-7 (Kuzey Marmara Otoyolu)",
        "roads_default": "D-100 (E-5) или TEM (O-3)",
        "roads_city": "Городские улицы",
        "toll_bridges": "Мосты через Босфор — платный проезд (HGS)",
        "toll_tunnel": "Альтернатива: Avrasya Tüneli — платный тоннель под Босфором",
        "toll_o7": "O-7 (Kuzey Marmara Otoyolu) — платная автомагистраль (HGS)",
        "traffic": "В часы пик (07:30–10:00 и 17:00–20:00) трассы стабильно загружены; вне пика время ближе к нижней оценке.",
        "ferry_access_west": "Метробус до Zeytinburnu → трамвай T1 до Eminönü",
        "ferry_access": "Доберитесь до пристани {pier_from}",
        "ferry_ride": "Паром İBB Şehir Hatları {pier_from} – {pier_to} (около 20 мин по воде)",
        "ferry_last": "От пристани {pier_to} до {destination} — пешком или на общественном транспорте",
        "ferry_note": "Самый живописный способ пересечь Босфор и без пробок на мостах.",
    },
    "tr": {
        "generic_steps": ["İBB'nin en uygun planına göre tek aktarmalı metro, Metrobüs veya tramvay",
                          "Kesin güzergah ve sefer saatleri İstanbul Senin uygulamasında"],
        "generic_bosphorus": "Boğaz geçişi Marmaray veya vapurla",
        "roads_bosphorus": "15 Temmuz Şehitler Köprüsü üzerinden D-100 (E-5) veya Fatih Sultan Mehmet Köprüsü üzerinden TEM (O-2)",
        "roads_airport": "TEM (O-3) veya ücretli O-7 (Kuzey Marmara Otoyolu)",
        "roads_default": "D-100 (E-5) veya TEM (O-3)",
        "roads_city": "Şehir içi yollar",
        "toll_bridges": "Boğaz köprüleri ücretlidir (HGS)",
        "toll_tunnel": "Alternatif: Avrasya Tüneli — Boğaz altından ücretli geçiş",
        "toll_o7": "O-7 (Kuzey Marmara Otoyolu) ücretli otoyoldur (HGS)",
        "traffic": "Yoğun saatlerde (07:30–10:00 ve 17:00–20:00) yollar sürekli yoğundur; yoğunluk dışında süre alt tahmine yakındır.",
        "ferry_access_west": "Metrobüs ile Zeytinburnu → T1 tramvay ile Eminönü",
        "ferry_access": "{pier_from} iskelesine ulaşın",
        "ferry_ride": "İBB Şehir Hatları vapuru {pier_from} – {pier_to} (denizde yaklaşık 20 dk)",
        "ferry_last": "{pier_to} iskelesinden {destination} yönüne yürüyerek veya toplu taşımayla",
        "ferry_note": "Boğaz'ı geçmenin en manzaralı ve köprü trafiğinden bağımsız yolu.",
    }
}

FERRY_PIERS = {"kadikoy": "Kadıköy", "uskudar": "Üsküdar", "atasehir": "Kadıköy", "besiktas": "Beşiktaş"}


def _normalize(text: str) -> str:
    table = str.maketrans({"ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u", "̇": None})
    return (text or "").lower().translate(table)


def find_district(text: str) -> Optional[str]:
    normalized = _normalize(text)
    for key, district in DISTRICTS.items():
        if any(alias in normalized for alias in district["aliases"]):
            return key
    return None


def _haversine_km(a: Dict[str, Any], b: Dict[str, Any]) -> float:
    lat1, lon1, lat2, lon2 = map(math.radians, (a["lat"], a["lon"], b["lat"], b["lon"]))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(h))


def _money(value: float) -> str:
    return f"≈ {int(round(value, -1)):,} TRY".replace(",", " ")


def _car_option(origin_key: str, dest_key: str, crosses: bool, lang: str) -> Dict[str, Any]:
    geometry = car_geometry(DISTRICTS[origin_key], DISTRICTS[dest_key], origin_key, dest_key, crosses)
    text = TEXT[lang]
    km = _haversine_km(DISTRICTS[origin_key], DISTRICTS[dest_key]) * ROAD_FACTOR + (BOSPHORUS_DETOUR_KM if crosses else 0)
    if crosses:
        roads, tolls = text["roads_bosphorus"], [text["toll_bridges"], text["toll_tunnel"]]
    elif dest_key == "airport" or origin_key == "airport":
        roads, tolls = text["roads_airport"], [text["toll_o7"]]
    elif km < CITY_TRIP_KM:
        roads, tolls = text["roads_city"], []
    else:
        roads, tolls = text["roads_default"], []
    return {
        "mode": "car",
        "distanceKm": round(km),
        "durationFree": f"{max(5, round(km / SPEED_FREE_KMH * 60))} {MINUTES[lang]}",
        "durationPeak": f"{max(10, round(km / SPEED_PEAK_KMH * 60))} {MINUTES[lang]}",
        "peakMinutes": round(km / SPEED_PEAK_KMH * 60),
        "fuelCost": _money(km * FUEL_L_PER_100KM / 100 * FUEL_PRICE_TRY),
        "taxiFare": _money(TAXI_START_TRY + km * TAXI_PER_KM_TRY),
        "roads": roads,
        "tolls": tolls,
        "traffic": text["traffic"],
        **geometry,
    }


def _transit_option(origin_key: Optional[str], dest_key: Optional[str], origin_name: str,
                    crosses: bool, lang: str) -> Dict[str, Any]:
    plan = WEST_TRANSIT.get(dest_key) if origin_key in WEST_ORIGIN_OFFSET_MIN else None
    if plan:
        minutes = plan["minutes"] + WEST_ORIGIN_OFFSET_MIN[origin_key]
        fare = plan.get("fare", TRANSIT_FARE)[lang]
        steps = [step.format(origin=origin_name) for step in plan["steps"][lang]]
    else:
        minutes = None
        if origin_key and dest_key:
            road_km = _haversine_km(DISTRICTS[origin_key], DISTRICTS[dest_key]) * ROAD_FACTOR
            minutes = round(road_km / 20 * 60 + 10)
        fare = TRANSIT_FARE[lang]
        steps = list(TEXT[lang]["generic_steps"])
        if crosses:
            steps.insert(1, TEXT[lang]["generic_bosphorus"])
    geometry = {}
    if origin_key and dest_key:
        geometry = transit_geometry(DISTRICTS[origin_key], DISTRICTS[dest_key], origin_key, (plan or {}).get("legs"))
    return {
        "mode": "transit",
        "minutes": minutes,
        "duration": f"≈ {minutes} {MINUTES[lang]}" if minutes else "—",
        "fare": fare,
        "steps": steps,
        **geometry,
    }


def _ferry_option(origin_key: str, dest_key: str, transit_minutes: Optional[int], destination: str, lang: str) -> Dict[str, Any]:
    text = TEXT[lang]
    to_asia = DISTRICTS[dest_key]["side"] == "as"
    asian_pier = FERRY_PIERS.get(dest_key if to_asia else origin_key, "Kadıköy")
    european_pier = FERRY_PIERS.get(origin_key if to_asia else dest_key, "Eminönü")
    pier_from, pier_to = (european_pier, asian_pier) if to_asia else (asian_pier, european_pier)
    access = text["ferry_access_west"] if origin_key in WEST_ORIGIN_OFFSET_MIN and pier_from == "Eminönü" \
        else text["ferry_access"].format(pier_from=pier_from)
    minutes = (transit_minutes or 60) + 5
    steps = [access, text["ferry_ride"].format(pier_from=pier_from, pier_to=pier_to)]
    if pier_to not in destination:
        steps.append(text["ferry_last"].format(pier_to=pier_to, destination=destination))
    return {
        "mode": "ferry",
        "minutes": minutes,
        "duration": f"≈ {minutes} {MINUTES[lang]}",
        "fare": TRANSIT_FARE[lang],
        "steps": steps,
        "note": text["ferry_note"],
        **ferry_geometry(DISTRICTS[origin_key], DISTRICTS[dest_key], origin_key, pier_from, pier_to),
    }


def plan_route(origin: str, destination: str, language: str = "ru") -> Dict[str, Any]:
    lang = "tr" if language == "tr" else "ru"
    origin_key, dest_key = find_district(origin), find_district(destination)
    origin_name = DISTRICTS[origin_key]["name"] if origin_key else origin.strip().title()
    dest_name = DISTRICTS[dest_key]["name"] if dest_key else destination.strip().title()
    crosses = bool(origin_key and dest_key and DISTRICTS[origin_key]["side"] != DISTRICTS[dest_key]["side"])

    transit = _transit_option(origin_key, dest_key, origin_name, crosses, lang)
    options: List[Dict[str, Any]] = []
    car = _car_option(origin_key, dest_key, crosses, lang) if origin_key and dest_key and origin_key != dest_key else None
    if car:
        options.append(car)
    options.append(transit)
    if crosses:
        options.append(_ferry_option(origin_key, dest_key, transit["minutes"], dest_name, lang))

    recommended = "transit"
    if car and transit["minutes"] and car["peakMinutes"] < transit["minutes"]:
        recommended = "car"

    return {
        "origin": origin_name,
        "destination": dest_name,
        "crossesBosphorus": crosses,
        "recommended": recommended,
        "options": options,
        "duration": transit["duration"],
        "fare": transit["fare"],
        "steps": transit["steps"],
        "source": "İBB TUHİM Toplu Ulaşım Ağı (2026)",
    }
