import sqlite3, time

def connect_sql(chat_id, sqlite_query, operation):
    try:
        sqlconnection = [sqlite3.connect('db/sqlite_bot.db')]
        cursor = sqlconnection[0].cursor()
        cursor.execute(sqlite_query)
        print(time.strftime("[%d.%m.%y %H:%M:%S] ") + "Test connection OK")

        if operation == 1:
            sqlconnection[0].commit()
            print("[chat_" + str(chat_id) + "_bot] Inserted")
        if operation == 2:
            sqlconnection.append(cursor.fetchall())
            print("[chat_" + str(chat_id) + "_bot] Selected")

        cursor.close()

    except sqlite3.Error as error:
        print(chat_id)
        print("[!!!] Error connecting", error)
        if (str(error) == "no such table: chat_" + str(chat_id) + "_bot"):
            cursor.execute("CREATE TABLE IF NOT EXISTS [chat_" + str(chat_id) + "_bot] (user_id INTEGER PRIMARY KEY, username TEXT NOT NULL, first_name TEXT NOT NULL, bd_day INTEGER NOT NULL, bd_month INTEGER NOT NULL, bd_year INTEGER NOT NULL);")
            cursor.close()

    return sqlconnection

def add_bd(message, bd_day, bd_month, bd_year):
    user = message.from_user
    chat_id = message.chat.id
    sqlite_query = "insert into [chat_" + str(message.chat.id) + "_bot] values(" + str(user.id) + ", '" + message.from_user.username + "', '" + message.from_user.first_name + "', " + str(bd_day) + ", " + str(bd_month) + ", " + str(bd_year) + ");"
    sqlconnection = connect_sql(chat_id, sqlite_query, 1)
    if (sqlconnection):
        sqlconnection[0].close()
        print("[Add_bd@" + str(user.id) + "] Connection closed ok")

def change_bd(message, bd_day, bd_month, bd_year):
    user = message.from_user
    chat_id = message.chat.id
    sqlite_query = "update [chat_" + str(message.chat.id) + "_bot] set bd_day = " + str(bd_day) + ", bd_month = " + str(bd_month) + ", bd_year = " + str(bd_year) + " WHERE user_id = " + str(user.id) + ";"
    sqlconnection = connect_sql(chat_id, sqlite_query, 1)
    if (sqlconnection):
        sqlconnection[0].close()
        print("[Change_bd@" + str(user.id) + "] Connection closed ok")

def check_bd(message):
    user = message.from_user
    chat_id = message.chat.id
    sqlite_query = "select * from [chat_" + str(message.chat.id) + "_bot] where user_id = " + str(user.id) + ";"
    sqlconnection = connect_sql(chat_id, sqlite_query, 2)
    if (sqlconnection):
        sqlconnection[0].close()
        print("[Check_bd@" + str(user.id) + "] Connection closed ok")
        if len(sqlconnection) == 2:
            return sqlconnection[1]
        else:
            return

def bd_list(chat_id, user_id, month, mode):
    if mode == 0:
        sqlite_query = "select * "
    else:
        sqlite_query = "select count (*) "
    sqlite_query += "from [chat_" + str(chat_id) + "_bot] " + str(month) + " order by bd_month, bd_day;"
    sqlconnection = connect_sql(chat_id, sqlite_query, 2)
    if (sqlconnection):
        sqlconnection[0].close()
        print("[Bd_list@" + str(user_id) + "] Connection closed ok")
        if len(sqlconnection) == 2:
            return sqlconnection[1]
        else:
            return
