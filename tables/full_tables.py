import sqlite3  

conn = sqlite3.connect('cooking_recipes.db')  
cursor = conn.cursor()  

cursor.execute('''  
CREATE TABLE IF NOT EXISTS countries (  
    id INTEGER PRIMARY KEY AUTOINCREMENT,  
    name TEXT UNIQUE NOT NULL  
)  
''')  

cursor.execute('''  
CREATE TABLE IF NOT EXISTS dishes (  
    id INTEGER PRIMARY KEY AUTOINCREMENT,  
    name TEXT NOT NULL,  
    country_id INTEGER,  
    image_path TEXT,  -- Поле для хранения пути к изображению  
    FOREIGN KEY (country_id) REFERENCES countries(id)  
)  
''')  

cursor.execute('''  
CREATE TABLE IF NOT EXISTS recipes (  
    id INTEGER PRIMARY KEY AUTOINCREMENT,  
    dish_id INTEGER,  
    ingredients TEXT NOT NULL,  
    instructions TEXT NOT NULL,  
    FOREIGN KEY (dish_id) REFERENCES dishes(id)  
)  
''')  

countries = [  
    ('Италия 🇮🇹',),   
    ('Франция 🇫🇷',),   
    ('Испания 🇪🇸',),   
    ('Мексика 🇲🇽',),   
    ('Япония 🇯🇵',),   
    ('Россия 🇷🇺',),  
    ('США 🇺🇸',)  
]  
for country in countries:  
    cursor.execute('INSERT OR IGNORE INTO countries (name) VALUES (?)', country)  
print("Заполнение таблицы стран завершено.")  

dishes = {  
    'Италия 🇮🇹': [  
        ('Паста', 'images/pasta.jpg'),   
        ('Пицца', 'images/pizza.jpg'),   
        ('Тирамису', 'images/tiramisu.jpg')  
    ],  
    'Франция 🇫🇷': [  
        ('Круассан', 'images/croissant.jpg'),   
        ('Бёф бургиньон', 'images/beef_bourguignon.jpg'),   
        ('Рататуй', 'images/ratatouille.jpg')  
    ],  
    'Испания 🇪🇸': [  
        ('Паэлья', 'images/paella.jpg'),   
        ('Тортилья', 'images/tortilla.jpg'),   
        ('Гаспачо', 'images/gazpacho.jpg')  
    ],  
    'Мексика 🇲🇽': [  
        ('Тако', 'images/taco.jpg'),   
        ('Энчилада', 'images/enchilada.jpg'),   
        ('Гуакамоле', 'images/guacamole.jpg')  
    ],  
    'Япония 🇯🇵': [  
        ('Суши', 'images/sushi.jpg'),   
        ('Рамэн', 'images/ramen.jpg'),   
        ('Тэриаки', 'images/teriyaki.jpg')  
    ],  
    'Россия 🇷🇺': [  
        ('Солянка', 'images/solyanka.jpg'),   
        ('Холодец', 'images/holodets.jpg'),   
        ('Пельмени', 'images/pelmeni.jpg')  
    ],  
    'США 🇺🇸': [  
        ('Бургер', 'images/hamburger.jpg'),   
        ('Хот-дог', 'images/hot_dog.jpg'),   
        ('Панкейки', 'images/pancakes.jpg')  
    ]  
}  

for country, dishes_list in dishes.items():  
    cursor.execute('SELECT id FROM countries WHERE name = ?', (country,))  
    country_row = cursor.fetchone()  
    if country_row:  
        country_id = country_row[0]  
        for dish, image_path in dishes_list:
            cursor.execute('INSERT INTO dishes (name, country_id, image_path) VALUES (?, ?, ?)', (dish, country_id, image_path))  
print("Заполнение таблицы блюд завершено.")  

recipes_data = {  
    'Паста': ('Ингредиенты: макароны, соус, сыр.', 'Приготовление: отварите макароны и смешайте с соусом.'),  
    'Пицца': ('Ингредиенты: тесто, томатный соус, сыр, начинки.', 'Приготовление: раскатайте тесто, добавьте начинку и выпекайте.'),  
    'Тирамису': ('Ингредиенты: савоярди, кофе, маскарпоне, какао.', 'Приготовление: пропитайте савоярди в кофе и слоями уложите с маскарпоне.'),  
    'Круассан': ('Ингредиенты: мука, масло, молоко, сахар, дрожжи.', 'Приготовление: замесите тесто, раскатайте и формируйте круассаны.'),  
    'Бёф бургиньон': ('Ингредиенты: говядина, красное вино, морковка, лук, чеснок.', 'Приготовление: тушите до мягкости.'),  
    'Рататуй': ('Ингредиенты: баклажан, цуккини, помидоры, перец.', 'Приготовление: нарежьте овощи и запекайте их с маслом и специями.'),  
    'Паэлья': ('Ингредиенты: рис, морепродукты, курица, шафран.', 'Приготовление: обжарьте все ингредиенты в сковороде и варите до готовности риса.'),  
    'Тортилья': ('Ингредиенты: яйца, картошка, лук.', 'Приготовление: обжарьте картошку с луком, затем залейте взбитыми яйцами и готовьте на сковороде.'),  
    'Гаспачо': ('Ингредиенты: помидоры, перец, лук, огурец, оливковое масло.', 'Приготовление: смешайте все ингредиенты в блендере и подавайте холодным.'),  
    'Тако': ('Ингредиенты: тортильи, мясо, овощи, соусы.', 'Приготовление: уложите начинку в тортильи и подавайте с соусом.'),  
    'Энчилада': ('Ингредиенты: тортильи, мясо, соус, сыр.', 'Приготовление: заверните начинку в тортилью, залейте соусом и запекайте.'),  
    'Гуакамоле': ('Ингредиенты: авокадо, лимон, чеснок, соль.', 'Приготовление: перемелите все ингредиенты до получения однородной массы.'),  
    'Суши': ('Ингредиенты: рис, нори, рыба.', 'Приготовление: сворачивайте рис с начинками в нори и нарежьте на кусочки.'),  
    'Рамэн': ('Ингредиенты: лапша, бульон, мясо, овощи.', 'Приготовление: отварите лапшу и подайте с горячим бульоном и начинками.'),  
    'Тэриаки': ('Ингредиенты: курица, соус терияки.', 'Приготовление: обжарьте курицу и полейте её соусом терияки перед подачей.'),  
    'Солянка': ('Ингредиенты: мясо, овощи, оливки, лимон.', 'Приготовление: отварите мясо, добавьте овощи и варите до готовности.'),  
    'Холодец': ('Ингредиенты: 1,5 кг мяса (свинина, говядина), 1 луковица, 2-3 моркови, 4-5 зубчиков чеснока (по желанию), соль, перец, лавровый лист.', 'Приготовление: приготовьте бульон из мяса, добавив лук и морковь. На дно формы выложите нарезанное мясо, залейте процеженным бульоном и остудите до застывания.'),  
    'Пельмени': ('Ингредиенты: мясо, тесто, лук, специи.', 'Приготовление: заверните фарш в тесто, отварите в воде.'),  
    'Бургер': ('Ингредиенты: булочка, котлета, салат, помидоры, соусы.', 'Приготовление: соберите бургер, укладывая ингредиенты между булочками.'),  
    'Хот-дог': ('Ингредиенты: сосиска, булочка, горчица, кетчуп.', 'Приготовление: положите сосиску в булочку и добавьте соусы по вкусу.'),  
    'Панкейки': ('Ингредиенты: мука, яйца, молоко, сахар, разрыхлитель.', 'Приготовление: смешайте все ингредиенты, жарьте на сковороде с обеих сторон до золотистой корочки.')  
}  

for dish, (ingredients, instructions) in recipes_data.items():  
    cursor.execute('SELECT id FROM dishes WHERE name = ?', (dish,))  
    dish_row = cursor.fetchone()  
    if dish_row:   
        dish_id = dish_row[0]  
        cursor.execute('INSERT INTO recipes (dish_id, ingredients, instructions) VALUES (?, ?, ?)', (dish_id, ingredients, instructions))  
print("Заполнение таблицы рецептов завершено.")  

conn.commit()  
conn.close()  
print("Все данные успешно добавлены и соединение закрыто.")