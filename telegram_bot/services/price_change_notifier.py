from typing import Any

import telegram


class PriceChangeNotifier:
    def __init__(self, bot: telegram.Bot):
        self.bot = bot

    async def notify(self, changes: list[dict[str, Any]]) -> None:
        for user_with_changes in changes:
            user_id = user_with_changes['telegram_id']
            for change in user_with_changes['changes']:
                text = self._form_text(change)
                await self.bot.send_message(
                    text=text,
                    chat_id=user_id,
                    disable_web_page_preview=True,
                    parse_mode='Markdown',
                )

    def _form_text(self, change: dict[str, Any]) -> str:
        id, name, url = change['id'], change['name'], change['url']
        old_price, new_price = change['old_price'], change['new_price']
        diff_price = old_price - new_price
        if diff_price > 0:
            return f"""📉 Уведомление о снижении цены ! 📉

Цена на товар [{name}]({url}) (ID: {id}) снизилась !

💸 Старая цена: *{old_price}* ₽
💰 Новая цена: *{new_price}* ₽

Ваша экономия составит: *{diff_price}* ₽"""
        return f"""📈 Уведомление о повышении цены ! 📈

Цена на товар [{name}]({url}) (ID: {id}) поднялась.

💸 Старая цена: *{old_price}* ₽
💰 Новая цена: *{new_price}* ₽"""
