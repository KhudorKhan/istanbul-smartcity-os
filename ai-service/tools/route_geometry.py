"""Schematic map geometry for route options: real transit corridors with approximate station coordinates."""
import math
from typing import Any, Dict, List, Optional, Sequence, Tuple

# name, lat, lon — approximate positions, accurate enough for a city-scale schematic map
POINTS: Dict[str, Tuple[str, float, float]] = {
    # Metrobüs along D-100 (E-5), west -> east
    "mb_beylikduzu": ("Beylikdüzü", 41.0010, 28.6430),
    "mb_haramidere": ("Haramidere", 40.9990, 28.6800),
    "mb_avcilar": ("Avcılar", 40.9840, 28.7220),
    "mb_kucukcekmece": ("Küçükçekmece", 40.9930, 28.7700),
    "mb_sirinevler": ("Şirinevler", 40.9930, 28.8450),
    "mb_incirli": ("İncirli", 40.9960, 28.8720),
    "mb_zeytinburnu": ("Zeytinburnu", 41.0010, 28.9050),
    "mb_cevizlibag": ("Cevizlibağ", 41.0150, 28.9150),
    "mb_topkapi": ("Topkapı", 41.0200, 28.9230),
    "mb_edirnekapi": ("Edirnekapı", 41.0330, 28.9370),
    "mb_okmeydani": ("Okmeydanı", 41.0500, 28.9550),
    "mb_caglayan": ("Çağlayan", 41.0650, 28.9800),
    "mb_mecidiyekoy": ("Mecidiyeköy", 41.0680, 28.9950),
    "mb_zincirlikuyu": ("Zincirlikuyu", 41.0690, 29.0120),
    "bridge_eu": ("15 Temmuz Şehitler Köprüsü", 41.0475, 29.0272),
    "bridge_as": ("Beylerbeyi", 41.0440, 29.0410),
    "mb_altunizade": ("Altunizade", 41.0220, 29.0450),
    "mb_sogutlucesme": ("Söğütlüçeşme", 40.9950, 29.0370),
    # T1 Kabataş – Bağcılar
    "t1_zeytinburnu": ("Zeytinburnu", 41.0010, 28.9050),
    "t1_cevizlibag": ("Cevizlibağ", 41.0150, 28.9150),
    "t1_topkapi": ("Topkapı", 41.0125, 28.9300),
    "t1_aksaray": ("Aksaray", 41.0080, 28.9510),
    "t1_beyazit": ("Beyazıt", 41.0100, 28.9640),
    "t1_sultanahmet": ("Sultanahmet", 41.0060, 28.9770),
    "t1_sirkeci": ("Sirkeci", 41.0150, 28.9770),
    "t1_eminonu": ("Eminönü", 41.0170, 28.9720),
    "t1_karakoy": ("Karaköy", 41.0240, 28.9760),
    "t1_kabatas": ("Kabataş", 41.0350, 28.9930),
    # M2 and M11
    "m2_taksim": ("Taksim", 41.0370, 28.9850),
    "m2_osmanbey": ("Osmanbey", 41.0520, 28.9870),
    "m2_sisli": ("Şişli-Mecidiyeköy", 41.0645, 28.9925),
    "m2_gayrettepe": ("Gayrettepe", 41.0680, 29.0080),
    "m11_kagithane": ("Kağıthane", 41.0850, 28.9750),
    "m11_kemerburgaz": ("Kemerburgaz", 41.1600, 28.9150),
    "m11_gokturk": ("Göktürk", 41.1800, 28.8850),
    "m11_ihsaniye": ("İhsaniye", 41.2100, 28.8200),
    "m11_airport": ("İstanbul Havalimanı", 41.2620, 28.7420),
    # Marmaray, M4, bus
    "mr_sirkeci": ("Sirkeci", 41.0150, 28.9770),
    "mr_uskudar": ("Üsküdar", 41.0260, 29.0150),
    "m4_ayrilik": ("Ayrılık Çeşmesi", 41.0000, 29.0300),
    "m4_kadikoy": ("Kadıköy", 40.9910, 29.0230),
    "bus_besiktas": ("Beşiktaş", 41.0430, 29.0050),
    # Ferry piers and a waypoint off Sarayburnu so ferry lines stay on water
    "pier_eminonu": ("Eminönü İskelesi", 41.0175, 28.9735),
    "pier_kadikoy": ("Kadıköy İskelesi", 40.9930, 29.0230),
    "pier_uskudar": ("Üsküdar İskelesi", 41.0270, 29.0130),
    "pier_besiktas": ("Beşiktaş İskelesi", 41.0410, 29.0060),
    "sea_sarayburnu": ("Sarayburnu", 41.0205, 28.9900),
}

LINES: Dict[str, List[str]] = {
    "metrobus": ["mb_beylikduzu", "mb_haramidere", "mb_avcilar", "mb_kucukcekmece", "mb_sirinevler", "mb_incirli",
                 "mb_zeytinburnu", "mb_cevizlibag", "mb_topkapi", "mb_edirnekapi", "mb_okmeydani", "mb_caglayan",
                 "mb_mecidiyekoy", "mb_zincirlikuyu", "bridge_eu", "bridge_as", "mb_altunizade", "mb_sogutlucesme"],
    "t1": ["t1_zeytinburnu", "t1_cevizlibag", "t1_topkapi", "t1_aksaray", "t1_beyazit", "t1_sultanahmet",
           "t1_sirkeci", "t1_eminonu", "t1_karakoy", "t1_kabatas"],
    "m2": ["m2_taksim", "m2_osmanbey", "m2_sisli", "m2_gayrettepe"],
    "m11": ["m2_gayrettepe", "m11_kagithane", "m11_kemerburgaz", "m11_gokturk", "m11_ihsaniye", "m11_airport"],
    "marmaray": ["mr_sirkeci", "mr_uskudar"],
    "m4": ["m4_ayrilik", "m4_kadikoy"],
    "bus": ["mb_zincirlikuyu", "bus_besiktas"],
}

# Metrobüs entry station for each western origin district
METROBUS_ENTRY = {"beylikduzu": "mb_beylikduzu", "esenyurt": "mb_beylikduzu", "haramidere": "mb_haramidere", "avcilar": "mb_avcilar"}

# D-100 for cars: Metrobüs corridor up to Zincirlikuyu, then the bridge
D100 = LINES["metrobus"][:LINES["metrobus"].index("mb_zincirlikuyu") + 1]
AIRPORT_ROAD = [(41.0340, 28.6800), (41.0900, 28.6600), (41.1500, 28.6900), (41.2100, 28.7200)]
PIER_KEYS = {"Eminönü": "pier_eminonu", "Kadıköy": "pier_kadikoy", "Üsküdar": "pier_uskudar", "Beşiktaş": "pier_besiktas"}

WALK_MAX_KM = 1.5   # longer access legs are drawn as a bus feeder
NEAR_KM = 0.4       # shorter gaps are not worth drawing


def _coord(point: str) -> List[float]:
    _, lat, lon = POINTS[point]
    return [lat, lon]


def _km(a: Sequence[float], b: Sequence[float]) -> float:
    lat1, lon1, lat2, lon2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(h))


def _line_slice(line: str, start: str, end: str) -> List[str]:
    points = LINES[line]
    i, j = points.index(start), points.index(end)
    return points[i:j + 1] if i <= j else list(reversed(points[j:i + 1]))


class _Builder:
    """Collects consecutive segments and derives start, transfer and end stops."""

    def __init__(self, start_name: str, start: Sequence[float]):
        self.segments: List[Dict[str, Any]] = []
        self.stops: List[Dict[str, Any]] = [{"name": start_name, "lat": start[0], "lon": start[1], "role": "start"}]
        self.cursor = list(start)

    def _transfer(self, name: str, at: Sequence[float]) -> None:
        if self.segments and self.stops[-1]["name"] != name:
            self.stops.append({"name": name, "lat": at[0], "lon": at[1], "role": "transfer"})

    def access(self, target: Sequence[float]) -> None:
        if _km(self.cursor, target) > NEAR_KM:
            kind = "walk" if _km(self.cursor, target) <= WALK_MAX_KM else "bus"
            self.segments.append({"kind": kind, "path": [self.cursor, list(target)]})
        self.cursor = list(target)

    def ride(self, kind: str, line: str, start: str, end: str) -> None:
        self.access(_coord(start))
        self._transfer(POINTS[start][0], _coord(start))
        self.segments.append({"kind": kind, "path": [_coord(p) for p in _line_slice(line, start, end)]})
        self.cursor = _coord(end)

    def path(self, kind: str, coords: List[Sequence[float]], via_name: Optional[str] = None) -> None:
        if via_name:
            self._transfer(via_name, self.cursor)
        self.segments.append({"kind": kind, "path": [self.cursor] + [list(c) for c in coords]})
        self.cursor = list(coords[-1])

    def finish(self, end_name: str, end: Sequence[float]) -> Dict[str, Any]:
        self.access(end)
        self.stops.append({"name": end_name, "lat": end[0], "lon": end[1], "role": "end"})
        return {"segments": self.segments, "stops": self.stops}


def transit_geometry(origin: Dict[str, Any], dest: Dict[str, Any], origin_key: Optional[str],
                     legs: Optional[List[Tuple[str, str, str, str]]]) -> Dict[str, Any]:
    start, end = (origin["lat"], origin["lon"]), (dest["lat"], dest["lon"])
    builder = _Builder(origin["name"], start)
    if legs and origin_key in METROBUS_ENTRY:
        for kind, line, leg_start, leg_end in legs:
            builder.ride(kind, line, METROBUS_ENTRY[origin_key] if leg_start == "@entry" else leg_start, leg_end)
    else:
        builder.path("generic", [end])
    return builder.finish(dest["name"], end)


def car_geometry(origin: Dict[str, Any], dest: Dict[str, Any], origin_key: str, dest_key: str, crosses: bool) -> Dict[str, Any]:
    start, end = (origin["lat"], origin["lon"]), (dest["lat"], dest["lon"])
    builder = _Builder(origin["name"], start)
    coords: List[Sequence[float]] = []
    if "airport" in (origin_key, dest_key):
        road = AIRPORT_ROAD if dest_key == "airport" else list(reversed(AIRPORT_ROAD))
        coords = list(road)
    elif origin_key in METROBUS_ENTRY:
        corridor = D100[D100.index(METROBUS_ENTRY[origin_key]):]
        if crosses:
            coords = [_coord(p) for p in corridor] + [_coord("bridge_eu"), _coord("bridge_as"), _coord("mb_altunizade")]
        else:
            nearest = min(corridor, key=lambda p: _km(_coord(p), end))
            coords = [_coord(p) for p in corridor[:corridor.index(nearest) + 1]]
    elif crosses:
        bridge = ["bridge_eu", "bridge_as"] if origin["side"] == "eu" else ["bridge_as", "bridge_eu"]
        coords = [_coord(p) for p in bridge]
    coords.append(end)
    builder.path("car", coords)
    if crosses:
        builder.stops.append({"name": POINTS["bridge_eu"][0], "lat": POINTS["bridge_eu"][1],
                              "lon": POINTS["bridge_eu"][2], "role": "transfer"})
    return builder.finish(dest["name"], end)


def ferry_geometry(origin: Dict[str, Any], dest: Dict[str, Any], origin_key: Optional[str],
                   pier_from: str, pier_to: str) -> Dict[str, Any]:
    start, end = (origin["lat"], origin["lon"]), (dest["lat"], dest["lon"])
    builder = _Builder(origin["name"], start)
    from_key, to_key = PIER_KEYS.get(pier_from, "pier_eminonu"), PIER_KEYS.get(pier_to, "pier_kadikoy")
    if origin_key in METROBUS_ENTRY and from_key == "pier_eminonu":
        builder.ride("metrobus", "metrobus", METROBUS_ENTRY[origin_key], "mb_zeytinburnu")
        builder.ride("t1", "t1", "t1_zeytinburnu", "t1_eminonu")
    else:
        builder.path("generic", [_coord(from_key)])
    builder.access(_coord(from_key))
    via = [_coord("sea_sarayburnu")] if "pier_eminonu" in (from_key, to_key) else []
    builder.path("ferry", via + [_coord(to_key)], via_name=POINTS[from_key][0])
    if _km(_coord(to_key), end) > NEAR_KM:
        builder._transfer(POINTS[to_key][0], _coord(to_key))
    return builder.finish(dest["name"], end)
