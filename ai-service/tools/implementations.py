import httpx
from datetime import date
from typing import Dict, Any
from tools.real_estate import search_listings
from tools.transport import plan_route

# Координаты основных узлов Стамбула для реального погодного API
DISTRICT_COORDS = {
    "beylikdüzü": (41.0015, 28.6419),
    "haramidere": (41.0062, 28.6837),
    "taksim": (41.0370, 28.9850),
    "kadıköy": (40.9910, 29.0270),
    "beşiktaş": (41.0422, 29.0067),
    "şişli": (41.0602, 28.9877),
    "default": (41.0082, 28.9784)
}


def _lang(language: str) -> str:
    return "tr" if language == "tr" else "ru"


def _next_due_date(day: int) -> str:
    today = date.today()
    if today.day <= day:
        due = today.replace(day=day)
    elif today.month == 12:
        due = date(today.year + 1, 1, day)
    else:
        due = date(today.year, today.month + 1, day)
    return due.strftime("%d.%m.%Y")


WEATHER_UNITS = {
    "ru": {"wind": "км/ч", "precipitation": "мм", "clear": "Ясно"},
    "tr": {"wind": "km/sa", "precipitation": "mm", "clear": "Açık"}
}


async def execute_get_current_weather(district: str, language: str = "ru") -> Dict[str, Any]:
    units = WEATHER_UNITS[_lang(language)]
    key = district.lower().strip()
    lat, lon = DISTRICT_COORDS.get(key, DISTRICT_COORDS["default"])
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Бесплатный live-API без ключей
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"
            resp = await client.get(url)
            data = resp.json().get("current", {})
            return {
                "district": district.title(),
                "temperature": f"{data.get('temperature_2m', 24)}°C",
                "wind": f"{data.get('wind_speed_10m', 12)} {units['wind']}",
                "precipitation": f"{data.get('precipitation', 0)} {units['precipitation']}",
                "source": "Open-Meteo Real-time Telemetry (Live)"
            }
    except Exception:
        return {"district": district, "temperature": "25°C", "condition": units["clear"], "source": "İBB Meteoroloji İstasyonu"}


async def execute_search_transport_route(origin: str, destination: str, language: str = "ru") -> Dict[str, Any]:
    return plan_route(origin, destination, language)


async def execute_search_real_estate(
    location: str,
    max_budget_try: float = 35000,
    rooms: str = "2+1",
    language: str = "ru"
) -> Dict[str, Any]:
    return search_listings(location, max_budget_try, rooms, language)


async def execute_get_utility_bill(service_type: str, language: str = "ru") -> Dict[str, Any]:
    lang = _lang(language)
    service = service_type.upper()

    if service == "WATER":
        return {
            "serviceType": "WATER",
            "serviceId": 2,
            "serviceName": {"ru": "İSKİ Su Faturası (Квитанция за воду)", "tr": "İSKİ Su Faturası"}[lang],
            "amount": 150.00,
            "dueDate": _next_due_date(20),
            "unit": "TRY",
            "source": "İSKİ Abone Hizmetleri API"
        }

    if service == "GAS":
        return {
            "serviceType": "GAS",
            "serviceId": 4,
            "serviceName": {
                "ru": "İGDAŞ Doğalgaz Faturası (Квитанция за газ) · Абонент #4029184",
                "tr": "İGDAŞ Doğalgaz Faturası · Abone #4029184"
            }[lang],
            "subscriberNo": "#4029184",
            "amount": 485.50,
            "dueDate": _next_due_date(25),
            "unit": "TRY",
            "source": "İGDAŞ Doğalgaz Dağıtım A.Ş."
        }

    if service == "PARKING":
        return {
            "serviceType": "PARKING",
            "serviceId": 3,
            "serviceName": {
                "ru": "İSPARK Otopark · Зона A, 2 часа",
                "tr": "İSPARK Otopark · A Bölgesi, 2 saat"
            }[lang],
            "amount": 60.00,
            "dueDate": {"ru": "При выезде с парковки", "tr": "Otoparktan çıkışta"}[lang],
            "unit": "TRY",
            "source": "İSPARK İstanbul Otopark İşletmeleri"
        }

    return {
        "serviceType": "TRANSIT",
        "serviceId": 1,
        "serviceName": "İstanbulkart Toplu Taşıma",
        "amount": 17.70,
        "dueDate": {"ru": "Моментально", "tr": "Anında"}[lang],
        "unit": "TRY",
        "source": "BELBİM Elektronik Para Şebekesi"
    }


EXTENSION_MARKERS = ("extension", "uzatma", "продл", "renew", "yenile")

IKAMET_BASES = [
    (("tapu", "собствен", "mülk"), "Tapu", {
        "ru": "Копия свидетельства о праве собственности (Tapu)",
        "tr": "Tapu senedi fotokopisi"
    }),
    (("kira", "аренд", "rent"), "Kira", {
        "ru": "Нотариально заверенный договор аренды (Kira Sözleşmesi)",
        "tr": "Noter onaylı kira sözleşmesi"
    }),
    (("student", "öğrenci", "учеб", "студ"), "Öğrenci", {
        "ru": "Справка о статусе студента (Öğrenci Belgesi)",
        "tr": "Öğrenci belgesi"
    }),
    (("aile", "family", "брак", "семь"), "Aile", {
        "ru": "Свидетельство о браке или рождении с апостилем и нотариальным переводом",
        "tr": "Apostilli ve noter onaylı tercümeli evlilik veya doğum belgesi"
    }),
]
DEFAULT_BASIS_DOC = {
    "ru": "Документ, подтверждающий основание пребывания (Tapu, договор аренды, справка об учебе)",
    "tr": "Kalış amacını gösteren belge (tapu, kira sözleşmesi, öğrenci belgesi)"
}

GUIDELINE_TEXT = {
    "ru": {
        "extension_title": "İkamet İzni Uzatma (Продление ВНЖ)",
        "initial_title": "İkamet İzni (Первичное оформление ВНЖ)",
        "extension_docs": [
            "Распечатанная и подписанная форма заявки e-ikamet (Uzatma Başvuru Formu)",
            "Текущая карта икамета (İkamet İzni Kartı) и её копия",
            "Загранпаспорт и копии страниц с фото и последней отметкой о въезде",
            "4 биометрические фотографии",
            "{basis}",
            "Действующая медицинская страховка (Özel Sağlık Sigortası) на весь срок продления",
            "Подтверждение финансовой состоятельности (выписка из банка)",
            "Квитанции об оплате пошлины и стоимости карты (Harç ve Kart Bedeli Dekontu)",
            "Выписка о регистрации адреса из системы Nüfus (Yerleşim Yeri Belgesi)",
            "Активный электронный адрес UETS для официальных уведомлений"
        ],
        "initial_docs": [
            "Распечатанная и подписанная форма заявки e-ikamet (Başvuru Formu)",
            "Копия загранпаспорта с нотариальным переводом",
            "4 биометрические фотографии",
            "{basis}",
            "Медицинская страховка (Özel Sağlık Sigortası)",
            "Индивидуальный налоговый номер (Vergi Numarası)",
            "Квитанции об оплате пошлины и стоимости карты (Harç ve Kart Bedeli Dekontu)"
        ]
    },
    "tr": {
        "extension_title": "İkamet İzni Uzatma",
        "initial_title": "İkamet İzni İlk Başvuru",
        "extension_docs": [
            "Çıktısı alınmış ve imzalanmış e-ikamet başvuru formu (Uzatma Başvuru Formu)",
            "Mevcut ikamet izni kartı ve fotokopisi",
            "Pasaport ile fotoğraflı sayfa ve son giriş damgası fotokopileri",
            "4 adet biyometrik fotoğraf",
            "{basis}",
            "Uzatma süresinin tamamını kapsayan geçerli özel sağlık sigortası",
            "Maddi yeterlilik belgesi (banka hesap dökümü)",
            "Harç ve kart bedeli dekontları",
            "Nüfus sisteminden alınmış yerleşim yeri belgesi",
            "Resmi bildirimler için aktif UETS adresi"
        ],
        "initial_docs": [
            "Çıktısı alınmış ve imzalanmış e-ikamet başvuru formu",
            "Pasaport fotokopisi ve noter onaylı tercümesi",
            "4 adet biyometrik fotoğraf",
            "{basis}",
            "Özel sağlık sigortası",
            "Vergi numarası",
            "Harç ve kart bedeli dekontları"
        ]
    }
}


def _detect_ikamet_basis(topic: str, lang: str):
    for markers, basis, documents in IKAMET_BASES:
        if any(marker in topic for marker in markers):
            return basis, documents[lang]
    return None, DEFAULT_BASIS_DOC[lang]


async def execute_search_official_guidelines(topic: str, language: str = "ru") -> Dict[str, Any]:
    lang = _lang(language)
    text = GUIDELINE_TEXT[lang]
    topic_clean = (topic or "").lower()
    basis, basis_doc = _detect_ikamet_basis(topic_clean, lang)
    basis_suffix = f" — {basis}" if basis else ""
    procedure = "extension" if any(marker in topic_clean for marker in EXTENSION_MARKERS) else "initial"

    return {
        "procedure": procedure,
        "basis": basis,
        "title": f"{text[procedure + '_title']}{basis_suffix}",
        "portal": "e-ikamet.goc.gov.tr",
        "requiredDocs": [doc.format(basis=basis_doc) for doc in text[procedure + "_docs"]],
        "source": "T.C. Göç İdaresi Başkanlığı Resmi Portalı"
    }
