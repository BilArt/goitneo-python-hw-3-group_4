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
        

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate_birthday()

    def validate_birthday(self):
        try:
            datetime.strptime(self.value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid birthday format. Use DD.MM.YYYY.")


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
    

def print_help():
    print("Available commands:")
    print("add [name] [phone]: Add a new contact with the specified name and phone number.")
    print("change [name] [new phone]: Change the phone number for the specified contact.")
    print("phone [name]: Show the phone number for the specified contact.")
    print("all: Show all contacts in the address book.")
    print("add-birthday [name] [birthday]: Add a birthday for the specified contact.")
    print("show-birthday [name]: Show the birthday for the specified contact.")
    print("birthdays: Show upcoming birthdays in the next week.")
    print("hello or hi: Get a greeting from the bot.")
    print("close or exit: Close the program.")
    print("help: Show this list of commands.")
        

# ... (попередній код залишається незмінним)

def main():
    book = AddressBook()

    while True:
        command = input("Enter command: ").split()

        if not command:
            continue

        if command[0] == "add":
            name, phone = command[1], command[2]
            record = Record(name)
            record.add_phone(phone)
            book.add_record(record)
            print(f"Contact {name} added with phone {phone}.")

        elif command[0] == "change":
            name, new_phone = command[1], command[2]
            record = book.find(name)
            if record:
                record.edit_phone(record.phones[0].value, new_phone)
                print(f"Phone number for {name} changed to {new_phone}.")
            else:
                print(f"Contact {name} not found.")

        elif command[0] == "phone":
            name = command[1]
            record = book.find(name)
            if record:
                print(f"Phone number for {name}: {record.phones[0].value}.")
            else:
                print(f"Contact {name} not found.")

        elif command[0] == "all":
            for record in book.data.values():
                print(record)

        elif command[0] == "add-birthday":
            name, birthday = command[1], command[2]
            record = book.find(name)
            if record:
                record.add_birthday(birthday)
                print(f"Birthday added for {name}.")
            else:
                print(f"Contact {name} not found.")

        elif command[0] == "show-birthday":
            name = command[1]
            record = book.find(name)
            if record and record.birthday:
                print(f"Birthday for {name}: {record.birthday}.")
            else:
                print(f"Birthday not found for {name}.")

        elif command[0] == "birthdays":
            upcoming_birthdays = book.get_birthdays_per_week()
            if upcoming_birthdays:
                print("Upcoming birthdays in the next week:")
                for name in upcoming_birthdays:
                    print(name)
            else:
                print("No upcoming birthdays in the next week.")

        elif command[0] in ["hello", "hi"]:
            print("Hello! How can I help you today?")

        elif command[0] in ["close", "exit"]:
            print("Closing the program.")
            break

        elif command[0] == "help":
            print_help()

        else:
            print("Invalid command. Try again.")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
