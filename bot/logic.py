import sqlite3

def connect_db():
    """Создает и возвращает соединение с базой данных."""
    conn = sqlite3.connect('cooking_recipes.db')
    return conn

def get_dishes(country):
    """Возвращает список блюд для заданной кухни из базы данных, включая их изображения."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM countries WHERE name = ?', (country.strip(),))
    country_row = cursor.fetchone()

    if country_row:
        country_id = country_row[0]
        cursor.execute('SELECT name, image_path FROM dishes WHERE country_id = ?', (country_id,))
        dishes = [(row[0], row[1]) for row in cursor.fetchall()] 
    else:
        dishes = []

    conn.close()
    return dishes 

def get_recipe(country, dish):
    """Возвращает рецепт для заданного блюда и кухни из базы данных, включая путь к изображению."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM countries WHERE name = ?', (country.strip(),))
    country_row = cursor.fetchone()

    if country_row:
        cursor.execute('SELECT id, image_path FROM dishes WHERE name = ? AND country_id = ?', (dish.strip(), country_row[0]))
        dish_row = cursor.fetchone()

        if dish_row:
            dish_id = dish_row[0]
            image_path = dish_row[1]
            cursor.execute('SELECT ingredients, instructions FROM recipes WHERE dish_id = ?', (dish_id,))
            recipe_row = cursor.fetchone()

            if recipe_row:
                ingredients, instructions = recipe_row
                recipe = f"{ingredients}\n\n{instructions}"  
            else:
                recipe = 'Рецепт не найден.'
        else:
            recipe = 'Блюдо не найдено.'
    else:
        recipe = 'Кухня не найдена.'

    conn.close()
    return recipe, image_path 
