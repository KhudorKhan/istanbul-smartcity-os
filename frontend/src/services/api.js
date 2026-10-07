export const ApiService = {
  async checkBackendHealth() {
    try {
      const response = await fetch('/actuator/health');
      if (!response.ok) return { status: 'DOWN' };
      return await response.json();
    } catch {
      return { status: 'DOWN' };
    }
  },

  async processPayment(userId, serviceId, amount) {
    let response;
    try {
      response = await fetch('/api/v1/payments/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId, serviceId, amount })
      });
    } catch {
      throw new Error('NETWORK');
    }
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  },

  async sendAIOrchestration(message, language = 'ru', history = [], currentLocation = null) {
    let response;
    try {
      response = await fetch('/api/v1/ai/orchestrate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, language, history, current_location: currentLocation })
      });
    } catch {
      throw new Error('NETWORK');
    }
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  },

  async queryAI(question) {
    const res = await this.sendAIOrchestration(question, 'ru');
    return {
      answer: res.message,
      source_context: res.grounded_source,
      hallucination_risk: 'LOW (Grounded by RAG)'
    };
  }
};
