import random


class Flower(object):
    def accept(self, visitor):
        visitor.visit(self)

    def pollinate(self, pollinator):
        print(self, "polenizata de", pollinator)

    def eat(self, eatter):
        print(self, "mancata de", eatter)

    def __str__(self):
        return self.__class__.__name__

class Gladiolus(Flower) : pass
class Runculus(Flower) : pass
class Chrysanthemum(Flower) : pass

class Carnivore(Flower):
    def pollinate(self, pollinator):
        if str(pollinator) == 'Bee':
            print(pollinator, "mancat de", self)

class Poison(Flower):
    def eat(self, eatter):
        if str(eatter) == 'Worm':
            print(eatter, "a fost otravit", self)

class Visitor:
    def __str__(self):
        return self.__class__.__name__


class Bug(Visitor): pass
class Pollinator(Bug) : pass
class Predator(Bug) : pass


class Bee(Pollinator):

    def visit(self, flower):
        flower.pollinate(self)


class Fly(Pollinator):

    def visit(self, flower):
        flower.pollinate(self)

class Worm(Predator):
    def visit(self, flower):
        flower.eat(self)

def flowerGen(n):
    flowers = Flower.__subclasses__()
    for i in range(n):
        yield random.choice(flowers)()

###########  Main ############

bee = Bee()
worm = Worm()
fly = Fly()

for flower in flowerGen(10):
    flower.accept(bee)
    flower.accept(fly)
    flower.accept(worm)