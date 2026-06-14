# example of a class with an abstract method
from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def make_sound(self):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod    
    def eat(self):
        pass

class Dog(Animal):
    def make_sound(self):
        return "Woof!"

    def move(self):
        return "The dog runs."

    def eat(self):
        return "The dog eats dog food."

class Cat(Animal):
    def make_sound(self):
        return "Meow!"


    def move(self):
        return "The cat jumps."


# create instances of Dog and Cat
dog = Dog("Buddy")
cat = Cat("Whiskers")
# call the methods
print(f"{dog.name} says: {dog.make_sound()}")
print(f"{dog.name} moves: {dog.move()}")
print(f"{cat.name} says: {cat.make_sound()}")
