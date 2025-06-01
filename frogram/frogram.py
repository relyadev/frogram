import requests
from typing import Dict, Optional, Union, List
import debugmes


def inline_keyboard(rows: List[List[Dict]]) -> Dict:
    """Create inline-keyboard"""
    return {"inline_keyboard": rows}


def reply_keyboard(
    rows: List[List[Dict]],
    resize_keyboard: bool = True,
    one_time_keyboard: bool = False,
    selective: bool = False,
) -> Dict:
    """Create reply-клавиатуру"""
    return {
        "keyboard": rows,
        "resize_keyboard": resize_keyboard,
        "one_time_keyboard": one_time_keyboard,
        "selective": selective,
    }


def remove_keyboard(selective: bool = False) -> Dict:
    """Delete reply-keyboard"""
    return {"remove_keyboard": True, "selective": selective}


def keyboard_button(
    text: str,
    request_contact: bool = False,
    request_location: bool = False,
    request_poll: Dict = None,
) -> Dict:
    """Create button for reply-keyboard"""
    button = {"text": text}
    if request_contact:
        button["request_contact"] = True
    if request_location:
        button["request_location"] = True
    if request_poll:
        button["request_poll"] = request_poll
    return button


def inline_button(
    text: str,
    callback_data: str = None,
    url: str = None,
    pay: bool = False,
    login_url: Dict = None,
    switch_inline_query: str = None,
    switch_inline_query_current_chat: str = None,
) -> Dict:
    """Create inline-button"""
    button = {"text": text}
    if callback_data:
        button["callback_data"] = callback_data
    if url:
        button["url"] = url
    if pay:
        button["pay"] = pay
    if login_url:
        button["login_url"] = login_url
    if switch_inline_query:
        button["switch_inline_query"] = switch_inline_query
    if switch_inline_query_current_chat:
        button["switch_inline_query_current_chat"] = switch_inline_query_current_chat
    return button


class Bot:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.command_handlers = {}
        self.message_handlers = []
        self.photo_handlers = []  # Handler for images
        self.callback_handlers = []  # callback-requests
        self._current_context = None
        self.running = False
        self.last_bot_messages: Dict[int, int] = {}  # {chat_id: message_id}

    def on_command(self, command: str):
        """Decorator for registering command handlers"""

        def decorator(func):
            self.command_handlers[command] = func
            return func

        return decorator

    def on_message(self, func):
        """Decorator for text message handlers"""
        self.message_handlers.append(func)
        return func

    def on_photo(self, func):
        """Decorator for photo message handlers"""
        self.photo_handlers.append(func)
        return func

    def on_callback(self, func):
        """Decorator for callback query handlers"""
        self.callback_handlers.append(func)
        return func

    def send_message(
        self,
        text: str,
        chat_id: Optional[int] = None,
        reply_markup: Optional[Dict] = None,
        parse_mode: Optional[str] = None,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        **kwargs,
    ) -> Dict:
        """
        Sends a message to the specified chat with optional keyboard
        :param text: Message text
        :param chat_id: Chat ID (if None, uses current context)
        :param reply_markup: Keyboard markup (inline or reply)
        :param parse_mode: Markdown or HTML formatting
        :param disable_web_page_preview: Disable link previews
        :param disable_notification: Send silently
        :param reply_to_message_id: Reply to specific message
        :return: Telegram API response
        """
        if chat_id is None and self._current_context:
            chat_id = self._current_context.message.get("chat", {}).get("id")

        if not chat_id:
            raise ValueError("Chat ID must be specified")

        url = f"https://api.telegram.org/bot{self.api_key}/sendMessage"
        params = {
            "chat_id": chat_id,
            "text": text,
            "reply_markup": reply_markup,
            "parse_mode": parse_mode,
            "disable_web_page_preview": disable_web_page_preview,
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id,
        }
        params.update(kwargs)
        params = {k: v for k, v in params.items() if v is not None}

        response = requests.post(url, json=params)

        if response.ok:
            message_id = response.json().get("result", {}).get("message_id")
            if message_id:
                self.last_bot_messages[chat_id] = message_id

        return response.json()

    def send(self, text: str, chat_id: Optional[int] = None) -> Dict:
        """Legacy send method for backward compatibility"""
        return self.send_message(text, chat_id)

    def send_photo(
        self,
        photo_url: str,
        caption: str = "",
        chat_id: Optional[int] = None,
        reply_markup: Optional[Dict] = None,
        parse_mode: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        **kwargs,
    ) -> Dict:
        """
        Sends a photo to the specified chat with optional keyboard
        :param photo_url: URL of the photo
        :param caption: Photo caption
        :param chat_id: Chat ID
        :param reply_markup: Keyboard markup (inline or reply)
        :param parse_mode: Markdown or HTML formatting
        :param disable_notification: Send silently
        :param reply_to_message_id: Reply to specific message
        :return: Telegram API response
        """
        if chat_id is None and self._current_context:
            chat_id = self._current_context.message.get("chat", {}).get("id")

        if not chat_id:
            raise ValueError("Chat ID must be specified")

        url = f"https://api.telegram.org/bot{self.api_key}/sendPhoto"
        params = {
            "chat_id": chat_id,
            "photo": photo_url,
            "caption": caption,
            "reply_markup": reply_markup,
            "parse_mode": parse_mode,
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id,
        }
        params.update(kwargs)
        params = {k: v for k, v in params.items() if v is not None}

        response = requests.post(url, json=params)
        return response.json()

    def edit_message_reply_markup(
        self,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        reply_markup: Optional[Dict] = None,
    ) -> Dict:
        """
        Edits only the reply markup of a message
        :param chat_id: Chat ID (required if inline_message_id not specified)
        :param message_id: Message ID (required if inline_message_id not specified)
        :param inline_message_id: Inline message ID (required if chat_id and message_id not specified)
        :param reply_markup: New inline keyboard
        :return: Telegram API response
        """
        if not any([inline_message_id, all([chat_id, message_id])]):
            raise ValueError(
                "Either inline_message_id or both chat_id and message_id must be specified"
            )

        url = f"https://api.telegram.org/bot{self.api_key}/editMessageReplyMarkup"
        params = {
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
            "reply_markup": reply_markup,
        }
        params = {k: v for k, v in params.items() if v is not None}

        response = requests.post(url, json=params)
        return response.json()

    def delete(
        self, chat_id: Optional[int] = None, message_id: Optional[int] = None
    ) -> Dict:
        """
        Deletes a message in chat
        :param chat_id: Chat ID (if None, uses current context)
        :param message_id: Message ID (if None, uses last sent message)
        :return: Telegram API response
        """
        if chat_id is None and self._current_context:
            chat_id = self._current_context.message.get("chat", {}).get("id")

        if message_id is None and chat_id in self.last_bot_messages:
            message_id = self.last_bot_messages.get(chat_id)

        if not chat_id or not message_id:
            raise ValueError("Chat ID and Message ID must be specified")

        url = f"https://api.telegram.org/bot{self.api_key}/deleteMessage"
        params = {"chat_id": chat_id, "message_id": message_id}
        response = requests.post(url, params=params)
        return response.json()

    def get_file_url(self, file_id: str) -> str:
        """
        Returns file URL by its ID
        :param file_id: Telegram file ID
        :return: File download URL
        """
        # Get file info
        file_info_url = (
            f"https://api.telegram.org/bot{self.api_key}/getFile?file_id={file_id}"
        )
        file_info = requests.get(file_info_url).json()

        if file_info.get("ok"):
            file_path = file_info["result"]["file_path"]
            return f"https://api.telegram.org/file/bot{self.api_key}/{file_path}"
        return ""

    def answer_callback_query(
        self,
        callback_query_id: str,
        text: str = None,
        show_alert: bool = False,
        url: str = None,
        cache_time: int = 0,
    ) -> Dict:
        """
        Answers a callback query
        :param callback_query_id: Callback query ID
        :param text: Notification text
        :param show_alert: Show as alert instead of notification
        :param url: URL to open
        :param cache_time: Cache time in seconds
        :return: Telegram API response
        """
        url_api = f"https://api.telegram.org/bot{self.api_key}/answerCallbackQuery"
        params = {
            "callback_query_id": callback_query_id,
            "text": text[:200] if text else None,  # Ограничение длины текста
            "show_alert": show_alert,
            "url": url,
            "cache_time": cache_time,
        }
        params = {k: v for k, v in params.items() if v is not None}
        response = requests.post(url_api, json=params)
        return response.json()

    def process_message(self, message: Dict):
        """Processes incoming message"""
        context = Context(message, self)
        self._current_context = context

        # Command processing (works for both text and photo captions)
        command_text = message.get("text", "") or message.get("caption", "")
        if command_text and command_text.startswith("/"):
            command = command_text.split()[0][1:].split("@")[0]
            if command in self.command_handlers:
                try:
                    self.command_handlers[command](context)
                except Exception as e:
                    debugmes.error(f"In command handler: {e}")
                return

        # Photo processing
        if "photo" in message and self.photo_handlers:
            for handler in self.photo_handlers:
                try:
                    handler(context)
                except Exception as e:
                    debugmes.error(f"In photo handler: {e}")
            return

        # Text message processing
        if "text" in message and self.message_handlers:
            for handler in self.message_handlers:
                try:
                    handler(context)
                except Exception as e:
                    debugmes.error(f"In message handler: {e}")

    def process_callback_query(self, callback_query: Dict):
        """Processes callback query"""
        context = CallbackContext(callback_query, self)
        self._current_context = context

        for handler in self.callback_handlers:
            try:
                handler(context)
            except Exception as e:
                debugmes.error(f"In callback handler: {e}")

    def start_polling(self, interval: int = 1, timeout: int = 30):
        """Starts infinite polling loop"""
        self.running = True
        offset = 0

        debugmes.success("Bot started polling...")
        while self.running:
            try:
                url = f"https://api.telegram.org/bot{self.api_key}/getUpdates"
                params = {
                    "offset": offset,
                    "timeout": timeout,
                    "allowed_updates": ["message", "callback_query", "photo"],
                }

                response = requests.get(url, params=params)
                data = response.json()

                if not data.get("ok", False):
                    debugmes.critical(
                        f"API Error: {data.get('description', 'Unknown error')}"
                    )
                    exit()

                for update in data.get("result", []):
                    offset = update["update_id"] + 1
                    if "message" in update:
                        self.process_message(update["message"])
                    elif "callback_query" in update:
                        self.process_callback_query(update["callback_query"])

            except requests.exceptions.RequestException as e:
                debugmes.critical(f"{e}")
                exit()
            except Exception as e:
                debugmes.critical(f"{e}")
                exit()

    def stop(self):
        """Stops the bot"""
        self.running = False


class Context:
    def __init__(self, message: Dict, bot: "Bot"):
        self._message = message
        self._bot = bot

    @property
    def message(self) -> Dict:
        """Returns the original message"""
        return self._message

    @property
    def bot(self) -> "Bot":
        """Returns the bot instance"""
        return self._bot

    def get(self, key: Optional[str] = None, default=None) -> Union[Dict, any]:
        """
        Gets value from message
        :param key: Key (if None, returns entire message)
        :param default: Default value
        """
        if key is None:
            return self._message
        return self._message.get(key, default)

    @property
    def text(self) -> str:
        """Returns message text"""
        return self._message.get("text", "")

    @property
    def caption(self) -> str:
        """Returns photo caption"""
        return self._message.get("caption", "")

    @property
    def photo(self) -> List[Dict]:
        """Returns photo information from message"""
        return self._message.get("photo", [])

    @property
    def best_photo(self) -> Dict:
        """Returns highest resolution photo"""
        photos = self.photo
        if photos:
            # Photos are sorted by size, last one is the largest
            return photos[-1]
        return {}

    @property
    def photo_url(self) -> str:
        """Returns URL of the largest photo"""
        best_photo = self.best_photo
        if best_photo:
            file_id = best_photo.get("file_id")
            return self._bot.get_file_url(file_id)
        return ""

    def delete(self) -> Dict:
        """Deletes the bot's last message in this chat"""
        return self._bot.delete()


class CallbackContext:
    def __init__(self, callback_query: Dict, bot: "Bot"):
        self._callback_query = callback_query
        self._bot = bot

    @property
    def data(self) -> str:
        """Returns callback data"""
        return self._callback_query.get("data", "")

    @property
    def message(self) -> Dict:
        """Returns original message"""
        return self._callback_query.get("message", {})

    @property
    def chat_id(self) -> int:
        """Returns chat ID"""
        return self.message.get("chat", {}).get("id")

    @property
    def from_user(self) -> Dict:
        """Returns user who pressed the button"""
        return self._callback_query.get("from", {})

    @property
    def id(self) -> str:
        """Returns callback query ID"""
        return self._callback_query.get("id", "")

    def answer(
        self,
        text: str = None,
        show_alert: bool = False,
        url: str = None,
        cache_time: int = 0,
    ) -> Dict:
        """Answers the callback query"""
        return self._bot.answer_callback_query(
            callback_query_id=self.id,
            text=text,
            show_alert=show_alert,
            url=url,
            cache_time=cache_time,
        )

    def edit_message_reply_markup(self, reply_markup: Dict = None) -> Dict:
        """Edits only the reply markup of the message"""
        message = self.message
        if not message:
            raise ValueError("No message to edit")

        return self._bot.edit_message_reply_markup(
            chat_id=message.get("chat", {}).get("id"),
            message_id=message.get("message_id"),
            reply_markup=reply_markup,
        )
