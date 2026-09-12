import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).parent / "contacts.db"


import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).parent / "contacts.db"


def get_contacts(city: str, region: str):
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        # Сначала ищем контакты указанного города.
        search_result = connection.execute(
            """
            SELECT name, category, phone, source_url, verified_at
            FROM contacts
            WHERE city = ? AND region = ?
            """,
            (city, region)
        )

        contact_rows = search_result.fetchall()

        # Если городских контактов нет, ищем региональные.
        if not contact_rows:
            search_result = connection.execute(
                """
                SELECT name, category, phone, source_url, verified_at
                FROM contacts
                WHERE region = ? AND city IS NULL
                """,
                (region,)
            )

            contact_rows = search_result.fetchall()

    finally:
        connection.close()

    contacts = []

    for contact_row in contact_rows:
        contacts.append({
            "name": contact_row[0],
            "category": contact_row[1],
            "phone": contact_row[2],
            "source_url": contact_row[3],
            "verified_at": contact_row[4]
        })

    return contacts