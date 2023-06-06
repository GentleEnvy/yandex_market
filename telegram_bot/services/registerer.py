from typing import Any

from telegram import Update

from services.api_requester import APIRequester


class Registerer:
    def __init__(self):
        self.api_requester = APIRequester()

    def register(self, update: Update) -> int:
        user_info = self._extract_user_info(update)
        self.api_requester.post_register_telegram(**user_info)
        return user_info['user_id']

    def _extract_user_info(self, update: Update) -> dict[str, Any]:
        return {
            'user_id': update.message.from_user.id,
            'username': update.message.from_user.username,
            'first_name': update.message.from_user.first_name,
            'last_name': getattr(update.message.from_user, 'last_name', None),
        }
