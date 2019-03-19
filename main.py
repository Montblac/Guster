import name
import greetgen

if __name__ == '__main__':
    ng = name.NameGenerator()
    ng.initialize()

    gg = greetgen.GreetGenerator()
    phrase = gg.get_greeting()

    print(phrase.format(ng.get_name()))