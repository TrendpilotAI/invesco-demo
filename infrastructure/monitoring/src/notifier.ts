/**
 * Notifier — sends alerts to Telegram and/or Discord
 *
 * Telegram: uses Bot API (TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID env vars)
 * Discord:  uses Webhook URL (DISCORD_WEBHOOK_URL env var)
 */

export interface NotifierConfig {
  telegramBotToken?: string;
  telegramChatId?: string;
  discordWebhookUrl?: string;
  /** Dry-run mode: log instead of sending */
  dryRun?: boolean;
}

export class Notifier {
  private cfg: NotifierConfig;

  constructor(cfg?: NotifierConfig) {
    this.cfg = cfg ?? {
      telegramBotToken: process.env.TELEGRAM_BOT_TOKEN,
      telegramChatId: process.env.TELEGRAM_CHAT_ID,
      discordWebhookUrl: process.env.DISCORD_WEBHOOK_URL,
      dryRun: process.env.ALERT_DRY_RUN === "true",
    };
  }

  async send(text: string): Promise<void> {
    if (this.cfg.dryRun) {
      console.log("[DRY-RUN] Would send alert:\n" + text);
      return;
    }
    const results = await Promise.allSettled([
      this.sendTelegram(text),
      this.sendDiscord(text),
    ]);
    for (const r of results) {
      if (r.status === "rejected") console.error("[Notifier] delivery error:", r.reason);
    }
  }

  private async sendTelegram(text: string): Promise<void> {
    const { telegramBotToken: token, telegramChatId: chatId } = this.cfg;
    if (!token || !chatId) return;

    const url = `https://api.telegram.org/bot${token}/sendMessage`;
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_id: chatId, text, parse_mode: "HTML" }),
    });
    if (!res.ok) {
      const body = await res.text();
      throw new Error(`Telegram API error ${res.status}: ${body}`);
    }
    console.log("[Notifier] Telegram ✓");
  }

  private async sendDiscord(text: string): Promise<void> {
    const { discordWebhookUrl: webhookUrl } = this.cfg;
    if (!webhookUrl) return;

    // Strip HTML tags for Discord (uses markdown, not HTML)
    const plain = text
      .replace(/<b>(.*?)<\/b>/gi, "**$1**")
      .replace(/<i>(.*?)<\/i>/gi, "_$1_")
      .replace(/<[^>]+>/g, "");

    const res = await fetch(webhookUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: plain }),
    });
    if (!res.ok) {
      const body = await res.text();
      throw new Error(`Discord webhook error ${res.status}: ${body}`);
    }
    console.log("[Notifier] Discord ✓");
  }
}
