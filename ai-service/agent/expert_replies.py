"""Expert, data-driven reply texts for tool results.

Each reply is composed from the tool output so the action card complements a full
consultant answer, without a second LLM roundtrip.
"""
from typing import Any, Dict, List

GUIDELINE_REPLIES = {
    "ru": {
        "extension": (
            "Продление ВНЖ (İkamet İzni Uzatma) проходит в три юридических этапа:\n"
            "1. **Онлайн-заявка** на e-ikamet.goc.gov.tr (раздел «Uzatma Başvurusu»). Подать её можно не ранее "
            "чем за 60 дней до окончания текущей карты и строго до даты её истечения.\n"
            "2. **Оплата пошлины и стоимости карты** (harç и kart bedeli) в налоговой или онлайн. Сохраните "
            "квитанции, они входят в досье.\n"
            "3. **Передача досье в Göç İdaresi**: распечатанная форма, квитанции и документы из списка ниже. "
            "Способ подачи (почтой или лично) указан в подтверждении заявки.\n"
            "Новая карта доставляется по адресу, зарегистрированному в системе Nüfus, а официальные уведомления "
            "приходят на электронный адрес UETS, поэтому оба должны быть актуальны.\n"
            "Официальный перечень документов:"
        ),
        "initial": (
            "Первичное оформление ВНЖ (İkamet İzni) проходит в три юридических этапа:\n"
            "1. **Онлайн-заявка** на e-ikamet.goc.gov.tr и выбор даты визита в Göç İdaresi.\n"
            "2. **Оплата пошлины и стоимости карты** (harç и kart bedeli) в налоговой или онлайн.\n"
            "3. **Визит в Göç İdaresi** в назначенную дату с полным досье из списка ниже.\n"
            "После одобрения карта доставляется по адресу, зарегистрированному в системе Nüfus.\n"
            "Официальный перечень документов:"
        )
    },
    "tr": {
        "extension": (
            "İkamet izni uzatma işlemi üç yasal adımdan oluşur:\n"
            "1. **Çevrim içi başvuru**: e-ikamet.goc.gov.tr üzerinden «Uzatma Başvurusu». Başvuru, mevcut kartın "
            "bitiminden en erken 60 gün önce ve kesinlikle bitiş tarihinden önce yapılmalıdır.\n"
            "2. **Harç ve kart bedeli ödemesi**: vergi dairesinde veya çevrim içi. Dekontları saklayın, "
            "dosyanın parçasıdır.\n"
            "3. **Dosyanın Göç İdaresi'ne teslimi**: çıktısı alınmış form, dekontlar ve aşağıdaki belgeler. "
            "Teslim yöntemi (posta veya şahsen) başvuru onayında belirtilir.\n"
            "Yeni kart Nüfus sisteminde kayıtlı adrese gönderilir, resmi bildirimler UETS adresine iletilir; "
            "ikisinin de güncel olması gerekir.\n"
            "Resmi belge listesi:"
        ),
        "initial": (
            "İlk ikamet izni başvurusu üç yasal adımdan oluşur:\n"
            "1. **Çevrim içi başvuru**: e-ikamet.goc.gov.tr üzerinden başvuru ve randevu tarihi seçimi.\n"
            "2. **Harç ve kart bedeli ödemesi**: vergi dairesinde veya çevrim içi.\n"
            "3. **Göç İdaresi randevusu**: aşağıdaki belgelerin tamamıyla randevu gününde başvuru.\n"
            "Onaydan sonra kart Nüfus sisteminde kayıtlı adrese gönderilir.\n"
            "Resmi belge listesi:"
        )
    }
}

DISTRICT_NOTES = {
    "beylikdüzü": {
        "ru": "Бейликдюзю — современный спальный район на западе Стамбула с жилыми комплексами (site) и развитой "
              "инфраструктурой. Ключевой транспортный узел — линия Метробуса вдоль трассы E-5: от неё зависит, "
              "сколько времени займет дорога до центра.",
        "tr": "Beylikdüzü, İstanbul'un batısında site yaşamı ve gelişmiş altyapısıyla öne çıkan modern bir yerleşim "
              "bölgesidir. Ana ulaşım ekseni E-5 boyunca uzanan Metrobüs hattıdır; merkeze ulaşım süresi buna bağlıdır."
    },
    "haramidere": {
        "ru": "Харамидере — район на границе Бейликдюзю и Авджылара с собственной станцией Метробуса, удобен для "
              "ежедневных поездок в центр без пересадок на автобус.",
        "tr": "Haramidere, Beylikdüzü ile Avcılar sınırında, kendi Metrobüs durağı olan ve merkeze günlük ulaşım "
              "için pratik bir bölgedir."
    },
    "kadıköy": {
        "ru": "Кадыкёй — оживленный центр азиатской стороны с паромами, линией метро M4 и Мармараем рядом. "
              "Аренда здесь заметно дороже, чем в западных районах.",
        "tr": "Kadıköy, vapur iskeleleri, M4 metro hattı ve yakınındaki Marmaray ile Anadolu yakasının canlı "
              "merkezidir. Kiralar batı ilçelerine göre belirgin şekilde yüksektir."
    },
    "başakşehir": {
        "ru": "Башакшехир — район новых жилых комплексов, популярный у семей; до центра удобнее всего добираться "
              "на метро.",
        "tr": "Başakşehir, ailelerin tercih ettiği yeni konut projeleriyle bilinen bir ilçedir; merkeze ulaşımda "
              "metro en pratik seçenektir."
    }
}

COPY = {
    "ru": {
        "estate_found": "Подобрал {count} примера в районе {location} под ваши параметры: от {low} до {high} TRY в месяц.",
        "estate_samples": "Это примеры типичных предложений: нажмите на карточку, и откроется актуальная выдача sahibinden.com по этому кварталу и планировке.",
        "estate_search_only": "Готовой подборки по району {location} у меня нет, но актуальные объявления по вашей планировке открываются по ссылке в карточке.",
        "estate_tips": [
            "Проверьте, не закрыт ли квартал (mahalle) для регистрации иностранцев: по закрытому адресу ВНЖ не оформят.",
            "Уточните размер депозита (depozito) и ежемесячного сбора жилого комплекса (aidat).",
            "Для ВНЖ договор аренды нужно заверить у нотариуса."
        ],
        "estate_next": "Если хотите, сузим поиск по бюджету, количеству комнат или расстоянию до Метробуса.",
        "district_default": "Перед выбором района оцените время в пути до работы в часы пик и близость к линии метро или Метробуса.",
        "route_intro": "Сравнил варианты {origin} → {destination}:",
        "route_transit": "Общественный транспорт: {duration}, {fare}.",
        "route_car": "На машине: {km} км, от {free} без пробок до {peak} в час пик; топливо {fuel}, такси {taxi}.",
        "route_ferry": "Паром: {duration}, {fare}.",
        "route_pick_transit": "В часы пик выгоднее общественный транспорт: время в пути предсказуемо, а при пересадке в течение 2 часов (aktarma) следующие поездки по Istanbulkart дешевле.",
        "route_pick_car": "Здесь быстрее машина или такси даже в час пик, но учитывайте стоимость и парковку.",
        "route_metrobus": "Метробус идет по выделенной полосе вдоль E-5 и не стоит в пробках.",
        "route_bosphorus": "Маршрут пересекает Босфор: мосты платные (HGS), а паром İBB Şehir Hatları — самый живописный вариант без пробок.",
        "route_estimate": "Стоимость поездки на машине и такси ориентировочная.",
        "route_card": "Сравнение и пошаговые схемы — во вкладках карточки ниже.",
        "water_intro": "Квитанция İSKİ: {amount:.2f} {unit}.",
        "water_rules": [
            "Вода до 15 м³ начисляется по базовому тарифу 25.50 TRY за м³.",
            "Оплатить нужно до 20 числа текущего месяца.",
            "При просрочке более 30 дней начисляется пеня 2.5% от суммы долга."
        ],
        "gas_intro": "Квитанция İGDAŞ за природный газ, абонент {subscriber}: {amount:.2f} {unit}.",
        "gas_rules": [
            "Счета İGDAŞ оплачиваются до 25 числа каждого месяца.",
            "При просрочке более 30 дней начисляется пеня 2.5% от суммы долга.",
            "Срок оплаты этой квитанции: {due}."
        ],
        "parking_intro": "Квитанция İSPARK: {amount:.2f} {unit} за 2 часа дневной парковки в зоне A.",
        "parking_rules": [
            "В зоне A первый час стоит 40.00 TRY, каждый следующий — 20.00 TRY; суточный абонемент — 150.00 TRY.",
            "Оплата только безналичная: Istanbulkart или банковская карта."
        ],
        "transit_intro": "Пополнение Istanbulkart: {amount:.2f} {unit}. Разовый проезд стоит 17.70 TRY, льготный студенческий — 8.85 TRY.",
        "transit_rules": [
            "Штраф за проезд без оплаты или по чужой льготной карте — 500.00 TRY."
        ],
        "gateway": "Платеж через финансовый шлюз города проходит мгновенно и без банковской комиссии: нажмите кнопку в карточке.",
        "weather": "Сейчас в районе {district}: {temperature}, ветер {wind}, осадки {precipitation}.",
        "weather_tip": "Если планируете поездку на пароме, при сильном ветре рейсы могут задерживаться."
    },
    "tr": {
        "estate_found": "{location} bölgesinde kriterlerinize uygun {count} örnek seçtim: aylık {low} – {high} TRY.",
        "estate_samples": "Bunlar tipik tekliflerden örneklerdir: karta tıklayınca bu mahalle ve oda sayısı için güncel sahibinden.com ilanları açılır.",
        "estate_search_only": "{location} için hazır bir seçkim yok, ancak oda sayınıza uygun güncel ilanlar karttaki bağlantıda.",
        "estate_tips": [
            "Mahallenin yabancıların ikamet kaydına kapalı olup olmadığını kontrol edin: kapalı adreste ikamet izni alınamaz.",
            "Depozito tutarını ve sitenin aylık aidatını sorun.",
            "İkamet izni için kira sözleşmesinin noter onaylı olması gerekir."
        ],
        "estate_next": "İsterseniz aramayı bütçe, oda sayısı veya Metrobüs'e uzaklığa göre daraltabiliriz.",
        "district_default": "Bölge seçmeden önce yoğun saatlerde işe ulaşım süresini ve metro ya da Metrobüs hattına yakınlığı değerlendirin.",
        "route_intro": "{origin} → {destination} için seçenekleri karşılaştırdım:",
        "route_transit": "Toplu taşıma: {duration}, {fare}.",
        "route_car": "Araba: {km} km, trafiksiz {free}, yoğun saatte {peak}; yakıt {fuel}, taksi {taxi}.",
        "route_ferry": "Vapur: {duration}, {fare}.",
        "route_pick_transit": "Yoğun saatlerde toplu taşıma daha avantajlı: süre öngörülebilir ve 2 saat içindeki aktarmalarda sonraki binişler İstanbulkart ile daha ucuz.",
        "route_pick_car": "Bu güzergahta yoğun saatte bile araba veya taksi daha hızlı; ancak maliyeti ve otoparkı hesaba katın.",
        "route_metrobus": "Metrobüs E-5 boyunca ayrılmış şeritte ilerler ve trafiğe takılmaz.",
        "route_bosphorus": "Güzergah Boğaz'ı geçiyor: köprüler ücretli (HGS), İBB Şehir Hatları vapuru ise trafiksiz ve en manzaralı seçenek.",
        "route_estimate": "Araba ve taksi tutarları yaklaşıktır.",
        "route_card": "Karşılaştırma ve adım adım güzergahlar aşağıdaki kartın sekmelerinde.",
        "water_intro": "İSKİ faturası: {amount:.2f} {unit}.",
        "water_rules": [
            "15 m³'e kadar su tüketimi m³ başına 25.50 TRY temel tarifeyle hesaplanır.",
            "Ödeme her ayın 20'sine kadar yapılmalıdır.",
            "30 günden fazla gecikmede borç tutarının %2.5'i gecikme zammı uygulanır."
        ],
        "gas_intro": "İGDAŞ doğalgaz faturası, abone {subscriber}: {amount:.2f} {unit}.",
        "gas_rules": [
            "İGDAŞ faturaları her ayın 25'ine kadar ödenmelidir.",
            "30 günden fazla gecikmede borç tutarının %2.5'i gecikme zammı uygulanır.",
            "Bu faturanın son ödeme tarihi: {due}."
        ],
        "parking_intro": "İSPARK faturası: A Bölgesi'nde 2 saatlik gündüz park için {amount:.2f} {unit}.",
        "parking_rules": [
            "A Bölgesi'nde ilk saat 40.00 TRY, sonraki her saat 20.00 TRY; günlük abonman 150.00 TRY'dir.",
            "Ödeme yalnızca nakitsizdir: İstanbulkart veya banka kartı."
        ],
        "transit_intro": "İstanbulkart yüklemesi: {amount:.2f} {unit}. Tam bilet 17.70 TRY, öğrenci bileti 8.85 TRY'dir.",
        "transit_rules": [
            "Ücretsiz geçiş veya başkasının indirimli kartını kullanma cezası 500.00 TRY'dir."
        ],
        "gateway": "Şehir finansal geçidi üzerinden ödeme anında ve banka komisyonu olmadan gerçekleşir: karttaki butona basın.",
        "weather": "{district} bölgesinde şu an: {temperature}, rüzgar {wind}, yağış {precipitation}.",
        "weather_tip": "Vapurla seyahat planlıyorsanız, kuvvetli rüzgarda seferler gecikebilir."
    }
}


def _bullets(lines: List[str]) -> str:
    return "\n".join(f"- {line}" for line in lines)


def _district_note(location: str, language: str) -> str:
    key = (location or "").lower()
    for district, note in DISTRICT_NOTES.items():
        if district in key:
            return note[language]
    return COPY[language]["district_default"]


def _estate_reply(data: Dict[str, Any], language: str) -> str:
    copy = COPY[language]
    items = data.get("items") or []
    location = data.get("location", "")
    prices = sorted(int(item.get("price") or 0) for item in items)
    parts = [_district_note(location, language)]
    if prices:
        parts.append(copy["estate_found"].format(
            count=len(items), location=location,
            low=f"{prices[0]:,}".replace(",", " "), high=f"{prices[-1]:,}".replace(",", " ")
        ))
        parts.append(copy["estate_samples"])
    else:
        parts.append(copy["estate_search_only"].format(location=location))
    parts.append(_bullets(copy["estate_tips"]))
    parts.append(copy["estate_next"])
    return "\n\n".join(parts)


def _route_reply(data: Dict[str, Any], language: str) -> str:
    copy = COPY[language]
    options = {option["mode"]: option for option in data.get("options") or []}
    transit, car, ferry = options.get("transit"), options.get("car"), options.get("ferry")

    lines = []
    if transit:
        lines.append(copy["route_transit"].format(duration=transit["duration"], fare=transit["fare"]))
    if car:
        lines.append(copy["route_car"].format(
            km=car["distanceKm"], free=car["durationFree"], peak=car["durationPeak"],
            fuel=car["fuelCost"], taxi=car["taxiFare"]
        ))
    if ferry:
        lines.append(copy["route_ferry"].format(duration=ferry["duration"], fare=ferry["fare"]))

    parts = [copy["route_intro"].format(origin=data.get("origin", ""), destination=data.get("destination", "")),
             _bullets(lines)]
    if car:
        parts.append(copy["route_pick_car"] if data.get("recommended") == "car" else copy["route_pick_transit"])
    steps = (transit or {}).get("steps") or []
    if any("метробус" in step.lower() or "metrobüs" in step.lower() for step in steps):
        parts.append(copy["route_metrobus"])
    if data.get("crossesBosphorus"):
        parts.append(copy["route_bosphorus"])
    if car:
        parts.append(copy["route_estimate"])
    parts.append(copy["route_card"])
    return "\n\n".join(parts)


def _bill_reply(data: Dict[str, Any], language: str) -> str:
    copy = COPY[language]
    amount = float(data.get("amount", 0))
    unit = data.get("unit", "TRY")
    service = data.get("serviceType")
    if service == "WATER":
        parts = [copy["water_intro"].format(amount=amount, unit=unit), _bullets(copy["water_rules"])]
    elif service == "GAS":
        rules = [rule.format(due=data.get("dueDate", "")) for rule in copy["gas_rules"]]
        parts = [copy["gas_intro"].format(subscriber=data.get("subscriberNo", ""), amount=amount, unit=unit), _bullets(rules)]
    elif service == "PARKING":
        parts = [copy["parking_intro"].format(amount=amount, unit=unit), _bullets(copy["parking_rules"])]
    else:
        parts = [copy["transit_intro"].format(amount=amount, unit=unit), _bullets(copy["transit_rules"])]
    parts.append(copy["gateway"])
    return "\n\n".join(parts)


def _weather_reply(data: Dict[str, Any], language: str) -> str:
    copy = COPY[language]
    text = copy["weather"].format(
        district=data.get("district", ""),
        temperature=data.get("temperature", "—"),
        wind=data.get("wind", "—"),
        precipitation=data.get("precipitation", "—")
    )
    return f"{text}\n\n{copy['weather_tip']}"


def _guideline_reply(data: Dict[str, Any], language: str) -> str:
    pack = GUIDELINE_REPLIES[language]
    return pack.get(data.get("procedure"), pack["initial"])


REPLY_BUILDERS = {
    "search_real_estate": _estate_reply,
    "search_transport_route": _route_reply,
    "get_utility_bill": _bill_reply,
    "get_current_weather": _weather_reply,
    "search_official_guidelines": _guideline_reply,
}


ROUTE_ORIGIN_QUESTIONS = {
    "ru": ("Чтобы рассчитать оптимальный маршрут до {destination}, подскажите: откуда вы отправляетесь?",
           "Чтобы рассчитать оптимальный маршрут, подскажите: откуда и куда вы едете?"),
    "tr": ("{destination} için en uygun güzergahı hesaplayabilmem için: nereden yola çıkıyorsunuz?",
           "En uygun güzergahı hesaplayabilmem için: nereden nereye gidiyorsunuz?")
}


ROUTE_DESTINATION_QUESTIONS = {
    "ru": "Куда едем? Точку старта беру по вашему местоположению: {origin}.",
    "tr": "Nereye gidiyoruz? Başlangıç noktası olarak konumunuzu kullanıyorum: {origin}."
}


def ask_route_destination(origin: str, language: str) -> str:
    return ROUTE_DESTINATION_QUESTIONS["tr" if language == "tr" else "ru"].format(origin=origin)


def ask_route_origin(destination: str, language: str) -> str:
    with_destination, without_destination = ROUTE_ORIGIN_QUESTIONS["tr" if language == "tr" else "ru"]
    if destination.strip():
        return with_destination.format(destination=destination.strip().title())
    return without_destination


def compose_tool_reply(tool_name: str, data: Dict[str, Any], language: str) -> str:
    lang = "tr" if language == "tr" else "ru"
    return REPLY_BUILDERS[tool_name](data, lang)
