import { ApiService } from '../services/api.js';

const DEFAULT_ORIGIN = 'Beylikdüzü';
const ISTANBUL_CENTER = { lat: 41.0082, lon: 28.9784 };
const ISTANBUL_RADIUS_KM = 50;

const POPULAR_DESTINATIONS = [
  { value: 'Taksim', ru: 'Таксим', tr: 'Taksim' },
  { value: 'Kadıköy', ru: 'Кадыкёй', tr: 'Kadıköy' },
  { value: 'Eminönü / Sultanahmet', ru: 'Эминёню / Султанахмет', tr: 'Eminönü / Sultanahmet' },
  { value: 'Beşiktaş', ru: 'Бешикташ', tr: 'Beşiktaş' },
  { value: 'İstanbul Havalimanı', ru: 'Аэропорт IST', tr: 'IST Havalimanı' },
  { value: 'Üsküdar', ru: 'Ускюдар', tr: 'Üsküdar' }
];

const DISTRICT_CENTERS = [
  { name: 'Beylikdüzü', lat: 41.0015, lon: 28.6419 },
  { name: 'Haramidere', lat: 41.0062, lon: 28.6837 },
  { name: 'Esenyurt', lat: 41.0343, lon: 28.6801 },
  { name: 'Avcılar', lat: 40.9796, lon: 28.7214 },
  { name: 'Bakırköy', lat: 40.9819, lon: 28.8772 },
  { name: 'Başakşehir', lat: 41.0931, lon: 28.8020 },
  { name: 'Eminönü / Sultanahmet', lat: 41.0170, lon: 28.9700 },
  { name: 'Karaköy', lat: 41.0256, lon: 28.9744 },
  { name: 'Taksim', lat: 41.0370, lon: 28.9850 },
  { name: 'Şişli', lat: 41.0602, lon: 28.9877 },
  { name: 'Beşiktaş', lat: 41.0422, lon: 29.0067 },
  { name: 'İstanbul Havalimanı', lat: 41.2620, lon: 28.7420 },
  { name: 'Kadıköy', lat: 40.9910, lon: 29.0270 },
  { name: 'Üsküdar', lat: 41.0226, lon: 29.0150 },
  { name: 'Ataşehir', lat: 40.9923, lon: 29.1244 }
];

const SESSION_ORIGIN_KEY = 'smartcity.routeOrigin';
const ROUTE_FROM_HERE = /(на машин|на авто|на такси|из дома|от дома|поехали|arabayla|araba ile|evden|taksiyle|hadi gidelim|by car|from home)/i;

const readSessionOrigin = () => {
  try { return sessionStorage.getItem(SESSION_ORIGIN_KEY); } catch { return null; }
};
const saveSessionOrigin = (origin) => {
  try { sessionStorage.setItem(SESSION_ORIGIN_KEY, origin); } catch { /* storage unavailable: origin is re-resolved next time */ }
};

const LINE_STYLES = {
  car: { color: '#f59e0b', weight: 5 },
  metrobus: { color: '#ef4444', weight: 5 },
  t1: { color: '#3b82f6', weight: 5 },
  m2: { color: '#22c55e', weight: 5 },
  m11: { color: '#a855f7', weight: 5 },
  marmaray: { color: '#0ea5e9', weight: 5 },
  m4: { color: '#ec4899', weight: 5 },
  bus: { color: '#eab308', weight: 4, dashArray: '6 6' },
  walk: { color: '#cbd5e1', weight: 3, dashArray: '2 6' },
  ferry: { color: '#38bdf8', weight: 4, dashArray: '8 8' },
  generic: { color: '#94a3b8', weight: 3, dashArray: '4 8' }
};
const STOP_STYLES = {
  start: { radius: 7, color: '#ecfdf5', fillColor: '#10b981', fillOpacity: 1, weight: 2 },
  end: { radius: 7, color: '#fff1f2', fillColor: '#f43f5e', fillOpacity: 1, weight: 2 },
  transfer: { radius: 5, color: '#0f172a', fillColor: '#f8fafc', fillOpacity: 1, weight: 2 }
};

const distanceKm = (a, b) => {
  const rad = (deg) => (deg * Math.PI) / 180;
  const h = Math.sin(rad(b.lat - a.lat) / 2) ** 2
    + Math.cos(rad(a.lat)) * Math.cos(rad(b.lat)) * Math.sin(rad(b.lon - a.lon) / 2) ** 2;
  return 2 * 6371 * Math.asin(Math.sqrt(h));
};

export const DashboardView = {
  currentLang: 'ru',

  render() {
    const isTr = this.currentLang === 'tr';
    const chipStyle = 'glass-card px-3.5 py-1.5 rounded-full text-slate-200 hover:bg-white/10 hover:text-white hover:-translate-y-0.5 hover:shadow-lg hover:shadow-blue-500/10 transition-all flex-shrink-0';
    const chip = `chip-btn ${chipStyle}`;
    return `
      <div class="max-w-4xl mx-auto space-y-6 pb-12">
        <!-- AI Hero Prompt Section -->
        <div class="text-center space-y-3 pt-6">
          <div class="glass-card inline-flex items-center space-x-2 px-3 py-1 rounded-full text-blue-300 text-xs font-medium">
            <i data-lucide="sparkles" class="w-3.5 h-3.5"></i>
            <span>Istanbul AI Operating System • 2026</span>
          </div>
          <h1 class="text-3xl sm:text-5xl font-semibold text-white tracking-tight drop-shadow-[0_2px_12px_rgba(0,0,0,0.6)]">
            ${isTr ? 'Bugün İstanbul için ne yapmak istersiniz?' : 'Чем вам помочь в Стамбуле сегодня?'}
          </h1>
          <p class="text-xs sm:text-sm text-slate-300/90 max-w-lg mx-auto">
            ${isTr ? 'Ulaşım, faturalar, ikamet ve şehir hizmetleri tek ekranda.' : 'Транспорт, оплата ЖКХ, оформление икамета и городская справка в один клик.'}
          </p>
        </div>

        <!-- Conversational Feed Viewport -->
        <div class="glass-panel rounded-3xl p-4 sm:p-6 space-y-6 min-h-[460px] flex flex-col justify-between">
          <div id="aiConversationFeed" class="space-y-4 overflow-y-auto max-h-[500px] pr-2">
            <!-- Initial AI Welcome -->
            <div class="flex items-start space-x-3">
              <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-blue-500/30 to-indigo-500/30 border border-blue-400/30 flex items-center justify-center text-blue-300 flex-shrink-0">
                <i data-lucide="bot" class="w-4 h-4"></i>
              </div>
              <div class="glass-panel border-white/10 rounded-2xl rounded-tl-none p-4 max-w-2xl text-sm text-slate-100 leading-relaxed">
                ${isTr ? 'Merhaba! Ben İstanbul Dijital Asistanıyım. Sorunuzu yazabilir veya aşağıdaki hazır eylemleri seçebilirsiniz.' : 'Здравствуйте! Я ваш проводник по Стамбулу. Напишите вашу задачу человеческим языком или нажмите на подсказку ниже:'}
              </div>
            </div>
          </div>

          <!-- Suggested Action Chips -->
          <div class="space-y-3 pt-3 border-t border-white/10">
            <div class="flex items-center space-x-2 overflow-x-auto text-xs py-1">
              <span class="text-slate-400 flex-shrink-0">${isTr ? 'Öneriler:' : 'Быстрые действия:'}</span>
              <button data-prompt="${isTr ? 'İSKİ su faturamı ödemek istiyorum' : 'Оплатить счет за воду İSKİ'}" class="${chip}">
                💧 ${isTr ? 'Su Faturası Öde' : 'Оплата воды (İSKİ)'}
              </button>
              <button id="routePlannerBtn" type="button" class="${chipStyle} inline-flex items-center">
                <i data-lucide="navigation" class="w-3.5 h-3.5 mr-1.5 text-blue-300"></i>
                <span>${isTr ? 'Rota Oluştur' : 'Построить маршрут'}</span>
              </button>
              <button data-prompt="${isTr ? 'İkamet izni için hangi belgeler gerekli?' : 'Как продлить икамет (ВНЖ)?'}" class="${chip}">
                🏛 ${isTr ? 'İkamet Rehberi' : 'Гайд по Икамету'}
              </button>
              <button data-prompt="${isTr ? 'Beylikdüzü kiralık daire bul' : 'Найти квартиру в Beylikdüzü'}" class="${chip}">
                🏠 ${isTr ? 'Kiralık Daire' : 'Аренда жилья'}
              </button>
            </div>

            <!-- Floating input capsule -->
            <form id="aiPromptForm" class="glass-panel rounded-full p-1.5 pl-5 flex items-center gap-2 focus-within:ring-2 focus-within:ring-blue-500/50 transition">
              <input
                type="text"
                id="aiPromptInput"
                placeholder="${isTr ? 'İstanbul hakkında bir şey sorun veya talimat verin...' : 'Спросите о транспорте, тарифах, икамете или оплатите счета...'}"
                class="flex-1 min-w-0 bg-transparent border-0 py-2.5 text-sm text-white placeholder-slate-400 focus:outline-none"
                autocomplete="off"
              />
              <button
                type="submit"
                id="aiSubmitBtn"
                class="px-5 sm:px-6 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 active:scale-95 text-white text-sm font-semibold rounded-full transition-all flex items-center space-x-2 shadow-lg shadow-blue-600/30"
              >
                <span>${isTr ? 'Gönder' : 'Решить'}</span>
                <i data-lucide="arrow-up-right" class="w-4 h-4"></i>
              </button>
            </form>
          </div>
        </div>

        <!-- Route planner modal -->
        <div id="routePlannerModal" class="hidden fixed inset-0 z-40 flex items-center justify-center p-4">
          <div data-planner-close class="absolute inset-0 bg-slate-950/60 backdrop-blur-sm"></div>
          <div class="glass-panel msg-enter relative w-full max-w-lg rounded-3xl p-5 sm:p-6 space-y-4" role="dialog" aria-modal="true">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white">
                  <i data-lucide="map-pin" class="w-4 h-4"></i>
                </div>
                <div class="text-sm font-semibold text-white">${isTr ? 'Rota Oluştur' : 'Построить маршрут'}</div>
              </div>
              <button type="button" data-planner-close class="w-8 h-8 rounded-lg text-slate-400 hover:text-white hover:bg-white/10 flex items-center justify-center transition" aria-label="close">
                <i data-lucide="x" class="w-4 h-4"></i>
              </button>
            </div>

            <label class="block space-y-1.5">
              <span class="text-[11px] uppercase tracking-wider text-slate-400">${isTr ? 'Nereden' : 'Откуда'}</span>
              <div class="glass-card rounded-2xl px-3 flex items-center focus-within:ring-2 focus-within:ring-blue-500/50">
                <i data-lucide="locate-fixed" class="w-4 h-4 text-emerald-300 flex-shrink-0"></i>
                <input id="plannerOrigin" type="text" autocomplete="off" class="flex-1 min-w-0 bg-transparent border-0 px-2 py-2.5 text-sm text-white focus:outline-none" />
              </div>
              <span id="plannerOriginHint" class="block text-[11px] text-slate-400"></span>
            </label>

            <label class="block space-y-1.5">
              <span class="text-[11px] uppercase tracking-wider text-slate-400">${isTr ? 'Nereye' : 'Куда'}</span>
              <div class="glass-card rounded-2xl px-3 flex items-center focus-within:ring-2 focus-within:ring-blue-500/50">
                <i data-lucide="search" class="w-4 h-4 text-blue-300 flex-shrink-0"></i>
                <input id="plannerDestination" type="text" autocomplete="off" placeholder="${isTr ? 'Semt, istasyon veya yer arayın…' : 'Район, станция или место…'}" class="flex-1 min-w-0 bg-transparent border-0 px-2 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none" />
              </div>
            </label>

            <div class="space-y-2">
              <div class="text-[11px] uppercase tracking-wider text-slate-400">${isTr ? 'Popüler yerler' : 'Популярные места'}</div>
              <div id="plannerPopular" class="grid grid-cols-2 sm:grid-cols-3 gap-2">
                ${POPULAR_DESTINATIONS.map(d => `
                  <button type="button" data-destination="${d.value}" data-search="${(d.value + ' ' + d.ru + ' ' + d.tr).toLowerCase()}" class="glass-card text-left rounded-xl px-3 py-2 hover:bg-white/10 hover:-translate-y-0.5 transition-all">
                    <div class="text-xs font-semibold text-white">${d.value}</div>
                    <div class="text-[10px] text-slate-400">${isTr ? d.tr : d.ru}</div>
                  </button>`).join('')}
              </div>
            </div>

            <button id="plannerSubmit" type="button" class="w-full py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white text-sm font-semibold rounded-2xl transition-all flex items-center justify-center space-x-2 shadow-lg shadow-blue-600/30">
              <i data-lucide="git-compare-arrows" class="w-4 h-4"></i>
              <span>${isTr ? 'Seçenekleri karşılaştır' : 'Сравнить варианты'}</span>
            </button>
          </div>
        </div>

        <!-- Global Toast Container -->
        <div id="toastNotificationArea" class="fixed bottom-6 right-6 z-50 space-y-2"></div>
      </div>
    `;
  },

  attachEvents() {
    const form = document.getElementById('aiPromptForm');
    const input = document.getElementById('aiPromptInput');
    const feed = document.getElementById('aiConversationFeed');
    const chips = document.querySelectorAll('.chip-btn');
    const toastArea = document.getElementById('toastNotificationArea');
    const isTr = DashboardView.currentLang === 'tr';
    const conversationHistory = [];
    const MAX_HISTORY = 6;
    const copy = isTr
      ? {
          due: 'Son ödeme tarihi',
          noFee: 'Komisyonsuz',
          payNow: 'Şimdi öde',
          loader: 'İstanbul resmi veritabanı ve RAG doğrulaması…',
          source: 'Kaynak',
          verified: 'Doğrulandı (Ağustos 2026)',
          processing: 'İşlem işleniyor…',
          paid: '✓ Fatura ödendi',
          payError: 'Hata',
          retry: 'Ödemeyi tekrar dene',
          payOk: 'Ödeme başarılı! İşlem',
          aiFail: 'Yapay zeka servisine bağlanılamadı',
          retryHint: 'Hizmet geçici olarak kullanılamıyor, lütfen biraz sonra tekrar deneyin.',
          requiredDocs: 'Gerekli belgeler:',
          sampleListing: 'Örnek ilan',
          openOnSahibinden: 'sahibinden.com',
          allListings: (location, rooms) => `${location} bölgesindeki tüm ${rooms} ilanları sahibinden.com'da`,
          floor: 'Kat',
          aidat: 'Aidat',
          area: 'Alan',
          rooms: 'Oda',
          locating: 'Konum belirleniyor…',
          geoDetected: 'Konumunuza göre belirlendi',
          geoDenied: `Konum kullanılamıyor, varsayılan başlangıç noktası: ${DEFAULT_ORIGIN}`,
          geoOutside: `İstanbul dışındasınız, varsayılan başlangıç noktası: ${DEFAULT_ORIGIN}`,
          editableHint: 'Başlangıç noktasını değiştirebilirsiniz',
          routeMessage: (from, to) => `${from} → ${to} nasıl giderim? Araba ve toplu taşıma seçeneklerini göster`,
          tabCar: '🚗 Araba & Taksi',
          tabTransit: '🚇 Toplu Taşıma',
          tabFerry: '⛴ Vapur',
          recommended: 'Önerilen',
          distance: 'Mesafe',
          time: 'Süre',
          freeToPeak: (free, peak) => `${free} – ${peak}`,
          trafficRange: 'trafiksiz – yoğun saat',
          fuel: 'Yakıt',
          taxi: 'Taksi',
          roads: 'Güzergah',
          tolls: 'Ücretli geçişler',
          fare: 'İBB tarifesi',
          estimate: 'Tutarlar yaklaşıktır',
          schematic: 'Güzergah şeması yaklaşıktır',
          lines: { car: 'Araba', metrobus: 'Metrobüs', t1: 'T1 Tramvay', m2: 'M2 Metro', m11: 'M11 Metro', marmaray: 'Marmaray', m4: 'M4 Metro', bus: 'Otobüs', walk: 'Yürüyüş', ferry: 'Vapur', generic: 'Şematik' }
        }
      : {
          due: 'Срок оплаты',
          noFee: 'Без комиссии',
          payNow: 'Оплатить прямо сейчас',
          loader: 'Поиск в базе данных Стамбула и верификация RAG...',
          source: 'Источник',
          verified: 'Верифицировано (Август 2026)',
          processing: 'Обработка транзакции...',
          paid: '✓ Счет оплачен',
          payError: 'Ошибка',
          retry: 'Повторить оплату',
          payOk: 'Оплата проведена успешно! Транзакция',
          aiFail: 'Не удалось связаться с ИИ-сервисом',
          retryHint: 'Сервис временно недоступен, повторите попытку чуть позже.',
          requiredDocs: 'Необходимый перечень документов:',
          sampleListing: 'Пример',
          openOnSahibinden: 'sahibinden.com',
          allListings: (location, rooms) => `Все объявления ${rooms} в районе ${location} на sahibinden.com`,
          floor: 'Этаж',
          aidat: 'Айдат',
          area: 'Площадь',
          rooms: 'Комнаты',
          locating: 'Определяем местоположение…',
          geoDetected: 'Определено по геолокации',
          geoDenied: `Геолокация недоступна, используется текущая точка по умолчанию: ${DEFAULT_ORIGIN}`,
          geoOutside: `Вы вне Стамбула, используется точка по умолчанию: ${DEFAULT_ORIGIN}`,
          editableHint: 'Точку отправления можно изменить',
          routeMessage: (from, to) => `Как добраться из ${from} в ${to}? Покажи варианты на машине и на общественном транспорте`,
          tabCar: '🚗 На автомобиле',
          tabTransit: '🚇 Общественный транспорт',
          tabFerry: '⛴ Паром',
          recommended: 'Рекомендуем',
          distance: 'Расстояние',
          time: 'Время',
          freeToPeak: (free, peak) => `${free} – ${peak}`,
          trafficRange: 'без пробок – час пик',
          fuel: 'Топливо',
          taxi: 'Такси',
          roads: 'Трасса',
          tolls: 'Платные участки',
          fare: 'Тариф İBB',
          estimate: 'Стоимость ориентировочная',
          schematic: 'Схема маршрута ориентировочная',
          lines: { car: 'Автомобиль', metrobus: 'Метробус', t1: 'Трамвай T1', m2: 'Метро M2', m11: 'Метро M11', marmaray: 'Мармарай', m4: 'Метро M4', bus: 'Автобус', walk: 'Пешком', ferry: 'Паром', generic: 'Схематично' }
        };

    const showToast = (text, isSuccess = true) => {
      const toast = document.createElement('div');
      toast.className = `glass-panel msg-enter p-4 rounded-2xl text-xs sm:text-sm flex items-center space-x-2 ${
        isSuccess ? 'border-emerald-400/30 text-emerald-200' : 'border-red-400/30 text-red-200'
      }`;
      toast.innerHTML = `<i data-lucide="${isSuccess ? 'check-circle' : 'alert-circle'}" class="w-4 h-4"></i><span>${text}</span>`;
      toastArea.appendChild(toast);
      lucide.createIcons();
      setTimeout(() => toast.remove(), 4000);
    };

    const escapeHtml = (text) => (text || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');

    const formatMessage = (text) => escapeHtml(text)
      .replace(/^\s*[*-]\s+/gm, '• ')
      .replace(/\*\*(.+?)\*\*/g, '<strong class="text-white">$1</strong>')
      .replace(/\*(.+?)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br>');

    const sourceBadge = (label, icon = 'landmark') => `
      <span class="inline-flex items-center gap-1 rounded-full bg-white/5 border border-white/10 px-2 py-0.5 text-[9px] font-semibold uppercase tracking-wider text-slate-300">
        <i data-lucide="${icon}" class="w-3 h-3"></i>${label}
      </span>`;

    const statTile = (label, value, hint = '') => `
      <div class="glass-card rounded-xl px-3 py-2">
        <div class="text-[10px] uppercase tracking-wider text-slate-400">${label}</div>
        <div class="text-sm font-semibold text-white">${value}</div>
        ${hint ? `<div class="text-[10px] text-slate-500">${hint}</div>` : ''}
      </div>`;

    const stepList = (steps) => `
      <div class="space-y-1.5 text-xs text-slate-300">
        ${steps.map(s => `<div class="flex items-start"><i data-lucide="arrow-right" class="w-3 h-3 text-indigo-300 mr-2 mt-0.5 flex-shrink-0"></i><span>${s}</span></div>`).join('')}
      </div>`;

    const routePanel = (option) => {
      if (option.mode === 'car') {
        return `
          <div class="grid grid-cols-2 gap-2">
            ${statTile(copy.distance, `${option.distanceKm} km`)}
            ${statTile(copy.time, copy.freeToPeak(option.durationFree, option.durationPeak), copy.trafficRange)}
            ${statTile(copy.fuel, option.fuelCost)}
            ${statTile(copy.taxi, option.taxiFare)}
          </div>
          <div class="text-xs text-slate-300 flex items-start"><i data-lucide="route" class="w-3.5 h-3.5 text-blue-300 mr-2 mt-0.5 flex-shrink-0"></i><span><span class="text-slate-400">${copy.roads}:</span> ${option.roads}</span></div>
          ${option.tolls.length ? `
            <div class="text-xs text-amber-200/90 space-y-1">
              ${option.tolls.map(t => `<div class="flex items-start"><i data-lucide="badge-dollar-sign" class="w-3.5 h-3.5 mr-2 mt-0.5 flex-shrink-0"></i><span>${t}</span></div>`).join('')}
            </div>` : ''}
          <div class="text-[11px] text-slate-400 flex items-start"><i data-lucide="traffic-cone" class="w-3.5 h-3.5 mr-2 mt-0.5 flex-shrink-0"></i><span>${option.traffic}</span></div>
          <div class="text-[10px] text-slate-500">${copy.estimate}</div>`;
      }
      return `
        <div class="grid grid-cols-2 gap-2">
          ${statTile(copy.time, option.duration)}
          ${statTile(copy.fare, option.fare)}
        </div>
        ${stepList(option.steps)}
        ${option.note ? `<div class="text-[11px] text-sky-200/90 flex items-start"><i data-lucide="sparkles" class="w-3.5 h-3.5 mr-2 mt-0.5 flex-shrink-0"></i><span>${option.note}</span></div>` : ''}`;
    };

    const routeCards = new Map();
    const routeMaps = new Map();
    let routeCardCounter = 0;

    const drawRoute = (cardId, mode) => {
      const entry = routeMaps.get(cardId);
      const option = routeCards.get(cardId)?.options.find(o => o.mode === mode);
      if (!entry || !option) return;
      const { map, layer, legend } = entry;
      layer.clearLayers();
      const points = [];
      (option.segments || []).forEach(segment => {
        const style = LINE_STYLES[segment.kind] || LINE_STYLES.generic;
        L.polyline(segment.path, { color: '#020617', weight: style.weight + 4, opacity: 0.55 }).addTo(layer);
        L.polyline(segment.path, { ...style, opacity: 0.95, lineCap: 'round', lineJoin: 'round' }).addTo(layer);
        points.push(...segment.path);
      });
      (option.stops || []).forEach(stop => {
        const marker = L.circleMarker([stop.lat, stop.lon], STOP_STYLES[stop.role] || STOP_STYLES.transfer).addTo(layer);
        marker.bindTooltip(escapeHtml(stop.name), {
          direction: 'top', offset: [0, -6], className: 'route-label', permanent: stop.role !== 'transfer'
        });
        points.push([stop.lat, stop.lon]);
      });
      if (points.length) map.fitBounds(L.latLngBounds(points), { padding: [28, 28], maxZoom: 14 });
      const kinds = [...new Set((option.segments || []).map(segment => segment.kind))];
      legend.innerHTML = kinds.map(kind => {
        const style = LINE_STYLES[kind] || LINE_STYLES.generic;
        return `<span class="inline-flex items-center gap-1.5"><span class="inline-block w-4 h-1 rounded-full" style="background:${style.color}"></span>${copy.lines[kind] || kind}</span>`;
      }).join('');
    };

    const mountRouteMaps = () => {
      feed.querySelectorAll('[data-route-map]:not([data-ready])').forEach(el => {
        el.dataset.ready = '1';
        const cardId = el.dataset.routeMap;
        const card = el.closest('[data-route-card]');
        if (typeof L === 'undefined') {
          el.hidden = true;
          return;
        }
        const map = L.map(el, { scrollWheelZoom: false, attributionControl: true });
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors',
          maxZoom: 19
        }).addTo(map);
        routeMaps.set(cardId, { map, layer: L.layerGroup().addTo(map), legend: card.querySelector('[data-route-legend]') });
        drawRoute(cardId, card.dataset.activeMode);
      });
    };

    const compactCardContext = (data) => JSON.stringify(data, (key, value) => (['segments', 'stops', 'path'].includes(key) ? undefined : value));

    const renderRouteComparison = (data) => {
      const labels = { car: copy.tabCar, transit: copy.tabTransit, ferry: copy.tabFerry };
      const active = [data.activeMode, data.recommended].find(m => m && data.options.some(o => o.mode === m)) || data.options[0].mode;
      const cardId = `route-${++routeCardCounter}`;
      routeCards.set(cardId, data);
      const hasMap = data.options.some(o => Array.isArray(o.segments) && o.segments.length);
      return `
        <div data-route-card="${cardId}" data-active-mode="${active}" class="accent-frame bg-gradient-to-br from-blue-500/60 via-indigo-400/30 to-violet-500/60 mt-3 shadow-lg shadow-blue-500/10">
          <div class="glass-card p-4 space-y-3">
            <div class="flex items-center justify-between gap-2">
              ${sourceBadge('İBB · Ulaşım', 'tram-front')}
              <span class="text-sm text-blue-200 font-semibold flex items-center"><i data-lucide="navigation" class="w-3.5 h-3.5 mr-1.5"></i>${data.origin} ➔ ${data.destination}</span>
            </div>
            <div class="flex flex-wrap gap-1.5 border-b border-white/10 pb-2">
              ${data.options.map(o => `
                <button type="button" data-route-tab="${o.mode}" class="route-tab${o.mode === active ? ' is-active' : ''}">
                  ${labels[o.mode]}${o.mode === data.recommended ? ` <span class="ml-1 text-[9px] uppercase tracking-wider text-emerald-300">★ ${copy.recommended}</span>` : ''}
                </button>`).join('')}
            </div>
            ${hasMap ? `
              <div class="route-map" data-route-map="${cardId}"></div>
              <div class="flex flex-wrap items-center gap-x-3 gap-y-1 text-[10px] text-slate-300">
                <span data-route-legend class="contents"></span>
                <span class="ml-auto text-slate-500">${copy.schematic}</span>
              </div>` : ''}
            ${data.options.map(o => `
              <div data-route-panel="${o.mode}" class="${o.mode === active ? '' : 'hidden'} space-y-3">
                ${routePanel(o)}
              </div>`).join('')}
          </div>
        </div>`;
    };

    const renderActionWidget = (action) => {
      if (!action) return '';

      // 1. Интерактивная карточка мгновенной оплаты
      if (action.type === 'PAYMENT_CARD') {
        const { serviceId, serviceName, amount, dueDate, unit } = action.data;
        return `
          <div class="accent-frame bg-gradient-to-br from-emerald-400/60 via-cyan-400/30 to-blue-500/60 mt-3 shadow-lg shadow-emerald-500/10">
            <div class="glass-card p-4 space-y-3">
              <div class="flex items-center justify-between">
                ${sourceBadge('İBB · Pay')}
                <span class="text-[10px] text-emerald-300/80">${copy.noFee}</span>
              </div>
              <div class="flex items-center justify-between gap-3">
                <div class="flex items-center space-x-2 min-w-0">
                  <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-emerald-400/25 to-cyan-400/25 border border-emerald-300/20 text-emerald-300 flex items-center justify-center font-bold text-[10px] flex-shrink-0">TRY</div>
                  <div class="min-w-0">
                    <div class="text-sm font-semibold text-white">${serviceName}</div>
                    <div class="text-[11px] text-slate-400">${copy.due}: ${dueDate}</div>
                  </div>
                </div>
                <div class="text-lg font-bold text-emerald-300 whitespace-nowrap">${amount.toFixed(2)} ${unit}</div>
              </div>
              <button data-service-id="${serviceId}" data-amount="${amount}" class="execute-payment-btn w-full py-2.5 bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-white text-xs font-semibold rounded-xl transition-all flex items-center justify-center space-x-2 shadow-lg shadow-emerald-500/25">
                <i data-lucide="check" class="w-3.5 h-3.5"></i>
                <span>${copy.payNow} (${amount.toFixed(2)} TRY)</span>
              </button>
            </div>
          </div>
        `;
      }

      // 2. Карточка маршрута
      if (action.type === 'ROUTE_CARD' && Array.isArray(action.data.options)) {
        return renderRouteComparison(action.data);
      }
      if (action.type === 'ROUTE_CARD') {
        const { origin, destination, fare, duration, steps } = action.data;
        return `
          <div class="accent-frame bg-gradient-to-br from-blue-500/60 via-indigo-400/30 to-violet-500/60 mt-3 shadow-lg shadow-blue-500/10">
            <div class="glass-card p-4 space-y-3">
              <div class="flex items-center justify-between gap-2">
                ${sourceBadge('İBB · Ulaşım', 'tram-front')}
                <span class="bg-blue-500/15 border border-blue-400/20 text-blue-200 px-2 py-0.5 rounded-full font-mono text-[11px]">${duration} • ${fare}</span>
              </div>
              <div class="text-sm text-blue-200 font-semibold flex items-center"><i data-lucide="navigation" class="w-3.5 h-3.5 mr-1.5"></i>${origin} ➔ ${destination}</div>
              <div class="space-y-1.5 border-t border-white/10 pt-2 text-xs text-slate-300">
                ${steps.map(s => `<div class="flex items-start"><i data-lucide="arrow-right" class="w-3 h-3 text-indigo-300 mr-2 mt-0.5 flex-shrink-0"></i><span>${s}</span></div>`).join('')}
              </div>
            </div>
          </div>
        `;
      }

      // 3. Карточка официального руководства (Икамет)
      if (action.type === 'INFO_GUIDE') {
        const { title, portal, requiredDocs } = action.data;
        return `
          <div class="accent-frame bg-gradient-to-br from-emerald-400/50 via-teal-400/25 to-sky-500/50 mt-3 shadow-lg shadow-teal-500/10">
            <div class="glass-card p-4 space-y-2 text-xs">
              <div class="flex items-center justify-between gap-2">
                ${sourceBadge('T.C. Göç İdaresi', 'shield-check')}
                <a href="https://${portal}" target="_blank" rel="noopener" class="text-sky-300 hover:text-sky-200 underline font-mono text-[11px]">${portal}</a>
              </div>
              <div class="font-semibold text-emerald-300 text-sm">${title}</div>
              <div class="text-slate-300">${copy.requiredDocs}</div>
              <ul class="list-disc list-inside text-slate-400 space-y-1">
                ${requiredDocs.map(d => `<li>${d}</li>`).join('')}
              </ul>
            </div>
          </div>
        `;
      }

      // 4. Карточка недвижимости
      if (action.type === 'ESTATE_CARD') {
        const { items = [], location, rooms, searchUrl } = action.data;
        const spec = (label, value) => `
          <div class="min-w-0">
            <div class="text-[9px] uppercase tracking-wider text-slate-500">${label}</div>
            <div class="text-[11px] text-slate-200 truncate">${escapeHtml(value)}</div>
          </div>`;
        return `
          <div class="mt-3 space-y-3">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              ${items.map(it => `
                <a href="${escapeHtml(it.url)}" target="_blank" rel="noopener noreferrer"
                   class="estate-listing accent-frame bg-gradient-to-br from-amber-400/60 via-orange-400/25 to-rose-500/60 shadow-lg shadow-amber-500/10 block">
                  <div class="glass-card p-3 space-y-2 h-full">
                    <div class="flex items-center justify-between gap-2">
                      <span class="inline-flex items-center gap-1 rounded-full bg-white/5 border border-white/10 px-2 py-0.5 text-[9px] font-semibold uppercase tracking-wider text-slate-300">
                        <i data-lucide="image" class="w-3 h-3"></i>${copy.sampleListing}
                      </span>
                      <span class="inline-flex items-center gap-1 text-[10px] font-medium text-amber-200">
                        ${copy.openOnSahibinden}<i data-lucide="external-link" class="w-3 h-3"></i>
                      </span>
                    </div>
                    <div>
                      <div class="text-xs font-semibold text-white leading-snug">${escapeHtml(it.title)}</div>
                      <div class="text-base font-bold text-amber-300 pt-0.5">${Number(it.price).toLocaleString('ru-RU')} ${it.currency}
                        <span class="text-[10px] text-slate-400 font-normal">${it.period}</span>
                      </div>
                    </div>
                    <div class="grid grid-cols-2 gap-x-3 gap-y-1.5 border-t border-white/10 pt-2">
                      ${spec(copy.rooms, it.rooms)}
                      ${spec(copy.area, it.area)}
                      ${spec(copy.floor, it.floor)}
                      ${spec(copy.aidat, it.aidat)}
                    </div>
                    <div class="text-[11px] text-emerald-300 flex items-start"><i data-lucide="train-front" class="w-3.5 h-3.5 mr-1.5 mt-0.5 flex-shrink-0"></i><span>${escapeHtml(it.transit)}</span></div>
                    ${it.features?.length ? `<div class="flex flex-wrap gap-1">${it.features.map(f => `<span class="rounded-full bg-white/5 border border-white/10 px-2 py-0.5 text-[10px] text-slate-300">${escapeHtml(f)}</span>`).join('')}</div>` : ''}
                    <div class="text-[10px] text-amber-200/90 flex items-start"><i data-lucide="shield-alert" class="w-3.5 h-3.5 mr-1.5 mt-0.5 flex-shrink-0"></i><span>${escapeHtml(it.ikamet_status)}</span></div>
                  </div>
                </a>
              `).join('')}
            </div>
            ${searchUrl ? `
              <a href="${escapeHtml(searchUrl)}" target="_blank" rel="noopener noreferrer"
                 class="glass-card flex items-center justify-between gap-2 rounded-xl px-3 py-2 text-xs text-amber-200 hover:bg-white/10 transition">
                <span class="flex items-center gap-2"><i data-lucide="search" class="w-3.5 h-3.5"></i>${escapeHtml(copy.allListings(location, rooms))}</span>
                <i data-lucide="external-link" class="w-3.5 h-3.5 flex-shrink-0"></i>
              </a>` : ''}
          </div>
        `;
      }

      return '';
    };

    const handlePrompt = async (text) => {
      const msg = text || input.value.trim();
      if (!msg) return;

      // Отрисовка сообщения пользователя
      feed.insertAdjacentHTML('beforeend', `
        <div class="msg-enter flex items-start justify-end space-x-2">
          <div class="bg-gradient-to-r from-blue-600/80 to-indigo-600/80 text-white backdrop-blur border border-blue-400/20 shadow-lg shadow-blue-500/10 rounded-2xl rounded-tr-none px-4 py-3 max-w-xl text-sm">
            ${escapeHtml(msg)}
          </div>
        </div>
      `);
      input.value = '';
      feed.scrollTop = feed.scrollHeight;

      // Лоадер
      const loadId = `load-${Date.now()}`;
      feed.insertAdjacentHTML('beforeend', `
        <div id="${loadId}" class="glass-card inline-flex items-center space-x-2 text-xs text-slate-300 px-3 py-2 rounded-full">
          <div class="w-2 h-2 rounded-full bg-blue-400 animate-pulse shadow-[0_0_8px_rgba(96,165,250,0.9)]"></div>
          <span>${copy.loader}</span>
        </div>
      `);
      feed.scrollTop = feed.scrollHeight;

      try {
        if (ROUTE_FROM_HERE.test(msg) && !readSessionOrigin()) {
          const located = await resolveOrigin();
          if (located.fallback) showToast(located.hint, false);
          saveSessionOrigin(located.origin);
        }
        const res = await ApiService.sendAIOrchestration(msg, DashboardView.currentLang, conversationHistory, readSessionOrigin());
        document.getElementById(loadId)?.remove();

        if (res.intent !== 'FALLBACK') {
          const cardContext = res.action ? `\n${compactCardContext(res.action.data)}` : '';
          conversationHistory.push(
            { role: 'user', content: msg },
            { role: 'assistant', content: `${res.message}${cardContext}` }
          );
          conversationHistory.splice(0, Math.max(0, conversationHistory.length - MAX_HISTORY));
        }

        feed.insertAdjacentHTML('beforeend', `
          <div class="msg-enter flex items-start space-x-3">
            <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-blue-500/30 to-indigo-500/30 border border-blue-400/30 flex items-center justify-center text-blue-300 flex-shrink-0">
              <i data-lucide="bot" class="w-4 h-4"></i>
            </div>
            <div class="glass-panel text-slate-100 border-white/10 rounded-2xl rounded-tl-none p-4 max-w-2xl space-y-2 text-sm">
              <div class="leading-relaxed">${formatMessage(res.message)}</div>
              ${renderActionWidget(res.action)}
              <div class="text-[10px] text-slate-400 pt-2 border-t border-white/10 flex items-center justify-between gap-2">
                <span>${copy.source}: ${escapeHtml(res.grounded_source)}</span>
                <span class="text-emerald-300 font-medium whitespace-nowrap">${copy.verified}</span>
              </div>
            </div>
          </div>
        `);

        mountRouteMaps();

        // Динамическое добавление событий на кнопку оплаты внутри карточки
        document.querySelectorAll('.execute-payment-btn').forEach(b => {
          b.onclick = async () => {
            b.disabled = true;
            b.innerHTML = copy.processing;
            try {
              const payRes = await ApiService.processPayment(1, parseInt(b.dataset.serviceId), parseFloat(b.dataset.amount));
              showToast(`${copy.payOk} #${payRes.transactionId}`);
              b.className = 'w-full py-2.5 glass-card text-emerald-300 border border-emerald-400/30 text-xs font-semibold rounded-xl';
              b.innerHTML = copy.paid;
            } catch (err) {
              const detail = err.message === 'NETWORK' ? copy.retryHint : err.message;
              showToast(`${copy.payError}: ${detail}`, false);
              b.disabled = false;
              b.innerHTML = copy.retry;
            }
          };
        });

      } catch (err) {
        document.getElementById(loadId)?.remove();
        feed.insertAdjacentHTML('beforeend', `
          <div class="msg-enter glass-panel p-4 border-red-400/30 rounded-2xl text-xs text-red-200">
            ${copy.aiFail}${err.message === 'NETWORK' ? '' : ` (${err.message})`}. ${copy.retryHint}
          </div>
        `);
      }

      lucide.createIcons();
      feed.scrollTop = feed.scrollHeight;
    };

    form.onsubmit = (e) => {
      e.preventDefault();
      handlePrompt();
    };

    chips.forEach(c => {
      c.onclick = () => handlePrompt(c.dataset.prompt);
    });

    feed.addEventListener('click', (e) => {
      const tab = e.target.closest('[data-route-tab]');
      if (!tab) return;
      const card = tab.closest('[data-route-card]');
      card.querySelectorAll('[data-route-tab]').forEach(b => b.classList.toggle('is-active', b === tab));
      card.querySelectorAll('[data-route-panel]').forEach(p => {
        p.classList.toggle('hidden', p.dataset.routePanel !== tab.dataset.routeTab);
      });
      card.dataset.activeMode = tab.dataset.routeTab;
      drawRoute(card.dataset.routeCard, tab.dataset.routeTab);
    });

    const plannerBtn = document.getElementById('routePlannerBtn');
    const plannerModal = document.getElementById('routePlannerModal');
    const plannerOrigin = document.getElementById('plannerOrigin');
    const plannerOriginHint = document.getElementById('plannerOriginHint');
    const plannerDestination = document.getElementById('plannerDestination');
    const plannerPopular = document.querySelectorAll('#plannerPopular [data-destination]');

    const openPlanner = (origin, hint) => {
      plannerOrigin.value = origin;
      plannerOriginHint.textContent = `${hint} · ${copy.editableHint}`;
      plannerDestination.value = '';
      plannerPopular.forEach(b => { b.hidden = false; });
      plannerModal.classList.remove('hidden');
      lucide.createIcons();
      plannerDestination.focus();
    };

    const closePlanner = () => plannerModal.classList.add('hidden');

    const submitRoute = (destination) => {
      const to = (destination || '').trim();
      if (!to) {
        plannerDestination.focus();
        return;
      }
      const from = plannerOrigin.value.trim() || DEFAULT_ORIGIN;
      saveSessionOrigin(from);
      closePlanner();
      handlePrompt(copy.routeMessage(from, to));
    };

    const resolveOrigin = () => new Promise((resolve) => {
      if (!navigator.geolocation) {
        resolve({ origin: DEFAULT_ORIGIN, hint: copy.geoDenied, fallback: true });
        return;
      }
      navigator.geolocation.getCurrentPosition(
        ({ coords }) => {
          const here = { lat: coords.latitude, lon: coords.longitude };
          if (distanceKm(here, ISTANBUL_CENTER) > ISTANBUL_RADIUS_KM) {
            resolve({ origin: DEFAULT_ORIGIN, hint: copy.geoOutside, fallback: true });
            return;
          }
          const nearest = DISTRICT_CENTERS.reduce((best, d) => (distanceKm(here, d) < distanceKm(here, best) ? d : best));
          resolve({ origin: nearest.name, hint: copy.geoDetected, fallback: false });
        },
        () => resolve({ origin: DEFAULT_ORIGIN, hint: copy.geoDenied, fallback: true }),
        { enableHighAccuracy: false, timeout: 8000, maximumAge: 600000 }
      );
    });

    plannerBtn.onclick = async () => {
      plannerBtn.disabled = true;
      const label = plannerBtn.querySelector('span');
      const original = label.textContent;
      label.textContent = copy.locating;
      const { origin, hint, fallback } = await resolveOrigin();
      label.textContent = original;
      plannerBtn.disabled = false;
      if (fallback) showToast(hint, false);
      openPlanner(fallback ? (readSessionOrigin() || origin) : origin, hint);
    };

    plannerModal.querySelectorAll('[data-planner-close]').forEach(el => { el.onclick = closePlanner; });
    plannerPopular.forEach(b => { b.onclick = () => submitRoute(b.dataset.destination); });
    document.getElementById('plannerSubmit').onclick = () => submitRoute(plannerDestination.value);

    plannerDestination.oninput = () => {
      const query = plannerDestination.value.trim().toLowerCase();
      plannerPopular.forEach(b => { b.hidden = Boolean(query) && !b.dataset.search.includes(query); });
    };
    plannerModal.onkeydown = (e) => {
      if (e.key === 'Escape') closePlanner();
      if (e.key === 'Enter' && e.target === plannerDestination) submitRoute(plannerDestination.value);
    };
  }
};