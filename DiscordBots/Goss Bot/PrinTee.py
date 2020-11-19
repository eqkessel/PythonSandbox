import os
import sys

import datetime

class PrinTee:
    def __init__(self, *, name='', suffix='.log', file_opt='a+', path='logs', path_is_absolute=False, auto_flush=True):
        #   Check if sys.stdout is already overridden. If so, reset it before continuing
        if isinstance(sys.stdout, PrinTee):
            sys.stdout.file.close()
            sys.stdout = sys.stdout.console

        #   Store the current console
        self.console = sys.stdout

        if not path_is_absolute:
            #   Path is given relative to the present working directory
            path = os.path.join(os.getcwd(), path)

        #   Create the directory if it doesn't exist
        os.makedirs(path, exist_ok=True)

        #   Assemble filepath from path, name, today's date, and suffix
        filepath = os.path.join(path, name + str(datetime.date.today()) + suffix)

        #   Attempt to open a file
        try:
            self.file = open(filepath, file_opt)
            self.file.write(f"---------[FILE LOGGING STARTED AT {datetime.datetime.now()}]---------\n")
        except Exception as e:
            self.file = None
            print(f"FAILED TO OPEN FILEPATH {filepath}\n{repr(e)}")

        self.auto_flush = auto_flush    #   Store for later use

    def write(self, msg):
        #   Echo message to stored console
        self.console.write(msg)
        if self.auto_flush:
            try:
                self.console.flush()    #   Flush automatically with each message
            except:
                pass    #   Some consoles do not have flush() availiable to the user. Move along

        if self.file is not None:
            #   File has to be opened to work
            # self.file.write('START OF MSG: ' + msg + ' :END OF MSG\n')
            
            if (msg == '\n'):
                return

            time_string = '[' + str(datetime.datetime.now()) + '] '
            spacer_string = ' '*len(time_string)

            substrings = msg.split('\n')
            self.file.write(time_string + substrings.pop(0) + '\n')
            for line in substrings:
                self.file.write(spacer_string + line + '\n')

            self.file.flush()

    def flush(self):
        #   Pass a flush down the line
        try:
            self.console.flush()
        except:
            pass    #   Some consoles do not have flush() availiable to the user. Move along

def start_printee_logging(**kwargs):
    '''
    start_printee_logging() - simplest way to enable tee-ed logging of sys.stdout

    KEYWORD ARGUMENTS:
        name -- start of log filename (default: '')
        suffix -- suffix of log filename (default: '.log')
        file_opt -- file opening options (default: 'a+')
        path -- folder to save logs to (default: 'logs')
        path_is_absolute -- whether path above is absolute or local to cwd (default: False)
        auto_flush -- whether to automatically flush messages on reciept (default: True)

    USAGE:
        import PrinTee
        start_printee_logging([arguments])
    '''
    sys.stdout = PrinTee(**kwargs)
    sys.stderr = sys.stdout

    return sys.stdout