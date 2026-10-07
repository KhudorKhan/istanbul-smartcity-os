import { ApiService } from '../services/api.js';

export const AIAssistantView = {
  render() {
    return `
      <div class="h-full flex flex-col bg-gray-900 border border-gray-800 rounded-2xl overflow-hidden shadow-2xl">
        <!-- Chat Header -->
        <div class="px-6 py-4 bg-gray-800/80 backdrop-blur border-b border-gray-700/60 flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
              <i data-lucide="bot" class="w-5 h-5"></i>
            </div>
            <div>
              <div class="flex items-center space-x-2">
                <h3 class="text-sm font-semibold text-white">SmartCity RAG Copilot</h3>
                <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  <span class="w-1.5 h-1.5 mr-1.5 rounded-full bg-emerald-400 live-indicator"></span>
                  Grounded (Anti-Hallucination)
                </span>
              </div>
              <p class="text-xs text-gray-400">Официальные городские регламенты и тарифы</p>
            </div>
          </div>
          <button id="clearChatBtn" class="p-2 text-gray-400 hover:text-gray-200 hover:bg-gray-700/50 rounded-lg transition" title="Очистить историю">
            <i data-lucide="trash-2" class="w-4 h-4"></i>
          </button>
        </div>

        <!-- Chat Messages Viewport -->
        <div id="chatMessages" class="flex-1 p-6 overflow-y-auto space-y-4">
          <!-- Welcome Message -->
          <div class="flex items-start space-x-3">
            <div class="w-8 h-8 rounded-lg bg-blue-600/20 flex-shrink-0 flex items-center justify-center text-blue-400">
              <i data-lucide="sparkles" class="w-4 h-4"></i>
            </div>
            <div class="bg-gray-800 border border-gray-700/60 rounded-2xl rounded-tl-none p-4 max-w-xl text-sm text-gray-200 leading-relaxed shadow-sm">
              Здравствуйте! Я официальный ИИ-ассистент умного города. Мои ответы строго верифицируются городской базой знаний, исключая неточные данные и галлюцинации. Чем я могу помочь?
            </div>
          </div>
        </div>

        <!-- Suggested Prompts Chips -->
        <div class="px-6 py-2 bg-gray-900 border-t border-gray-800 flex items-center space-x-2 overflow-x-auto text-xs">
          <span class="text-gray-500 flex-shrink-0">Частые вопросы:</span>
          <button class="suggested-chip px-3 py-1 bg-gray-800 hover:bg-gray-700 border border-gray-700 text-gray-300 rounded-full transition whitespace-nowrap">
            Сколько стоит проезд на автобусе?
          </button>
          <button class="suggested-chip px-3 py-1 bg-gray-800 hover:bg-gray-700 border border-gray-700 text-gray-300 rounded-full transition whitespace-nowrap">
            Тарифы на воду İSKİ
          </button>
          <button class="suggested-chip px-3 py-1 bg-gray-800 hover:bg-gray-700 border border-gray-700 text-gray-300 rounded-full transition whitespace-nowrap">
            Стоимость парковки ISPARK
          </button>
        </div>

        <!-- Chat Input Form -->
        <div class="p-4 bg-gray-800/60 border-t border-gray-700/60">
          <form id="chatForm" class="flex items-center space-x-2">
            <input 
              type="text" 
              id="chatInput" 
              placeholder="Задайте вопрос о городских услугах (Enter для отправки)..." 
              class="flex-1 bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 transition"
              autocomplete="off"
            />
            <button 
              type="submit" 
              id="sendBtn"
              class="px-5 py-3 bg-blue-600 hover:bg-blue-500 active:scale-95 text-white text-sm font-medium rounded-xl transition flex items-center space-x-1.5 shadow-lg shadow-blue-600/20 disabled:opacity-50"
            >
              <span>Отправить</span>
              <i data-lucide="send" class="w-4 h-4"></i>
            </button>
          </form>
        </div>
      </div>
    `;
  },

  attachEvents() {
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatMessages = document.getElementById('chatMessages');
    const clearChatBtn = document.getElementById('clearChatBtn');
    const chips = document.querySelectorAll('.suggested-chip');

    const scrollToBottom = () => {
      chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    const handleSendMessage = async (text) => {
      const question = text || chatInput.value.trim();
      if (!question) return;

      // 1. Рендерим сообщение пользователя
      chatMessages.innerHTML += `
        <div class="flex items-start justify-end space-x-3">
          <div class="bg-blue-600 rounded-2xl rounded-tr-none p-4 max-w-xl text-sm text-white leading-relaxed shadow-sm">
            ${question}
          </div>
        </div>
      `;
      chatInput.value = '';
      chatInput.disabled = true;
      document.getElementById('sendBtn').disabled = true;
      scrollToBottom();

      // 2. Индикатор загрузки
      const loadingId = `loading-${Date.now()}`;
      chatMessages.innerHTML += `
        <div id="${loadingId}" class="flex items-start space-x-3">
          <div class="w-8 h-8 rounded-lg bg-blue-600/20 flex-shrink-0 flex items-center justify-center text-blue-400">
            <i data-lucide="bot" class="w-4 h-4"></i>
          </div>
          <div class="bg-gray-800 border border-gray-700/60 rounded-2xl rounded-tl-none p-4 text-sm text-gray-400 flex items-center space-x-2">
            <div class="w-2 h-2 rounded-full bg-blue-500 animate-bounce"></div>
            <div class="w-2 h-2 rounded-full bg-blue-500 animate-bounce" style="animation-delay: 0.2s"></div>
            <div class="w-2 h-2 rounded-full bg-blue-500 animate-bounce" style="animation-delay: 0.4s"></div>
            <span class="text-xs ml-2">Верификация в базе регламентов...</span>
          </div>
        </div>
      `;
      lucide.createIcons();
      scrollToBottom();

      // 3. Запрос к реальному бэкенду
      try {
        const response = await ApiService.queryAI(question);
        document.getElementById(loadingId)?.remove();

        chatMessages.innerHTML += `
          <div class="flex items-start space-x-3">
            <div class="w-8 h-8 rounded-lg bg-blue-600/20 flex-shrink-0 flex items-center justify-center text-blue-400">
              <i data-lucide="sparkles" class="w-4 h-4"></i>
            </div>
            <div class="bg-gray-800 border border-gray-700/60 rounded-2xl rounded-tl-none p-4 max-w-xl space-y-3 shadow-sm">
              <p class="text-sm text-gray-200 leading-relaxed">${response.answer}</p>
              
              <!-- Grounding & RAG Citation Box -->
              <div class="pt-2 border-t border-gray-700/40 text-xs flex flex-col space-y-1">
                <div class="flex items-center justify-between text-gray-400">
                  <span class="flex items-center"><i data-lucide="shield-check" class="w-3.5 h-3.5 mr-1 text-emerald-400"></i> Первоисточник:</span>
                  <span class="badge-rag-low px-2 py-0.5 rounded text-[10px] font-semibold">${response.hallucination_risk}</span>
                </div>
                <div class="bg-gray-900/60 p-2 rounded text-gray-400 font-mono text-[11px] border border-gray-800">
                  ${response.source_context}
                </div>
              </div>
            </div>
          </div>
        `;
      } catch (err) {
        document.getElementById(loadingId)?.remove();
        chatMessages.innerHTML += `
          <div class="flex items-start space-x-3">
            <div class="w-8 h-8 rounded-lg bg-red-600/20 flex-shrink-0 flex items-center justify-center text-red-400">
              <i data-lucide="alert-circle" class="w-4 h-4"></i>
            </div>
            <div class="bg-red-950/40 border border-red-800/50 rounded-2xl rounded-tl-none p-4 max-w-xl text-sm text-red-300">
              ИИ-ассистент временно недоступен, повторите запрос чуть позже.${err.message === 'NETWORK' ? '' : ` (${err.message})`}
            </div>
          </div>
        `;
      } finally {
        chatInput.disabled = false;
        document.getElementById('sendBtn').disabled = false;
        chatInput.focus();
        lucide.createIcons();
        scrollToBottom();
      }
    };

    chatForm.addEventListener('submit', (e) => {
      e.preventDefault();
      handleSendMessage();
    });

    chips.forEach(chip => {
      chip.addEventListener('click', () => {
        handleSendMessage(chip.innerText.trim());
      });
    });

    clearChatBtn.addEventListener('click', () => {
      chatMessages.innerHTML = `
        <div class="flex items-start space-x-3">
          <div class="w-8 h-8 rounded-lg bg-blue-600/20 flex-shrink-0 flex items-center justify-center text-blue-400">
            <i data-lucide="sparkles" class="w-4 h-4"></i>
          </div>
          <div class="bg-gray-800 border border-gray-700/60 rounded-2xl rounded-tl-none p-4 max-w-xl text-sm text-gray-200">
            Диалог очищен. Чем я могу помочь вам сейчас?
          </div>
        </div>
      `;
      lucide.createIcons();
    });
  }
};