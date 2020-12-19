import random
# суперкласс человек в котором содержится атрибут для учёта всех людей
# - словарь с типами и объектами этих типов. Хотелось сделать, чтобы объекты
# сами записывались в список, но как сделать это по другому не придумал.
# Поэтому сделал изменяемый атрибут
class Human:
    _of_all_kind = {}
    def __init__(self, name, surname='Smith'):
        self.name = name
        self.surname = surname
        self._of_all_kind.setdefault(type(self), [])
        self._of_all_kind[type(self)] += [self]

    # вычисление средней оценки по ключу из словаря
    # можно было бы вынести эту фунуцию из методов класса, но я не знаю,
    # хорошо ли внутри объявления класса вызывать внешнюю функцию?
    def average_grade_for_something(self, course, dict_of_courses):
        if course in dict_of_courses.keys() and dict_of_courses != {}:
            list_of_grades = [0]
            if dict_of_courses[course] != [] and list_of_grades == [0]:
                list_of_grades = dict_of_courses[course]
            elif dict_of_courses[course] != [] and list_of_grades != [0]:
                list_of_grades += dict_of_courses[course]

            average_grade = round(sum(list_of_grades) / len(list_of_grades), 1)
            return average_grade
        else:
            return 0

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'

# директор  - самый главный человек. Он ведёт журнал учёта и ещё распределяет людей на курсы
class Principle(Human):
    def __init__(self, name, surname='Smith'):
        super().__init__(name, surname)


# класс студентов
class Student(Human):
    def __init__(self, name, surname='Smith'):
        super().__init__(name, surname)
        self.courses_finished = {}
        self.courses_in_progress = {}

    # постановка оценки лектору
    def rate(self, other, course, grade):
        if isinstance(other, Lector) and isinstance(grade, int):
            if course in self.courses_in_progress.keys() and course in other.courses_attached.keys() and 1 <= grade <= 10:
                if other.courses_attached[course] != None:
                    other.courses_attached[course] += [grade]
                else:
                    other.courses_attached[course] = [grade]
            else:
                print('Нельзя ставить оценку')
        else:
            print('Где то ошибка')

    def __str__(self):
        average_grade_for_all = 0
        sum_of_grades = 0
        if len(self.courses_in_progress) != 0:
            for entry in self.courses_in_progress.keys():
                sum_of_grades += super().average_grade_for_something(entry, self.courses_in_progress)
            average_grade_for_all = round(sum_of_grades / len(self.courses_in_progress), 1)

        return super().__str__() + f'\nСредняя оценка за домашку:' \
                                   f' {average_grade_for_all}' \
                                   f'\nКурсы в процессе изучения:' \
                                   f' {list(self.courses_in_progress.keys())}' \
                                   f'\nЗавершенные курсы:' \
                                   f' {list(self.courses_finished.keys())}'

# класс метроров
class Mentor(Human):
    def __init__(self, name, surname='Smith'):
        super().__init__(name, surname)
        self.courses_attached = {}


# класс лекторы
class Lector(Mentor):
    def __init__(self, name, surname='Smith'):
        super().__init__(name, surname)

    def __str__(self):
        if self.courses_attached != {} and isinstance(self, Lector):
            sum_of_grades = 0
            for entry in self.courses_attached.keys():
                sum_of_grades += super().average_grade_for_something(entry, self.courses_attached)
            average_grade_for_all = round(sum_of_grades / len(self.courses_attached), 1)

            return super().__str__() + f'\nСредняя оценка от студентов:' \
                                       f' {average_grade_for_all}'
        else:
            return super().__str__() + f'\nКурсов нет'


# класс проверяторы
class Reviewer(Mentor):
    def __init__(self, name, surname='Smith'):
        super().__init__(name, surname)

    # постановка оценки студенту
    def rate(self, other, course, grade):
        if isinstance(other, Student) and isinstance(grade, int):
            if course in self.courses_attached.keys() and course in other.courses_in_progress.keys() and 1 <= grade <= 10:
                if other.courses_in_progress[course] != None:
                    other.courses_in_progress[course] += [grade]
                else:
                    other.courses_in_progress[course] = [grade]
            else:
                print('Нельзя ставить оценку')
        else:
            print('Где то ошибка')

# функция для назначения студентам и преподавателям случайного набора курсов
def go_to_course_and_get_yor_scores(other):
    # создавалка словаря случайных курсов и оценок, чтобы в ручную не заполнять
    def some_list_of_courses_with_scores():
        all_courses = ['Math', 'Phyton', 'Physics', 'Art', 'Sport', 'Music']
        how_much = random.randint(1, len(all_courses))
        some_courses = {}
        for ii in range(1, how_much + 1):
            some_scores = []
            for ii in range(1, random.randint(1, 7)):
                some_scores += [random.randint(1, 10)]
            some_courses.setdefault(random.choice(all_courses), some_scores)
        return some_courses

    # назначение курсов студентам с оценками
    if isinstance(other, Student):
        other.courses_finished = dict.fromkeys(some_list_of_courses_with_scores(), [])
        other.courses_in_progress = some_list_of_courses_with_scores()

    # лекторам с оценками от студентов
    if isinstance(other, Lector):
        other.courses_attached = some_list_of_courses_with_scores()

    # проверяющим курсы без оценок
    if isinstance(other, Reviewer):
        other.courses_attached = dict.fromkeys(some_list_of_courses_with_scores(), [])

# создаём по 2 экземпляра каждого класса и даём им предметы и оценки

principle_adam = Principle('Adam')

lector_jonh = Lector('John', 'Jameson')
go_to_course_and_get_yor_scores(lector_jonh)

lector_sean = Lector('Sean', 'Connery')
go_to_course_and_get_yor_scores(lector_sean)

student_pit = Student('Pit', 'Poppins')
go_to_course_and_get_yor_scores(student_pit)

student_bob = Student('Bob', 'Bobbins')
go_to_course_and_get_yor_scores(student_bob)

reviewer_sally = Reviewer('Sally', 'Simons')
go_to_course_and_get_yor_scores(reviewer_sally)

reviever_molly = Reviewer('Molly', 'Miles')
go_to_course_and_get_yor_scores(reviever_molly)

# коньроль


print(student_bob)

print(lector_sean)

print(reviever_molly)
#
# print(lector_sean.courses_attached)
# print(lector_sean)

