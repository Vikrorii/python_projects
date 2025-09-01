import datetime
#Приклад  Car
class Car:
    brand=None
    model=None
    year=None

    def __init__(self,brand,model,year):
        self.brand = brand
        self.model = model
        self.year = year

    def get_age(self):
        age= datetime.datetime.now().year - self.year
        return age

car1 =Car("BMW","X5", 2020)
car2 =Car("Fhjig","A4", 2000)
print(car2.get_age())





# Клас Movie
class Movie():
    title = None
    year = None
    rating = None

    def __init__(self, title, year, rating):
        self.title = str(title)
        self.year = str(year)
        self.rating = str(rating)

    def is_classic(self):
        age= datetime.datetime.now().year - int(self.year)
        if age >= 25:
            return True

movie1 = Movie("Tet", 1997, "12" )
movie2 = Movie("Ket", 2022, "11")
print(movie1.is_classic())
print(movie2.is_classic())

#Person, Student, Teacher
class Person:
    def __init__(self,name,age):
        self.name=name
        self.age=age

    def introduce(self):
        print("Ім'я", self.name, "Вік", self.age)

class Student(Person):

    def __init__(self,name,age, university):
        super().__init__(name, age)
        self.university=university

    def introduce(self):
        print("Ім'я", self.name, "Вік", self.age, " Університет", self.university)

class Teacher(Person):

    def __init__(self, name, age, subject):
        super().__init__(name, age)
        self.subject= subject

    def introduce(self):
        print("Ім'я", self.name, "Вік", self.age, " предмет", self.subject)

person1=Person("Feda", 25)
student1=Student("Ana", 20, "KPI")
teacher1=Teacher("Mari", 75, "Математика")
person1.introduce()
student1.introduce()
teacher1.introduce()

#Product, Shop
class Product():
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Shop():
    def __init__(self, product=None):
        self.product =[]

    def addProduct(self, product):
        if self.product is None:
            self.product = []
        self.product.append(product)

    def show_products(self):
        for product in self.product:
            print(product.name, product.price)

    def get_total_price(self):
        if not self.product:
            return 0
        return sum(product.price for product in self.product)




shop = Shop()
product = Product('Хліб', 50)
product1 = Product('Молоко', 80)
product2 = Product('Яйця', 120)

shop.addProduct(product)
shop.addProduct(product1)
shop.addProduct(product2)

shop.show_products()
print(shop.get_total_price())






#Бібліотека
class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

class Library:
    def __init__(self, spisok_book=None):
        self.spisok_book =[]

    def add_book(self, book):
        if self.spisok_book is None:
            self.spisok_book =[]
        self.spisok_book.append(book)

    def show_all_books(self):
        for book in self.spisok_book:
            print(book.title, book.author, book.year)

    def search_book(self, author):
        found = []
        for book in self.spisok_book:
            if book.author.lower() == author.lower():
                found.append(book)
        return found

book1 = Book("Hmmm", "Mike J", 1989)
book2 = Book("OKkkk", "Cat", 1997)
book3 = Book("Myhaous", "Mike", 1915)

biblioteka = Library()
biblioteka.add_book(book1)
biblioteka.add_book(book3)
biblioteka.add_book(book2)

biblioteka.show_all_books()

for book in biblioteka.search_book("Mike"):
    print(book.title, book.author, book.year)