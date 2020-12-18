# project about students

class Human:
    def __init__(self, name, surename = 'Smith'):
        self.name = name
        self.surname = surename
        self.__role = []

# директор тоже человек, он назначает на роли разные классы и ведёт журнал учёта

class Principle(Human):
    def __init__(self, name, surename):
        super().__init__(name, surename)
        self._Human__role.append('Principle')
        self.index = {self: self._Human__role}

    def recruit_as(self, other, some_role):
        pass
        other._Human__role.append(some_role)
        self.index[other] = other._Human__role


class Student(Human):
    pass


class Lector(Human):
    pass


class Reviewer(Human):
    pass


aaa = Principle('Pet', 'Jhons')
bbb = Lector('Baba', 'Gump')
ccc = Student('Pepe')


aaa.recruit_as(bbb, 'shrimplover')
aaa.recruit_as(bbb, 'janitor')
aaa.recruit_as(ccc, 'stupid student')


#print(aaa._Human__role)
for person in aaa.index.keys():
    print(f'имя: {person.name} \n'
          f'фамилия: {person.surname} \n'
          f'роли:  {aaa.index[person]}')

# test = {'names': 'tesssssting'}
# for entry in test.keys():
#     print(test[entry])