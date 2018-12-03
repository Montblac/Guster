import namegen

if __name__ == '__main__':
    ng = namegen.NameGenerator()
    ng.initialize()

    print(ng.get_name())