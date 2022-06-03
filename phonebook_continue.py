from collections import UserDict
from datetime import datetime
from datetime import date


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phones = []
        self.birthday = birthday

        if phone:
            self.add_phone(phone)

    def __check_phone(self, phone) -> bool:
        if phone in self.phones:
            return True
        return False

    def add_phone(self, phone) -> bool:
        if not self.__check_phone(phone):
            self.phones.append(phone)
            return True
        return False

    def update_phone(self, phone, new_phone) -> bool:
        if self.__check_phone(phone):
            self.delete_phone(phone)
            self.add_phone(new_phone)
            return True
        return False

    def delete_phone(self, phone) -> bool:
        if self.__check_phone(phone):
            self.phones.remove(phone)
            return True
        return False

    def days_to_birthday(self):
        if self.birthday:
            today = date.today()
            splitted_data = self.birthday.value.split('.')
            needed_data = datetime(year=int(today.year), month=int(splitted_data[1]),
                                   day=int(splitted_data[0]))
            needed_data = needed_data.date()
            difference = needed_data - today
            result = difference.days
            return f'Дней до дня рождения осталось -- {result}'
        else:
            return None


class Field:
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    def __eq__(self, __o: object) -> bool:
        if self.__value == __o.value:
            return True
        return False


class Name(Field):
    pass


class Phone(Field):

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, n_value):
        n_value = n_value.strip()
        for ch in n_value:
            if ch not in "0123456789()-+":
                raise ValueError("Invalid phone number")
        self.__value = n_value


class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, b_value):
        if b_value:
            try:
                from datetime import datetime
                datetime.strptime(b_value, "%d.%m.%Y")
            except ValueError:
                raise ValueError("Invalid birthday")
        self.__value = b_value


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def __next__(self):
        return next(self.iterator())

    def iterator(self, count_of_records=None):
        values = {"Name": None, "Phone": None, "Birthday": None}
        for index, key in enumerate(self.data):
            if count_of_records and index >= count_of_records:
                break
            values["Name"] = key
            if self.data[key].phones:
                if len(self.data[key].phones) == 1:
                    values["Phone"] = self.data[key].phones[0].value
                values["Phone"] = [phone.value for phone in self.data[key].phones]
            else:
                values["Phone"] = None
            if self.data[key].birthday:
                values["Birthday"] = self.data[key].birthday.value
            else:
                values["Birthday"] = None
            yield f"{index + 1}. {values['Name']}", values["Phone"], values["Birthday"]
            values = {"Name": None, "Phone": None, "Birthday": None}



if __name__ == '__main__':

    print("Проверка работы классов Phone и Birthday:")
    name = Name("Самоходов Павел Сигизмундович")
    phone = Phone("+38(095)789-12-34")
    # incorrect_phone = Phone("+38(095)789-1s2-34")
    print(phone.value)
    birthday = Birthday("31.08.1999")
    # incorrect_birthday = Birthday("31.08-1999")
    print(birthday.value)
    print("-----------------------------------------------------")
    print("Проверка работы класса Record и метода days_to_birthday:")
    record = Record(name, phone, birthday)
    print(record.name.value)
    print(record.phones[0].value)
    print(record.birthday.value)
    print(record.days_to_birthday())
    print("-----------------------------------------------------")
    ...
    # Заполняю класс Record некоторыми значениями

    name_2 = Name("Вырвиглазов Андрей Владимирович")
    phone_2 = Phone("+38(093)789-42-34")
    birthday_2 = Birthday("21.12.2001")
    record_2 = Record(name_2, phone_2, birthday_2)
    name_3 = Name("Шевченко Тарас Григорьевич")
    record_3 = Record(name=name_3)
    name_4 = Name("Шампуршвили Шашлосси Аджикович")
    phone_4 = Phone("+38(093)222-44-34")
    record_4 = Record(name_4, phone=phone_4)
    record_4.add_phone(Phone("+38(093)111-11-11"))
    name_5 = Name("Быков Леонтий Фёдорович")
    birthday_5 = Birthday("21.11.1901")
    record_5 = Record(name_5, birthday=birthday_5)
    ...
    print("Проверка работы поля Birthday:")
    print(birthday.value)
    print(birthday_2.value)
    print(birthday_5.value)
    print(record.birthday)
    print(record_2.birthday)
    print(record_5.birthday.value)
    print("-----------------------------------------------------")

    ...

    print("Проверка работы класса AddressBook:")
    #  Создаю адресную книгу
    address_book = AddressBook()
    address_book.add_record(record)
    address_book.add_record(record_2)
    address_book.add_record(record_3)
    address_book.add_record(record_4)
    address_book.add_record(record_5)
    for k, v in address_book.items():
        print(k)
        if v.birthday:
            print(f"{v.birthday.value}")
            print(f"{v.days_to_birthday()}")
        if v.phones:
            if len(v.phones) == 1:
                print(f"{v.phones[0].value}")
            else:
                print(f"{v.phones[0].value, v.phones[1].value}")
    print("-----------------------------------------------------")
    print("Проверка работы метода next (если убрать комментарий, то через цикл прогонится меньше вариантов):")
    a = address_book.iterator(count_of_records=2)
    # print(next(a))
    # print(next(a))
    # print(next(a))
    print("Проверка прогона через цикл:")
    for contact in a:
        print(contact)
    print(address_book['Вырвиглазов Андрей Владимирович'].days_to_birthday())