import scrape

if __name__ == '__main__':
    parser = scrape.URLParser()
    parser.initialize()

    names = parser.names()
    for name in names:
        print(name)
    print(len(names))