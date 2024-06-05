import sqlite3
from datetime import datetime, date

async def create_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS channels (
                    channel_id INTEGER,
                    channel_name TEXT,
                    channel_link TEXT,
                    PRIMARY KEY (channel_id)
                )
            """)
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS movies (
                    movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    movie_name TEXT,
                    movie_description TEXT
                )
            """)
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER,
                        date_of_join DATETIME,
                        PRIMARY KEY (user_id)
                    )
                """)
    conn.close()
async def get_channels():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS channels (
                channel_id INTEGER,
                channel_name TEXT,
                channel_link TEXT,
                PRIMARY KEY (channel_id)
            )
        """)
    cursor.execute('SELECT * FROM channels')
    rows = cursor.fetchall()
    conn.close()
    two_dimensional_array = [list(row) for row in rows]


    for row in two_dimensional_array:
        print(row)
    return two_dimensional_array

async def get_movies():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_name TEXT,
                movie_description TEXT
            )
        """)
    cursor.execute('SELECT * FROM movies')
    rows = cursor.fetchall()
    conn.close()
    two_dimensional_array = [list(row) for row in rows]


    for row in two_dimensional_array:
        print(row)
    return two_dimensional_array


async def get_channels_data_as_string():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT channel_id, channel_name, channel_link FROM channels")
    rows = cursor.fetchall()
    conn.close()

    if len(rows) > 0:
        data_string = ""
        for row in rows:
            channel_id, channel_name, channel_link = row
            channel_data = f"{channel_id}: <a href='{channel_link}'><b>{channel_name}</b></a> \n"
            data_string += channel_data
    else:
        data_string = "Нет доступных каналов"

    return data_string

async def get_movies_data_as_string():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT movie_id, movie_name FROM movies")
    rows = cursor.fetchall()
    conn.close()

    if len(rows) > 0:
        data_string = ""
        for row in rows:
            movie_id, movie_name = row
            movie_data = f"{movie_id}: <b>{movie_name}</b> \n"
            data_string += movie_data
    else:
        data_string = "Нет доступных фильмов"

    return data_string

async def get_movie_data_as_string(movie_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT movie_id, movie_name, movie_description FROM movies WHERE movie_id = ?", (movie_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        movie_id, movie_name, movie_description = row
        data_string = f"{movie_id}: <b>{movie_name}</b> \n{movie_description}"
    else:
        data_string = "Фильм не найден"

    return data_string
async def delete_channel(channel):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        delete_channel_id = channel['deletechannelid']
        print(delete_channel_id)
        cursor.execute("DELETE FROM channels WHERE channel_id = ?", (delete_channel_id,))
        conn.commit()
        deleted_rows = cursor.rowcount
        if deleted_rows > 0:
            print(f"Удалена запись с channel_id: {delete_channel_id}")
        else:
            print("Запись не найдена")
    except sqlite3.Error as e:
        print("Произошла ошибка при удалении записи:")
        print(e)
    finally:
        if conn:
            conn.close()

async def delete_movie(movie):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        delete_movie_id = movie['deletemovieid']
        print(delete_movie_id)
        cursor.execute("DELETE FROM movies WHERE movie_id = ?", (delete_movie_id,))
        conn.commit()
        deleted_rows = cursor.rowcount
        if deleted_rows > 0:
            print(f"Удалена запись: {delete_movie_id}")
        else:
            print("Запись не найдена")
    except sqlite3.Error as e:
        print("Произошла ошибка при удалении записи:")
        print(e)
    finally:
        if conn:
            conn.close()

async def add_channel(channel):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        add_channel_id = channel['addchannelid']
        add_channel_name = channel['addchannelname']
        add_channel_link = channel['addchannellink']

        cursor.execute("INSERT INTO channels (channel_id, channel_name, channel_link) VALUES (?, ?, ?)",
                       (add_channel_id, add_channel_name, add_channel_link))
        conn.commit()
        print("Запись успешно добавлена в базу данных")
    except sqlite3.Error as e:
        print("Произошла ошибка при добавлении записи:")
        print(e)
    finally:
        if conn:
            conn.close()

async def add_movie(channel):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        add_movie_name = channel['addmoviename']
        add_movie_description = channel['addmoviedescription']

        cursor.execute("INSERT INTO movies (movie_name, movie_description) VALUES (?, ?)",
                       (add_movie_name, add_movie_description))
        conn.commit()
        print("Запись успешно добавлена в базу данных")
    except sqlite3.Error as e:
        print("Произошла ошибка при добавлении записи:")
        print(e)
    finally:
        if conn:
            conn.close()
async def add_user(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER,
                    date_of_join DATETIME,
                    PRIMARY KEY (user_id)
                )
            """)
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    existing_user = cursor.fetchone()

    if existing_user is None:

        current_time = datetime.now()
        cursor.execute("INSERT INTO users (user_id, date_of_join) VALUES (?, ?)", (user_id, current_time))
        conn.commit()
        print("Пользователь добавлен в таблицу.")
    else:
        print("Пользователь уже существует в таблице.")

    conn.close()
async def get_total_user_count():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    total_count = cursor.fetchone()[0]
    conn.close()

    return total_count

async def get_users_joined_today_count():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    today = date.today()
    cursor.execute("SELECT COUNT(*) FROM users WHERE date_of_join = ?", (today,))
    today_count = cursor.fetchone()[0]
    conn.close()

    return today_count