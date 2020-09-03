class TurarRyskulove():

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def tell(self):
        print("{0} age {1}".format(self.name, self.age))


class children(TurarRyskulove):

    def __init__(self, name, age, grade):
        super(children, self).__init__(name, age )
        self.grade = grade

    def tell(self):
        print("{0} age {1} grade {2}".format(self.name, self.age, self.grade))


class teacher(TurarRyskulove):

    def __init__(self, name, age, zarplata):
        super(teacher, self).__init__(name, age)
        self.zarplata = zarplata

    def tell(self):
        print("{0} age {1} salary {2}".format(self.name, self.age, self.zarplata))



a = [("Arnal", 15), ("Roditel", 42), ("Sveta", 43, 30000)]


Name = input("Введите имя: ")
Age = input("Введите возраст: ")
Grade = input("Введите класс в котором учится человек(если человек учитель, то введите учитель): ")

try:
    Grade = int(Grade)
    obj = children(Name, Age, Grade)
    obj.tell()
except ValueError:
    Grade = Grade.lower()
    if (Grade == "учитель"):
        salary = input("Введите зарплату: ")
        obj = teacher(Name, Age, salary)
        obj.tell()

