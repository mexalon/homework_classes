import random
# суперкласс человек в котором содержится атрибут для учёта всех людей
# - словарь с типами и объектами этих типов
class Human:
    __of_all_kind = {}

    def __init__(self, name, surname='Smith'):
        self.name = name
        self.surname = surname
        self.__of_all_kind.setdefault(type(self), [])
        self.__of_all_kind[type(self)] += [self]

# директор  - самый главный человек. Он ведёт журнал учёта и ещё распределяет людей на курсы
class Principle(Human):
    def __init__(self, name, surname='Smith'):
        super().__init__(name, surname)

    # метод для назначения студентам и преподавателям случайного набора курсов
    def go_to_course_and_get_yor_scores(self, other):
        # создавалка словаря случайных курсов и оценок, чтобы в ручную не заполнять
        def some_list_of_courses_with_scores():
            all_courses = ['Math', 'Phyton', 'Physics', 'Art', 'Sport', 'Music']
            how_much = random.randint(1, len(all_courses))
            some_courses = {}
            for ii in range(1, how_much + 1):
                some_scores = []
                for ii in range(1, random.randint(1, 7)):
                    some_scores += [random.randint(1, 11)]
                some_courses.setdefault(random.choice(all_courses), some_scores)
            return some_courses

        # назначение курсов различным классам
        if isinstance(other, Student):
            other.courses_finished = some_list_of_courses_with_scores()
            other.courses_in_progress = some_list_of_courses_with_scores()

        if isinstance(other, Lector):
            other.courses_attached = some_list_of_courses_with_scores()

# класс студентов
class Student(Human):
    def __init__(self, name, surname='Smith'):
        super().__init__(name, surname)
        self.courses_finished = {}
        self.courses_in_progress = {}

# класс метроров
class Mentor(Human):
    def __init__(self, name, surname='Smith'):
        super().__init__(name, surname)
        self.courses_attached = {}

# лекторы
class Lector(Mentor):
    def __init__(self, name, surname='Smith'):
        super().__init__(name, surname)

# проверяторы
class Reviewer(Mentor):
    def __init__(self, name, surname='Smith'):
        super().__init__(name, surname)

# создаём по 2 экземпляра каждого класса и даём им предметы и оценки

principle_adam = Principle('Adam')

lector_jonh = Lector('John', 'Jameson')
principle_adam.go_to_course_and_get_yor_scores(lector_jonh)

lector_sean = Lector('Sean', 'Connery')
principle_adam.go_to_course_and_get_yor_scores(lector_sean)

student_pit = Student('Pit', 'Poppins')
principle_adam.go_to_course_and_get_yor_scores(student_pit)

student_bob = Student('Bob', 'Bobbins')
principle_adam.go_to_course_and_get_yor_scores(student_bob)

reviewer_sally = Reviewer('Sally', 'Simons')
reviever_molly = Reviewer('Molly', 'Miles')

# коньроль
print(lector_jonh.courses_attached)
print(student_bob.courses_finished)
print(student_pit.courses_in_progress)
print(student_bob.courses_in_progress)



