from telethon import TelegramClient, events
import re

# Ваші API ID і HASH
api_id = '22984319'  # Заміни на ваш API ID
api_hash = '187de50c70b7752c04769d66da59ed69'  # Заміни на ваш API HASH

# Ініціалізація клієнта Telegram
client = TelegramClient('my_session', api_id, api_hash)

SOURCE_CHANNEL = [ '@war_monitor', '@eRadarrua', '@raketa_trevoga', '@kyivdviz', '@tryvoga_chomu' ]  # Канал джерело
TARGET_CHANNEL = '@radarukppo'  # Канал призначення

# Список заборонених слів
FORBIDDEN_WORDS = ['банка', 'донат', 'реклама', '@', '#']

# Функція для перевірки тексту на наявність заборонених слів
def contains_forbidden_words(text):
    # Регулярний вираз для пошуку заборонених слів
    pattern = r'\b(?:' + '|'.join(re.escape(word) for word in FORBIDDEN_WORDS) + r')\b'
    return bool(re.search(pattern, text, re.IGNORECASE))

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    try:
        # Якщо в повідомленні є текст
        if event.message.message:
            text = event.message.message.strip()  # Очищаємо текст від зайвих пробілів
            
            # Перевірка на наявність заборонених слів
            if contains_forbidden_words(text):
                print(f"Повідомлення містить заборонені слова: {text}, пропущено.")
                return  # Пропускаємо це повідомлення

            # Якщо є медіа (фото, відео тощо)
            if event.message.media:
                # Пересилаємо фото/відео та текст разом
                await client.send_message(TARGET_CHANNEL, text, file=event.message.media)
                print(f"Фото/відео та текст успішно переслані з каналу {event.chat.title}")
            else:
                # Якщо є тільки текст, пересилаємо його
                await client.send_message(TARGET_CHANNEL, text)
                print(f"Текстове повідомлення успішно переслане з каналу {event.chat.title}")
        
        # Якщо є тільки медіа (без тексту), пересилаємо лише медіа
        elif event.message.media:
            await client.send_file(TARGET_CHANNEL, event.message.media)
            print(f"Медіа успішно переслано з каналу {event.chat.title}")

    except Exception as e:
        print(f"Помилка пересилання: {e}")

# Старт бота
client.start()
client.run_until_disconnected()
