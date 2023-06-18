from handlers.base import BaseHandler


class HelpHandler(BaseHandler):
    command = '/help'

    def __init__(self):
        pass

    def answer(self, args: str = None, **kwargs) -> tuple[str, dict]:
        bot_description = (
            "🤖 Добро пожаловать в наш Telegram бот для отслеживания цен товаров на "
            "Яндекс.Маркет ! 🤖\nВот список доступных команд:\n\n"
        )
        command_descriptions = {
            "/add <ссылка на товар>": (
                "Добавить товар для отслеживания. Товару будет присвоен уникальный "
                "ID."
            ),
            "/del <ID товара>": (
                "Удалить товар из списка отслеживаемых товаров по его ID."
            ),
            "/list [номер страницы] [размер страницы]": (
                "Получить список отслеживаемых товаров. Номер страницы и размер "
                "страницы являются необязательными."
            ),
            "/plot <ID товара>": "Получить график истории цены товара по его ID.",
            "/help": "Получить эту справочную информацию.",
        }
        help_text = bot_description + '\n'.join(
            f"{command}: {description}"
            for command, description in command_descriptions.items()
        )
        return 'text', {'text': help_text}
