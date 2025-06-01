# frogram - Telegram Bot Library

## Overview
frogram is a lightweight Python library for building Telegram bots with a simple and intuitive interface. It provides decorator-based handlers for commands, text messages, and photos, along with convenient methods for sending and managing messages.

## Features
- Command handlers with `@bot.on_command` decorator
- Text message handlers with `@bot.on_message` decorator
- Photo handlers with `@bot.on_photo` decorator
- Callback query handlers with `@bot.on_callback` decorator
- **Keyboard support** (inline and reply keyboards)
- Easy message sending (`send()`, `send_photo()`)
- Message deletion functionality
- File URL retrieval for photos and documents
- Context-based message processing

## Installation
```bash
pip install frogram
```

## Quick Start
```python
from frogram import Bot, inline_keyboard, inline_button

bot = Bot("YOUR_TELEGRAM_BOT_TOKEN")

@bot.on_command("start")
def start_command(ctx):
    # Create inline keyboard
    keyboard = inline_keyboard([
        [inline_button("Option 1", callback_data="opt1"),
        inline_button("Option 2", callback_data="opt2")]
    ])

    ctx.bot.send_message("Welcome! Choose an option:",
                        reply_markup=keyboard)

@bot.on_callback
def handle_callback(ctx):
    if ctx.data == "opt1":
        ctx.answer("You chose Option 1")
    elif ctx.data == "opt2":
        ctx.answer("You chose Option 2")

bot.start_polling()
```

## Keyboard Features

### Inline Keyboard
```python
from frogram import inline_keyboard, inline_button

# Create inline keyboard with buttons
keyboard = inline_keyboard([
    [inline_button("Button 1", callback_data="btn1"),
     inline_button("Button 2", callback_data="btn2")],
    [inline_button("Visit Site", url="https://example.com")]
])

# Send with keyboard
bot.send_message("Choose an option:", reply_markup=keyboard)
```

### Reply Keyboard
```python
from frogram import reply_keyboard, keyboard_button, remove_keyboard

# Create reply keyboard
keyboard = reply_keyboard([
    [keyboard_button("Yes"), keyboard_button("No")],
    [keyboard_button("Share Contact", request_contact=True)]
])

# Send with reply keyboard
bot.send_message("Please answer:", reply_markup=keyboard)

# To remove reply keyboard
bot.send_message("Keyboard removed", reply_markup=remove_keyboard())
```

### Callback Handling
```python
@bot.on_callback
def callback_handler(ctx):
    if ctx.data == "btn1":
        ctx.answer("You pressed Button 1")
    elif ctx.data == "btn2":
        # Edit message after callback
        new_keyboard = inline_keyboard([
            [inline_button("New Button", callback_data="new")]
        ])
        ctx.edit_message_reply_markup(reply_markup=new_keyboard)
```

## Documentation

### Keyboard Functions
`inline_keyboard(rows)` - Create inline keyboard from button rows
`inline_button(text, callback_data=None, url=None)` - Create inline keyboard button
`reply_keyboard(rows, resize_keyboard=True, one_time_keyboard=False)` - Create reply keyboard
`keyboard_button(text, request_contact=False, request_location=False)` - Create reply keyboard button
`remove_keyboard(selective=False)` - Remove reply keyboard

### Updated Bot Methods
`send_message(text, chat_id=None, reply_markup=None, **kwargs)` - Send message with optional keyboard
`send_photo(photo_url, caption="", chat_id=None, reply_markup=None, **kwargs)` - Send photo with optional keyboard
`edit_message_reply_markup(chat_id=None, message_id=None, inline_message_id=None, reply_markup=None)` - Edit message keyboard
`answer_callback_query(callback_query_id, text=None, show_alert=False)` - Answer callback query

### Callback Context
`ctx.data` - Callback data from button
`ctx.message` - Original message with keyboard
`ctx.answer(text, show_alert=False)` - Answer callback query
`ctx.edit_message_reply_markup(reply_markup)` - Edit message keyboard

## Examples

### Complex Keyboard
```python
@bot.on_command("menu")
def show_menu(ctx):
    keyboard = inline_keyboard([
        [inline_button("Settings", callback_data="menu_settings"),
         inline_button("Help", callback_data="menu_help")],
        [inline_button("Close", callback_data="menu_close")]
    ])
    ctx.bot.send_message("Main Menu:", reply_markup=keyboard)
```

### Dynamic Keyboard Update
```python
@bot.on_callback
def handle_menu(ctx):
    if ctx.data == "menu_settings":
        new_kb = inline_keyboard([
            [inline_button("Notifications", callback_data="set_notify"),
             inline_button("Language", callback_data="set_lang")],
            [inline_button("Back", callback_data="menu_back")]
        ])
        ctx.edit_message_reply_markup(reply_markup=new_kb)
        ctx.answer("Settings menu")
```

### Request User Data
```python
@bot.on_command("register")
def register(ctx):
    keyboard = reply_keyboard([
        [keyboard_button("Share Phone", request_contact=True)],
        [keyboard_button("Cancel")]
    ], one_time_keyboard=True)

    ctx.bot.send_message("Please share your phone number:",
                        reply_markup=keyboard)
```
