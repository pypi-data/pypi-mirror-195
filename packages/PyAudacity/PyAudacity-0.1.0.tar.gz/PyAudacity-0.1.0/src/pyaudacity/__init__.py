"""PyAudacity
By Al Sweigart al@inventwithpython.com

A Python module to control a running instance of Audacity through its macro system."""

__version__ = '0.1.0'

import os, sys, time

NON_INTERACTIVE_MODE = True

class PyAudacityException(Exception):
    """The base exception class for PyAudacity-related exceptions."""
    pass


class RequiresInteractionException(PyAudacityException):
    """Raised when a macro that requires human user interaction (such as 
    selecting a file in the Open File dialog) was attempted while 
    NON_INTERACTIVE_MODE was set to True."""
    pass

def do(command):
    if sys.platform == 'win32':
        write_pipe_name = '\\\\.\\pipe\\ToSrvPipe'
        read_pipe_name = '\\\\.\\pipe\\FromSrvPipe'
        eol = '\r\n\0'
    else:
        write_pipe_name = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
        read_pipe_name = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
        eol = '\n'

    if not os.path.exists(write_pipe_name):
        raise PyAudacityException(write_pipe_name + ' does not exist.  Ensure Audacity is running with mod-script-pipe.')
        sys.exit()
    time.sleep(0.0001)  # For reasons unknown, we need a slight pause after checking for the existence of the write file on Windows.

    if not os.path.exists(read_pipe_name):
        raise PyAudacityException(read_pipe_name + ' does not exist.  Ensure Audacity is running with mod-script-pipe.')
        sys.exit()
    time.sleep(0.0001)  # For reasons unknown, we need a slight pause after checking for the existence of the read file on Windows.

    write_pipe = open(write_pipe_name, 'w')
    read_pipe = open(read_pipe_name)

    write_pipe.write(command + eol)
    write_pipe.flush()

    response = ''
    line = ''
    while True:
        response += line
        line = read_pipe.readline()
        if line == '\n' and len(response) > 0:
            break

    write_pipe.close()
    time.sleep(0.0001)  # For reasons unknown, we need a slight pause after closing the write file on Windows.
    read_pipe.close()  
 
    #return response
    print(response)


def _requireInteraction():
    if NON_INTERACTIVE_MODE:
        raise RequiresInteractionException()


def new():
    """Creates a new empty project window, to start working on new or 
    imported tracks.

    NOTE: The macros issued from pyaudacity always apply to the last Audacity 
    window opened. There's no way to pick which Audacity window macros are
    applied to."""
    do('New')

def open():
    """Presents a standard dialog box where you can select either audio 
    files, a list of files (.LOF) or an Audacity Project file to open."""
    _requireInteraction()
    do('Open')
