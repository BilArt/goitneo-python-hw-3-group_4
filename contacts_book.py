from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    

class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate_phone()

    def validate_phone(self):
        if not self.value.isdigit() or len (self.value) != 10:
            raise ValueError("Phone must be a 10-digit numeric value.")

class Bithday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate_birhday()

    def validate_birthday(self):
        try:
            datetime.strptime(self.value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid birthday format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        raise ValueError("Phone is not found.")
                         
    def __str__(self):
        phones_str = ': '.join(str(p) for p in self.phones)
        birthday_str = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"
    

class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError("Record not found.")

    def get_birthdays_per_week(self):
        today = datetime.today()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").replace(year=today.year)
                if today <= birthday_date < next_week:
                    upcoming_birthdays.append(record.name.value)

        return upcoming_birthdays
        

# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

#Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

#Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name.value}: {found_phone}")  # Виведення 5555555555

# Видалення запису Jane
book.delete("Jane")