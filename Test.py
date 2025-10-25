import pickle
class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade # 0 - 100
    def get_grade(self):
        print (self.grade)
s1 = Student("Tim", 19, 95)

#save it
with open(f'test.pickle', 'wb') as file:
    pickle.dump(s1, file) 

#load it
with open(f'test.pickle', 'rb') as file2:
    s1_new = pickle.load(file2)

#check it
s1_new.get_grade()