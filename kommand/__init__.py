import os
import sys
import importlib
import json
from colorama import init, Fore, Back, deinit, Style


ROOT = os.path.dirname(sys.modules['__main__'].__file__)
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


def build():
    '''
    ____it's just build json template, if you prefer using command with json and not bother with
    dictionary kwargs and stuff____
    '''
    init()
    q = {
        'name': f'{Fore.CYAN} Your app name: {Style.RESET_ALL}',
        'version': f'{Fore.CYAN} Your app version: {Style.RESET_ALL}',
        'command': f'{Back.CYAN} READY FOR COMMAND OFFICER! '
    }
    r = {'name': '', 'version': '', 'command': [{'your_command': dict(exec='MYFUNC', help='MYHELP')}]}
    for k, v in q.items():
        if k != 'command':
            r[k] = input(v)
        else:
            with open(os.path.join(os.getcwd(), 'command.json'), 'w') as f:
                json.dump(r, f, indent=4)
                f.close()
            print(v)
    deinit()


def control(**kwargs):
    '''
    ____this is your kommand!. this function is created to manage arguments in CLI, just like apps that needs
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
                        execute = kwargs[z]['exec']

                        # ____if there's an dot in execute, then it's must be import otherwise is a locals____
                        if '.' in execute:
                            data = kwargs[z]['exec'].split('.')
                            execute = getattr(importlib.import_module('.'.join(data[:-1])), data[-1])
                        else:
                            print(getattr('.', execute))
                            execute = execute

                        if callable(execute):
                            execute()
        except IndexError:
            print(f'{INFO} \n')
            print(f'ver: {VERSION} \n')
            print('---------- \n')
            print(show_help)
