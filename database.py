import mysql.connector

cnx = mysql.connector.connect(
    user="deerhack",
    password="winter_is_coming",
    host="127.0.0.1",
    database="deerhack_fs",
)


class Database:
    """Database class is responsible with interacting with the database and seeding the necessary data"""

    def __init__(self):
        self.connection = cnx
        self.cursor = self.connection.cursor()

    def migrate_tables(self, filename: str = "schema.sql"):
        """This Method Migrates the schema of the database from a static
        schema.sql file in the current directory
        """
        with open(filename, "r", encoding="utf-8") as query_reader:
            self.cursor.execute(query_reader.read())
            self.connection.commit()

    def seed_into_database(self, user_uuid: str, data: dict, base_64_data: str):
        """Seeds the relevant information into the database"""
        sql = "INSERT INTO Participant (uuid,first_name, last_name, gender, email, team_name,  qr_data) VALUES (%s,%s, %s, %s, %s, %s, %s)"
        values = (
            str(user_uuid),
            data["First Name"],
            data["Last Name"],
            data["Gender"],
            data["Email"],
            data["Team Name"],
            base_64_data,
        )
        self.cursor.execute(sql, values)
        self.connection.commit()

    def end(self):
        """Closes the db connection"""
        self.connection.close()


if __name__ == "__main__":
    db = Database()
    db.migrate_tables()
