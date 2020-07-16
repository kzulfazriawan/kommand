import sys
import importlib


VERSION = '0.1-a'
INFO = '''
____THIZ IZ YOUR KOMMAND!____
|||    |||     |||     ||||||     |||||| ||||||     ||||||      ||||      ||||     ||| ||||||     |||||||
|||  |||     ||| |||   |||  ||| |||  ||| |||  ||| |||  |||     ||||||     |||||    ||| |||  |||   |||||||
||||||     |||     ||| |||    |||    ||| |||    |||    |||    |||  |||    ||| |||  ||| |||   |||   |||||
||||||     |||     ||| |||     |     ||| |||     |     |||   |||    |||   |||  ||| ||| |||   |||    |||
|||  |||     ||| |||   |||           ||| |||           |||  ||||||||||||  |||   |||||| |||  |||  
|||    |||     |||     |||           ||| |||           ||| |||        ||| |||    ||||| ||||||       |||
'''


def control(**kwargs):
    '''
    ____this is your kommander!. this function is created to manage arguments in CLI, just like apps that needs
    arguments in CLI to run some options or modules, for example: python kommand.py test more-test. the script
    will run function that registered on it from first command to second.____
    '''
    argv = sys.argv

    # ____first I'll find the biggest string from kwargs, it'll be used as biggest edge of space in string____
    big_len = len(max([i for i in kwargs.keys()], key=len))
    show_help = ''

    for k, v in kwargs.items():
        h_key = f'{k}'

        # ____if the key is smaller than the biggest one, then it fill with spaces leftover. otherwise pass____
        if len(k) < big_len:
            space = ''.join([' ' for x in range(0, big_len - len(k))])
            h_key = f'{k}{space}'

        show_help += f'{h_key} {v["help"]}\n'

    if isinstance(argv, list):
        # ____delete argv[0] because it's name file____
        # file = argv[0]
        del argv[0]

        # ____if help is show help, otherwise run the function that need to be run____
        show_help = f'Usage example: "python myscript.py [Options]"\nOptions: \n---\n{show_help}'
        try:
            if argv[0] == 'help':
                print(show_help)
            else:
                for z in argv:
                    if z in kwargs:
                        data = kwargs[z]['module'].split('.')
                        func = getattr(importlib.import_module('.'.join(data[:-1])), data[-1])
                        if callable(func):
                            func()
        except IndexError:
            print(f'{INFO} \n')
            print(f'ver: {VERSION} \n')
            print('---------- \n')
            print(show_help)
