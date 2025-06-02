
# Frogram - Modern Telegram Bot Libary for Python

[![MIT License](https://img.shields.io/badge/license-MIT-red.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-green)](https://python.org)
[![Telegram API](https://img.shields.io/badge/Telegram%20API-6.0%2B-blue)](https://core.telegram.org/bots/api)

Frogram is a lightweight yet powerful Python library for building Telegram bots with an elegant and developer-friendly interface. Designed for both beginners and experienced developers, it provides all the essential tools to create feature-rich bots quickly and efficiently.

## Features

✨ **Intuitive Interface**
- Clean, Pythonic API design
- Decorator-based handlers
- Context-aware processing

⌨️ **Keyboard Support**
- Full inline keyboard functionality
- Reply keyboard with all options
- Dynamic keyboard editing

📨 **Message Handling**
- Commands, text, and photo processing
- Media and file support
- Message lifecycle management (send/edit/delete)

🔄 **Callback System**
- Advanced callback query handling
- Alert and notification responses
- Interactive message updates

⚡ **Performance**
- Lightweight with minimal dependencies
- Synchronous and asynchronous support
- Efficient polling mechanism

## Installation

```bash
pip install frogram
```

## Quick Start

```python
from frogram import Bot, inline_keyboard, inline_button

bot = Bot("YOUR_BOT_TOKEN")

@bot.on_command("start")
def start_handler(ctx):
    keyboard = inline_keyboard([
        [inline_button("Option 1", callback_data="opt1"),
         inline_button("Option 2", callback_data="opt2")]
    ])
    ctx.bot.send_message("Welcome! Choose an option:", reply_markup=keyboard)

@bot.on_callback
def callback_handler(ctx):
    ctx.answer(f"You selected: {ctx.data}")

bot.start_polling()
```

## Core Components

### 1. Keyboard System

#### Inline Keyboard
```python
keyboard = inline_keyboard([
    [inline_button("Button", callback_data="action"),
    [inline_button("Open URL", url="https://example.com")]
])
```

#### Reply Keyboard
```python
keyboard = reply_keyboard([
    [keyboard_button("Yes"), keyboard_button("No")],
    [keyboard_button("Share Contact", request_contact=True)]
])
```

#### Remove Keyboard
```python
remove_keyboard(selective=True)
```

### 2. Message Handling

#### Command Handler
```python
@bot.on_command("help")
def help_command(ctx):
    ctx.bot.send_message("Available commands: /start, /help")
```

#### Text Message Handler
```python
@bot.on_message
def echo_handler(ctx):
    ctx.bot.send_message(f"Echo: {ctx.text}")
```

#### Photo Handler
```python
@bot.on_photo
def photo_handler(ctx):
    print(f"Received photo: {ctx.photo_url}")
```

### 3. Callback System

```python
@bot.on_callback
def callback_handler(ctx):
    if ctx.data == "confirm":
        ctx.answer("Confirmed!", show_alert=True)
        ctx.edit_message_reply_markup(reply_markup=None)
```

## Advanced Usage

### Dynamic Keyboard Update
```python
@bot.on_callback
def update_keyboard(ctx):
    new_kb = inline_keyboard([
        [inline_button("New Option", callback_data="new")]
    ])
    ctx.edit_message_reply_markup(reply_markup=new_kb)
```

### Message Management
```python
# Send photo with caption
bot.send_photo(
    photo_url="https://example.com/image.jpg",
    caption="Check this out!",
    reply_markup=keyboard
)

# Delete message
bot.delete(chat_id=12345, message_id=42)
```

### File Handling
```python
# Get file URL from file_id
file_url = bot.get_file_url(file_id)
```

## Error Handling

Frogram integrates with debugmes for comprehensive error reporting:

```python
try:
    bot.start_polling()
except Exception as e:
    debugmes.critical(f"Bot crashed: {e}")
```

## API Reference

### Bot Class Methods
| Method | Description |
|--------|-------------|
| `send_message()` | Send text message with optional keyboard |
| `send_photo()` | Send photo with caption |
| `edit_message_reply_markup()` | Update message keyboard |
| `delete()` | Delete message |
| `get_file_url()` | Get downloadable file URL |
| `answer_callback_query()` | Respond to callback query |

### Context Objects
| Property/Method | Description |
|-----------------|-------------|
| `message` | Original message dictionary |
| `text`/`caption` | Message content |
| `photo_url` | Highest quality photo URL |
| `delete()` | Delete current message |
| `answer()` | Answer callback query |

## Best Practices

1. **Error Handling**: Always wrap handlers in try-except blocks
2. **Rate Limiting**: Respect Telegram's API limits (30 messages/second)
3. **State Management**: Implement proper session handling
4. **Security**: Validate all user input and callback data

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Frogram** - Build better Telegram bots, faster. 🚀
``
