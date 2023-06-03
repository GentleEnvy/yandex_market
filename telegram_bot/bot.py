import telegram

from handlers.base import BaseHandler
from handlers.get_plot import GetPlotHandler
from handlers.get_products import GetProductsHandler


class Bot:
    def __init__(self, token: str, **kwargs):
        self._bot = telegram.Bot(token, **kwargs)
        self.commands = self._collect_handlers(GetProductsHandler(), GetPlotHandler())

    def _collect_handlers(self, *handlers: BaseHandler) -> dict[str, BaseHandler]:
        commands = {}
        for handler in handlers:
            commands[handler.command] = handler
        return commands

    async def listen(self):
        updates = await self._bot.get_updates()
        last_update_id = updates[0].update_id if updates else None
        while True:
            async with self._bot:
                try:
                    updates = await self._bot.get_updates(offset=last_update_id)
                except telegram.error.TimedOut:
                    continue
                for update in updates:
                    print(f"{update = }")
                    query = update.message.text
                    try:
                        answer_type, answer = self.get_answer(query)
                        match answer_type:
                            case 'text':
                                await update.message.chat.send_message(**answer)
                            case 'photo':
                                await update.message.chat.send_photo(**answer)
                            case _:
                                raise TypeError(f"Invalid answer_type: {answer_type}")
                    except Exception as exc:
                        print(exc)
                        await update.message.chat.send_message("Ой, всё сломалось")
                    last_update_id = update.update_id + 1

    def get_answer(self, query: str) -> tuple[str, dict]:
        query.rsplit()
        command, args = query.split(maxsplit=1) if ' ' in query else (query, None)
        try:
            handler = self.commands[command]
        except KeyError:
            return 'text', {'text': "Нет такой команды"}
        try:
            return handler.answer(args)
        except ValueError:
            return 'text', {'text': "Неверные аргументы команды"}