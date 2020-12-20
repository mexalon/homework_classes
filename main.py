import random

# функция для подсчёта средней оценки одного объекта по определеннуму курсу
# если оценок нет, то средняя оценка для определённости счмтается 0
def average_grade_for_something(course, dict_of_courses):
    average_grade_num = 0
    if course in dict_of_courses.keys() and isinstance(dict_of_courses[course], list):
        if len(dict_of_courses[course]) != 0:
            average_grade_num = sum(dict_of_courses[course]) / len(dict_of_courses[course])

    return average_grade_num

# функция для определения средней оценки одного объекта по всем курсам
# считается среднее среди средних оценок по предметам != среднему всех оценок
def average_grade_for_all(dict_of_courses):
    average_grade_for_all_num = 0
    sum_of_grades = 0
    if len(dict_of_courses) != 0:
        for entry in dict_of_courses.keys():
            sum_of_grades += average_grade_for_something(entry, dict_of_courses)

        average_grade_for_all_num = round(sum_of_grades / len(dict_of_courses), 2)

    return average_grade_for_all_num

# функция подсчёта средней оценки по предмету для набора объектов
def average_grade_in_class(course, *list_of_persons):
    average_grade_in_class_num = 0
    sum_of_grades = 0
    if len(list_of_persons) != 0:
        counter = 0
        for entry in list_of_persons:
            if isinstance(entry, Student):
                if course in entry.courses_in_progress.keys():
                    sum_of_grades += average_grade_for_something(course, entry.courses_in_progress)
                    counter += 1

            if isinstance(entry, Lector):
                if course in entry.courses_attached.keys():
                    sum_of_grades += average_grade_for_something(course, entry.courses_attached)
                    counter += 1
        if counter > 0:
            average_grade_in_class_num = round(sum_of_grades / counter, 2)
        else:
            average_grade_in_class_num = 0

    return average_grade_in_class_num

# функция для назначения студентам и преподавателям случайного набора курсов и оценок
def go_to_course_and_get_yor_scores(other):
    # создавалка словаря случайных курсов и оценок, чтобы в ручную не заполнять
    def some_list_of_courses_with_scores():
        all_courses = ['Math', 'Phyton', 'Physics', 'Art', 'Sport', 'Music']
        how_much = random.randint(1, len(all_courses))
        some_courses = {}
        for ii in range(1, how_much + 1):
            some_scores = []
            for ii in range(1, random.randint(2, 7)):
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


# класс человек из которого получаются все прочие. По заданию нужно было сделатьотдельные
# классы менторов: лекторов, проверяющих и студентов.
class Human:
    #словарь для индексирования объектов, чтобы не собирать их вручную при создании
    all_kind_of_people = {}

    def __init__(self, name, surname='Smith'):
        self.name = name
        self.surname = surname
        self.all_kind_of_people.setdefault(type(self), [])
        self.all_kind_of_people[type(self)] += [self]

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


# класс студентов
class Student(Human):
    def __init__(self, name, surname='Smith'):
        super().__init__(name, surname)
        self.courses_finished = {}
        self.courses_in_progress = {}

    # метод оценки лектора
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


# класс ревьюверы
class Reviewer(Mentor):
    def __init__(self, name, surname='Smith'):
        super().__init__(name, surname)

    # метод для оценки студента
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


# создаём по 2 экземпляра каждого класса и даём им предметы и оценки
lector_john = Lector('John', 'Jameson')
lector_john.courses_attached['Math'] = [4, 5, 6]

lector_sean = Lector('Sean', 'Connery')
lector_sean.courses_attached['Art'] = [4, 5, 6, 9]
lector_sean.courses_attached['Math'] = [7]

student_pit = Student('Pit', 'Poppins')
student_pit.courses_in_progress['Math'] = [4, 5]
student_pit.courses_finished['Art'] = [2, 4, 7]

student_bob = Student('Bob', 'Bobbins')
student_bob.courses_in_progress['Math'] = [1, 2]
student_bob.courses_finished['Art'] = [4, 7, 8]

reviewer_sally = Reviewer('Sally', 'Simons')
reviewer_sally.courses_attached['Math'] = []

reviewer_molly = Reviewer('Molly', 'Miles')
go_to_course_and_get_yor_scores(reviewer_molly)

# вызовите все созданные методы, а также реализуйте две функции.
# выставление оценок ревьювером студенту + результат перегрузки __str__
print(f'Студент до оценивания:\n{student_pit}')
print(f'Его оценки по математике: {student_pit.courses_in_progress["Math"]}')

# пытаемся поставить оценку студенту
reviewer_sally.rate(student_pit, 'Math', 9)
print(f'Его оценки после оценивания ревьювером: {student_pit.courses_in_progress["Math"]}')
print(f'Оценил ревьювер:\n{reviewer_sally}\n')

# студент стави оценку лектору
print(f'Лектор:\n{lector_john}')
print(f'Его оценки от студентов курса математики: {lector_john.courses_attached["Math"]}')
student_pit.rate(lector_john, 'Math', 9)
print(f'Его оценки после оценивания: {lector_john.courses_attached["Math"]}\n')

# результат перегрузки метода __gt__
def compare_two_person(first, second):
    if first > second:
        result = 'лучше чем'
    else:
        result = 'хуже чем'
    print(f'{first.name} {first.surname} {result} {second.name} {second.surname}')

compare_two_person(lector_sean, lector_john)
compare_two_person(student_bob, student_pit)

#добавляем ещё рандомных студентов и лекторов для Задания №4, чтобы было интересней
list_of_random_students = [Student(f'Random_student_#{ii}') for ii in range(1, 11)]
[go_to_course_and_get_yor_scores(entry) for entry in list_of_random_students]

list_of_random_lectors = [Lector(f'Random_lector_#{ii}') for ii in range(1, 11)]
[go_to_course_and_get_yor_scores(entry) for entry in list_of_random_lectors]

#создаём списки всех студентов и лекторов
know_it_all_man = Human('Sam')
list_of_students = know_it_all_man.all_kind_of_people[Student]
list_of_lectors = know_it_all_man.all_kind_of_people[Lector]

#средняя оцека студентов на курсе
print('\nКурсы и оценки студентов, учащихся на курсе математики: ')
for entry in list_of_students:
    if 'Math' in entry.courses_in_progress.keys():
        print(f'Студент {entry.name} {entry.surname} имеет по математике {entry.courses_in_progress["Math"]}')

print(f'\nСредняя оценка студентов по Математике: {average_grade_in_class("Math", *list_of_students)}')

#средняя оценка лекторов курса математики
print('\nКурсы и оценки лекторов, преподающих математику: ')
for entry in list_of_lectors:
    if 'Math' in entry.courses_attached.keys():
        print(f'Лектор {entry.name} {entry.surname} оценён студентами: {entry.courses_attached["Math"]}')

print(f'\nСредняя оценка всех лекторов Математики: {average_grade_in_class("Math", *list_of_lectors)}')


