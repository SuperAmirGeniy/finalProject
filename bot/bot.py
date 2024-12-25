import logging
import telebot
from telebot import types
from config import TOKEN
from logic import connect_db, get_dishes, get_recipe

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TOKEN)

def get_cuisines():
    """Функция для получения доступных кухонь из базы данных."""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT name FROM countries')
    cuisines = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return cuisines

@bot.message_handler(commands=['start'])
def start(message):
    """Отправляет сообщение с доступными кухнями."""
    cuisines = get_cuisines()   
    keyboard = types.InlineKeyboardMarkup()

    for country in cuisines:
        keyboard.add(types.InlineKeyboardButton(text=country, callback_data=country))

    bot.send_message(message.chat.id, 'Выберите кухню:', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    """Обрабатывает нажатия кнопок для выбора кухни и блюда."""
    data = call.data.split('|')
    conn = None 
    try:
        if len(data) == 1:  
            country = data[0]
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute('SELECT id FROM countries WHERE name = ?', (country.strip(),))
            country_row = cursor.fetchone()

            if country_row:
                bot.answer_callback_query(call.id)
                bot.edit_message_text(text=f"Выберите блюдо из {country}:", chat_id=call.message.chat.id, message_id=call.message.message_id)

                dishes = get_dishes(country)
                keyboard = types.InlineKeyboardMarkup()

                for dish, image_path in dishes: 
                    keyboard.add(types.InlineKeyboardButton(text=dish, callback_data=f"{country}|{dish}"))
                 
                    history_url = f"https://ru.wikipedia.org/wiki/{dish.replace(' ', '_')}"
                    keyboard.add(types.InlineKeyboardButton(text=f"Узнать историю блюда 🔍", url=history_url))

                bot.send_message(call.message.chat.id, text=f"Выберите блюдо из {country}:", reply_markup=keyboard)
            else:
                bot.send_message(call.message.chat.id, "Ошибка: Кухня не найдена.")
        else: 
            country = data[0]
            dish = data[1]
            recipe, image_path = get_recipe(country, dish) 
            bot.edit_message_text(text=f"Рецепт для {dish}:\n{recipe}", chat_id=call.message.chat.id, message_id=call.message.message_id)
            
            if image_path:  
                with open(image_path, 'rb') as img:
                    bot.send_photo(call.message.chat.id, img, caption=f"Вот изображение для {dish}")

    except Exception as e:
        bot.send_message(call.message.chat.id, "Произошла ошибка при обработке запроса.")
        logger.error(f"Ошибка: {e}")  
    finally:
        if conn:
            conn.close() 

def main():
    """Запускает бота."""
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()
