import random


# хорошо ли внутри объявления класса вызывать внешнюю функцию?
def average_grade_for_something(course, dict_of_courses):
    average_grade_num = 0
    if course in dict_of_courses.keys() and isinstance(dict_of_courses[course], list):
        if len(dict_of_courses[course]) != 0:
            average_grade_num = sum(dict_of_courses[course]) / len(dict_of_courses[course])

    return average_grade_num


# метод для определения средней оценки по всем курсам из словаря
# считается среднее среди средних оценок по предметам != среднему всех оценок
def average_grade_for_all(dict_of_courses):
    average_grade_for_all_num = 0
    sum_of_grades = 0
    if len(dict_of_courses) != 0:
        for entry in dict_of_courses.keys():
            sum_of_grades += average_grade_for_something(entry, dict_of_courses)
        average_grade_for_all_num = round(sum_of_grades / len(dict_of_courses), 1)

    return average_grade_for_all_num


# класс человек из которого получаются все прочие. По заданию нужно было сделатьотдельные
# классы менторов: лекторов, проверяющих и студентов. Мне кажется, можно все сделать гораздо компактней,
# если не делать эти подклассы, а разбиение по ролям сделать при помощи атрибутов
class Human:
    _of_all_kind = {}

    def __init__(self, name, surname='Smith'):
        self.name = name
        self.surname = surname
        self._of_all_kind.setdefault(type(self), [])
        self._of_all_kind[type(self)] += [self]

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


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
                if other.courses_attached[course] is not None:
                    other.courses_attached[course] += [grade]
                else:
                    other.courses_attached[course] = [grade]
            else:
                print('Нельзя ставить оценку')
        else:
            print('Где то ошибка')

    def __str__(self):
        if self.courses_in_progress != {}:
            str_of_progress_courses = ', '.join(list(self.courses_in_progress.keys()))
        else:
            str_of_progress_courses = 'Курсов нет'

        if self.courses_finished != {}:
            str_of_finished_courses = ', '.join(list(self.courses_finished.keys()))
        else:
            str_of_finished_courses = 'Курсов нет'

        return super().__str__() + f'\nСредняя оценка за домашку:' \
                                       f' {average_grade_for_all(self.courses_in_progress)}' \
                                       f'\nКурсы в процессе изучения:' \
                                       f' {str_of_progress_courses}' \
                                       f'\nЗавершенные курсы:' \
                                       f' {str_of_finished_courses}'

    def __gt__(self, other):
        result = False
        if isinstance(other, Student):
            if average_grade_for_all(self.courses_in_progress) > average_grade_for_all(
                    other.courses_in_progress):
                result = True
            else:
                result = False

        return result


# класс метроров - самый бессмысленный
class Mentor(Human):
    def __init__(self, name, surname='Smith'):
        super().__init__(name, surname)
        self.courses_attached = {}


# класс лекторы
class Lector(Mentor):
    def __init__(self, name, surname='Smith'):
        super().__init__(name, surname)

    def __str__(self):
        if self.courses_attached != {}:
            return super().__str__() + f'\nСредняя оценка от студентов:' \
                                       f' {average_grade_for_all(self.courses_attached)}'
        else:
            return super().__str__() + f'\nКурсов нет'

    def __gt__(self, other):
        result = False
        if isinstance(other, Lector):
            if average_grade_for_all(self.courses_attached) > average_grade_for_all(
                    other.courses_attached):
                result = True
            else:
                result = False

        return result


# класс проверяторы
class Reviewer(Mentor):
    def __init__(self, name, surname='Smith'):
        super().__init__(name, surname)

    # постановка оценки студенту
    def rate(self, other, course, grade):
        if isinstance(other, Student) and isinstance(grade, int):
            if course in self.courses_attached.keys() and course in other.courses_in_progress.keys() and 1 <= grade <= 10:
                if other.courses_in_progress[course] is not None:
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

test_student = Student('Tester')

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
print(test_student)
print(test_student.courses_in_progress)
print(student_bob > test_student)
print(student_bob > lector_jonh)
print('\n')

print(student_bob)
print(student_bob.courses_in_progress)
print('\n')
print(student_pit)
print(student_pit.courses_in_progress)
print('\n')
print(student_bob > student_pit)
print('\n')
print(lector_sean)
print(lector_sean.courses_attached)
print('\n')
print(lector_jonh)
print(lector_jonh.courses_attached)
print('\n')
print(lector_sean > lector_jonh)
print('\n')
print(reviever_molly)
#
# print(lector_sean.courses_attached)
# print(lector_sean)
