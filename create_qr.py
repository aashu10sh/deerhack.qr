from qr_generator import QRGenerator
from database import Database
import csv
import dataclasses
import uuid


class FoodSystem:
    """This class creates qr and seeds it to the database"""

    def __init__(self, file_name) -> None:
        self.file_name = file_name

    def run(self):
        """This method, fetches the data (in csv format), creates qr for it and seeds relevant data to the database"""
        db = Database()
        with open(self.file_name, "r", encoding="utf-8") as file:
            csvreader = csv.DictReader(file)
            data_len = 0
            for row in csvreader:
                print(f"Creating QR For {row['First Name']}")
                uuid_user = uuid.uuid4()
                b64_data = self.create_qrcode(uuid_user, row)
                db.seed_into_database(uuid_user, row, b64_data)
                data_len = data_len + 1
        db.end()
        print(f"Created {data_len} QR Codes !")

    def create_qrcode(self, uuid: str, data: dict) -> str:
        """Creates the QR code based on the dict value provided"""
        individual = QRGenerator(
            uuid,
            data["First Name"],
            data["Last Name"],
            data["Email"],
            "",
        )
        return individual.main()

    # def seed_to_database(self,user_uuid, data: dict, b64_data: str):
    #     pass


if __name__ == "__main__":
    d = FoodSystem("deerhack_participants.csv")
    d.run()
