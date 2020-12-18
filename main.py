# project about students

class Human:
    def __init__(self, name, surename):
        self.name = name
        self.surname = surename
        self.__role = []


class Principle(Human):
    def __init__(self, name, surename):
        super().__init__(name, surename)
        self._Human__role.append('Principle')
        self.index = [{self: self._Human__role}]
#
    def recruit_as(self, other, some_role):
        pass
        other._Human__role.append(some_role)
        self.index.append({other: other._Human__role})

class Student(Human):
    pass


class Lector(Human):
    pass


class Reviewer(Human):
    pass


aaa = Principle('Pet', 'Jhons')
bbb = Lector('Baba', 'Gump')
aaa.recruit_as(bbb, 'shrimplover')
aaa.recruit_as(bbb, 'janitor')

#print(aaa._Human__role)
for person in aaa.index:
    for persons_class in person.keys():
        print(f'имя: {persons_class.name} \n'
              f'фамилия: {persons_class.surname} \n'
              f'роли:  {person[persons_class]}')

# test = {'names': 'tesssssting'}
# for entry in test.keys():
#     print(test[entry])