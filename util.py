from settings import *

def debug_print(content):
    '''
    Special print statement (prints only in debug mode, otherwise logs to file)
    Input:
        content - content to be printed
    '''
    if debug:
        print(content)
    else:
        debug_log.write(str(content))
        debug_log.write("\n")
        
        