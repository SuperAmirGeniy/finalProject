import sqlite3  

DB_PATH = 'cooking_recipes.db'  

def create_tables():  
    """Создание таблиц в базе данных."""  
    with sqlite3.connect(DB_PATH) as conn:  
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
                image_path TEXT,  -- Добавляем image_path  
                FOREIGN KEY (country_id) REFERENCES countries(id)  
            )  
        ''')   
 
        cursor.execute('''  
            CREATE TABLE IF NOT EXISTS recipes (  
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                dish_id INTEGER,  
                ingredients TEXT,  
                instructions TEXT,  
                FOREIGN KEY (dish_id) REFERENCES dishes(id)   
            )  
        ''')  
        
        conn.commit()  

if __name__ == "__main__":  
    create_tables()  
    print("Таблицы созданы.")