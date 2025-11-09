import pickle
from collections import UserDict



class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Номер телефону має складатися з 10 цифр")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return True
        return False

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        return f"{self.name.value}: {phones}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]



def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()



def main():
    book = load_data() 

    print("📘 Вітаю в Адресній книзі!")
    print("Доступні команди: add, change, delete, show, exit")

    while True:
        command = input("\nВведіть команду: ").strip().lower()

        if command == "add":
            name = input("Введіть ім'я: ").strip()
            phone = input("Введіть телефон (10 цифр): ").strip()

            record = book.find(name)
            if not record:
                record = Record(name)
                book.add_record(record)
            try:
                record.add_phone(phone)
                print(f"✅ Контакт {name} додано/оновлено.")
            except ValueError as e:
                print(f"❌ {e}")

        elif command == "change":
            name = input("Ім'я: ").strip()
            old_phone = input("Старий номер: ").strip()
            new_phone = input("Новий номер: ").strip()

            record = book.find(name)
            if record and record.edit_phone(old_phone, new_phone):
                print("🔁 Номер змінено.")
            else:
                print("❌ Контакт або номер не знайдено.")

        elif command == "delete":
            name = input("Ім'я для видалення: ").strip()
            if book.find(name):
                book.delete(name)
                print(f"🗑 Контакт {name} видалено.")
            else:
                print("❌ Контакт не знайдено.")

        elif command == "show":
            if not book:
                print("📭 Адресна книга порожня.")
            else:
                for record in book.values():
                    print(record)

        elif command == "exit":
            save_data(book)
            print("💾 Дані збережено. До зустрічі!")
            break

        else:
            print("❓ Невідома команда. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
