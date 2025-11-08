import pickle
from collections import UserDict

# Класи для адресної книги

class Record:
    def __init__(self, name, phone=None, email=None):
        self.name = name
        self.phones = []
        self.email = email
        if phone:
            self.add_phone(phone)

    def add_phone(self, phone):
        self.phones.append(phone)

    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            idx = self.phones.index(old_phone)
            self.phones[idx] = new_phone

    def __str__(self):
        phones = ", ".join(self.phones)
        return f"{self.name}: {phones}" + (f", email: {self.email}" if self.email else "")


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

# Функції для збереження та завантаження

def save_data(book, filename="addressbook.pkl"):
    """Зберігає адресну книгу у файл."""
    with open(filename, "wb") as f:
        pickle.dump(book, f)
    print("✅ Дані успішно збережено у файл.")


def load_data(filename="addressbook.pkl"):
    """Завантажує адресну книгу з файлу або створює нову, якщо файл відсутній."""
    try:
        with open(filename, "rb") as f:
            book = pickle.load(f)
            print("📂 Дані успішно завантажено з файлу.")
            return book
    except FileNotFoundError:
        print("⚠️ Файл не знайдено. Створюємо нову адресну книгу.")
        return AddressBook()
    except Exception as e:
        print(f"❌ Помилка при завантаженні: {e}")
        return AddressBook()

# Основний цикл програми

def main():
    book = load_data()  # відновлення (запуск)

    while True:
        command = input("\nВведіть команду (add, show, delete, exit): ").strip().lower()

        if command == "add":
            name = input("Ім'я: ")
            phone = input("Телефон: ")
            email = input("Email (необов’язково): ")
            record = Record(name, phone, email)
            book.add_record(record)
            print(f"✅ Контакт {name} додано.")

        elif command == "show":
            if not book:
                print("Адресна книга порожня.")
            else:
                for rec in book.values():
                    print(rec)

        elif command == "delete":
            name = input("Ім'я контакту для видалення: ")
            book.delete(name)
            print(f"🗑️ Контакт {name} видалено.")

        elif command == "exit":
            save_data(book)  # збереження при виході
            print("👋 До побачення!")
            break

        else:
            print("Невідома команда. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
