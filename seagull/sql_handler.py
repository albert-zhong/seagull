import mysql.connector


class Database:
    def __init__(self, host, user, password, db_name):
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            autocommit=True,
        )

    def dictionary_to_sql(self, dictionary, table_name):
        cursor = self.db.cursor()

        create_table = f"CREATE TABLE IF NOT EXISTS {table_name} (word VARCHAR(15) NOT NULL, frequency INT DEFAULT 0 NOT NULL, PRIMARY KEY (word))"
        cursor.execute(create_table)

        for word, frequency in dictionary.items():
            check_for_word = f"SELECT EXISTS(SELECT 1 FROM {table_name} where word = '{word}')"
            cursor.execute(check_for_word)
            exists = [row for row in cursor]

            if exists[0][0] > 0:
                update_row = f"UPDATE {table_name} SET frequency = frequency + {frequency} WHERE word = '{word}'"
                cursor.execute(update_row)
            else:
                add_row = f"INSERT INTO {table_name}(word, frequency) VALUES('{word}', {frequency})"
                cursor.execute(add_row)

    def sql_to_dictionary(self, table_name):
        cursor = self.db.cursor()

        show_rows = f"SELECT * FROM {table_name}"
        cursor.execute(show_rows)

        dictionary = {}

        for word, frequency in cursor:
            dictionary[word] = frequency

        return dictionary
