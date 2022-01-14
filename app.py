

from ui import login_window


def login():
    if login_window():
        print('Parent logged in')
    else:
        print('Child logged in')

def main():
    login()

if __name__ == '__main__':
    main()