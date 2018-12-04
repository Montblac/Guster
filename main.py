import namegen
import greetgen

if __name__ == '__main__':
    ng = namegen.NameGenerator()
    ng.initialize()

    gg = greetgen.GreetGenerator()
    phrase = gg.get_greeting()

    print(phrase.format(ng.get_name()))