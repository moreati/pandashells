#! /usr/bin/env python

# standard library imports
import argparse
import datetime
import importlib
import os
import re
import sys

from pandashells.lib import module_checker_lib, arg_lib, io_lib


def needs_plots(command_list):
    # define regex to identify plot commands
    plot_command_list = [
        'plot', 'hist', 'scatter', 'figure', 'subplot', 'xlabel', 'ylabel',
        'set_xlabel', 'set_ylabel', 'title', 'set_xlim', 'set_ylim', 'legend',
        'twinx', 'gca', 'gcf'
    ]
    rex_plot_str = r'.*({})\(.*\).*'.format('|'.join(plot_command_list))
    if re.compile(rex_plot_str).match(' '.join(command_list)):
        return True
    else:
        return False


def get_modules_and_shortcuts(command_list):
    names_shortcuts = [
        ('numpy', 'np'),
        ('scipy', 'scp'),
        ('pylab', 'pl'),
        ('seaborn', 'sns'),
    ]
    base_requirements = [
        ('pandas', 'pd'),
        ('dateutil', 'dateutil'),
    ]
    out = base_requirements + [
        tup for tup in names_shortcuts
        if '{}.'.format(tup[1]) in ' '.join(command_list)
    ]
    if needs_plots(command_list):
        out = list(set([('pylab', 'pl')] + out))
    return out


def main():
    # read command line arguments
    msg = (
        "Bring pandas manipulation to command line.  Input from stdin "
         "is placed into a dataframe named 'df'.  The output of each "
         "specified command must evaluate to a dataframe that will "
         "overwrite 'df'. The output of the final command will be sent "
         "to stdout.  The namespace in which the commands are executed "
         "includes pandas as pd, numpy as np, scipy as scp, pylab as pl, "
         "dateutil.parser.parse as parse, datetime.  Plot-specific "
         "commands will be ignored unless a supplied command creates "
         "a plot. "
    )
    parser = argparse.ArgumentParser(description=msg)
    arg_lib.add_args(parser, 'io_in', 'io_out', 'decorating', 'example')
    parser.add_argument("statement", help="Statement to execute", nargs="*")
    args = parser.parse_args()

    # get a list of commands to execute
    command_list = args.statement

    # make sure all the required modules are installed
    module_checker_lib.check_for_modules([
        m for (m, s) in get_modules_and_shortcuts(command_list)
    ])

    # import required modules
    from dateutil.parser import parse
    for (module, shortcut) in get_modules_and_shortcuts(command_list):
        exec('import {} as {}'.format(module, shortcut))




if __name__ == '__main__':
    main()

#
#
#
#
#
#
#
###############################################################################
#
## standard library imports
#import os
#import sys
#import argparse
#import re
#
#from pandashells.lib import module_checker_lib, arg_lib, io_lib, plot_lib
#
## import required dependencies
#modulesOkay = module_checker_lib.check_for_modules([
#    'pandas',
#    'numpy',
#    'scipy',
#    'dateutil',
#    'matplotlib'])
#if not modulesOkay:
#    sys.exit(1)
#
#import pandas as pd
#import numpy as np
#import scipy as scp
#import pylab as pl
#from dateutil.parser import parse
#import datetime
#
#
#
#
#
#
#
## ============================================================================
#if __name__ == '__main__':
#    msg = "Bring pandas manipulation to command line.  Input from stdin "
#    msg += "is placed into a dataframe named 'df'.  The output of each "
#    msg += "specified command must evaluate to a dataframe that will "
#    msg += "overwrite 'df'. The output of the final command will be sent "
#    msg += "to stdout.  The namespace in which the commands are executed "
#    msg += "includes pandas as pd, numpy as np, scipy as scp, pylab as pl, "
#    msg += "dateutil.parser.parse as parse, datetime.  Plot-specific "
#    msg += "commands will be ignored unless a supplied command creates "
#    msg += "a plot. "
#
#    # read command line arguments
#    parser = argparse.ArgumentParser(description=msg)
#
#    options = {}
#    arg_lib.addArgs(parser, 'io_in', 'io_out', 'decorating', 'example')
#    parser.add_argument("statement", help="Statement to execute", nargs="*")
#
#    # parse arguments
#    args = parser.parse_args()
#
#    # set up plot styling in case it's needed
#    plot_lib.set_plot_styling(args)
#
#    # get the input dataframe
#    df = io_lib.df_from_input(args)
#
#    # define regex to identify if supplied command is for col assignment
#    rex_col_cmd = re.compile(r'.*?df\[.+\].*?=')
#
#    # define regex to identify plot commands
#    plot_command_list = [
#        'plot',
#        'hist',
#        'scatter',
#        'figure',
#        'subplot',
#        'xlabel',
#        'ylabel',
#        'set_xlabel',
#        'set_ylabel',
#        'title',
#        'set_xlim',
#        'set_ylim',
#        'legend',
#        'twinx',
#        'gca',
#        'gcf']
#
#    pstring = '|'.join(plot_command_list)
#    rex_plot_str = r'.*({})\(.*\).*'.format(pstring)
#    rex_plot_cmd = re.compile(rex_plot_str)
#    needs_show = False
#
#    # default temp to df to handle no statement provided case
#    temp = df
#
#    # execute the statements in sequence
#    for cmd in args.statement:
#        # if this is a column-assignment command, just execute it
#        if rex_col_cmd.match(cmd):
#            exec(cmd)
#            temp = df
#        # if this is a plot command, execute it and quit
#        elif rex_plot_cmd.match(cmd):
#            exec(cmd)
#            needs_show = True
#
#        # if instead this is a command on the whole frame
#        else:
#            # put results of command in temp var
#            cmd = 'temp = {}'.format(cmd)
#            exec(cmd)
#
#        # transform results to dataframe if needed
#        if not rex_plot_cmd.match(cmd):
#            if isinstance(temp, pd.DataFrame):
#                df = temp
#            else:
#                try:
#                    df = pd.DataFrame(temp)
#                except pd.core.common.PandasError:
#                    print temp
#                    sys.exit(0)
#
#    # show plots if requested
#    if needs_show:
#        plot_lib.refine_plot(args)
#        plot_lib.show(args)
#    # otherwise print results
#    else:
#        io_lib.df_to_output(args, df)
#
#
#
#
#
#
##class CommandProcessor(object):
##    def __init__(self, args):
##        self.args = args
##        # define regex to identify if supplied command is for col assignment
##        self.rex_col_cmd = re.compile(r'.*?df\[.+\].*?=')
##
##        # define regex to identify plot commands
##        plot_command_list = [
##            'plot', 'hist', 'scatter', 'figure', 'subplot', 'xlabel', 'ylabel',
##            'set_xlabel', 'set_ylabel', 'title', 'set_xlim', 'set_ylim',
##            'legend', 'twinx', 'gca', 'gcf'
##        ]
##        pstring = '|'.join(plot_command_list)
##        rex_plot_str = r'.*({})\(.*\).*'.format(pstring)
##        self.rex_plot_cmd = re.compile(rex_plot_str)
##
##        # read in the commands
##        self.command_list = args.statement
##
##        # read the input dataframe
##        self.df = io_lib.df_from_input(self.args)
##
##
##    def _
##
#
#
