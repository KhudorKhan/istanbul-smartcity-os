import { DashboardView } from './views/dashboard.js';

class App {
  constructor() {
    this.contentEl = document.getElementById('appContent');
  }

  async init() {
    this.setupLanguageSwitcher();
    await this.renderCurrentView();
  }

  setupLanguageSwitcher() {
    const ruBtn = document.getElementById('langRuBtn');
    const trBtn = document.getElementById('langTrBtn');

    if (ruBtn && trBtn) {
      ruBtn.addEventListener('click', async () => {
        DashboardView.currentLang = 'ru';
        ruBtn.className = 'px-2.5 py-1 rounded-lg bg-blue-600 text-white font-medium transition';
        trBtn.className = 'px-2.5 py-1 rounded-lg text-gray-400 hover:text-white transition';
        await this.renderCurrentView();
      });

      trBtn.addEventListener('click', async () => {
        DashboardView.currentLang = 'tr';
        trBtn.className = 'px-2.5 py-1 rounded-lg bg-blue-600 text-white font-medium transition';
        ruBtn.className = 'px-2.5 py-1 rounded-lg text-gray-400 hover:text-white transition';
        await this.renderCurrentView();
      });
    }
  }

  async renderCurrentView() {
    if (this.contentEl) {
      this.contentEl.innerHTML = DashboardView.render();
      DashboardView.attachEvents();
      if (window.lucide) {
        window.lucide.createIcons();
      }
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const app = new App();
  app.init();
});
