#!/usr/bin/env python

# Copyright 2015-2020 Earth Sciences Department, BSC-CNS

# This file is part of Autosubmit.

# Autosubmit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Autosubmit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Autosubmit.  If not, see <http://www.gnu.org/licenses/>.
import threading
import traceback
import requests
import collections

from .job.job_packager import JobPackager
from .job.job_exceptions import WrongTemplateException
from .platforms.paramiko_submitter import ParamikoSubmitter
from .platforms.platform import Platform
from .notifications.notifier import Notifier
from .notifications.mail_notifier import MailNotifier
from bscearth.utils.date import date2str
from pathlib import Path
from autosubmitconfigparser.config.yamlparser import YAMLParserFactory

try:
    # noinspection PyCompatibility
    from configparser import SafeConfigParser
except ImportError:
    # noinspection PyCompatibility
    from bscearth.utils.config_parser import ConfigParser as SafeConfigParser

from .monitor.monitor import Monitor
from .database.db_common import get_autosubmit_version, check_experiment_exists
from .database.db_common import delete_experiment, update_experiment_descrip_version, get_experiment_descrip
from .database.db_structure import get_structure
from .experiment.experiment_common import copy_experiment
from .experiment.experiment_common import new_experiment
from .database.db_common import create_db
from .job.job_grouping import JobGrouping
from .job.job_list_persistence import JobListPersistencePkl
from .job.job_list_persistence import JobListPersistenceDb
from .job.job_package_persistence import JobPackagePersistence
from .job.job_packages import JobPackageThread, JobPackageBase
from .job.job_list import JobList
from .job.job_utils import SubJob, SubJobManager
from .job.job import Job
from .git.autosubmit_git import AutosubmitGit
from .job.job_common import Status
from autosubmitconfigparser.config.configcommon import AutosubmitConfig
from autosubmitconfigparser.config.basicconfig import BasicConfig
import locale
from distutils.util import strtobool
from log.log import Log, AutosubmitError, AutosubmitCritical
from typing import Set
from autosubmit.database.db_common import update_experiment_descrip_version

import sqlite3

# try:
#    import pythondialog as dialog
# except Exception:
dialog = None
from time import sleep
import argparse
import subprocess
import json
import tarfile
import time
import copy
import os
import glob
import pwd
import sys
import shutil
import re
import random
import signal
import datetime

import portalocker
from pkg_resources import require, resource_listdir, resource_exists, resource_string, resource_filename
from collections import defaultdict
from pyparsing import nestedExpr
from .history.experiment_status import ExperimentStatus
from .history.experiment_history import ExperimentHistory
from typing import List
import autosubmit.history.utils as HUtils
import autosubmit.helpers.autosubmit_helper as AutosubmitHelper
import autosubmit.statistics.utils as StatisticsUtils

"""
Main module for autosubmit. Only contains an interface class to all functionality implemented on autosubmit
"""

sys.path.insert(0, os.path.abspath('.'))


# noinspection PyUnusedLocal


def signal_handler(signal_received, frame):
    """
    Used to handle interrupt signals, allowing autosubmit to clean before exit

    :param signal_received:
    :param frame:
    """
    Log.info('Autosubmit will interrupt at the next safe occasion')
    Autosubmit.exit = True


def signal_handler_create(signal_received, frame):
    """
    Used to handle KeyboardInterrupt signals while the create method is being executed

    :param signal_received:
    :param frame:
    """
    raise AutosubmitCritical(
        'Autosubmit has been closed in an unexpected way. Killed or control + c.', 7010)


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


class Autosubmit:
    """
    Interface class for autosubmit.
    """

    def __init__(self):
        self._experiment_data = {}

    @property
    def experiment_data(self):
        """Get the current voltage."""
        return self.experiment_data

    sys.setrecursionlimit(500000)
    # Get the version number from the relevant file. If not, from autosubmit package
    script_dir = os.path.abspath(os.path.dirname(__file__))

    if not os.path.exists(os.path.join(script_dir, 'VERSION')):
        script_dir = os.path.join(script_dir, os.path.pardir)

    version_path = os.path.join(script_dir, 'VERSION')
    readme_path = os.path.join(script_dir, 'README')
    changes_path = os.path.join(script_dir, 'CHANGELOG')
    if os.path.isfile(version_path):
        with open(version_path) as f:
            autosubmit_version = f.read().strip()
    else:
        autosubmit_version = require("autosubmit")[0].version

    exit = False

    @staticmethod
    def parse_args():
        """
        Parse arguments given to an executable and start execution of command given
        """

        try:
            BasicConfig.read()
            parser = MyParser(
                description='Main executable for autosubmit. ')
            parser.add_argument('-v', '--version', action='version',
                                version=Autosubmit.autosubmit_version)
            parser.add_argument('-lf', '--logfile', choices=('NO_LOG', 'INFO', 'WARNING', 'DEBUG'),
                                default='DEBUG', type=str,
                                help="sets file's log level.")
            parser.add_argument('-lc', '--logconsole', choices=('NO_LOG', 'INFO', 'WARNING', 'DEBUG'),
                                default='INFO', type=str,
                                help="sets console's log level")

            subparsers = parser.add_subparsers(dest='command')
            # Run
            subparser = subparsers.add_parser(
                'run', description="runs specified experiment")
            subparser.add_argument('expid', help='experiment identifier')
            subparser.add_argument('-nt', '--notransitive', action='store_true',
                                   default=False, help='Disable transitive reduction')
            subparser.add_argument('-v', '--update_version', action='store_true',
                                   default=False, help='Update experiment version')
            subparser.add_argument('-st', '--start_time', required=False,
                                   help='Sets the starting time for this experiment')
            subparser.add_argument('-sa', '--start_after', required=False,
                                   help='Sets a experiment expid which completion will trigger the start of this experiment.')
            subparser.add_argument('-rom', '--run_only_members', required=False,
                                   help='Sets members allowed on this run.')


            # Expid
            subparser = subparsers.add_parser(
                'expid', description="Creates a new experiment")
            group = subparser.add_mutually_exclusive_group()
            group.add_argument(
                '-y', '--copy', help='makes a copy of the specified experiment')
            group.add_argument('-dm', '--dummy', action='store_true',
                               help='creates a new experiment with default values, usually for testing')
            group.add_argument('-min', '--minimal_configuration', action='store_true',
                               help='creates a new experiment with minimal configuration, usually combined with -repo')
            subparser.add_argument('-repo', '--git_repo', type=str, default="", required=False,
                                   help='sets a git repository for the experiment')
            subparser.add_argument('-b', '--git_branch', type=str, default="", required=False,
                                   help='sets a git branch for the experiment')
            subparser.add_argument('-conf', '--git_as_conf', type=str, default="", required=False,help='sets the git path to as_conf')

            group.add_argument('-op', '--operational', action='store_true',
                               help='creates a new experiment with operational experiment id')
            subparser.add_argument('-H', '--HPC', required=False, default="local",
                                   help='specifies the HPC to use for the experiment')
            subparser.add_argument('-d', '--description', type=str, required=True,
                                   help='sets a description for the experiment to store in the database.')

            # Delete
            subparser = subparsers.add_parser(
                'delete', description="delete specified experiment")
            subparser.add_argument('expid', help='experiment identifier')
            subparser.add_argument(
                '-f', '--force', action='store_true', help='deletes experiment without confirmation')
            subparser.add_argument('-v', '--update_version', action='store_true',
                                   default=False, help='Update experiment version')
            # Monitor
            subparser = subparsers.add_parser(
                'monitor', description="plots specified experiment")
            subparser.add_argument('expid', help='experiment identifier')
            subparser.add_argument('-o', '--output', choices=('pdf', 'png', 'ps', 'svg', 'txt'),
                                   help='chooses type of output for generated plot')  # Default -o value comes from .yml
            subparser.add_argument('-group_by', choices=('date', 'member', 'chunk', 'split', 'automatic'), default=None,
                                   help='Groups the jobs automatically or by date, member, chunk or split')
            subparser.add_argument('-expand', type=str,
                                   help='Supply the list of dates/members/chunks to filter the list of jobs. Default = "Any". '
                                        'LIST = "[ 19601101 [ fc0 [1 2 3 4] fc1 [1] ] 19651101 [ fc0 [16-30] ] ]"')
            subparser.add_argument(
                '-expand_status', type=str, help='Select the stat uses to be expanded')
            subparser.add_argument('--hide_groups', action='store_true',
                                   default=False, help='Hides the groups from the plot')
            subparser.add_argument('-cw', '--check_wrapper', action='store_true',
                                   default=False, help='Generate possible wrapper in the current workflow')
            group2 = subparser.add_mutually_exclusive_group(required=False)

            group.add_argument('-fs', '--filter_status', type=str,
                               choices=('Any', 'READY', 'COMPLETED',
                                        'WAITING', 'SUSPENDED', 'FAILED', 'UNKNOWN'),
                               help='Select the original status to filter the list of jobs')
            group = subparser.add_mutually_exclusive_group(required=False)
            group.add_argument('-fl', '--list', type=str,
                               help='Supply the list of job names to be filtered. Default = "Any". '
                                    'LIST = "b037_20101101_fc3_21_sim b037_20111101_fc4_26_sim"')
            group.add_argument('-fc', '--filter_chunks', type=str,
                               help='Supply the list of chunks to filter the list of jobs. Default = "Any". '
                                    'LIST = "[ 19601101 [ fc0 [1 2 3 4] fc1 [1] ] 19651101 [ fc0 [16-30] ] ]"')
            group.add_argument('-fs', '--filter_status', type=str,
                               choices=('Any', 'READY', 'COMPLETED',
                                        'WAITING', 'SUSPENDED', 'FAILED', 'UNKNOWN'),
                               help='Select the original status to filter the list of jobs')
            group.add_argument('-ft', '--filter_type', type=str,
                               help='Select the job type to filter the list of jobs')
            subparser.add_argument('--hide', action='store_true', default=False,
                                   help='hides plot window')
            group2.add_argument('-txt', '--text', action='store_true', default=False,
                                help='Generates only txt status file')

            group2.add_argument('-txtlog', '--txt_logfiles', action='store_true', default=False,
                                help='Generates only txt status file(AS < 3.12b behaviour)')

            subparser.add_argument('-nt', '--notransitive', action='store_true',
                                   default=False, help='Disable transitive reduction')
            # subparser.add_argument('-d', '--detail', action='store_true',
            #                        default=False, help='Shows Job List view in terminal')
            subparser.add_argument('-v', '--update_version', action='store_true',
                                   default=False, help='Update experiment version')
            # Stats
            subparser = subparsers.add_parser(
                'stats', description="plots statistics for specified experiment")
            subparser.add_argument('expid', help='experiment identifier')
            subparser.add_argument('-ft', '--filter_type', type=str, help='Select the job type to filter '
                                                                          'the list of jobs')
            subparser.add_argument('-fp', '--filter_period', type=int, help='Select the period to filter jobs '
                                                                            'from current time to the past '
                                                                            'in number of hours back')
            subparser.add_argument('-o', '--output', choices=('pdf', 'png', 'ps', 'svg'), default='pdf',
                                   help='type of output for generated plot')
            subparser.add_argument('--hide', action='store_true', default=False,
                                   help='hides plot window')
            subparser.add_argument('-nt', '--notransitive', action='store_true',
                                   default=False, help='Disable transitive reduction')
            subparser.add_argument('-v', '--update_version', action='store_true',
                                   default=False, help='Update experiment version')
            # Clean
            subparser = subparsers.add_parser(
                'clean', description="clean specified experiment")
            subparser.add_argument('expid', help='experiment identifier')
            subparser.add_argument(
                '-pr', '--project', action="store_true", help='clean project')
            subparser.add_argument('-p', '--plot', action="store_true",
                                   help='clean plot, only 2 last will remain')
            subparser.add_argument('-s', '--stats', action="store_true",
                                   help='clean stats, only last will remain')
            subparser.add_argument('-v', '--update_version', action='store_true',
                                   default=False, help='Update experiment version')
            # Recovery
            subparser = subparsers.add_parser(
                'recovery', description="recover specified experiment")
            subparser.add_argument(
                'expid', type=str, help='experiment identifier')
            subparser.add_argument(
                '-np', '--noplot', action='store_true', default=False, help='omit plot')
            subparser.add_argument('--all', action="store_true", default=False,
                                   help='Get completed files to synchronize pkl')
            subparser.add_argument(
                '-s', '--save', action="store_true", default=False, help='Save changes to disk')
            subparser.add_argument('--hide', action='store_true', default=False,
                                   help='hides plot window')
            subparser.add_argument('-group_by', choices=('date', 'member', 'chunk', 'split', 'automatic'), default=None,
                                   help='Groups the jobs automatically or by date, member, chunk or split')
            subparser.add_argument('-expand', type=str,
                                   help='Supply the list of dates/members/chunks to filter the list of jobs. Default = "Any". '
                                        'LIST = "[ 19601101 [ fc0 [1 2 3 4] fc1 [1] ] 19651101 [ fc0 [16-30] ] ]"')
            subparser.add_argument(
                '-expand_status', type=str, help='Select the statuses to be expanded')
            subparser.add_argument('-nt', '--notransitive', action='store_true',
                                   default=False, help='Disable transitive reduction')
            subparser.add_argument('-nl', '--no_recover_logs', action='store_true', default=False,
                                   help='Disable logs recovery')
            subparser.add_argument('-d', '--detail', action='store_true',
                                   default=False, help='Show Job List view in terminal')
            subparser.add_argument('-f', '--force', action='store_true',
                                   default=False, help='Cancel active jobs ')
            subparser.add_argument('-v', '--update_version', action='store_true',
                                   default=False, help='Update experiment version')
            # Migrate
            subparser = subparsers.add_parser(
                'migrate', description="Migrate experiments from current user to another")
            subparser.add_argument('expid', help='experiment identifier')
            group = subparser.add_mutually_exclusive_group(required=True)
            group.add_argument('-o', '--offer', action="store_true",
                               default=False, help='Offer experiment')
            group.add_argument('-p', '--pickup', action="store_true",
                               default=False, help='Pick-up released experiment')
            subparser.add_argument('-r', '--onlyremote', action="store_true",
                                   default=False, help='Only moves remote files')
            subparser.add_argument('-v', '--update_version', action='store_true',
                                   default=False, help='Update experiment version')
            # Inspect
            subparser = subparsers.add_parser(
                'inspect', description="Generate all .cmd files")
            subparser.add_argument('expid', help='experiment identifier')
            subparser.add_argument('-nt', '--notransitive', action='store_true',
                                   default=False, help='Disable transitive reduction')
            subparser.add_argument(
                '-f', '--force', action="store_true", help='Overwrite all cmd')
            subparser.add_argument('-cw', '--check_wrapper', action='store_true',
                                   default=False, help='Generate possible wrapper in the current workflow')
            subparser.add_argument('-v', '--update_version', action='store_true',
                                   default=False, help='Update experiment version')
            group.add_argument('-fs', '--filter_status', type=str,
                               choices=('Any', 'READY', 'COMPLETED',
                                        'WAITING', 'SUSPENDED', 'FAILED', 'UNKNOWN'),
                               help='Select the original status to filter the list of jobs')
            group = subparser.add_mutually_exclusive_group(required=False)
            group.add_argument('-fl', '--list', type=str,
                               help='Supply the list of job names to be filtered. Default = "Any". '
                                    'LIST = "b037_20101101_fc3_21_sim b037_20111101_fc4_26_sim"')
            group.add_argument('-fc', '--filter_chunks', type=str,
                               help='Supply the list of chunks to filter the list of jobs. Default = "Any". '
                                    'LIST = "[ 19601101 [ fc0 [1 2 3 4] fc1 [1] ] 19651101 [ fc0 [16-30] ] ]"')
            group.add_argument('-fs', '--filter_status', type=str,
                               choices=('Any', 'READY', 'COMPLETED',
                                        'WAITING', 'SUSPENDED', 'FAILED', 'UNKNOWN'),
                               help='Select the original status to filter the list of jobs')
            group.add_argument('-ft', '--filter_type', type=str,
                               help='Select the job type to filter the list of jobs')

            # Check
            subparser = subparsers.add_parser(
                'check', description="check configuration for specified experiment")
            subparser.add_argument('expid', help='experiment identifier')
            subparser.add_argument('-nt', '--notransitive', action='store_true',
                                   default=False, help='Disable transitive reduction')
            subparser.add_argument('-v', '--update_version', action='store_true',
                                   default=False, help='Update experiment version')
            # Describe
            subparser = subparsers.add_parser(
                'describe', description="Show details for specified experiment")
            subparser.add_argument('expid', help='experiment identifier, can be a list of expid separated by comma or spaces', default="*", nargs="?")
            subparser.add_argument('-u','--user', help='username, default is current user or listed expid', default=""),
            subparser.add_argument('-v', '--update_version', action='store_true',
                                   default=False, help='Update experiment version')

            # Report
            subparser = subparsers.add_parser(
                'report', description="Show metrics.. ")  # TODO
            subparser.add_argument('expid', help='experiment identifier')
            subparser.add_argument(
                '-t', '--template', type=str, help='Supply the metric template.')
            subparser.add_argument('-all', '--show_all_parameters', action='store_true',
                                   default=False, help='Writes a file containing all parameters')
            subparser.add_argument(
                '-fp', '--folder_path', type=str, help='Allows to select a non-default folder.')
            subparser.add_argument(
                '-p', '--placeholders', default=False, action='store_true',
                help='disables the substitution of placeholders by -')
            subparser.add_argument('-v', '--update_version', action='store_true',
                                   default=False, help='Update experiment version')
            # Create
            subparser = subparsers.add_parser(
                'create', description="create specified experiment joblist")
            subparser.add_argument('expid', help='experiment identifier')
            subparser.add_argument(
                '-np', '--noplot', action='store_true', default=False, help='omit plot')
            subparser.add_argument('--hide', action='store_true', default=False,
                                   help='hides plot window')
            subparser.add_argument('-d', '--detail', action='store_true',
                                   default=False, help='Show Job List view in terminal')
            subparser.add_argument('-o', '--output', choices=('pdf', 'png', 'ps', 'svg'),
                                   help='chooses type of output for generated plot')  # Default -o value comes from .conf
            subparser.add_argument('-group_by', choices=('date', 'member', 'chunk', 'split', 'automatic'), default=None,
                                   help='Groups the jobs automatically or by date, member, chunk or split')
            subparser.add_argument('-expand', type=str,
                                   help='Supply the list of dates/members/chunks to filter the list of jobs. Default = "Any". '
                                        'LIST = "[ 19601101 [ fc0 [1 2 3 4] fc1 [1] ] 19651101 [ fc0 [16-30] ] ]"')
            subparser.add_argument(
                '-expand_status', type=str, help='Select the statuses to be expanded')
            subparser.add_argument('-nt', '--notransitive', action='store_true',
                                   default=False, help='Disable transitive reduction')
            subparser.add_argument('-cw', '--check_wrapper', action='store_true',
                                   default=False, help='Generate possible wrapper in the current workflow')
            subparser.add_argument('-v', '--update_version', action='store_true',
                                   default=False, help='Update experiment version')
            # Configure
            subparser = subparsers.add_parser('configure', description="configure database and path for autosubmit. It "
                                                                       "can be done at machine, user or local level."
                                                                       "If no arguments specified configure will "
                                                                       "display dialog boxes (if installed)")
            subparser.add_argument(
                '--advanced', action="store_true", help="Open advanced configuration of autosubmit")
            subparser.add_argument('-db', '--databasepath', default=None, help='path to database. If not supplied, '
                                                                               'it will prompt for it')
            subparser.add_argument(
                '-dbf', '--databasefilename', default=None, help='database filename')
            subparser.add_argument('-lr', '--localrootpath', default=None, help='path to store experiments. If not '
                                                                                'supplied, it will prompt for it')
            subparser.add_argument('-pc', '--platformsconfpath', default=None, help='path to platforms.yml file to '
                                                                                    'use by default. Optional')
            subparser.add_argument('-jc', '--jobsconfpath', default=None, help='path to jobs.yml file to use by '
                                                                               'default. Optional')
            subparser.add_argument(
                '-sm', '--smtphostname', default=None, help='SMTP server hostname. Optional')
            subparser.add_argument(
                '-mf', '--mailfrom', default=None, help='Notifications sender address. Optional')
            group = subparser.add_mutually_exclusive_group()
            group.add_argument('--all', action="store_true",
                               help='configure for all users')
            group.add_argument('--local', action="store_true", help='configure only for using Autosubmit from this '
                                                                    'path')

            # Install
            subparsers.add_parser(
                'install', description='install database for autosubmit on the configured folder')

            # Set status
            subparser = subparsers.add_parser(
                'setstatus', description="sets job status for an experiment")
            subparser.add_argument('expid', help='experiment identifier')
            subparser.add_argument(
                '-np', '--noplot', action='store_true', default=False, help='omit plot')
            subparser.add_argument(
                '-s', '--save', action="store_true", default=False, help='Save changes to disk')
            subparser.add_argument('-t', '--status_final',
                                   choices=('READY', 'COMPLETED', 'WAITING', 'SUSPENDED', 'FAILED', 'UNKNOWN',
                                            'QUEUING', 'RUNNING', 'HELD'),
                                   required=True,
                                   help='Supply the target status')
            subparser.add_argument('-v', '--update_version', action='store_true',
                                   default=False, help='Update experiment version')
            group = subparser.add_mutually_exclusive_group(required=True)
            group.add_argument('-fl', '--list', type=str,
                               help='Supply the list of job names to be changed. Default = "Any". '
                                    'LIST = "b037_20101101_fc3_21_sim b037_20111101_fc4_26_sim"')
            group.add_argument('-fc', '--filter_chunks', type=str,
                               help='Supply the list of chunks to change the status. Default = "Any". '
                                    'LIST = "[ 19601101 [ fc0 [1 2 3 4] fc1 [1] ] 19651101 [ fc0 [16-30] ] ]"')
            group.add_argument('-fs', '--filter_status', type=str,
                               help='Select the status (one or more) to filter the list of jobs.'
                                    "Valid values = ['Any', 'READY', 'COMPLETED', 'WAITING', 'SUSPENDED', 'FAILED', 'UNKNOWN']")
            group.add_argument('-ft', '--filter_type', type=str,
                               help='Select the job type to filter the list of jobs')
            group.add_argument('-ftc', '--filter_type_chunk', type=str,
                               help='Supply the list of chunks to change the status. Default = "Any". When the member name "all" is set, all the chunks \
                               selected from for that member will be updated for all the members. Example: all [1], will have as a result that the \
                                   chunks 1 for all the members will be updated. Follow the format: '
                                    '"[ 19601101 [ fc0 [1 2 3 4] Any [1] ] 19651101 [ fc0 [16-30] ] ],SIM,SIM2,SIM3"')

            subparser.add_argument('--hide', action='store_true', default=False,
                                   help='hides plot window')
            subparser.add_argument('-group_by', choices=('date', 'member', 'chunk', 'split', 'automatic'), default=None,
                                   help='Groups the jobs automatically or by date, member, chunk or split')
            subparser.add_argument('-expand', type=str,
                                   help='Supply the list of dates/members/chunks to filter the list of jobs. Default = "Any". '
                                        'LIST = "[ 19601101 [ fc0 [1 2 3 4] fc1 [1] ] 19651101 [ fc0 [16-30] ] ]"')
            subparser.add_argument(
                '-expand_status', type=str, help='Select the statuses to be expanded')
            subparser.add_argument('-nt', '--notransitive', action='store_true',
                                   default=False, help='Disable transitive reduction')
            subparser.add_argument('-cw', '--check_wrapper', action='store_true',
                                   default=False, help='Generate possible wrapper in the current workflow')
            subparser.add_argument('-d', '--detail', action='store_true',
                                   default=False, help='Generate detailed view of changes')

            # Test Case
            subparser = subparsers.add_parser(
                'testcase', description='create test case experiment')
            subparser.add_argument(
                '-y', '--copy', help='makes a copy of the specified experiment')
            subparser.add_argument(
                '-d', '--description', required=True, help='description of the test case')
            subparser.add_argument('-c', '--chunks', help='chunks to run')
            subparser.add_argument('-m', '--member', help='member to run')
            subparser.add_argument('-s', '--stardate', help='stardate to run')
            subparser.add_argument(
                '-H', '--HPC', required=True, help='HPC to run experiment on it')
            subparser.add_argument(
                '-b', '--branch', help='branch of git to run (or revision from subversion)')

            # Database Fix
            subparser = subparsers.add_parser(
                'dbfix', description='tries to fix a corrupted jobs database')
            subparser.add_argument('expid', help='experiment identifier')

            # Pkl Fix
            subparser = subparsers.add_parser(
                'pklfix', description='restore the backup of your pkl')
            subparser.add_argument('expid', help='experiment identifier')

            # Update Description
            subparser = subparsers.add_parser(
                'updatedescrip', description="Updates the experiment's description.")
            subparser.add_argument('expid', help='experiment identifier')
            subparser.add_argument('description', help='New description.')
            subparser.add_argument('-v', '--update_version', action='store_true',
                                   default=False, help='Update experiment version')
            # Test
            subparser = subparsers.add_parser(
                'test', description='test experiment')
            subparser.add_argument('expid', help='experiment identifier')
            subparser.add_argument(
                '-c', '--chunks', required=True, help='chunks to run')
            subparser.add_argument('-m', '--member', help='member to run')
            subparser.add_argument('-s', '--stardate', help='stardate to run')
            subparser.add_argument(
                '-H', '--HPC', help='HPC to run experiment on it')
            subparser.add_argument(
                '-b', '--branch', help='branch of git to run (or revision from subversion)')
            subparser.add_argument('-v', '--update_version', action='store_true',
                                   default=False, help='Update experiment version')
            # Refresh
            subparser = subparsers.add_parser(
                'refresh', description='refresh project directory for an experiment')
            subparser.add_argument('expid', help='experiment identifier')
            subparser.add_argument('-mc', '--model_conf', default=False, action='store_true',
                                   help='overwrite model conf file')
            subparser.add_argument('-jc', '--jobs_conf', default=False, action='store_true',
                                   help='overwrite jobs conf file')
            subparser.add_argument('-v', '--update_version', action='store_true',
                                   default=False, help='Update experiment version')
            # Update Version
            subparser = subparsers.add_parser(
                'updateversion', description='refresh experiment version')
            subparser.add_argument('expid', help='experiment identifier')
            subparser.add_argument('-v', '--update_version', action='store_true',
                                   default=False, help='Update experiment version')
            # Archive
            subparser = subparsers.add_parser(
                'archive', description='archives an experiment')
            subparser.add_argument('expid', help='experiment identifier')
            subparser.add_argument('-nclean', '--noclean', default=False, action='store_true',
                                   help='Avoid Cleaning of experiment folder')
            subparser.add_argument('-uc', '--uncompress', default=False, action='store_true',
                                   help='Only does a container without compress')
            subparser.add_argument('-v', '--update_version', action='store_true',
                                   default=False, help='Update experiment version')
            # Unarchive
            subparser = subparsers.add_parser(
                'unarchive', description='unarchives an experiment')
            subparser.add_argument('expid', help='experiment identifier')
            subparser.add_argument('-nclean', '--noclean', default=False, action='store_true',
                                   help='Avoid Cleaning of experiment folder')
            subparser.add_argument('-uc', '--uncompressed', default=False, action='store_true',
                                   help='Untar an uncompressed tar')
            subparser.add_argument('-v', '--update_version', action='store_true',
                                   default=False, help='Update experiment version')
            # update proj files
            subparser = subparsers.add_parser('upgrade', description='Updates autosubmit 3 proj files to autosubmit 4')
            subparser.add_argument('expid', help='experiment identifier')
            subparser.add_argument('-f','--files',default='',type=str, help='list of files')
            # Readme
            subparsers.add_parser('readme', description='show readme')

            # Changelog
            subparsers.add_parser('changelog', description='show changelog')
            args = parser.parse_args()

            if args.command is None:
                parser.print_help()
                parser.exit()

        except Exception as e:
            if type(e) is SystemExit:  # todo check
                # Version keyword force an exception in parse arg due and os_exit(0) but the program is successfully finished
                if "0" in str(e):
                    print(Autosubmit.autosubmit_version)
                    return 0
            raise AutosubmitCritical(
                "Incorrect arguments for this command", 7011)

        expid = "None"
        if hasattr(args, 'expid'):
            expid = args.expid
        if args.command != "configure" and args.command != "install":
            Autosubmit._init_logs(args, args.logconsole, args.logfile, expid)

        if args.command == 'run':
            return Autosubmit.run_experiment(args.expid, args.notransitive, args.update_version, args.start_time,
                                             args.start_after, args.run_only_members)
        elif args.command == 'expid':
            return Autosubmit.expid(args.description,args.HPC,args.copy, args.dummy,args.minimal_configuration,args.git_repo,args.git_branch,args.git_as_conf,args.operational) != ''
        elif args.command == 'delete':
            return Autosubmit.delete(args.expid, args.force)
        elif args.command == 'monitor':
            return Autosubmit.monitor(args.expid, args.output, args.list, args.filter_chunks, args.filter_status,
                                      args.filter_type, args.hide, args.text, args.group_by, args.expand,
                                      args.expand_status, args.hide_groups, args.notransitive, args.check_wrapper,
                                      args.txt_logfiles, detail=False)
        elif args.command == 'stats':
            return Autosubmit.statistics(args.expid, args.filter_type, args.filter_period, args.output, args.hide,
                                         args.notransitive)
        elif args.command == 'clean':
            return Autosubmit.clean(args.expid, args.project, args.plot, args.stats)
        elif args.command == 'recovery':
            return Autosubmit.recovery(args.expid, args.noplot, args.save, args.all, args.hide, args.group_by,
                                       args.expand, args.expand_status, args.notransitive, args.no_recover_logs,
                                       args.detail, args.force)
        elif args.command == 'check':
            return Autosubmit.check(args.expid, args.notransitive)
        elif args.command == 'inspect':
            return Autosubmit.inspect(args.expid, args.list, args.filter_chunks, args.filter_status,
                                      args.filter_type, args.notransitive, args.force, args.check_wrapper)
        elif args.command == 'report':
            return Autosubmit.report(args.expid, args.template, args.show_all_parameters, args.folder_path,
                                     args.placeholders)
        elif args.command == 'describe':
            return Autosubmit.describe(args.expid,args.user)
        elif args.command == 'migrate':
            return Autosubmit.migrate(args.expid, args.offer, args.pickup, args.onlyremote)
        elif args.command == 'create':
            return Autosubmit.create(args.expid, args.noplot, args.hide, args.output, args.group_by, args.expand,
                                     args.expand_status, args.notransitive, args.check_wrapper, args.detail)
        elif args.command == 'configure':
            if not args.advanced or (args.advanced and dialog is None):
                return Autosubmit.configure(args.advanced, args.databasepath, args.databasefilename,
                                            args.localrootpath, args.platformsconfpath, args.jobsconfpath,
                                            args.smtphostname, args.mailfrom, args.all, args.local)
            else:
                return Autosubmit.configure_dialog()
        elif args.command == 'install':
            return Autosubmit.install()
        elif args.command == 'setstatus':
            return Autosubmit.set_status(args.expid, args.noplot, args.save, args.status_final, args.list,
                                         args.filter_chunks, args.filter_status, args.filter_type,
                                         args.filter_type_chunk, args.hide,
                                         args.group_by, args.expand, args.expand_status, args.notransitive,
                                         args.check_wrapper, args.detail)
        elif args.command == 'testcase':
            return Autosubmit.testcase(args.copy, args.description, args.chunks, args.member, args.stardate,
                                       args.HPC, args.branch)
        elif args.command == 'test':
            return Autosubmit.test(args.expid, args.chunks, args.member, args.stardate, args.HPC, args.branch)
        elif args.command == 'refresh':
            return Autosubmit.refresh(args.expid, args.model_conf, args.jobs_conf)
        elif args.command == 'updateversion':
            return Autosubmit.update_version(args.expid)
        elif args.command == 'upgrade':
            return Autosubmit.upgrade_scripts(args.expid,files=args.files)
        elif args.command == 'archive':
            return Autosubmit.archive(args.expid, noclean=args.noclean, uncompress=args.uncompress)
        elif args.command == 'unarchive':
            return Autosubmit.unarchive(args.expid, uncompressed=args.uncompressed)

        elif args.command == 'readme':
            if os.path.isfile(Autosubmit.readme_path):
                with open(Autosubmit.readme_path) as f:
                    print(f.read())
                    return True
            return False
        elif args.command == 'changelog':
            if os.path.isfile(Autosubmit.changes_path):
                with open(Autosubmit.changes_path) as f:
                    print(f.read())
                    return True
            return False
        elif args.command == 'dbfix':
            return Autosubmit.database_fix(args.expid)
        elif args.command == 'pklfix':
            return Autosubmit.pkl_fix(args.expid)
        elif args.command == 'updatedescrip':
            return Autosubmit.update_description(args.expid, args.description)

    @staticmethod
    def _init_logs(args, console_level='INFO', log_level='DEBUG', expid='None'):
        Log.set_console_level(console_level)
        if args.command != "configure":
            if not BasicConfig.CONFIG_FILE_FOUND:
                raise AutosubmitCritical('No configuration file(autosubmitrc) found in this filesystem. Please run "autosubmit configure" first.',7006)
            if args.command != "install":
                if not os.path.exists(BasicConfig.DB_PATH):
                    raise AutosubmitCritical('Experiments database not found in this filesystem. Please run "autosubmit installation" first.',7072)
                else:
                    permissions = os.access(BasicConfig.DB_PATH, os.R_OK)  # Check for read access
                    if not permissions:
                        raise AutosubmitCritical('Experiments database {0} not readable. Please check permissions.'.format(BasicConfig.DB_PATH),7007)
                    permissions = os.access(BasicConfig.DB_PATH, os.W_OK)  # Check for write access
                    if not permissions:
                        raise AutosubmitCritical('Experiments database {0} not writable. Please check permissions.'.format(BasicConfig.DB_PATH),7007)



        expid_less = ["expid", "describe", "testcase", "install", "-v",
                      "readme", "changelog", "configure", "unarchive"]
        global_log_command = ["delete", "archive", "upgrade"]
        if "offer" in args:
            if args.offer:
                global_log_command.append("migrate")  # offer
            else:
                expid_less.append("migrate")  # pickup
        import platform
        fullhost = platform.node()
        if "." in fullhost:
            host = fullhost.split(".")[0]
        elif "," in fullhost:
            host = fullhost.split(",")[0]
        else:
            host = fullhost
        forbidden = BasicConfig.DENIED_HOSTS
        authorized = BasicConfig.ALLOWED_HOSTS
        message = "Command: {0} is not allowed to run in host: {1}.\n".format(args.command.upper(), host)
        message += "List of permissions as follows:Command | hosts \nAllowed hosts\n"
        for command in authorized:
            message += "   {0}:{1} \n".format(command, authorized[command])
        message += "Denied hosts\n"
        for command in forbidden:
            message += "   {0}:{1} \n".format(command, forbidden[command])
        message += "[Command: autosubmit {0}] is not allowed to run in [host: {1}].".format(args.command.upper(), host)
        if args.command in BasicConfig.DENIED_HOSTS:
            if 'all' in BasicConfig.DENIED_HOSTS[args.command] or host in BasicConfig.DENIED_HOSTS[args.command] or fullhost in BasicConfig.DENIED_HOSTS[args.command]:
                raise AutosubmitCritical(message, 7071)
        if args.command in BasicConfig.ALLOWED_HOSTS:
            if 'all' not in BasicConfig.ALLOWED_HOSTS[args.command] and not (host in BasicConfig.ALLOWED_HOSTS[args.command] or fullhost in BasicConfig.ALLOWED_HOSTS[args.command]):
                raise AutosubmitCritical(message, 7071)
        if expid != 'None' and args.command not in expid_less and args.command not in global_log_command:
            as_conf = AutosubmitConfig(expid, BasicConfig, YAMLParserFactory())
            as_conf.reload(force_load=True)
            if len(as_conf.experiment_data) == 0:
                if args.command not in ["expid", "upgrade"]:
                    raise AutosubmitCritical(
                        "Experiment {0} has no yml data. Please, if you really wish to use AS 4 prompt:\nautosubmit upgrade {0}".format(
                            expid), 7012)
            exp_path = os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid)
            tmp_path = os.path.join(exp_path, BasicConfig.LOCAL_TMP_DIR)
            aslogs_path = os.path.join(tmp_path, BasicConfig.LOCAL_ASLOG_DIR)
            if not os.path.exists(exp_path):
                raise AutosubmitCritical("Experiment does not exist", 7012)
            # delete is treated differently
            if args.command not in ["monitor", "describe", "delete", "report", "stats", "dbfix"]:
                owner, eadmin, currentOwner = Autosubmit._check_ownership(expid, raise_error=True)
            else:
                owner, eadmin, currentOwner = Autosubmit._check_ownership(expid, raise_error=False)

            if not os.path.exists(tmp_path):
                os.mkdir(tmp_path)
            if not os.path.exists(aslogs_path):
                os.mkdir(aslogs_path)
            if owner:
                os.chmod(tmp_path, 0o775)
                Log.set_file(os.path.join(aslogs_path, args.command + '.log'), "out", log_level)
                Log.set_file(os.path.join(aslogs_path, args.command + '_err.log'), "err")
                if args.command in ["run"]:
                    if os.path.exists(os.path.join(aslogs_path, 'jobs_active_status.log')):
                        os.remove(os.path.join(aslogs_path, 'jobs_active_status.log'))
                    if os.path.exists(os.path.join(aslogs_path, 'jobs_failed_status.log')):
                        os.remove(os.path.join(aslogs_path, 'jobs_failed_status.log'))
                        Log.set_file(os.path.join(aslogs_path, 'jobs_active_status.log'), "status")
                        Log.set_file(os.path.join(aslogs_path, 'jobs_failed_status.log'), "status_failed")
            else:
                st = os.stat(tmp_path)
                oct_perm = str(oct(st.st_mode))[-3:]
                if int(oct_perm[1]) in [6, 7] or int(oct_perm[2]) in [6, 7]:
                    Log.set_file(os.path.join(tmp_path, args.command + '.log'), "out", log_level)
                    Log.set_file(os.path.join(tmp_path, args.command + '_err.log'), "err")
                else:
                    Log.set_file(os.path.join(BasicConfig.GLOBAL_LOG_DIR,
                                              args.command + expid + '.log'), "out", log_level)
                    Log.set_file(os.path.join(BasicConfig.GLOBAL_LOG_DIR,
                                              args.command + expid + '_err.log'), "err")
                    Log.printlog(
                        "Permissions of {0} are {1}. The log is being written in the {2} path instead of {1}. Please tell to the owner to fix the permissions".format(
                            tmp_path, oct_perm, BasicConfig.GLOBAL_LOG_DIR))
            Log.file_path = tmp_path
            if owner:
                if "update_version" in args:
                    force_update_version = args.update_version
                else:
                    force_update_version = False
                if args.command not in ["upgrade", "updateversion"]:
                    if force_update_version:
                        if as_conf.get_version() != Autosubmit.autosubmit_version:
                            Log.info(
                                "The {2} experiment {0} version is being updated to {1} for match autosubmit version",
                                as_conf.get_version(), Autosubmit.autosubmit_version, expid)
                            as_conf.set_version(Autosubmit.autosubmit_version)
                            update_experiment_descrip_version(expid, version=Autosubmit.autosubmit_version)

                    else:
                        if as_conf.get_version() is not None and as_conf.get_version() != Autosubmit.autosubmit_version:
                            raise AutosubmitCritical(
                                "Current experiment uses ({0}) which is not the running Autosubmit version  \nPlease, update the experiment version if you wish to continue using AutoSubmit {1}\nYou can achieve this using the command autosubmit updateversion {2} \n"
                                "Or with the -v parameter: autosubmit {3} {2} -v ".format(as_conf.get_version(),
                                                                                          Autosubmit.autosubmit_version, expid,args.command),
                                7014)
        else:
            if expid == 'None':
                exp_id = ""
            else:
                exp_id = "_" + expid
            if args.command not in expid_less:
                exp_path = os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid)
                if not os.path.exists(exp_path):
                    raise AutosubmitCritical("Experiment does not exist", 7012)
            Log.set_file(os.path.join(BasicConfig.GLOBAL_LOG_DIR,
                                      args.command + exp_id + '.log'), "out", log_level)
            Log.set_file(os.path.join(BasicConfig.GLOBAL_LOG_DIR,
                                      args.command + exp_id + '_err.log'), "err")
        # Enforce LANG=UTF-8
        try:
            try:
                locale.setlocale(locale.LC_ALL, 'C.UTF-8')
            except Exception as e:
                try:
                    locale.setlocale(locale.LC_ALL, 'C.utf8')
                except Exception as e:
                    try:
                        locale.setlocale(locale.LC_ALL, 'en_GB')
                    except Exception as e:
                        locale.setlocale(locale.LC_ALL, 'es_ES')
        except Exception as e:
            Log.info("Locale C.utf8 is not found, using '{0}' as fallback".format("C"))
            locale.setlocale(locale.LC_ALL, 'C')

        Log.info(
            "Autosubmit is running with {0}", Autosubmit.autosubmit_version)

    @staticmethod
    def _check_ownership(expid, raise_error=False):
        """
        Check if user owns or if it is edamin
        :return: owner,eadmin
        :rtype: boolean,boolean
        """
        # return HelperUtils.check_experiment_ownership(expid, BasicConfig, raise_error, Log)
        # Read current login
        # Read current user uid
        my_user = os.getuid()
        # Read eadmin user uid
        owner = False
        eadmin = False
        # execute a id -u eadmin and supress error message
        FNULL = open(os.devnull, 'w')
        id_eadmin = subprocess.call(['id', '-u', 'eadmin'],
                                    stdout=FNULL,
                                    stderr=subprocess.STDOUT)

        # id_eadmin = subprocess.Popen('id -u eadmin',stdout=fp)
        ret = False
        # Handling possible failure of retrieval of current owner data
        currentOwner_id = 0
        currentOwner = "empty"
        try:
            currentOwner_id = os.stat(os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid)).st_uid
            currentOwner = pwd.getpwuid(os.stat(os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid)).st_uid).pw_name
        except Exception as e:
            pass
        finally:
            if currentOwner_id <= 0:
                Log.info("Current owner '{0}' of experiment {1} does not exist anymore.", currentOwner, expid)
        if currentOwner_id == my_user:
            owner = True
        if my_user == id_eadmin:
            eadmin = True
        if owner and raise_error:
            try:
                current_user_id = pwd.getpwuid(os.getuid())[0]
                current_owner_id = pwd.getpwuid(os.stat(os.path.join(
                    BasicConfig.LOCAL_ROOT_DIR, expid)).st_uid).pw_name
                if current_user_id != current_owner_id:
                    raise AutosubmitCritical(
                        "You don't own the experiment {0}.".format(expid), 7012)
            except BaseException as e:
                raise AutosubmitCritical(
                    "User or owner does not exists", 7012, str(e))
            except AutosubmitCritical as e:
                raise
        return owner, eadmin, currentOwner

    @staticmethod
    def _delete_expid(expid_delete, force=False):
        """
        Removes an experiment from path and database
        If current user is eadmin and -f has been sent, it deletes regardless
        of experiment owner

        :type expid_delete: str
        :param expid_delete: identifier of the experiment to delete
        :type force: boolean
        :param force: True if the force flag has been sent
        :return: True if successfully deleted, False otherwise
        :rtype: boolean
        """
        message = "The {0} experiment was removed from the local disk and from the database.".format(expid_delete)
        message += " Note that this action does not delete any data written by the experiment.\n"
        message += "Complete list of files/directories deleted:\n"
        for root, dirs, files in os.walk(os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid_delete)):
            for dir_ in dirs:
                message += os.path.join(root, dir_) + "\n"
        message += os.path.join(BasicConfig.LOCAL_ROOT_DIR, BasicConfig.STRUCTURES_DIR,
                                "structure_{0}.db".format(expid_delete)) + "\n"
        message += os.path.join(BasicConfig.LOCAL_ROOT_DIR, BasicConfig.JOBDATA_DIR,
                                "job_data_{0}.db".format(expid_delete)) + "\n"
        owner, eadmin, currentOwner = Autosubmit._check_ownership(expid_delete)
        if expid_delete == '' or expid_delete is None and not os.path.exists(
                os.path.join(str(BasicConfig.LOCAL_ROOT_DIR), str(expid_delete))):
            Log.printlog("Experiment directory does not exist.", Log.WARNING)
        else:
            # Deletion workflow continues as usual, a disjunction is included for the case when
            # force is sent, and user is eadmin
            error_message = ""
            try:
                if owner or (force and eadmin):
                    if force and eadmin:
                        Log.info("Preparing deletion of experiment {0} from owner: {1}, as eadmin.", expid_delete,
                                 currentOwner)
                    try:
                        Log.info("Deleting experiment from database...")
                        try:
                            ret = delete_experiment(expid_delete)
                            if ret:
                                Log.result("Experiment {0} deleted".format(expid_delete))
                        except BaseException as e:
                            error_message += 'Can not delete experiment entry: {0}\n'.format(str(e))
                        Log.info("Removing experiment directory...")
                        try:
                            shutil.rmtree(os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid_delete))
                        except BaseException as e:
                            error_message += 'Can not delete directory: {0}\n'.format(str(e))
                        try:
                            Log.info("Removing Structure db...")
                            structures_path = os.path.join(BasicConfig.LOCAL_ROOT_DIR, BasicConfig.STRUCTURES_DIR,
                                                           "structure_{0}.db".format(expid_delete))
                            if os.path.exists(structures_path):
                                os.remove(structures_path)
                        except BaseException as e:
                            error_message += 'Can not delete structure: {0}\n'.format(str(e))
                        try:
                            Log.info("Removing job_data db...")
                            job_data_path = os.path.join(BasicConfig.LOCAL_ROOT_DIR, BasicConfig.JOBDATA_DIR,
                                                         "job_data_{0}.db".format(expid_delete))
                            if os.path.exists(job_data_path):
                                os.remove(job_data_path)
                        except BaseException as e:
                            error_message += 'Can not delete job_data: {0}\n'.format(str(e))
                    except OSError as e:
                        error_message += 'Can not delete directory: {0}\n'.format(str(e))
                else:
                    if not eadmin:
                        raise AutosubmitCritical(
                            'Detected Eadmin user however, -f flag is not found.  {0} can not be deleted!'.format(
                                expid_delete), 7012)
                    else:
                        raise AutosubmitCritical(
                            'Current user is not the owner of the experiment. {0} can not be deleted!'.format(
                                expid_delete), 7012)
                if error_message == "":
                    Log.printlog(message, Log.RESULT)
                else:
                    Log.printlog(error_message, Log.ERROR)
            except Exception as e:
                # Avoid calling Log at this point since it is possible that tmp folder is already deleted.
                error_message += "Couldn't delete the experiment".format(str(e))
            if error_message != "":
                raise AutosubmitError(
                    "Some experiment files weren't correctly deleted\nPlease if the trace shows DATABASE IS LOCKED, report it to git\nIf there are I/O issues, wait until they're solved and then use this command again.\n",
                    error_message, 6004)

    @staticmethod
    def copy_as_config(exp_id,copy_id):
        for conf_file in os.listdir(os.path.join(BasicConfig.LOCAL_ROOT_DIR, copy_id,"conf")):
            # Copy only relevant files
            if conf_file.endswith((".conf, .yml, .yaml")):
                shutil.copy(os.path.join(BasicConfig.LOCAL_ROOT_DIR, copy_id, "conf", conf_file),
                            os.path.join(BasicConfig.LOCAL_ROOT_DIR, exp_id, "conf", conf_file.replace(copy_id,exp_id)))
            # if ends with .conf convert it to AS4 yaml file
            if conf_file.endswith(".conf"):
                try:
                    AutosubmitConfig.ini_to_yaml(os.path.join(BasicConfig.LOCAL_ROOT_DIR, exp_id,"conf"),
                                                 os.path.join(BasicConfig.LOCAL_ROOT_DIR, exp_id,"conf",conf_file.replace(copy_id,exp_id)))
                except Exception as e:
                    Log.warning("Error converting {0} to yml: {1}".format(conf_file.replace(copy_id,exp_id),str(e)))
    @staticmethod
    def generate_as_config(exp_id,dummy=False,minimal_configuration=False):
        # obtain from autosubmitconfigparser package
        # get all as_conf_files from autosubmitconfigparser package
        files = resource_listdir('autosubmitconfigparser.config', 'files')
        for as_conf_file in files:
            if dummy:
                if as_conf_file.endswith("dummy.yml"):
                    shutil.copy(resource_filename('autosubmitconfigparser.config', 'files/'+as_conf_file), os.path.join(BasicConfig.LOCAL_ROOT_DIR, exp_id, "conf",as_conf_file.split("-")[0]+"_"+exp_id+".yml"))
            elif minimal_configuration:
                if as_conf_file.endswith("minimal.yml"):
                    shutil.copy(resource_filename('autosubmitconfigparser.config', 'files/'+as_conf_file), os.path.join(BasicConfig.LOCAL_ROOT_DIR, exp_id, "conf","minimal.yml"))
            else:
                if not as_conf_file.endswith("dummy.yml") and not as_conf_file.endswith("minimal.yml"):
                    shutil.copy(resource_filename('autosubmitconfigparser.config', 'files/'+as_conf_file), os.path.join(BasicConfig.LOCAL_ROOT_DIR, exp_id, "conf",as_conf_file[:-4]+"_"+exp_id+".yml"))
    @staticmethod
    def as_conf_default_values(exp_id,hpc="local",minimal_configuration=False,git_repo="",git_branch="main",git_as_conf=""):
        """
        Replace default values in as_conf files
        :param exp_id: experiment id
        :param hpc: platform
        :param minimal_configuration: minimal configuration
        :param git_repo: path to project git repository
        :param git_branch: main branch
        :param git_as_conf: path to as_conf file in git repository
        :return: None
        """
        # open and replace values
        for as_conf_file in os.listdir(os.path.join(BasicConfig.LOCAL_ROOT_DIR, exp_id,"conf")):
            if as_conf_file.endswith(".yml") or as_conf_file.endswith(".yaml"):
                with open(os.path.join(BasicConfig.LOCAL_ROOT_DIR, exp_id,"conf", as_conf_file), 'r') as f:
                    # Copied files could not have default names.
                    content = f.read()
                    search = re.search('AUTOSUBMIT_VERSION: .*', content, re.MULTILINE)
                    if search is not None:
                        content = content.replace(search.group(0), "AUTOSUBMIT_VERSION: \""+Autosubmit.autosubmit_version+"\"")
                    search = re.search('NOTIFICATIONS: .*', content, re.MULTILINE)
                    if search is not None:
                        content = content.replace(search.group(0),"NOTIFICATIONS: False")
                    search = re.search('TO: .*', content, re.MULTILINE)
                    if search is not None:
                        content = content.replace(search.group(0), "TO: \"\"")
                    search = re.search('EXPID: .*', content, re.MULTILINE)
                    if search is not None:
                        content = content.replace(search.group(0),"EXPID: \""+exp_id+"\"")
                    search = re.search('HPCARCH: .*', content, re.MULTILINE)
                    if search is not None:
                        content = content.replace(search.group(0),"HPCARCH: \""+hpc+"\"")
                    if minimal_configuration:
                        search = re.search('CUSTOM_CONFIG: .*', content, re.MULTILINE)
                        if search is not None:
                            content = content.replace(search.group(0), "CUSTOM_CONFIG: \"%ROOTDIR%/proj/git_project/"+git_as_conf+"\"")
                        search = re.search('PROJECT_ORIGIN: .*', content, re.MULTILINE)
                        if search is not None:
                            content = content.replace(search.group(0), "PROJECT_ORIGIN: \""+git_repo+"\"")
                        search = re.search('PROJECT_BRANCH: .*', content, re.MULTILINE)
                        if search is not None:
                            content = content.replace(search.group(0), "PROJECT_BRANCH: \""+git_branch+"\"")

                with open(os.path.join(BasicConfig.LOCAL_ROOT_DIR, exp_id,"conf", as_conf_file), 'w') as f:
                    f.write(content)

    @staticmethod
    def expid(description,hpc="", copy_id='', dummy=False,minimal_configuration=False,git_repo="",git_branch="",git_as_conf="",operational=False):
        """
        Creates a new experiment for given HPC
        description: description of the experiment
        hpc: HPC where the experiment will be executed
        copy_id: if specified, experiment id to copy
        dummy: if true, creates a dummy experiment
        minimal_configuration: if true, creates a minimal configuration
        git_repo: git repository to clone
        git_branch: git branch to clone
        git_as_conf: path to as_conf file in git repository
        operational: if true, creates an operational experiment
        """
        exp_id = ""
        root_folder = os.path.join(BasicConfig.LOCAL_ROOT_DIR)
        if description is None:
            raise AutosubmitCritical(
                "Check that the parameters are defined (-d) ", 7011)
        if hpc is None and not minimal_configuration:
            raise AutosubmitCritical(
                "Check that the parameters are defined (-H) ", 7011)
        # Register the experiment in the database
        try:
            # Copy another experiment from the database
            if copy_id != '' and copy_id is not None:
                copy_id_folder = os.path.join(root_folder, copy_id)
                if not os.path.exists(copy_id_folder):
                    raise AutosubmitCritical(
                        "Experiment {0} doesn't exists".format(copy_id), 7011)
                exp_id = copy_experiment(copy_id, description, Autosubmit.autosubmit_version, False, operational)
            else:
                # Create a new experiment from scratch
                exp_id = new_experiment(description, Autosubmit.autosubmit_version, False, operational)

            if exp_id == '':
                raise AutosubmitCritical("No expid", 7011)
        except Exception as e:
            raise AutosubmitCritical("Error while generating a new experiment in the db: {0}".format(str(e)), 7011)

        # Create the experiment structure
        Log.info("Generating folder structure...")

        exp_folder = os.path.join(root_folder, exp_id)
        try:
            os.mkdir(exp_folder)
            os.mkdir(os.path.join(exp_folder, "conf"))
            os.mkdir(os.path.join(exp_folder, "pkl"))
            os.mkdir(os.path.join(exp_folder, "tmp"))
            os.mkdir(os.path.join(exp_folder, "tmp", "ASLOGS"))
            os.mkdir(os.path.join(exp_folder, "tmp", "LOG_"+exp_id.upper()))
            os.mkdir(os.path.join(exp_folder, "plot"))
            os.mkdir(os.path.join(exp_folder, "status"))
            # Setting permissions
            os.chmod(exp_folder, 0o755)
            os.chmod(os.path.join(exp_folder, "conf"), 0o755)
            os.chmod(os.path.join(exp_folder, "pkl"), 0o755)
            os.chmod(os.path.join(exp_folder, "tmp"), 0o755)
            os.chmod(os.path.join(exp_folder, "tmp", "ASLOGS"), 0o755)
            os.chmod(os.path.join(exp_folder, "tmp", "LOG_"+exp_id.upper()), 0o755)
            os.chmod(os.path.join(exp_folder, "plot"), 0o755)
            os.chmod(os.path.join(exp_folder, "status"), 0o755)
        except OSError as e:
            try:
                Autosubmit._delete_expid(exp_id, True)
            except:
                pass
            raise AutosubmitCritical("Error while creating the experiment structure: {0}".format(str(e)), 7011)

        # Create the experiment configuration
        Log.info("Generating config files...")
        try:
            if copy_id != '' and copy_id is not None:
                # Copy the configuration from selected experiment
                Autosubmit.copy_as_config(exp_id, copy_id)
            else:
                # Create a new configuration
                Autosubmit.generate_as_config(exp_id,dummy, minimal_configuration)
        except Exception as e:
            try:
                Autosubmit._delete_expid(exp_id, True)
            except:
                pass
            raise AutosubmitCritical("Error while creating the experiment configuration: {0}".format(str(e)), 7011)
        # Change template values by default values specified from the commandline
        try:
            Autosubmit.as_conf_default_values(exp_id,hpc,minimal_configuration,git_repo,git_branch,git_as_conf)
        except Exception as e:
            try:
                Autosubmit._delete_expid(exp_id, True)
            except:
                pass
            raise AutosubmitCritical("Error while setting the default values: {0}".format(str(e)), 7011)

        Log.result("Experiment {0} created".format(exp_id))
        return exp_id

    @staticmethod
    def delete(expid, force):
        """
        Deletes and experiment from database and experiment's folder

        :type force: bool
        :type expid: str
        :param expid: identifier of the experiment to delete
        :param force: if True, does not ask for confirmation

        :returns: True if successful, False if not
        :rtype: bool
        """

        if os.path.exists(os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid)):
            if force or Autosubmit._user_yes_no_query("Do you want to delete " + expid + " ?"):

                Log.debug('Enter Autosubmit._delete_expid {0}', expid)
                try:
                    return Autosubmit._delete_expid(expid, force)
                except AutosubmitCritical as e:
                    raise
                except BaseException as e:
                    raise AutosubmitCritical("Seems that something went wrong, please check the trace", 7012, str(e))
            else:
                raise AutosubmitCritical("Insufficient permissions", 7012)
        else:
            raise AutosubmitCritical("Experiment does not exist", 7012)

    @staticmethod
    def _load_parameters(as_conf, job_list, platforms):
        """
        Add parameters from configuration files into platform objects, and into the job_list object.

        :param as_conf: Basic configuration handler.\n
        :type as_conf: AutosubmitConfig object\n
        :param job_list: Handles the list as a unique entity.\n
        :type job_list: JobList() object\n
        :param platforms: List of platforms related to the experiment.\n
        :type platforms: List() of Platform Objects. e.g EcPlatform(), SgePlatform().
        :return: Nothing, modifies input.
        """

        Log.debug("Loading parameters...")
        parameters = as_conf.load_parameters()
        Log.debug("Parameters load.")
        for platform_name in platforms:
            platform = platforms[platform_name]
            # Call method from platform.py parent object
            platform.add_parameters(parameters)
        # Platform = from DEFAULT.HPCARCH, e.g. marenostrum4
        if as_conf.get_platform() not in platforms.keys():
            Log.warning("Main platform is not defined in platforms.yml")
        else:
            platform = platforms[as_conf.get_platform()]
            platform.add_parameters(parameters, True)
        # Attach parameters to JobList
        parameters['STARTDATES'] = []
        for date in job_list._date_list:
            parameters['STARTDATES'].append(date2str(date, job_list.get_date_format()))

        job_list.parameters = parameters

    @staticmethod
    def inspect(expid, lst, filter_chunks, filter_status, filter_section, notransitive=False, force=False,
                check_wrapper=False):
        """
         Generates cmd files experiment.

         :param check_wrapper:
         :param force:
         :param notransitive:
         :param filter_section:
         :param filter_status:
         :param filter_chunks:
         :param lst:
         :type expid: str
         :param expid: identifier of experiment to be run
         :return: True if run to the end, False otherwise
         :rtype: bool
         """
        try:
            Autosubmit._check_ownership(expid, raise_error=True)
            exp_path = os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid)
            tmp_path = os.path.join(exp_path, BasicConfig.LOCAL_TMP_DIR)
            if os.path.exists(os.path.join(tmp_path, 'autosubmit.lock')):
                locked = True
            else:
                locked = False
            Log.info("Starting inspect command")
            os.system('clear')
            signal.signal(signal.SIGINT, signal_handler)
            as_conf = AutosubmitConfig(expid, BasicConfig, YAMLParserFactory())
            as_conf.check_conf_files(True)
            project_type = as_conf.get_project_type()
            safetysleeptime = as_conf.get_safetysleeptime()
            Log.debug("The Experiment name is: {0}", expid)
            Log.debug("Sleep: {0}", safetysleeptime)
            packages_persistence = JobPackagePersistence(os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid, "pkl"),
                                                         "job_packages_" + expid)
            os.chmod(os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid,
                                  "pkl", "job_packages_" + expid + ".db"), 0o644)

            packages_persistence.reset_table(True)
            job_list_original = Autosubmit.load_job_list(
                expid, as_conf, notransitive=notransitive)
            job_list = copy.deepcopy(job_list_original)
            job_list.packages_dict = {}

            Log.debug("Length of the jobs list: {0}", len(job_list))

            # variables to be updated on the fly
            safetysleeptime = as_conf.get_safetysleeptime()
            Log.debug("Sleep: {0}", safetysleeptime)
            # Generate
            Log.info("Starting to generate cmd scripts")
            jobs = []
            jobs_cw = []

            if not isinstance(job_list, type([])):
                if check_wrapper and (not locked or (force and locked)):
                    Log.info("Generating all cmd script adapted for wrappers")
                    jobs = job_list.get_uncompleted()

                    jobs_cw = job_list.get_completed()
                else:
                    if (force and not locked) or (force and locked):
                        Log.info("Overwriting all cmd scripts")
                        jobs = job_list.get_job_list()
                    elif locked:
                        Log.warning(
                            "There is a .lock file and not -f, generating only all unsubmitted cmd scripts")
                        jobs = job_list.get_unsubmitted()
                    else:
                        Log.info("Generating cmd scripts only for selected jobs")
                        if filter_chunks:
                            fc = filter_chunks
                            Log.debug(fc)
                            if fc == 'Any':
                                jobs = job_list.get_job_list()
                            else:
                                # noinspection PyTypeChecker
                                data = json.loads(Autosubmit._create_json(fc))
                                for date_json in data['sds']:
                                    date = date_json['sd']
                                    jobs_date = [j for j in job_list.get_job_list() if date2str(
                                        j.date) == date]

                                    for member_json in date_json['ms']:
                                        member = member_json['m']
                                        jobs_member = [j for j in jobs_date if j.member == member]

                                        for chunk_json in member_json['cs']:
                                            chunk = int(chunk_json)
                                            jobs = jobs +  [job for job in [j for j in jobs_member if j.chunk == chunk]]

                        elif filter_status:
                            Log.debug(
                                "Filtering jobs with status {0}", filter_status)
                            if filter_status == 'Any':
                                jobs = job_list.get_job_list()
                            else:
                                fs = Autosubmit._get_status(filter_status)
                                jobs = [job for job in [j for j in job_list.get_job_list() if j.status == fs]]

                        elif filter_section:
                            ft = filter_section
                            Log.debug(ft)

                            if ft == 'Any':
                                jobs = job_list.get_job_list()
                            else:
                                for job in job_list.get_job_list():
                                    if job.section == ft:
                                        jobs.append(job)
                        elif lst:
                            jobs_lst = lst.split()

                            if jobs == 'Any':
                                jobs = job_list.get_job_list()
                            else:
                                for job in job_list.get_job_list():
                                    if job.name in jobs_lst:
                                        jobs.append(job)
                        else:
                            jobs = job_list.get_job_list()
            if isinstance(jobs, type([])):
                referenced_jobs_to_remove = set()
                for job in jobs:
                    for child in job.children:
                        if child not in jobs:
                            referenced_jobs_to_remove.add(child)
                    for parent in job.parents:
                        if parent not in jobs:
                            referenced_jobs_to_remove.add(parent)

                for job in jobs:
                    job.status = Status.WAITING

                Autosubmit.generate_scripts_andor_wrappers(
                    as_conf, job_list, jobs, packages_persistence, False)
            if len(jobs_cw) > 0:
                referenced_jobs_to_remove = set()
                for job in jobs_cw:
                    for child in job.children:
                        if child not in jobs_cw:
                            referenced_jobs_to_remove.add(child)
                    for parent in job.parents:
                        if parent not in jobs_cw:
                            referenced_jobs_to_remove.add(parent)

                for job in jobs_cw:
                    job.status = Status.WAITING
                Autosubmit.generate_scripts_andor_wrappers(
                    as_conf, job_list, jobs_cw, packages_persistence, False)

            Log.info("no more scripts to generate, now proceed to check them manually")
            time.sleep(safetysleeptime)
        except AutosubmitCritical as e:
            raise
        except AutosubmitError as e:
            raise
        except BaseException as e:
            raise AutosubmitCritical(
                "There are issues that occurred during the templates generation, please check that job parameters are well set and the template path exists.",
                7014, str(e))
        return True

    @staticmethod
    def generate_scripts_andor_wrappers(as_conf, job_list, jobs_filtered, packages_persistence, only_wrappers=False):
        """
        :param as_conf: Class that handles basic configuration parameters of Autosubmit. \n
        :type as_conf: AutosubmitConfig() Object \n
        :param job_list: Representation of the jobs of the experiment, keeps the list of jobs inside. \n
        :type job_list: JobList() Object \n
        :param jobs_filtered: list of jobs that are relevant to the process. \n
        :type jobs_filtered: List() of Job Objects \n
        :param packages_persistence: Object that handles local db persistence.  \n
        :type packages_persistence: JobPackagePersistence() Object \n
        :param only_wrappers: True when coming from Autosubmit.create(). False when coming from Autosubmit.inspect(), \n
        :type only_wrappers: Boolean \n
        :return: Nothing\n
        :rtype: \n
        """
        Log.warning("Generating the auxiliary job_list used for the -CW flag.")
        job_list._job_list = jobs_filtered
        job_list._persistence_file = job_list._persistence_file + "_cw_flag"
        parameters = as_conf.load_parameters()
        date_list = as_conf.get_date_list()
        if len(date_list) != len(set(date_list)):
            raise AutosubmitCritical(
                'There are repeated start dates!', 7014)
        num_chunks = as_conf.get_num_chunks()
        chunk_ini = as_conf.get_chunk_ini()
        member_list = as_conf.get_member_list()
        run_only_members = as_conf.get_member_list(run_only=True)
        date_format = ''
        if as_conf.get_chunk_size_unit() == 'hour':
            date_format = 'H'
        for date in date_list:
            if date.hour > 1:
                date_format = 'H'
            if date.minute > 1:
                date_format = 'M'
        wrapper_jobs = dict()
        for wrapper_section, wrapper_data in as_conf.experiment_data.get("WRAPPERS", {}).items():
            if type(wrapper_data) is not dict:
                continue
            wrapper_jobs[wrapper_section] = as_conf.get_wrapper_jobs(wrapper_data)
        Log.warning("Aux Job_list was generated successfully")
        submitter = Autosubmit._get_submitter(as_conf)
        submitter.load_platforms(as_conf)
        hpcarch = as_conf.get_platform()
        Autosubmit._load_parameters(as_conf, job_list, submitter.platforms)
        platforms_to_test = set()
        for job in job_list.get_job_list():
            if job.platform_name == "" or job.platform_name is None:
                job.platform_name = hpcarch
            job.platform = submitter.platforms[job.platform_name]
            if job.platform is not None and job.platform != "":
                platforms_to_test.add(job.platform)

        job_list.check_scripts(as_conf)

        job_list.update_list(as_conf, False)
        # Loading parameters again
        Autosubmit._load_parameters(as_conf, job_list, submitter.platforms)
        # Related to TWO_STEP_START new variable defined in expdef
        unparsed_two_step_start = as_conf.get_parse_two_step_start()
        if unparsed_two_step_start != "":
            job_list.parse_jobs_by_filter(unparsed_two_step_start)
        job_list.create_dictionary(date_list, member_list, num_chunks, chunk_ini, date_format, as_conf.get_retrials(),
                                   wrapper_jobs)
        for job in job_list.get_active():
            if job.status != Status.WAITING:
                job.status = Status.READY
        while job_list.get_active():
            Autosubmit.submit_ready_jobs(as_conf, job_list, platforms_to_test, packages_persistence, True,
                                         only_wrappers, hold=False)
            # for job in job_list.get_uncompleted_and_not_waiting():
            #    job.status = Status.COMPLETED
            job_list.update_list(as_conf, False)

    @staticmethod
    def terminate(all_threads):
        # Closing threads on Ctrl+C
        Log.info(
            "Looking for active threads before closing Autosubmit. Ending the program before these threads finish may result in unexpected behavior. This procedure will last until all threads have finished or the program has waited for more than 30 seconds.")
        timeout = 0
        active_threads = True
        while active_threads and timeout <= 60:
            active_threads = False
            for thread in all_threads:
                if "JOB_" in thread.name:
                    if thread.is_alive():
                        active_threads = True
                        Log.info("{0} is still retrieving outputs, time remaining is {1} seconds.".format(
                            thread.name, 60 - timeout))
                        break
            if active_threads:
                sleep(10)
                timeout += 10

    @staticmethod
    def manage_wrapper_job(as_conf, job_list, platform, wrapper_id, save=False):
        check_wrapper_jobs_sleeptime = as_conf.get_wrapper_check_time()
        Log.debug('WRAPPER CHECK TIME = {0}'.format(
            check_wrapper_jobs_sleeptime))
        # Setting prev_status as an easy way to check status change for inner jobs
        wrapper_job = job_list.job_package_map[wrapper_id]
        if as_conf.get_notifications() == "true":
            for inner_job in wrapper_job.job_list:
                inner_job.prev_status = inner_job.status
        check_wrapper = True
        if wrapper_job.status == Status.RUNNING:
            check_wrapper = True if datetime.timedelta.total_seconds(datetime.datetime.now(
            ) - wrapper_job.checked_time) >= check_wrapper_jobs_sleeptime else False
        if check_wrapper:
            Log.debug('Checking Wrapper {0}'.format(str(wrapper_id)))
            wrapper_job.checked_time = datetime.datetime.now()
            platform.check_job(wrapper_job)
            try:
                if wrapper_job.status != wrapper_job.new_status:
                    Log.info('Wrapper job ' + wrapper_job.name + ' changed from ' + str(
                        Status.VALUE_TO_KEY[wrapper_job.status]) + ' to status ' + str(
                        Status.VALUE_TO_KEY[wrapper_job.new_status]))
                    save = True
            except Exception as e:
                raise AutosubmitCritical(
                    "Wrapper is in Unknown Status couldn't get wrapper parameters", 7050)

            # New status will be saved and inner_jobs will be checked.
            wrapper_job.check_status(
                wrapper_job.new_status)
            # Erase from packages if the wrapper failed to be queued ( Hold Admin bug )
            if wrapper_job.status == Status.WAITING:
                for inner_job in wrapper_job.job_list:
                    inner_job.packed = False
                job_list.job_package_map.pop(
                    wrapper_id, None)
                job_list.packages_dict.pop(
                    wrapper_id, None)
            save = True
        return wrapper_job, save

    @staticmethod
    def run_experiment(expid, notransitive=False, update_version=False, start_time=None, start_after=None,
                       run_only_members=None):
        """
        Runs and experiment (submitting all the jobs properly and repeating its execution in case of failure).

        :param run_only_ºmembers:
        :param start_after:
        :param start_time:
        :param update_version:
        :param notransitive:
        :type expid: str
        :param expid: identifier of experiment to be run
        :return: True if run to the end, False otherwise
        :rtype: bool
        """
        try:
            exp_path = os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid)
            tmp_path = os.path.join(exp_path, BasicConfig.LOCAL_TMP_DIR)
            import platform
            host = platform.node()
        except BaseException as e:
            raise AutosubmitCritical("Failure during the loading of the experiment configuration, check file paths",
                                     7014, str(e))
        as_conf = AutosubmitConfig(expid, BasicConfig, YAMLParserFactory())
        as_conf.check_conf_files(running_time=True, force_load=True)
        try:
            # Handling starting time
            AutosubmitHelper.handle_start_time(start_time)

            # Start after completion trigger block
            AutosubmitHelper.handle_start_after(start_after, expid, BasicConfig())

            # Handling run_only_members
            allowed_members = AutosubmitHelper.get_allowed_members(run_only_members, as_conf)
        except AutosubmitCritical as e:
            raise
        except BaseException as e:
            raise AutosubmitCritical("Failure during setting the start time check trace for details", 7014, str(e))

        # checking if there is a lock file to avoid multiple running on the same expid
        try:
            with portalocker.Lock(os.path.join(tmp_path, 'autosubmit.lock'), timeout=1):
                try:
                    Log.info(
                        "Preparing .lock file to avoid multiple instances with same experiment id")
                    os.system('clear')
                    signal.signal(signal.SIGINT, signal_handler)

                    hpcarch = as_conf.get_platform()
                    safetysleeptime = as_conf.get_safetysleeptime()
                    retrials = as_conf.get_retrials()
                    submitter = Autosubmit._get_submitter(as_conf)
                    submitter.load_platforms(as_conf)
                    Log.debug("The Experiment name is: {0}", expid)
                    Log.debug("Sleep: {0}", safetysleeptime)
                    Log.debug("Default retrials: {0}", retrials)
                    Log.info("Starting job submission...")
                    pkl_dir = os.path.join(
                        BasicConfig.LOCAL_ROOT_DIR, expid, 'pkl')
                    try:
                        job_list = Autosubmit.load_job_list(
                            expid, as_conf, notransitive=notransitive)
                    except IOError as e:
                        raise AutosubmitError(
                            "Job_list not found", 6016, str(e))
                    except AutosubmitCritical as e:
                        raise AutosubmitCritical(
                            "Corrupted job_list, backup couldn't be restored", 7040, e.message)
                    except BaseException as e:
                        raise AutosubmitCritical(
                            "Corrupted job_list, backup couldn't be restored", 7040, str(e))

                    Log.debug(
                        "Starting from job list restored from {0} files", pkl_dir)
                    Log.debug("Length of the jobs list: {0}", len(job_list))
                    Autosubmit._load_parameters(
                        as_conf, job_list, submitter.platforms)
                    # check the job list script creation
                    Log.debug("Checking experiment templates...")
                    platforms_to_test = set()
                    for job in job_list.get_job_list():
                        if job.platform_name is None or job.platform_name == "":
                            job.platform_name = hpcarch
                        # noinspection PyTypeChecker
                        try:
                            job.platform = submitter.platforms[job.platform_name.upper()]
                        except Exception as e:
                            raise AutosubmitCritical(
                                "hpcarch={0} not found in the platforms configuration file".format(job.platform_name),
                                7014)
                        # noinspection PyTypeChecker
                        if job.status not in (Status.COMPLETED, Status.SUSPENDED):
                            platforms_to_test.add(job.platform)
                    try:
                        job_list.check_scripts(as_conf)
                    except Exception as e:
                        raise AutosubmitCritical(
                            "Error while checking job templates", 7014, str(e))
                    Log.debug("Loading job packages")
                    try:
                        packages_persistence = JobPackagePersistence(os.path.join(
                            BasicConfig.LOCAL_ROOT_DIR, expid, "pkl"), "job_packages_" + expid)
                    except IOError as e:
                        raise AutosubmitError(
                            "job_packages not found", 6016, str(e))
                    except BaseException as e:
                        raise AutosubmitCritical(
                            "Corrupted job_packages, python 2.7 and sqlite doesn't allow to restore these packages",
                            7040, str(e))
                    if as_conf.get_wrapper_type() != 'none':
                        os.chmod(os.path.join(BasicConfig.LOCAL_ROOT_DIR,
                                              expid, "pkl", "job_packages_" + expid + ".db"), 0o644)
                        try:
                            packages = packages_persistence.load()
                        except IOError as e:
                            raise AutosubmitError(
                                "job_packages not found", 6016, str(e))
                        except BaseException as e:
                            raise AutosubmitCritical(
                                "Corrupted job_packages, python 2.7 and sqlite doesn't allow to restore these packages(will work on autosubmit4)",
                                7040, str(e))
                        Log.debug("Processing job packages")

                        try:
                            for (exp_id, package_name, job_name) in packages:
                                if package_name not in job_list.packages_dict:
                                    job_list.packages_dict[package_name] = []
                                job_list.packages_dict[package_name].append(
                                    job_list.get_job_by_name(job_name))
                            for package_name, jobs in job_list.packages_dict.items():
                                from .job.job import WrapperJob
                                wrapper_status = Status.SUBMITTED
                                all_completed = True
                                running = False
                                queuing = False
                                failed = False
                                hold = False
                                submitted = False
                                if jobs[0].status == Status.RUNNING or jobs[0].status == Status.COMPLETED:
                                    running = True
                                for job in jobs:
                                    if job.status == Status.QUEUING:
                                        queuing = True
                                        all_completed = False
                                    elif job.status == Status.FAILED:
                                        failed = True
                                        all_completed = False
                                    elif job.status == Status.HELD:
                                        hold = True
                                        all_completed = False
                                    elif job.status == Status.SUBMITTED:
                                        submitted = True
                                        all_completed = False
                                if all_completed:
                                    wrapper_status = Status.COMPLETED
                                elif hold:
                                    wrapper_status = Status.HELD
                                else:
                                    if running:
                                        wrapper_status = Status.RUNNING
                                    elif queuing:
                                        wrapper_status = Status.QUEUING
                                    elif submitted:
                                        wrapper_status = Status.SUBMITTED
                                    elif failed:
                                        wrapper_status = Status.FAILED
                                    else:
                                        wrapper_status = Status.SUBMITTED
                                wrapper_job = WrapperJob(package_name, jobs[0].id, wrapper_status, 0, jobs,
                                                         None,
                                                         None, jobs[0].platform, as_conf, jobs[0].hold)
                                job_list.job_package_map[jobs[0].id] = wrapper_job
                        except Exception as e:
                            raise AutosubmitCritical(
                                "Autosubmit failed while processing job packages. This might be due to a change in your experiment configuration files after 'autosubmit create' was performed.",
                                7014, str(e))

                    Log.debug("Checking job_list current status")
                    job_list.update_list(as_conf, first_time=True)
                    job_list.save()

                    Log.info("Autosubmit is running with v{0}", Autosubmit.autosubmit_version)
                    # Before starting main loop, setup historical database tables and main information
                    Log.debug("Running job data structure")
                    try:
                        # Historical Database: Can create a new run if there is a difference in the number of jobs or if the current run does not exist.
                        exp_history = ExperimentHistory(expid, jobdata_dir_path=BasicConfig.JOBDATA_DIR,
                                                        historiclog_dir_path=BasicConfig.HISTORICAL_LOG_DIR)
                        exp_history.initialize_database()
                        exp_history.process_status_changes(job_list.get_job_list(), as_conf.get_chunk_size_unit(),
                                                           as_conf.get_chunk_size(),
                                                           current_config=as_conf.get_full_config_as_json())
                        Autosubmit.database_backup(expid)
                    except Exception as e:
                        try:
                            Autosubmit.database_fix(expid)
                            # This error is important
                        except Exception as e:
                            pass
                    try:
                        ExperimentStatus(expid).set_as_running()
                    except Exception as e:
                        # Connection to status database ec_earth.db can fail.
                        # API worker will fix the status.
                        Log.debug(
                            "Autosubmit couldn't set your experiment as running on the autosubmit times database: {1}. Exception: {0}".format(
                                str(e), os.path.join(BasicConfig.DB_DIR, BasicConfig.AS_TIMES_DB)), 7003)
                    if allowed_members:
                        # Set allowed members after checks have been performed. This triggers the setter and main logic of the -rm feature.
                        job_list.run_members = allowed_members
                        Log.result(
                            "Only jobs with member value in {0} or no member will be allowed in this run. Also, those jobs already SUBMITTED, QUEUING, or RUNNING will be allowed to complete and will be tracked.".format(
                                str(allowed_members)))
                except AutosubmitCritical as e:
                    e.message += " HINT: check the CUSTOM_DIRECTIVE syntax in your jobs configuration files."
                    raise AutosubmitCritical(e.message, 7014, e.trace)
                except Exception as e:
                    raise AutosubmitCritical(
                        "Error in run initialization", 7014, str(e))  # Changing default to 7014
                # Related to TWO_STEP_START new variable defined in expdef
                unparsed_two_step_start = as_conf.get_parse_two_step_start()
                if unparsed_two_step_start != "":
                    job_list.parse_jobs_by_filter(unparsed_two_step_start)

                main_loop_retrials = 3650  # Hard limit of tries 3650 tries at 15-120seconds sleep each try
                # establish the connection to all platforms

                Autosubmit.restore_platforms(platforms_to_test)
                save = True
                # @main
                Log.debug("Running main loop")
                #########################
                # AUTOSUBMIT - MAIN LOOP
                #########################
                # Main loop. Finishing when all jobs have been submitted

                while job_list.get_active():
                    # Log.info("FD: {0}".format(log.fd_show.fd_table_status_str()))
                    try:
                        if Autosubmit.exit:
                            Autosubmit.terminate(threading.enumerate())
                            return 0
                        # reload parameters changes
                        Log.debug("Reloading parameters...")
                        try:
                            Autosubmit._load_parameters(as_conf, job_list, submitter.platforms)
                            # Log.info("FD 2: {0}".format(log.fd_show.fd_table_status_str()))
                        except BaseException as e:
                            raise AutosubmitError("Config files seems to not be accessible", 6040, str(e))
                        total_jobs = len(job_list.get_job_list())
                        Log.info("\n\n{0} of {1} jobs remaining ({2})".format(
                            total_jobs - len(job_list.get_completed()), total_jobs, time.strftime("%H:%M")))
                        if len(job_list.get_failed()) > 0:
                            Log.info("{0} jobs has been  failed ({1})".format(
                                len(job_list.get_failed()), time.strftime("%H:%M")))
                        safetysleeptime = as_conf.get_safetysleeptime()
                        default_retrials = as_conf.get_retrials()
                        check_wrapper_jobs_sleeptime = as_conf.get_wrapper_check_time()
                        Log.debug("Sleep: {0}", safetysleeptime)
                        Log.debug("Number of retrials: {0}", default_retrials)

                        if save:  # previous iteration
                            job_list.backup_save()
                        save = False
                        slurm = []
                        job_changes_tracker = {}  # to easily keep track of changes per iteration
                        Log.debug("End of checking")
                        # End Check Current jobs
                        # jobs_to_check are no wrapped jobs.
                        jobs_to_check = dict()
                        # Check Wrappers and add non-wrapped jobs to be checked later.
                        for platform in platforms_to_test:
                            queuing_jobs = job_list.get_in_queue_grouped_id(platform)
                            Log.debug('Checking jobs for platform={0}'.format(platform.name))
                            for job_id, job in queuing_jobs.items():
                                # Check Wrappers one-by-one
                                # TODO CHECK this before continue
                                if job_list.job_package_map and job_id in job_list.job_package_map:
                                    wrapper_job, save = Autosubmit.manage_wrapper_job(as_conf, job_list, platform,
                                                                                      job_id)

                                    # Notifications e-mail
                                    if as_conf.get_notifications() == "true":
                                        for inner_job in wrapper_job.job_list:
                                            if inner_job.prev_status != inner_job.status:
                                                if Status.VALUE_TO_KEY[inner_job.status] in inner_job.notify_on:
                                                    Notifier.notify_status_change(MailNotifier(BasicConfig), expid,
                                                                                  inner_job.name,
                                                                                  Status.VALUE_TO_KEY[
                                                                                      inner_job.prev_status],
                                                                                  Status.VALUE_TO_KEY[inner_job.status],
                                                                                  as_conf.experiment_data["MAIL"]["TO"])
                                    # Detect and store changes for the GUI
                                    job_changes_tracker = {job.name: (
                                        job.prev_status, job.status) for job in wrapper_job.job_list if
                                        job.prev_status != job.status}
                                else:  # Adds to a list all running jobs to be checked.
                                    if job.status == Status.FAILED:
                                        continue
                                    job_prev_status = job.status
                                    # If exist key has been pressed and previous status was running, do not check
                                    if not (Autosubmit.exit is True and job_prev_status == Status.RUNNING):
                                        if platform.name in jobs_to_check:
                                            jobs_to_check[platform.name].append([job, job_prev_status])
                                        else:
                                            jobs_to_check[platform.name] = [[job, job_prev_status]]
                        for platform in platforms_to_test:
                            platform_jobs = jobs_to_check.get(platform.name, [])

                            # not all platforms are doing this check simultaneously
                            if len(platform_jobs) == 0:
                                continue
                            platform.check_Alljobs(platform_jobs, as_conf)
                            # mail notification
                            for job, job_prev_status in jobs_to_check[platform.name]:
                                if job_prev_status != job.update_status(as_conf):
                                    # Keeping track of changes
                                    job_changes_tracker[job.name] = (job_prev_status, job.status)
                                    if as_conf.get_notifications() == "true":
                                        if Status.VALUE_TO_KEY[job.status] in job.notify_on:
                                            Notifier.notify_status_change(MailNotifier(BasicConfig), expid, job.name,
                                                                          Status.VALUE_TO_KEY[job_prev_status],
                                                                          Status.VALUE_TO_KEY[job.status],
                                                                          as_conf.experiment_data["MAIL"]["TO"])
                                save = True
                        save2 = job_list.update_list(
                            as_conf, submitter=submitter)
                        job_list.save()
                        if len(job_list.get_ready()) > 0:
                            save = Autosubmit.submit_ready_jobs(
                                as_conf, job_list, platforms_to_test, packages_persistence, hold=False)
                            job_list.update_list(as_conf, submitter=submitter)
                            job_list.save()

                        if as_conf.get_remote_dependencies() == "true" and len(job_list.get_prepared()) > 0:
                            Autosubmit.submit_ready_jobs(
                                as_conf, job_list, platforms_to_test, packages_persistence, hold=True)
                            job_list.update_list(as_conf, submitter=submitter)
                            job_list.save()
                        # Safe spot to store changes
                        try:
                            exp_history = ExperimentHistory(expid, jobdata_dir_path=BasicConfig.JOBDATA_DIR,
                                                            historiclog_dir_path=BasicConfig.HISTORICAL_LOG_DIR)
                            if len(job_changes_tracker) > 0:
                                exp_history.process_job_list_changes_to_experiment_totals(job_list.get_job_list())
                                Autosubmit.database_backup(expid)
                        except BaseException as e:
                            Log.printlog("Historic database seems corrupted, AS will repair it and resume the run",
                                         Log.INFO)
                            try:
                                Autosubmit.database_fix(expid)
                                exp_history = ExperimentHistory(expid, jobdata_dir_path=BasicConfig.JOBDATA_DIR,
                                                                historiclog_dir_path=BasicConfig.HISTORICAL_LOG_DIR)
                                if len(job_changes_tracker) > 0:
                                    exp_history.process_job_list_changes_to_experiment_totals(job_list.get_job_list())
                                    Autosubmit.database_backup(expid)
                            except Exception as e:
                                Log.warning(
                                    "Couldn't recover the Historical database, AS will continue without it, GUI may be affected")
                        job_changes_tracker = {}
                        if Autosubmit.exit:
                            job_list.save()
                        time.sleep(safetysleeptime)

                    except AutosubmitError as e:  # If an error is detected, restore all connections and job_list
                        Log.error("Trace: {0}", e.trace)
                        Log.error("{1} [eCode={0}]", e.code, e.message)
                        # Log.debug("FD recovery: {0}".format(log.fd_show.fd_table_status_str()))
                        # No need to wait until the remote platform reconnection
                        recovery = False
                        as_conf = AutosubmitConfig(expid, BasicConfig, YAMLParserFactory())
                        consecutive_retrials = 1
                        failed_names = {}
                        Log.info("Storing failed job count...")
                        try:
                            for job in job_list.get_job_list():
                                if job.fail_count > 0:
                                    failed_names[job.name] = job.fail_count
                        except BaseException as e:
                            Log.printlog("Error trying to store failed job count", Log.WARNING)
                        Log.result("Storing failed job count...done")
                        while not recovery and main_loop_retrials > 0:
                            delay = min(15 * consecutive_retrials, 120)
                            main_loop_retrials = main_loop_retrials - 1
                            sleep(delay)
                            consecutive_retrials = consecutive_retrials + 1
                            Log.info("Waiting {0} seconds before continue".format(delay))
                            try:
                                as_conf.reload(force_load=True)
                                Log.info("Recovering job_list...")
                                job_list = Autosubmit.load_job_list(
                                    expid, as_conf, notransitive=notransitive)
                                Log.info("Recovering job_list... Done")
                                if allowed_members:
                                    # Set allowed members after checks have been performed. This triggers the setter and main logic of the -rm feature.
                                    job_list.run_members = allowed_members
                                    Log.result(
                                        "Only jobs with member value in {0} or no member will be allowed in this run. Also, those jobs already SUBMITTED, QUEUING, or RUNNING will be allowed to complete and will be tracked.".format(
                                            str(allowed_members)))
                                platforms_to_test = set()
                                Log.info("Recovering platform information...")
                                for job in job_list.get_job_list():
                                    if job.platform_name is None or job.platform_name == "":
                                        job.platform_name = hpcarch
                                    job.platform = submitter.platforms[job.platform_name]
                                    platforms_to_test.add(job.platform)

                                Log.info("Recovering platform information... Done")
                                Log.info("Recovering Failure count...")
                                for job in job_list.get_job_list():
                                    if job.name in list(failed_names.keys()):
                                        job.fail_count = failed_names[job.name]
                                Log.info("Recovering Failure count... Done")

                                Log.info("Recovering parameters...")
                                Autosubmit._load_parameters(as_conf, job_list, submitter.platforms)
                                # Recovery wrapper [Packages]
                                Log.info("Recovering Wrappers...")
                                packages_persistence = JobPackagePersistence(
                                    os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid, "pkl"), "job_packages_" + expid)
                                packages = packages_persistence.load()
                                for (exp_id, package_name, job_name) in packages:
                                    if package_name not in job_list.packages_dict:
                                        job_list.packages_dict[package_name] = []
                                    job_list.packages_dict[package_name].append(
                                        job_list.get_job_by_name(job_name))
                                # Recovery wrappers [Wrapper status]
                                for package_name, jobs in job_list.packages_dict.items():
                                    from .job.job import WrapperJob
                                    wrapper_status = Status.SUBMITTED
                                    all_completed = True
                                    running = False
                                    queuing = False
                                    failed = False
                                    hold = False
                                    submitted = False
                                    if jobs[0].status == Status.RUNNING or jobs[0].status == Status.COMPLETED:
                                        running = True
                                    for job in jobs:
                                        if job.status == Status.QUEUING:
                                            queuing = True
                                            all_completed = False
                                        elif job.status == Status.FAILED:
                                            failed = True
                                            all_completed = False
                                        elif job.status == Status.HELD:
                                            hold = True
                                            all_completed = False
                                        elif job.status == Status.SUBMITTED:
                                            submitted = True
                                            all_completed = False
                                    if all_completed:
                                        wrapper_status = Status.COMPLETED
                                    elif hold:
                                        wrapper_status = Status.HELD
                                    else:
                                        if running:
                                            wrapper_status = Status.RUNNING
                                        elif queuing:
                                            wrapper_status = Status.QUEUING
                                        elif submitted:
                                            wrapper_status = Status.SUBMITTED
                                        elif failed:
                                            wrapper_status = Status.FAILED
                                        else:
                                            wrapper_status = Status.SUBMITTED
                                    wrapper_job = WrapperJob(package_name, jobs[0].id, wrapper_status, 0, jobs,
                                                             None,
                                                             None, jobs[0].platform, as_conf, jobs[0].hold)
                                    job_list.job_package_map[jobs[0].id] = wrapper_job
                                Log.info("Recovering wrappers... Done")
                                job_list.update_list(as_conf)
                                Log.info("Saving recovered job list...")
                                job_list.save()
                                Log.info("Saving recovered job list... Done")
                                recovery = True
                                Log.result("Recover of job_list is completed")
                            except AutosubmitError as e:
                                recovery = False
                                Log.result("Recover of job_list has fail {0}".format(e.message))
                            except IOError as e:
                                recovery = False
                                Log.result("Recover of job_list has fail {0}".format(str(e)))
                            except BaseException as e:
                                recovery = False
                                Log.result("Recover of job_list has fail {0}".format(str(e)))
                        # Restore platforms and try again, to avoid endless loop with failed configuration, a hard limit is set.
                        reconnected = False
                        mail_notify = True
                        times = 0
                        max_times = 10
                        Log.info("Restoring the connection to all experiment platforms")
                        consecutive_retrials = 1
                        delay = min(15 * consecutive_retrials, 120)
                        while not reconnected and main_loop_retrials > 0:
                            main_loop_retrials = main_loop_retrials - 1
                            Log.info("Recovering the remote platform connection")
                            Log.info("Waiting {0} seconds before continue".format(delay))
                            sleep(delay)
                            consecutive_retrials = consecutive_retrials + 1
                            try:
                                if times % max_times == 0:
                                    mail_notify = True
                                    max_times = max_times + max_times
                                    times = 0
                                else:
                                    mail_notify = False
                                times = times + 1
                                Autosubmit.restore_platforms(platforms_to_test, mail_notify=mail_notify,
                                                             as_conf=as_conf, expid=expid)
                                reconnected = True
                            except AutosubmitCritical as e:
                                # Message prompt by restore_platforms.
                                Log.info(
                                    "{0}\nCouldn't recover the platforms, retrying in 15seconds...".format(e.message))
                                reconnected = False
                            except IOError:
                                reconnected = False
                            except BaseException:
                                reconnected = False
                        if main_loop_retrials <= 0:
                            raise AutosubmitCritical(
                                "Autosubmit Encounter too much errors during running time, limit of 4hours reached",
                                7051, e.message)
                    except AutosubmitCritical as e:  # Critical errors can't be recovered. Failed configuration or autosubmit error
                        raise AutosubmitCritical(e.message, e.code, e.trace)
                    except (portalocker.AlreadyLocked, portalocker.LockException) as e:
                        message = "We have detected that there is another Autosubmit instance using the experiment\n. Stop other Autosubmit instances that are using the experiment or delete autosubmit.lock file located on tmp folder"
                        raise AutosubmitCritical(message, 7000)
                    except BaseException as e:  # If this happens, there is a bug in the code or an exception not-well caught
                        raise AutosubmitCritical("There is a bug in the code, please contact via git", 7070, str(e))
                Log.result("No more jobs to run.")
                # Updating job data header with current information when experiment ends
                try:
                    exp_history = ExperimentHistory(expid, jobdata_dir_path=BasicConfig.JOBDATA_DIR,
                                                    historiclog_dir_path=BasicConfig.HISTORICAL_LOG_DIR)
                    exp_history.process_job_list_changes_to_experiment_totals(job_list.get_job_list())
                    Autosubmit.database_backup(expid)
                except Exception as e:
                    try:
                        Autosubmit.database_fix(expid)
                    except Exception as e:
                        pass
                # Wait for all remaining threads of I/O, close remaining connections
                timeout = 0
                active_threads = True
                all_threads = threading.enumerate()
                while active_threads and timeout <= 180:
                    active_threads = False
                    for thread in all_threads:
                        if "JOB_" in thread.name:
                            if thread.is_alive():
                                active_threads = True
                                Log.info("{0} is still retrieving outputs, time remaining is {1} seconds.".format(
                                    thread.name, 180 - timeout))
                                break
                    if active_threads:
                        sleep(10)
                        timeout += 10
                for platform in platforms_to_test:
                    platform.closeConnection()
                if len(job_list.get_failed()) > 0:
                    Log.info("Some jobs have failed and reached maximum retrials")
                else:
                    Log.result("Run successful")
                    # Updating finish time for job data header
                    exp_history.finish_current_experiment_run()
        except (portalocker.AlreadyLocked, portalocker.LockException) as e:
            message = "We have detected that there is another Autosubmit instance using the experiment\n. Stop other Autosubmit instances that are using the experiment or delete autosubmit.lock file located on tmp folder"
            raise AutosubmitCritical(message, 7000)
        except AutosubmitCritical as e:
            raise
        except BaseException as e:
            raise AutosubmitCritical("This seems like a bug in the code, please contact AS developers", 7070, str(e))

    @staticmethod
    def restore_platforms(platform_to_test, mail_notify=False, as_conf=None, expid=None):
        Log.info("Checking the connection to all platforms in use")
        issues = ""
        platform_issues = ""
        ssh_config_issues = ""
        private_key_error = "Please, add your private key to the ssh-agent ( ssh-add <path_to_key> ) or use a non-encrypted key\nIf ssh agent is not initialized, prompt first eval `ssh-agent -s`"
        for platform in platform_to_test:
            platform_issues = ""
            try:
                message = platform.test_connection()
                if message is None:
                    message = "OK"
                if message != "OK":
                    if message.find("doesn't accept remote connections") != -1:
                        ssh_config_issues += message
                    elif message.find("Authentication failed") != -1:
                        ssh_config_issues += message + ". Please, check the user and project of this platform\nIf it is correct, try another host"
                    elif message.find("private key file is encrypted") != -1:
                        if private_key_error not in ssh_config_issues:
                            ssh_config_issues += private_key_error
                    elif message.find("Invalid certificate") != -1:
                        ssh_config_issues += message + ".Please, the eccert expiration date"
                    else:
                        ssh_config_issues += message + " this is an PARAMIKO SSHEXCEPTION: indicates that there is something incompatible in the ssh_config for host:{0}\n maybe you need to contact your sysadmin".format(
                            platform.host)
            except BaseException as e:
                try:
                    if mail_notify:
                        email = as_conf.get_mails_to()
                        if "@" in email[0]:
                            Notifier.notify_experiment_status(MailNotifier(BasicConfig), expid, email, platform)
                except Exception as e:
                    pass
                platform_issues += "\n[{1}] Connection Unsuccessful to host {0} ".format(
                    platform.host, platform.name)
                issues += platform_issues
                continue
            if platform.check_remote_permissions():
                Log.result("[{1}] Correct user privileges for host {0}",
                           platform.host, platform.name)
            else:
                platform_issues += "\n[{0}] has configuration issues.\n Check that the connection is passwd-less.(ssh {1}@{4})\n Check the parameters that build the root_path are correct:{{scratch_dir/project/user}} = {{{3}/{2}/{1}}}".format(
                    platform.name, platform.user, platform.project, platform.scratch, platform.host)
                issues += platform_issues
            if platform_issues == "":

                Log.printlog("[{1}] Connection successful to host {0}".format(platform.host, platform.name), Log.RESULT)
            else:
                if platform.connected:
                    platform.connected = False
                    Log.printlog("[{1}] Connection successful to host {0}, however there are issues with %HPCROOT%".format(platform.host, platform.name),
                                 Log.WARNING)
                else:
                    Log.printlog("[{1}] Connection failed to host {0}".format(platform.host, platform.name), Log.WARNING)
        if issues != "":
            if ssh_config_issues.find(private_key_error[:-2]) != -1:
                raise AutosubmitCritical("Private key is encrypted, Autosubmit does not run in interactive mode.\nPlease, add the key to the ssh agent(ssh-add <path_to_key>).\nIt will remain open as long as session is active, for force clean you can prompt ssh-add -D",7073, issues + "\n" + ssh_config_issues)
            else:
                raise AutosubmitCritical("Issues while checking the connectivity of platforms.", 7010, issues + "\n" + ssh_config_issues)

    @staticmethod
    def submit_ready_jobs(as_conf, job_list, platforms_to_test, packages_persistence, inspect=False,
                          only_wrappers=False, hold=False):

        # type: (AutosubmitConfig, JobList, Set[Platform], JobPackagePersistence, bool, bool, bool) -> bool
        """
        Gets READY jobs and send them to the platforms if there is available space on the queues

        :param hold:
        :param as_conf: autosubmit config object \n
        :type as_conf: AutosubmitConfig object  \n
        :param job_list: job list to check  \n
        :type job_list: JobList object  \n
        :param platforms_to_test: platforms used  \n
        :type platforms_to_test: set of Platform Objects, e.g. SgePlatform(), LsfPlatform().  \n
        :param packages_persistence: Handles database per experiment. \n
        :type packages_persistence: JobPackagePersistence object \n
        :param inspect: True if coming from generate_scripts_andor_wrappers(). \n
        :type inspect: Boolean \n
        :param only_wrappers: True if it comes from create -cw, False if it comes from inspect -cw. \n
        :type only_wrappers: Boolean \n
        :return: True if at least one job was submitted, False otherwise \n
        :rtype: Boolean
        """
        save_1 = False
        save_2 = False
        try:
            for platform in platforms_to_test:
                packages_to_submit = JobPackager(as_conf, platform, job_list, hold=hold).build_packages()
                save_1, failed_packages, error_message, valid_packages_to_submit = platform.submit_ready_jobs(as_conf,
                                                                                                              job_list,
                                                                                                              platforms_to_test,
                                                                                                              packages_persistence,
                                                                                                              packages_to_submit,
                                                                                                              inspect=inspect,
                                                                                                              only_wrappers=only_wrappers,
                                                                                                              hold=hold)
                # Jobs that are being retrieved in batch. Right now, only available for slurm platforms.
                if not inspect and len(valid_packages_to_submit) > 0:
                    job_list.save()
                save_2 = False
                if platform.type == "slurm" and not inspect and not only_wrappers:
                    # Process the script generated in submit_ready_jobs
                    save_2, valid_packages_to_submit = platform.process_batch_ready_jobs(valid_packages_to_submit,
                                                                                         failed_packages,
                                                                                         error_message="", hold=hold)
                    if not inspect and len(valid_packages_to_submit) > 0:
                        job_list.save()
                # Save wrappers(jobs that has the same id) to be visualized and checked in other parts of the code
                job_list.save_wrappers(valid_packages_to_submit, failed_packages, as_conf, packages_persistence,
                                       hold=hold, inspect=inspect)
                if error_message != "":
                    raise AutosubmitCritical("Submission Failed due wrong configuration:{0}".format(error_message),
                                             7014)
            if save_1 or save_2:
                return True
            else:
                return False
        except AutosubmitError as e:
            raise
        except AutosubmitCritical as e:
            raise
        except BaseException as e:
            raise AutosubmitCritical("This seems like a bug in the code, please contact AS developers", 7070, str(e))

    @staticmethod
    def monitor(expid, file_format, lst, filter_chunks, filter_status, filter_section, hide, txt_only=False,
                group_by=None, expand="", expand_status=list(), hide_groups=False, notransitive=False,
                check_wrapper=False, txt_logfiles=False, detail=False):
        """
        Plots workflow graph for a given experiment with status of each job coded by node color.
        Plot is created in experiment's plot folder with name <expid>_<date>_<time>.<file_format>

        :param txt_logfiles:
        :type file_format: str
        :type expid: str
        :param expid: identifier of the experiment to plot
        :param file_format: plot's file format. It can be pdf, png, ps or svg
        :param lst: list of jobs to change status
        :type lst: str
        :param filter_chunks: chunks to change status
        :type filter_chunks: str
        :param filter_status: current status of the jobs to change status
        :type filter_status: str
        :param filter_section: sections to change status
        :type filter_section: str
        :param hide: hides plot window
        :type hide: bool
        :param txt_only: workflow will only be written as text
        :type txt_only: bool
        :param group_by: workflow will only be written as text
        :type group_by: bool
        :param expand: Filtering of jobs for its visualization
        :type expand: str
        :param expand_status: Filtering of jobs for its visualization
        :type expand_status: str
        :param hide_groups: Simplified workflow illustration by encapsulating the jobs.
        :type hide_groups: bool
        :param notransitive: workflow will only be written as text
        :type notransitive: bool
        :param check_wrapper: Shows a preview of how the wrappers will look
        :type check_wrapper: bool
        :param notransitive: Some dependencies will be omitted
        :type notransitive: bool
        :param detail: better text format representation but more expensive
        :type detail: bool



        """
        try:
            exp_path = os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid)
            Log.info("Getting job list...")
            as_conf = AutosubmitConfig(expid, BasicConfig, YAMLParserFactory())
            as_conf.check_conf_files(False)
            # Getting output type from configuration
            output_type = as_conf.get_output_type()
            pkl_dir = os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid, 'pkl')
            job_list = Autosubmit.load_job_list(
                expid, as_conf, notransitive=notransitive, monitor=True)
            Log.debug("Job list restored from {0} files", pkl_dir)
        except AutosubmitError as e:
            raise AutosubmitCritical(e.message, e.code, e.trace)
        except AutosubmitCritical as e:
            raise
        except BaseException as e:
            raise AutosubmitCritical("Error while checking the configuration files or loading the job_list", 7040,
                                     str(e))
        try:
            jobs = []
            if not isinstance(job_list, type([])):
                if filter_chunks:
                    fc = filter_chunks
                    Log.debug(fc)

                    if fc == 'Any':
                        jobs = job_list.get_job_list()
                    else:
                        # noinspection PyTypeChecker
                        data = json.loads(Autosubmit._create_json(fc))
                        for date_json in data['sds']:
                            date = date_json['sd']
                            jobs_date = [j for j in job_list.get_job_list() if date2str(
                                j.date) == date]

                            for member_json in date_json['ms']:
                                member = member_json['m']
                                jobs_member = [j for j in jobs_date if j.member == member]

                                for chunk_json in member_json['cs']:
                                    chunk = int(chunk_json)
                                    jobs = jobs + \
                                           [job for job in [j for j in jobs_member if j.chunk == chunk]]

                elif filter_status:
                    Log.debug("Filtering jobs with status {0}", filter_status)
                    if filter_status == 'Any':
                        jobs = job_list.get_job_list()
                    else:
                        fs = Autosubmit._get_status(filter_status)
                        jobs = [job for job in [j for j in job_list.get_job_list() if j.status == fs]]

                elif filter_section:
                    ft = filter_section
                    Log.debug(ft)

                    if ft == 'Any':
                        jobs = job_list.get_job_list()
                    else:
                        for job in job_list.get_job_list():
                            if job.section == ft:
                                jobs.append(job)

                elif lst:
                    jobs_lst = lst.split()

                    if jobs == 'Any':
                        jobs = job_list.get_job_list()
                    else:
                        for job in job_list.get_job_list():
                            if job.name in jobs_lst:
                                jobs.append(job)
                else:
                    jobs = job_list.get_job_list()
        except BaseException as e:
            raise AutosubmitCritical("Issues during the job_list generation. Maybe due I/O error", 7040, str(e))

        referenced_jobs_to_remove = set()
        for job in jobs:
            for child in job.children:
                if child not in jobs:
                    referenced_jobs_to_remove.add(child)
            for parent in job.parents:
                if parent not in jobs:
                    referenced_jobs_to_remove.add(parent)
        if len(referenced_jobs_to_remove) > 0:
            for job in jobs:
                job.children = job.children - referenced_jobs_to_remove
                job.parents = job.parents - referenced_jobs_to_remove
        # WRAPPERS
        try:
            if as_conf.get_wrapper_type() != 'none' and check_wrapper:
                # Class constructor creates table if it does not exist
                packages_persistence = JobPackagePersistence(os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid, "pkl"),
                                                             "job_packages_" + expid)
                # Permissions
                os.chmod(os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid, "pkl", "job_packages_" + expid + ".db"), 0o644)
                # Database modification
                packages_persistence.reset_table(True)
                referenced_jobs_to_remove = set()
                job_list_wrappers = copy.deepcopy(job_list)
                jobs_wr_aux = copy.deepcopy(jobs)
                jobs_wr = []
                [jobs_wr.append(job) for job in jobs_wr_aux]
                for job in jobs_wr:
                    for child in job.children:
                        if child not in jobs_wr:
                            referenced_jobs_to_remove.add(child)
                    for parent in job.parents:
                        if parent not in jobs_wr:
                            referenced_jobs_to_remove.add(parent)

                for job in jobs_wr:
                    job.children = job.children - referenced_jobs_to_remove
                    job.parents = job.parents - referenced_jobs_to_remove

                Autosubmit.generate_scripts_andor_wrappers(as_conf, job_list_wrappers, jobs_wr,
                                                           packages_persistence, True)

                packages = packages_persistence.load(True)
                packages += JobPackagePersistence(os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid, "pkl"),
                                                  "job_packages_" + expid).load()
            else:
                packages = JobPackagePersistence(os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid, "pkl"),
                                                 "job_packages_" + expid).load()
        except BaseException as e:
            raise AutosubmitCritical("Issues during the wrapper loading, may be related to IO issues", 7040, str(e))
        groups_dict = dict()
        try:
            if group_by:
                status = list()
                if expand_status:
                    for s in expand_status.split():
                        status.append(Autosubmit._get_status(s.upper()))

                job_grouping = JobGrouping(group_by, copy.deepcopy(
                    jobs), job_list, expand_list=expand, expanded_status=status)
                groups_dict = job_grouping.group_jobs()
        except BaseException as e:
            raise AutosubmitCritical(
                "Jobs can't be grouped, perhaps you're using an invalid format. Take a look into readthedocs", 7011,
                str(e))

        monitor_exp = Monitor()
        try:
            if txt_only or txt_logfiles or file_format == "txt":
                monitor_exp.generate_output_txt(expid, jobs, os.path.join(
                    exp_path, "/tmp/LOG_" + expid), txt_logfiles, job_list_object=job_list)
                if txt_only:
                    current_length = len(job_list.get_job_list())
                    if current_length > 1000:
                        Log.info(
                            "Experiment has too many jobs to be printed in the terminal. Maximum job quantity is 1000, your experiment has " + str(
                                current_length) + " jobs.")
                    else:
                        Log.info(job_list.print_with_status())
            else:
                # if file_format is set, use file_format, otherwise use conf value
                monitor_exp.generate_output(expid,
                                            jobs,
                                            os.path.join(
                                                exp_path, "/tmp/LOG_", expid),
                                            output_format=file_format if file_format is not None and len(
                                                str(file_format)) > 0 else output_type,
                                            packages=packages,
                                            show=not hide,
                                            groups=groups_dict,
                                            hide_groups=hide_groups,
                                            job_list_object=job_list)
        except BaseException as e:
            raise AutosubmitCritical(
                "An error has occurred while printing the workflow status. Check if you have X11 redirection and an img viewer correctly set",
                7014, str(e))

        return True

    @staticmethod
    def statistics(expid, filter_type, filter_period, file_format, hide, notransitive=False):
        """
        Plots statistics graph for a given experiment.
        Plot is created in experiment's plot folder with name <expid>_<date>_<time>.<file_format>

        :type file_format: str
        :type expid: str
        :param expid: identifier of the experiment to plot
        :param filter_type: type of the jobs to plot
        :param filter_period: period to plot
        :param file_format: plot's file format. It can be pdf, png, ps or svg
        :param hide: hides plot window
        :type hide: bool
        :param notransitive: Reduces workflow linkage complexity
        :type hide: bool

        """
        try:
            Log.info("Loading jobs...")
            as_conf = AutosubmitConfig(expid, BasicConfig, YAMLParserFactory())
            as_conf.check_conf_files(False)

            pkl_dir = os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid, 'pkl')
            job_list = Autosubmit.load_job_list(expid, as_conf, notransitive=notransitive)
            Log.debug("Job list restored from {0} files", pkl_dir)
            jobs = StatisticsUtils.filter_by_section(job_list.get_job_list(), filter_type)
            jobs, period_ini, period_fi = StatisticsUtils.filter_by_time_period(jobs, filter_period)
            # Package information
            job_to_package, package_to_jobs, _, _ = JobList.retrieve_packages(BasicConfig, expid, [job.name for job in
                                                                                                   job_list.get_job_list()])
            queue_time_fixes = {}
            if job_to_package:
                current_table_structure = get_structure(expid, BasicConfig.STRUCTURES_DIR)
                subjobs = []
                for job in job_list.get_job_list():
                    job_info = JobList.retrieve_times(job.status, job.name, job._tmp_path, make_exception=False,
                                                      job_times=None, seconds=True, job_data_collection=None)
                    time_total = (job_info.queue_time + job_info.run_time) if job_info else 0
                    subjobs.append(
                        SubJob(job.name,
                               job_to_package.get(job.name, None),
                               job_info.queue_time if job_info else 0,
                               job_info.run_time if job_info else 0,
                               time_total,
                               job_info.status if job_info else Status.UNKNOWN)
                    )
                queue_time_fixes = SubJobManager(subjobs, job_to_package, package_to_jobs,
                                                 current_table_structure).get_collection_of_fixes_applied()

            if len(jobs) > 0:
                try:
                    Log.info("Plotting stats...")
                    monitor_exp = Monitor()
                    # noinspection PyTypeChecker
                    monitor_exp.generate_output_stats(expid, jobs, file_format, period_ini, period_fi, not hide,
                                                      queue_time_fixes)
                    Log.result("Stats plot ready")
                except Exception as e:
                    raise AutosubmitCritical(
                        "Stats couldn't be shown", 7061, str(e))
            else:
                Log.info("There are no {0} jobs in the period from {1} to {2}...".format(
                    filter_type, period_ini, period_fi))
        except BaseException as e:
            raise AutosubmitCritical("Stats couldn't be generated. Check trace for more details", 7061, str(e))
        return True

    @staticmethod
    def clean(expid, project, plot, stats):
        """
        Clean experiment's directory to save storage space.
        It removes project directory and outdated plots or stats.

        :type plot: bool
        :type project: bool
        :type expid: str
        :type stats: bool
        :param expid: identifier of experiment to clean
        :param project: set True to delete project directory
        :param plot: set True to delete outdated plots
        :param stats: set True to delete outdated stats
        """
        try:
            exp_path = os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid)

            if project:
                autosubmit_config = AutosubmitConfig(
                    expid, BasicConfig, YAMLParserFactory())
                autosubmit_config.check_conf_files(False)

                project_type = autosubmit_config.get_project_type()
                if project_type == "git":
                    Log.info("Registering commit SHA...")
                    autosubmit_config.set_git_project_commit(autosubmit_config)
                    autosubmit_git = AutosubmitGit(expid[0])
                    Log.info("Cleaning GIT directory...")
                    if not autosubmit_git.clean_git(autosubmit_config):
                        return False
                else:
                    Log.info("No project to clean...\n")
            if plot:
                Log.info("Cleaning plots...")
                monitor_autosubmit = Monitor()
                monitor_autosubmit.clean_plot(expid)
            if stats:
                Log.info("Cleaning stats directory...")
                monitor_autosubmit = Monitor()
                monitor_autosubmit.clean_stats(expid)
        except BaseException as e:
            raise AutosubmitCritical("Couldn't clean this experiment, check if you have the correct permissions", 7012,
                                     str(e))
        return True

    @staticmethod
    def recovery(expid, noplot, save, all_jobs, hide, group_by=None, expand=list(), expand_status=list(),
                 notransitive=False, no_recover_logs=False, detail=False, force=False):
        """
        Method to check all active jobs. If COMPLETED file is found, job status will be changed to COMPLETED,
        otherwise it will be set to WAITING. It will also update the jobs list.

        :param detail:
        :param no_recover_logs:
        :param notransitive:
        :param expand_status:
        :param expand:
        :param group_by:
        :param noplot:
        :param expid: identifier of the experiment to recover
        :type expid: str
        :param save: If true, recovery saves changes to the jobs list
        :type save: bool
        :param all_jobs: if True, it tries to get completed files for all jobs, not only active.
        :type all_jobs: bool
        :param hide: hides plot window
        :type hide: bool
        :param force: Allows to restore the workflow even if there are running jobs
        :type force: bool
        """
        try:
            Autosubmit._check_ownership(expid, raise_error=True)

            exp_path = os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid)

            as_conf = AutosubmitConfig(expid, BasicConfig, YAMLParserFactory())
            as_conf.check_conf_files(True)

            Log.info('Recovering experiment {0}'.format(expid))
            pkl_dir = os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid, 'pkl')
            job_list = Autosubmit.load_job_list(
                expid, as_conf, notransitive=notransitive, monitor=True)

            current_active_jobs = job_list.get_in_queue()

            as_conf.check_conf_files(False)

            # Getting output type provided by the user in config, 'pdf' as default
            output_type = as_conf.get_output_type()
            hpcarch = as_conf.get_platform()

            submitter = Autosubmit._get_submitter(as_conf)
            submitter.load_platforms(as_conf)
            if submitter.platforms is None:
                return False
            platforms = submitter.platforms

            platforms_to_test = set()
            if len(current_active_jobs) > 0:
                if force and save:
                    for job in current_active_jobs:
                        if job.platform_name is None:
                            job.platform_name = hpcarch
                        job.platform = submitter.platforms[job.platform_name]
                        platforms_to_test.add(job.platform)
                    for platform in platforms_to_test:
                        platform.test_connection()
                    for job in current_active_jobs:
                        job.platform.send_command(job.platform.cancel_cmd + " " + str(job.id), ignore_log=True)

                if not force:
                    raise AutosubmitCritical(
                        "Experiment can't be recovered due being {0} active jobs in your experiment, If you want to recover the experiment, please use the flag -f and all active jobs will be cancelled".format(
                            len(current_active_jobs)), 7000)
            Log.debug("Job list restored from {0} files", pkl_dir)
        except BaseException as e:
            raise AutosubmitCritical(
                "Couldn't restore the job_list or packages, check if the filesystem is having issues", 7040, str(e))
        Log.info('Recovering experiment {0}'.format(expid))
        try:
            for job in job_list.get_job_list():
                job.submitter = submitter
                if job.platform_name is None:
                    job.platform_name = hpcarch
                # noinspection PyTypeChecker
                job.platform = platforms[job.platform_name]
                # noinspection PyTypeChecker
                platforms_to_test.add(platforms[job.platform_name])
            # establish the connection to all platforms
            Autosubmit.restore_platforms(platforms_to_test)

            if all_jobs:
                jobs_to_recover = job_list.get_job_list()
            else:
                jobs_to_recover = job_list.get_active()
        except BaseException as e:
            raise AutosubmitCritical(
                "Couldn't restore the experiment platform, check if the filesystem is having issues", 7040, str(e))

        Log.info("Looking for COMPLETED files")
        try:
            start = datetime.datetime.now()
            for job in jobs_to_recover:
                if job.platform_name is None:
                    job.platform_name = hpcarch
                # noinspection PyTypeChecker
                job.platform = platforms[job.platform_name]

                if job.platform.get_completed_files(job.name, 0, recovery=True):
                    job.status = Status.COMPLETED
                    Log.info(
                        "CHANGED job '{0}' status to COMPLETED".format(job.name))
                    # Log.status("CHANGED job '{0}' status to COMPLETED".format(job.name))

                    if not no_recover_logs:
                        try:
                            job.platform.get_logs_files(expid, job.remote_logs)
                        except Exception as e:
                            pass
                elif job.status != Status.SUSPENDED:
                    job.status = Status.WAITING
                    job.fail_count = 0
                    # Log.info("CHANGED job '{0}' status to WAITING".format(job.name))
                    # Log.status("CHANGED job '{0}' status to WAITING".format(job.name))

            end = datetime.datetime.now()
            Log.info("Time spent: '{0}'".format(end - start))
            Log.info("Updating the jobs list")
            job_list.update_list(as_conf)

            if save:
                job_list.save()
            else:
                Log.warning(
                    'Changes NOT saved to the jobList. Use -s option to save')

            Log.result("Recovery finalized")
        except BaseException as e:
            raise AutosubmitCritical("Couldn't restore the experiment workflow", 7040, str(e))

        try:
            packages = JobPackagePersistence(os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid, "pkl"),
                                             "job_packages_" + expid).load()

            groups_dict = dict()
            if group_by:
                status = list()
                if expand_status:
                    for s in expand_status.split():
                        status.append(Autosubmit._get_status(s.upper()))

                job_grouping = JobGrouping(group_by, copy.deepcopy(job_list.get_job_list()), job_list,
                                           expand_list=expand,
                                           expanded_status=status)
                groups_dict = job_grouping.group_jobs()

            if not noplot:
                Log.info("\nPlotting the jobs list...")
                monitor_exp = Monitor()
                monitor_exp.generate_output(expid,
                                            job_list.get_job_list(),
                                            os.path.join(
                                                exp_path, "/tmp/LOG_", expid),
                                            output_format=output_type,
                                            packages=packages,
                                            show=not hide,
                                            groups=groups_dict,
                                            job_list_object=job_list)

            if detail is True:
                current_length = len(job_list.get_job_list())
                if current_length > 1000:
                    Log.warning(
                        "-d option: Experiment has too many jobs to be printed in the terminal. Maximum job quantity is 1000, your experiment has " + str(
                            current_length) + " jobs.")
                else:
                    Log.info(job_list.print_with_status())
                    Log.status(job_list.print_with_status())
            # Warnings about precedence completion
            # time_0 = time.time()
            notcompleted_parents_completed_jobs = [job for job in job_list.get_job_list(
            ) if job.status == Status.COMPLETED and len(
                [jobp for jobp in job.parents if jobp.status != Status.COMPLETED]) > 0]

            if notcompleted_parents_completed_jobs and len(notcompleted_parents_completed_jobs) > 0:
                Log.error(
                    "The following COMPLETED jobs depend on jobs that have not been COMPLETED (this can result in unexpected behavior): {0}".format(
                        str([job.name for job in notcompleted_parents_completed_jobs])))
            # print("Warning calc took {0} seconds".format(time.time() - time_0))
        except BaseException as e:
            raise AutosubmitCritical(
                "An error has occurred while printing the workflow status. Check if you have X11 redirection and an img viewer correctly set",
                7000, str(e))

        return True

    @staticmethod
    def migrate(experiment_id, offer, pickup, only_remote):
        """
        Migrates experiment files from current to other user.
        It takes mapping information for new user from config files.

        :param experiment_id: experiment identifier:
        :param pickup:
        :param offer:
        :param only_remote:
        """

        if offer:
            as_conf = AutosubmitConfig(
                experiment_id, BasicConfig, YAMLParserFactory())
            as_conf.check_conf_files(True)
            pkl_dir = os.path.join(
                BasicConfig.LOCAL_ROOT_DIR, experiment_id, 'pkl')
            job_list = Autosubmit.load_job_list(
                experiment_id, as_conf, notransitive=True, monitor=True)
            Log.debug("Job list restored from {0} files", pkl_dir)
            error = False
            platforms_to_test = set()
            submitter = Autosubmit._get_submitter(as_conf)
            submitter.load_platforms(as_conf)
            if submitter.platforms is None:
                raise AutosubmitCritical("No platforms configured!!!", 7014)
            platforms = submitter.platforms
            for job in job_list.get_job_list():
                job.submitter = submitter
                if job.platform_name is None:
                    job.platform_name = as_conf.get_platform()
                platforms_to_test.add(platforms[job.platform_name])
            # establish the connection to all platforms on use
            Autosubmit.restore_platforms(platforms_to_test)
            Log.info('Migrating experiment {0}'.format(experiment_id))
            Autosubmit._check_ownership(experiment_id, raise_error=True)
            if submitter.platforms is None:
                return False
            Log.info("Checking remote platforms")
            platforms = [x for x in submitter.platforms if x not in [
                'local', 'LOCAL']]
            already_moved = set()
            backup_files = []
            backup_conf = []
            error = False
            err_message = 'Invalid Configuration:'
            for platform in platforms:
                # Checks
                Log.info(
                    "Checking [{0}] from platforms configuration...", platform)
                if as_conf.get_migrate_user_to(platform) == '':
                    err_message += "\nInvalid USER_TO target [ USER == USER_TO in [{0}] ]".format(
                        platform)
                    error = True
                elif not as_conf.get_migrate_duplicate(platform) and as_conf.get_migrate_user_to(
                        platform) == as_conf.get_current_user(platform):
                    err_message += "\nInvalid USER_TO target [ USER == USER_TO in ({0}) ] while parameter SAME_USER is false (or unset)".format(
                        platform)
                    error = True
                p = submitter.platforms[platform]
                if p.temp_dir is None:
                    err_message += "\nInvalid TEMP_DIR, Parameter must be present even if empty in [{0}]".format(
                        platform)
                    error = True
                elif p.temp_dir != "":
                    if not p.check_tmp_exists():
                        err_message += "\nTEMP_DIR {0}, does not exists in [{1}]".format(
                            p.temp_dir, platform)
                        error = True
                if error:
                    raise AutosubmitCritical(err_message, 7014)
            for platform in platforms:
                if as_conf.get_migrate_project_to(platform) != '':
                    Log.info("Project in platform configuration file successfully updated to {0}",
                             as_conf.get_current_project(platform))
                    as_conf.get_current_project(platform)
                    backup_conf.append([platform, as_conf.get_current_user(
                        platform), as_conf.get_current_project(platform)])
                    as_conf.set_new_user(
                        platform, as_conf.get_migrate_user_to(platform))

                    as_conf.set_new_project(
                        platform, as_conf.get_migrate_project_to(platform))
                    as_conf.get_current_project(platform)
                    as_conf.get_current_user(platform)
                else:
                    Log.result(
                        "[OPTIONAL] PROJECT_TO directive not found. The directive PROJECT will remain unchanged")
                    backup_conf.append(
                        [platform, as_conf.get_current_user(platform), None])
                    as_conf.set_new_user(
                        platform, as_conf.get_migrate_user_to(platform))
                    as_conf.get_current_project(platform)
                    as_conf.get_current_user(platform)

                if as_conf.get_migrate_host_to(platform) != "none" and len(as_conf.get_migrate_host_to(platform)) > 0:
                    Log.result(
                        "Host in platform configuration file successfully updated to {0}",
                        as_conf.get_migrate_host_to(platform))
                    as_conf.set_new_host(
                        platform, as_conf.get_migrate_host_to(platform))
                else:
                    Log.result(
                        "[OPTIONAL] HOST_TO directive not found. The directive HOST will remain unchanged")
                p = submitter.platforms[platform]
                if p.temp_dir not in already_moved:
                    if p.root_dir != p.temp_dir and len(p.temp_dir) > 0:
                        already_moved.add(p.temp_dir)
                        # find /home/bsc32/bsc32070/dummy3 -type l -lname '/*' -printf ' ln -sf "$(realpath -s --relative-to="%p" $(readlink "%p")")" \n' > script.sh
                        # command = "find " + p.root_dir + " -type l -lname \'/*\' -printf 'var=\"$(realpath -s --relative-to=\"%p\" \"$(readlink \"%p\")\")\" && var=${var:3} && ln -sf $var \"%p\"  \\n'"
                        Log.info(
                            "Converting the absolute symlinks into relatives on platform {0} ", platform)
                        command = "find " + p.root_dir + \
                                  " -type l -lname \'/*\' -printf 'var=\"$(realpath -s --relative-to=\"%p\" \"$(readlink \"%p\")\")\" && var=${var:3} && ln -sf $var \"%p\"  \\n' "
                        try:
                            p.send_command(command, True)
                            if p.get_ssh_output().startswith("var="):
                                convertLinkPath = os.path.join(
                                    BasicConfig.LOCAL_ROOT_DIR, experiment_id, BasicConfig.LOCAL_TMP_DIR,
                                    'convertLink.sh')
                                with open(convertLinkPath, 'w') as convertLinkFile:
                                    convertLinkFile.write(p.get_ssh_output())
                                p.send_file("convertLink.sh")
                                convertLinkPathRemote = os.path.join(
                                    p.remote_log_dir, "convertLink.sh")
                                command = "chmod +x " + convertLinkPathRemote + " && " + \
                                          convertLinkPathRemote + " && rm " + convertLinkPathRemote
                                p.send_command(command, True)
                            else:
                                Log.result("No links found in {0} for [{1}] ".format(
                                    p.root_dir, platform))

                        except IOError:
                            Log.debug(
                                "The platform {0} does not contain absolute symlinks", platform)
                        except BaseException:
                            Log.printlog(
                                "Absolute symlinks failed to convert, check user in platform.yml", 3000)
                            error = True
                            break
                        try:
                            Log.info(
                                "Moving remote files/dirs on {0}", platform)
                            p.send_command("chmod 777 -R " + p.root_dir)
                            if not p.move_file(p.root_dir, os.path.join(p.temp_dir, experiment_id), False):
                                Log.result("No data found in {0} for [{1}]\n".format(
                                    p.root_dir, platform))
                        except IOError as e:
                            Log.printlog("The files/dirs on {0} cannot be moved to {1}.".format(p.root_dir,
                                                                                                os.path.join(p.temp_dir,
                                                                                                             experiment_id),
                                                                                                6012))
                            error = True
                            break
                        except Exception as e:
                            Log.printlog("Trace: {2}\nThe files/dirs on {0} cannot be moved to {1}.".format(
                                p.root_dir, os.path.join(p.temp_dir, experiment_id), str(e)), 6012)
                            error = True
                            break
                        backup_files.append(platform)
                Log.result(
                    "Files/dirs on {0} have been successfully offered", platform)
            if error:
                as_conf = AutosubmitConfig(
                    experiment_id, BasicConfig, YAMLParserFactory())
                as_conf.check_conf_files(False)
                for platform in backup_files:
                    p = submitter.platforms[platform]
                    p.move_file(os.path.join(
                        p.temp_dir, experiment_id), p.root_dir, True)
                for platform in backup_conf:
                    as_conf.set_new_user(platform[0], platform[1])
                    if platform[2] is not None and len(str(platform[2])) > 0:
                        as_conf.set_new_project(platform[0], platform[2])
                    if as_conf.get_migrate_host_to(platform[0]) != "none" and len(
                            as_conf.get_migrate_host_to(platform[0])) > 0:
                        as_conf.set_new_host(
                            platform[0], as_conf.get_migrate_host_to(platform[0]))
                raise AutosubmitCritical(
                    "The experiment cannot be offered, changes are reverted", 7014)
            else:
                try:
                    if not only_remote:
                        if not Autosubmit.archive(experiment_id, True, True):
                            for platform in backup_files:
                                p = submitter.platforms[platform]
                                p.move_file(os.path.join(
                                    p.temp_dir, experiment_id), p.root_dir, True)
                            for platform in backup_conf:
                                as_conf.set_new_user(platform[0], platform[1])
                                if platform[2] is not None and len(str(platform[2])) > 0:
                                    as_conf.set_new_project(
                                        platform[0], platform[2])
                            raise AutosubmitCritical(
                                "The experiment cannot be offered, changes are reverted", 7014)
                    Log.result("The experiment has been successfully offered.")
                except Exception as e:
                    for platform in backup_files:
                        p = submitter.platforms[platform]
                        p.move_file(os.path.join(
                            p.temp_dir, experiment_id), p.root_dir, True)
                    for platform in backup_conf:
                        as_conf.set_new_user(platform[0], platform[1])
                        if platform[2] is not None and len(str(platform[2])) > 0:
                            as_conf.set_new_project(platform[0], platform[2])
                    raise AutosubmitCritical(
                        "The experiment cannot be offered, changes are reverted", 7014, str(e))
        elif pickup:
            Log.info('Migrating experiment {0}'.format(experiment_id))
            Log.info("Moving local files/dirs")
            if not only_remote:
                if not Autosubmit.unarchive(experiment_id, True):
                    raise AutosubmitCritical(
                        "The experiment cannot be picked up", 7012)
                Log.info("Local files/dirs have been successfully picked up")
            else:
                exp_path = os.path.join(
                    BasicConfig.LOCAL_ROOT_DIR, experiment_id)
                if not os.path.exists(exp_path):
                    raise AutosubmitCritical(
                        "Experiment seems to be archived, no action is performed", 7012)

            as_conf = AutosubmitConfig(
                experiment_id, BasicConfig, YAMLParserFactory())
            as_conf.check_conf_files(False)
            pkl_dir = os.path.join(
                BasicConfig.LOCAL_ROOT_DIR, experiment_id, 'pkl')
            job_list = Autosubmit.load_job_list(
                experiment_id, as_conf, notransitive=True, monitor=True)
            Log.debug("Job list restored from {0} files", pkl_dir)
            error = False
            platforms_to_test = set()
            submitter = Autosubmit._get_submitter(as_conf)
            submitter.load_platforms(as_conf)
            if submitter.platforms is None:
                raise AutosubmitCritical("No platforms configured!!!", 7014)
            platforms = submitter.platforms
            for job in job_list.get_job_list():
                job.submitter = submitter
                if job.platform_name is None:
                    job.platform_name = as_conf.get_platform()
                platforms_to_test.add(platforms[job.platform_name])

            Log.info("Checking remote platforms")
            platforms = [x for x in submitter.platforms if x not in [
                'local', 'LOCAL']]
            already_moved = set()
            backup_files = []
            # establish the connection to all platforms on use
            try:
                Autosubmit.restore_platforms(platforms_to_test)
            except AutosubmitCritical as e:
                raise AutosubmitCritical(
                    e.message + "\nInvalid Remote Platform configuration, recover them manually or:\n 1) Configure platform.yml with the correct info\n 2) autosubmit expid -p --onlyremote",
                    7014, e.trace)
            except Exception as e:
                raise AutosubmitCritical(
                    "Invalid Remote Platform configuration, recover them manually or:\n 1) Configure platform.yml with the correct info\n 2) autosubmit expid -p --onlyremote",
                    7014, str(e))
            for platform in platforms:
                p = submitter.platforms[platform]
                if p.temp_dir is not None and p.temp_dir not in already_moved:
                    if p.root_dir != p.temp_dir and len(p.temp_dir) > 0:
                        already_moved.add(p.temp_dir)
                        Log.info(
                            "Copying remote files/dirs on {0}", platform)
                        Log.info("Copying from {0} to {1}", os.path.join(
                            p.temp_dir, experiment_id), p.root_dir)
                        finished = False
                        limit = 150
                        rsync_retries = 0
                        try:
                            # Avoid infinite loop unrealistic upper limit, only for rsync failure
                            while not finished and rsync_retries < limit:
                                finished = False
                                pipeline_broke = False
                                Log.info(
                                    "Rsync launched {0} times. Can take up to 150 retrials or until all data is transferred".format(
                                        rsync_retries + 1))
                                try:
                                    p.send_command(
                                        "rsync --timeout=3600 --bwlimit=20000 -aq --remove-source-files " + os.path.join(
                                            p.temp_dir, experiment_id) + " " + p.root_dir[:-5])
                                except BaseException as e:
                                    Log.debug("{0}".format(str(e)))
                                    rsync_retries += 1
                                    try:
                                        if p.get_ssh_output_err() == "":
                                            finished = True
                                        elif p.get_ssh_output_err().lower().find("no such file or directory") == -1:
                                            finished = True
                                        else:
                                            finished = False
                                    except Exception as e:
                                        finished = False
                                    pipeline_broke = True
                                if not pipeline_broke:
                                    if p.get_ssh_output_err().lower().find("no such file or directory") == -1:
                                        finished = True
                                    elif p.get_ssh_output_err().lower().find(
                                        "warning: rsync") != -1 or p.get_ssh_output_err().lower().find(
                                        "closed") != -1 or p.get_ssh_output_err().lower().find(
                                        "broken pipe") != -1 or p.get_ssh_output_err().lower().find(
                                        "directory has vanished") != -1:
                                        rsync_retries += 1
                                        finished = False
                                    elif p.get_ssh_output_err() == "":
                                        finished = True
                                    else:
                                        error = True
                                        finished = False
                                        break
                                p.send_command(
                                    "find {0} -depth -type d -empty -delete".format(
                                        os.path.join(p.temp_dir, experiment_id)))
                                Log.result(
                                    "Empty dirs on {0} have been successfully deleted".format(p.temp_dir))
                            if finished:
                                p.send_command("chmod 755 -R " + p.root_dir)
                                Log.result(
                                    "Files/dirs on {0} have been successfully picked up", platform)
                                # p.send_command(
                                #    "find {0} -depth -type d -empty -delete".format(os.path.join(p.temp_dir, experiment_id)))
                                Log.result(
                                    "Empty dirs on {0} have been successfully deleted".format(p.temp_dir))
                            else:
                                Log.printlog("The files/dirs on {0} cannot be copied to {1}.".format(
                                    os.path.join(p.temp_dir, experiment_id), p.root_dir), 6012)
                                error = True
                                break

                        except IOError as e:
                            raise AutosubmitError(
                                "I/O Issues", 6016, e.message)
                        except BaseException as e:
                            error = True
                            Log.printlog("The files/dirs on {0} cannot be copied to {1}.\nTRACE:{2}".format(
                                os.path.join(p.temp_dir, experiment_id), p.root_dir, str(e)), 6012)
                            break
                    else:
                        Log.result(
                            "Files/dirs on {0} have been successfully picked up", platform)
            if error:
                raise AutosubmitCritical(
                    "Unable to pickup all platforms, the non-moved files are on the TEMP_DIR\n You can try again with autosubmit {0} -p --onlyremote".format(
                        experiment_id), 7012)
            else:
                Log.result("The experiment has been successfully picked up.")
                return True

    @staticmethod
    def check(experiment_id, notransitive=False):
        """
        Checks experiment configuration and warns about any detected error or inconsistency.

        :param notransitive:
        :param experiment_id: experiment identifier:
        :type experiment_id: str
        """
        try:
            exp_path = os.path.join(BasicConfig.LOCAL_ROOT_DIR, experiment_id)

            as_conf = AutosubmitConfig(
                experiment_id, BasicConfig, YAMLParserFactory())
            as_conf.check_conf_files(False)

            project_type = as_conf.get_project_type()

            submitter = Autosubmit._get_submitter(as_conf)
            submitter.load_platforms(as_conf)
            if len(submitter.platforms) == 0:
                return False

            pkl_dir = os.path.join(
                BasicConfig.LOCAL_ROOT_DIR, experiment_id, 'pkl')
            job_list = Autosubmit.load_job_list(
                experiment_id, as_conf, notransitive=notransitive)
            Log.debug("Job list restored from {0} files", pkl_dir)

            Autosubmit._load_parameters(as_conf, job_list, submitter.platforms)

            hpc_architecture = as_conf.get_platform()
            for job in job_list.get_job_list():
                if job.platform_name is None:
                    job.platform_name = hpc_architecture
                job.platform = submitter.platforms[job.platform_name]
                job.update_parameters(as_conf, job_list.parameters)
        except AutosubmitError:
            raise
        except BaseException as e:
            raise AutosubmitCritical("Checking incomplete due an unknown error. Please check the trace", 7070, str(e))

        return job_list.check_scripts(as_conf)

    @staticmethod
    def capitalize_keys(dictionary):
        upper_dictionary = defaultdict()
        for key in list(dictionary.keys()):
            upper_key = key.upper()
            upper_dictionary[upper_key] = dictionary[key]
        return upper_dictionary

    @staticmethod
    def report(expid, template_file_path="", show_all_parameters=False, folder_path="", placeholders=False):
        """
        Show report for specified experiment
        :param expid: experiment identifier
        :type expid: str
        :param template_file_path: path to template file
        :type template_file_path: str
        :param show_all_parameters: show all parameters
        :type show_all_parameters: bool
        :param folder_path: path to folder
        :type folder_path: str
        :param placeholders: show placeholders
        :type placeholders: bool
        """
        # todo
        try:
            exp_parameters = defaultdict()
            performance_metrics = None
            ignore_performance_keys = ["error_message",
                                       "warnings_job_data", "considered"]
            exp_path = os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid)
            tmp_path = os.path.join(exp_path, BasicConfig.LOCAL_TMP_DIR)
            if folder_path is not None and len(str(folder_path)) > 0:
                tmp_path = folder_path
            import platform
            host = platform.node()
            # Gather experiment info
            as_conf = AutosubmitConfig(expid, BasicConfig, YAMLParserFactory())
            try:
                as_conf.check_conf_files(False)
            except Exception as e:
                raise AutosubmitCritical(
                    "Unable to gather the parameters from config files, check permissions.", 7012)
            # Performance Metrics call
            try:
                BasicConfig.read()
                request = requests.get(
                    "{0}/performance/{1}".format(BasicConfig.AUTOSUBMIT_API_URL, expid))
                performance_metrics = json.loads(request.text)
                # If error, then None
                performance_metrics = None if performance_metrics and performance_metrics[
                    "error"] is True else performance_metrics
                if performance_metrics:
                    for key in ignore_performance_keys:
                        performance_metrics.pop(key, None)
            except Exception as e:
                Log.printlog("Autosubmit couldn't retrieve performance metrics.")
                performance_metrics = None
            # Preparation for section parameters
            no_load_sections = False
            no_load_platforms = False

            try:
                submitter = Autosubmit._get_submitter(as_conf)
                submitter.load_platforms(as_conf)
                hpcarch = submitter.platforms[as_conf.get_platform()]

            except Exception as e:
                no_load_platforms = True
                submitter = Autosubmit._get_submitter(as_conf)
                submitter.load_local_platform(as_conf)
                hpcarch = submitter.platforms[as_conf.get_platform()]

            job_list = Autosubmit.load_job_list(
                expid, as_conf, notransitive=False)
            for job in job_list.get_job_list():
                if job.platform_name is None or job.platform_name == "":
                    job.platform_name = hpcarch.name
                job.platform = submitter.platforms[job.platform_name]

            try:
                # Gathering parameters of autosubmit and expdef config files
                as_conf.reload(True)
                exp_parameters = as_conf.load_parameters()
                try:
                    for job in job_list.get_job_list():
                        exp_parameters.update(job.update_parameters(as_conf, job_list.parameters))
                except:
                    pass
            except Exception as e:
                raise AutosubmitCritical(
                    "Couldn't gather the experiment parameters", 7012, str(e))

            if show_all_parameters:
                Log.info("Gathering all parameters (all keys are on upper_case)")
                parameter_output = '{0}_parameter_list_{1}.txt'.format(expid,
                                                                       datetime.datetime.today().strftime(
                                                                           '%Y%m%d-%H%M%S'))

                parameter_file = open(os.path.join(
                    tmp_path, parameter_output), 'w')
                for key, value in exp_parameters.items():
                    if value is not None and len(str(value)) > 0:
                        full_value = key + "=" + str(value) + "\n"
                        parameter_file.write(full_value)
                    else:
                        if placeholders:
                            parameter_file.write(
                                key + "=" + "%" + key + "%" + "\n")
                        else:
                            parameter_file.write(key + "=" + "-" + "\n")

                if performance_metrics is not None and len(str(performance_metrics)) > 0:
                    for key in performance_metrics:
                        parameter_file.write("{0} = {1}\n".format(
                            key, performance_metrics.get(key, "-")))
                parameter_file.close()

                os.chmod(os.path.join(tmp_path, parameter_output), 0o755)
                Log.result("A list of all parameters has been written on {0}".format(
                    os.path.join(tmp_path, parameter_output)))

            if template_file_path is not None and len(str(template_file_path)) > 0:
                if os.path.exists(template_file_path):
                    Log.info(
                        "Gathering the selected parameters (all keys are on upper_case)")
                    template_file = open(template_file_path, 'rb')
                    template_content = template_file.read()
                    for key, value in exp_parameters.items():
                        template_content = re.sub(
                            '%(?<!%%)' + key + '%(?!%%)', str(exp_parameters[key]), template_content, flags=re.I)
                    # Performance metrics
                    if performance_metrics is not None and len(str(performance_metrics)) > 0:
                        for key in performance_metrics:
                            template_content = re.sub(
                                '%(?<!%%)' + key + '%(?!%%)', str(performance_metrics[key]), template_content,
                                flags=re.I)
                    template_content = template_content.replace("%%", "%")
                    if not placeholders:
                        template_content = re.sub(
                            r"%[^% \n\t]+%", "-", template_content, flags=re.I)
                    report = '{0}_report_{1}.txt'.format(
                        expid, datetime.datetime.today().strftime('%Y%m%d-%H%M%S'))
                    open(os.path.join(tmp_path, report),
                         'wb').write(template_content)
                    os.chmod(os.path.join(tmp_path, report), 0o755)
                    template_file.close()
                    Log.result("Report {0} has been created on {1}".format(
                        report, os.path.join(tmp_path, report)))
                else:
                    raise AutosubmitCritical(
                        "Template {0} doesn't exists ".format(template_file_path), 7014)
        except AutosubmitError as e:
            raise
        except AutosubmitCritical as e:
            raise
        except BaseException as e:
            raise AutosubmitCritical("Unknown error while reporting the parameters list, likely it is due IO issues",
                                     7040, str(e))

    @staticmethod
    def describe(input_experiment_list="*",get_from_user=""):
        """
        Show details for specified experiment

        :param experiments_id: experiments identifier:
        :type experiments_id: str
        :param get_from_user: user to get the experiments from
        :type get_from_user: str
        :return: str,str,str,str
        """
        experiments_ids = input_experiment_list
        not_described_experiments = []
        if get_from_user == "*" or get_from_user == "":
            get_from_user = pwd.getpwuid(os.getuid())[0]
        user =""
        created=""
        model=""
        branch=""
        hpc=""
        if ',' in experiments_ids:
            experiments_ids = experiments_ids.split(',')
        elif '*' in experiments_ids:
            experiments_ids = []
            basic_conf = BasicConfig()
            for f in Path(basic_conf.LOCAL_ROOT_DIR).glob("????"):
                if f.is_dir() and f.owner() == get_from_user:
                    experiments_ids.append(f.name)
        else:
            experiments_ids = experiments_ids.split(' ')
        for experiment_id in experiments_ids:
            try:
                experiment_id = experiment_id.strip(" ")
                exp_path = os.path.join(BasicConfig.LOCAL_ROOT_DIR, experiment_id)

                as_conf = AutosubmitConfig(
                    experiment_id, BasicConfig, YAMLParserFactory())
                as_conf.check_conf_files(False,no_log=True)
                user = os.stat(as_conf.experiment_file).st_uid
                try:
                    user = pwd.getpwuid(user).pw_name
                except Exception as e:
                    Log.warning(
                        "The user does not exist anymore in the system, using id instead")

                created = datetime.datetime.fromtimestamp(
                    os.path.getmtime(as_conf.experiment_file))

                project_type = as_conf.get_project_type()
                if as_conf.get_svn_project_url():
                    model = as_conf.get_svn_project_url()
                    branch = as_conf.get_svn_project_url()
                else:
                    model = as_conf.get_git_project_origin()
                    branch = as_conf.get_git_project_branch()
                if model == "":
                    model = "Not Found"
                if branch == "":
                    branch = "Not Found"

                submitter = Autosubmit._get_submitter(as_conf)
                submitter.load_platforms(as_conf)
                if len(submitter.platforms) == 0:
                    return False
                hpc = as_conf.get_platform()
                description = get_experiment_descrip(experiment_id)
                Log.info("Describing {0}", experiment_id)

                Log.result("Owner: {0}", user)
                Log.result("Created: {0}", created)
                Log.result("Model: {0}", model)
                Log.result("Branch: {0}", branch)
                Log.result("HPC: {0}", hpc)
                Log.result("Description: {0}", description[0][0])
            except BaseException as e:
                not_described_experiments.append(experiment_id)
        if len(not_described_experiments) > 0:
            Log.printlog("Could not describe the following experiments:\n{0}".format(not_described_experiments),Log.WARNING)
        if len(experiments_ids) == 1:
            # for backward compatibility or GUI
            return user, created, model, branch, hpc
        elif len(experiments_ids) == 0:
            Log.result("No experiments found for expid={0} and user {1}".format(input_experiment_list,get_from_user))

    @staticmethod
    def configure(advanced, database_path, database_filename, local_root_path, platforms_conf_path, jobs_conf_path,
                  smtp_hostname, mail_from, machine, local):
        """
        Configure several paths for autosubmit: database, local root and others. Can be configured at system,
        user or local levels. Local level configuration precedes user level and user level precedes system
        configuration.

        :param advanced:
        :param database_path: path to autosubmit database
        :type database_path: str
        :param database_filename: database filename
        :type database_filename: str
        :param local_root_path: path to autosubmit's experiments' directory
        :type local_root_path: str
        :param platforms_conf_path: path to platforms conf file to be used as model for new experiments
        :type platforms_conf_path: str
        :param jobs_conf_path: path to jobs conf file to be used as model for new experiments
        :type jobs_conf_path: str
        :param machine: True if this configuration has to be stored for all the machine users
        :type machine: bool
        :param local: True if this configuration has to be stored in the local path
        :type local: bool
        :param mail_from:
        :type mail_from: str
        :param smtp_hostname:
        :type smtp_hostname: str
        """
        try:
            home_path = os.path.expanduser('~')
            autosubmitapi_url = "http://192.168.11.91:8081" + " # Replace me?"
            # Setting default values
            if not advanced and database_path is None and local_root_path is None:
                database_path = os.path.join(home_path, "autosubmit")
                local_root_path = os.path.join(home_path, "autosubmit")
                global_logs_path = os.path.join(home_path, "autosubmit", "logs")
                structures_path = os.path.join(home_path, "autosubmit", "metadata", "structures")
                historicdb_path = os.path.join(home_path, "autosubmit", "metadata", "data")
                historiclog_path = os.path.join(home_path, "autosubmit", "metadata", "logs")
                database_filename = "autosubmit.db"

            while database_path is None:
                database_path = input("Introduce Database path: ")
                if database_path.find("~/") < 0:
                    database_path = None
                    Log.error("Not a valid path. You must include '~/' at the beginning.")
            database_path = database_path.replace('~', home_path)
            # if not os.path.exists(database_path):
            HUtils.create_path_if_not_exists(database_path)
            # Log.error("Database path does not exist.")
            # return False
            while database_filename is None:
                database_filename = input("Introduce Database name: ")

            while local_root_path is None:
                local_root_path = input("Introduce path to experiments: ")
                if local_root_path.find("~/") < 0:
                    local_root_path = None
                    Log.error("Not a valid path. You must include '~/' at the beginning.")
            local_root_path = local_root_path.replace('~', home_path)

            # if not os.path.exists(local_root_path):
            HUtils.create_path_if_not_exists(local_root_path)
            # Log.error("Local Root path does not exist.")
            # return False
            # else:
            global_logs_path = os.path.join(local_root_path, "logs")
            structures_path = os.path.join(local_root_path, "metadata", "structures")
            historicdb_path = os.path.join(local_root_path, "metadata", "data")
            historiclog_path = os.path.join(local_root_path, "metadata", "logs")

            if platforms_conf_path is not None and len(str(platforms_conf_path)) > 0:
                platforms_conf_path = platforms_conf_path.replace('~', home_path)
                if not os.path.exists(platforms_conf_path):
                    Log.error("platforms.yml path does not exist.")
                    return False
            if jobs_conf_path is not None and len(str(jobs_conf_path)) > 0:
                jobs_conf_path = jobs_conf_path.replace('~', home_path)
                if not os.path.exists(jobs_conf_path):
                    Log.error("jobs.yml path does not exist.")
                    return False

            if machine:
                rc_path = '/etc'
            elif local:
                rc_path = '.'
            else:
                rc_path = home_path
            rc_path = os.path.join(rc_path, '.autosubmitrc')

            config_file = open(rc_path, 'w')
            Log.info("Writing configuration file...")
            try:
                parser = SafeConfigParser()
                parser.add_section('database')
                parser.set('database', 'path', database_path)
                if database_filename is not None and len(str(database_filename)) > 0:
                    parser.set('database', 'filename', database_filename)
                parser.add_section('local')
                parser.set('local', 'path', local_root_path)
                if (jobs_conf_path is not None and len(str(jobs_conf_path)) > 0) or (
                        platforms_conf_path is not None and len(str(platforms_conf_path)) > 0):
                    parser.add_section('conf')
                    if jobs_conf_path is not None:
                        parser.set('conf', 'jobs', jobs_conf_path)
                    if platforms_conf_path is not None:
                        parser.set('conf', 'platforms', platforms_conf_path)
                if smtp_hostname is not None or mail_from is not None:
                    parser.add_section('mail')
                    parser.set('mail', 'smtp_server', smtp_hostname)
                    parser.set('mail', 'mail_from', mail_from)
                parser.add_section("globallogs")
                parser.set("globallogs", "path", global_logs_path)
                parser.add_section("structures")
                parser.set("structures", "path", structures_path)
                parser.add_section("historicdb")
                parser.set("historicdb", "path", historicdb_path)
                parser.add_section("historiclog")
                parser.set("historiclog", "path", historiclog_path)
                parser.add_section("autosubmitapi")
                parser.set("autosubmitapi", "url", autosubmitapi_url)
                # parser.add_section("hosts")
                # parser.set("hosts", "whitelist", " localhost # Add your machine names")
                parser.write(config_file)
                config_file.close()
                Log.result("Configuration file written successfully: \n\t{0}".format(rc_path))
                HUtils.create_path_if_not_exists(local_root_path)
                HUtils.create_path_if_not_exists(global_logs_path)
                HUtils.create_path_if_not_exists(structures_path)
                HUtils.create_path_if_not_exists(historicdb_path)
                HUtils.create_path_if_not_exists(historiclog_path)
                Log.result(
                    "Directories configured successfully: \n\t{5} \n\t{0} \n\t{1} \n\t{2} \n\t{3} \n\t{4}".format(
                        local_root_path,
                        global_logs_path,
                        structures_path,
                        historicdb_path,
                        historiclog_path,
                        database_path
                    ))
            except (IOError, OSError) as e:
                raise AutosubmitCritical(
                    "Can not write config file: {0}", 7012, e.message)
        except (AutosubmitCritical, AutosubmitError) as e:
            raise
        except BaseException as e:
            raise AutosubmitCritical(str(e), 7014)
        return True

    @staticmethod
    def configure_dialog():
        """
        Configure several paths for autosubmit interactively: database, local root and others.
        Can be configured at system, user or local levels. Local level configuration precedes user level and user level
        precedes system configuration.
        """

        not_enough_screen_size_msg = 'The size of your terminal is not enough to draw the configuration wizard,\n' \
                                     'so we\'ve closed it to prevent errors. Resize it and then try it again.'

        home_path = os.path.expanduser('~')

        try:
            d = dialog.Dialog(
                dialog="dialog", autowidgetsize=True, screen_color='GREEN')
        except dialog.DialogError:
            raise AutosubmitCritical(
                "Graphical visualization failed, not enough screen size", 7060)
        except Exception:
            raise AutosubmitCritical(
                "Dialog libs aren't found in your Operational system", 7060)

        d.set_background_title("Autosubmit configure utility")
        if os.geteuid() == 0:
            text = ''
            choice = [
                ("All", "All users on this machine (may require root privileges)")]
        else:
            text = "If you want to configure Autosubmit for all users, you will need to provide root privileges"
            choice = []

        choice.append(("User", "Current user"))
        choice.append(
            ("Local", "Only when launching Autosubmit from this path"))

        try:
            code, level = d.menu(text, choices=choice, width=60,
                                 title="Choose when to apply the configuration")
            if code != dialog.Dialog.OK:
                os.system('clear')
                return False
        except dialog.DialogError:
            raise AutosubmitCritical(
                "Graphical visualization failed, not enough screen size", 7060)

        filename = '.autosubmitrc'
        if level == 'All':
            path = '/etc'
            filename = 'autosubmitrc'
        elif level == 'User':
            path = home_path
        else:
            path = '.'
        path = os.path.join(path, filename)

        # Setting default values
        database_path = home_path
        local_root_path = home_path
        database_filename = 'autosubmit.db'
        jobs_conf_path = ''
        platforms_conf_path = ''

        d.infobox("Reading configuration file...", width=50, height=5)
        try:
            if os.path.isfile(path):
                parser = SafeConfigParser()
                parser.optionxform = str
                parser.load(path)
                if parser.has_option('database', 'path'):
                    database_path = parser.get('database', 'path')
                if parser.has_option('database', 'filename'):
                    database_filename = parser.get('database', 'filename')
                if parser.has_option('local', 'path'):
                    local_root_path = parser.get('local', 'path')
                if parser.has_option('conf', 'platforms'):
                    platforms_conf_path = parser.get('conf', 'platforms')
                if parser.has_option('conf', 'jobs'):
                    jobs_conf_path = parser.get('conf', 'jobs')

        except (IOError, OSError) as e:
            raise AutosubmitCritical(
                "Can not read config file", 7014, e.message)

        while True:
            try:
                code, database_path = d.dselect(database_path, width=80, height=20,
                                                title='\Zb\Z1Select path to database\Zn', colors='enable')
            except dialog.DialogError:
                raise AutosubmitCritical(
                    "Graphical visualization failed, not enough screen size", 7060)
            if Autosubmit._requested_exit(code, d):
                raise AutosubmitCritical(
                    "Graphical visualization failed, requested exit", 7060)
            elif code == dialog.Dialog.OK:
                database_path = database_path.replace('~', home_path)
                if not os.path.exists(database_path):
                    d.msgbox(
                        "Database path does not exist.\nPlease, insert the right path", width=50, height=6)
                else:
                    break

        while True:
            try:
                code, local_root_path = d.dselect(local_root_path, width=80, height=20,
                                                  title='\Zb\Z1Select path to experiments repository\Zn',
                                                  colors='enable')
            except dialog.DialogError:
                raise AutosubmitCritical(
                    "Graphical visualization failed, not enough screen size", 7060)

            if Autosubmit._requested_exit(code, d):
                raise AutosubmitCritical(
                    "Graphical visualization failed,requested exit", 7060)
            elif code == dialog.Dialog.OK:
                database_path = database_path.replace('~', home_path)
                if not os.path.exists(database_path):
                    d.msgbox(
                        "Local root path does not exist.\nPlease, insert the right path", width=50, height=6)
                else:
                    break
        while True:
            try:
                (code, tag) = d.form(text="",
                                     elements=[("Database filename", 1, 1, database_filename, 1, 40, 20, 20),
                                               (
                                                   "Default platform.yml path", 2, 1, platforms_conf_path, 2, 40, 40,
                                                   200),
                                               ("Default jobs.yml path", 3, 1, jobs_conf_path, 3, 40, 40, 200)],
                                     height=20,
                                     width=80,
                                     form_height=10,
                                     title='\Zb\Z1Just a few more options:\Zn', colors='enable')
            except dialog.DialogError:
                raise AutosubmitCritical(
                    "Graphical visualization failed, not enough screen size", 7060)

            if Autosubmit._requested_exit(code, d):
                raise AutosubmitCritical(
                    "Graphical visualization failed, _requested_exit", 7060)
            elif code == dialog.Dialog.OK:
                database_filename = tag[0]
                platforms_conf_path = tag[1]
                jobs_conf_path = tag[2]

                platforms_conf_path = platforms_conf_path.replace(
                    '~', home_path).strip()
                jobs_conf_path = jobs_conf_path.replace('~', home_path).strip()

                if platforms_conf_path and not os.path.exists(platforms_conf_path):
                    d.msgbox(
                        "Platforms conf path does not exist.\nPlease, insert the right path", width=50, height=6)
                elif jobs_conf_path and not os.path.exists(jobs_conf_path):
                    d.msgbox(
                        "Jobs conf path does not exist.\nPlease, insert the right path", width=50, height=6)
                else:
                    break

        smtp_hostname = "mail.bsc.es"
        mail_from = "automail@bsc.es"
        while True:
            try:
                (code, tag) = d.form(text="",
                                     elements=[("SMTP server hostname", 1, 1, smtp_hostname, 1, 40, 20, 20),
                                               ("Notifications sender address", 2, 1, mail_from, 2, 40, 40, 200)],
                                     height=20,
                                     width=80,
                                     form_height=10,
                                     title='\Zb\Z1Mail notifications configuration:\Zn', colors='enable')
            except dialog.DialogError:
                raise AutosubmitCritical(
                    "Graphical visualization failed, not enough screen size", 7060)

            if Autosubmit._requested_exit(code, d):
                raise AutosubmitCritical(
                    "Graphical visualization failed, requested exit", 7060)
            elif code == dialog.Dialog.OK:
                smtp_hostname = tag[0]
                mail_from = tag[1]
                break
                # TODO: Check that is a valid config?

        config_file = open(path, 'w')
        d.infobox("Writing configuration file...", width=50, height=5)
        try:
            parser = SafeConfigParser()
            parser.add_section('database')
            parser.set('database', 'path', database_path)
            if database_filename:
                parser.set('database', 'filename', database_filename)
            parser.add_section('local')
            parser.set('local', 'path', local_root_path)
            if jobs_conf_path or platforms_conf_path:
                parser.add_section('conf')
                if jobs_conf_path:
                    parser.set('conf', 'jobs', jobs_conf_path)
                if platforms_conf_path:
                    parser.set('conf', 'platforms', platforms_conf_path)
            parser.add_section('mail')
            parser.set('mail', 'smtp_server', smtp_hostname)
            parser.set('mail', 'mail_from', mail_from)
            parser.write(config_file)
            config_file.close()
            d.msgbox("Configuration file written successfully",
                     width=50, height=5)
            os.system('clear')
        except (IOError, OSError) as e:
            raise AutosubmitCritical(
                "Can not write config file", 7012, e.message)
        return True

    @staticmethod
    def _requested_exit(code, d):
        if code != dialog.Dialog.OK:
            code = d.yesno(
                'Exit configure utility without saving?', width=50, height=5)
            if code == dialog.Dialog.OK:
                os.system('clear')
                return True
        return False

    @staticmethod
    def install():
        """
        Creates a new database instance for autosubmit at the configured path

        """
        if not os.path.exists(BasicConfig.DB_PATH):
            Log.info("Creating autosubmit database...")
            qry = resource_string('autosubmit.database', 'data/autosubmit.sql').decode(locale.getlocale()[1])
            if not create_db(qry):
                raise AutosubmitCritical("Can not write database file", 7004)
            Log.result("Autosubmit database created successfully")
        else:
            raise AutosubmitCritical("Database already exists.", 7004)
        return True

    @staticmethod
    def refresh(expid, model_conf, jobs_conf):
        """
        Refresh project folder for given experiment

        :param model_conf:
        :type model_conf: bool
        :param jobs_conf:
        :type jobs_conf: bool
        :param expid: experiment identifier
        :type expid: str
        """
        try:
            Autosubmit._check_ownership(expid, raise_error=True)
            as_conf = AutosubmitConfig(expid, BasicConfig, YAMLParserFactory())
            # as_conf.reload(force_load=True)
            as_conf.check_conf_files(refresh=True)
        except (AutosubmitError, AutosubmitCritical):
            raise
        except BaseException as e:
            raise AutosubmitCritical("Error while reading the configuration files", 7064, str(e))
        try:
            if "Expdef" in as_conf.wrong_config:
                as_conf.show_messages()
            project_type = as_conf.get_project_type()
            if Autosubmit._copy_code(as_conf, expid, project_type, True):
                Log.result("Project folder updated")
            Autosubmit._create_project_associated_conf(
                as_conf, model_conf, jobs_conf)
        except (AutosubmitError, AutosubmitCritical):
            raise
        except BaseException as e:
            raise AutosubmitCritical("  Download failed", 7064, str(e))
        return True

    @staticmethod
    def update_version(expid):
        """
        Refresh experiment version with the current autosubmit version
        :param expid: experiment identifier
        :type expid: str
        """
        Autosubmit._check_ownership(expid, raise_error=True)

        as_conf = AutosubmitConfig(expid, BasicConfig, YAMLParserFactory())
        as_conf.reload(force_load=True)
        as_conf.check_expdef_conf()

        Log.info("Changing {0} experiment version from {1} to  {2}",
                 expid, as_conf.get_version(), Autosubmit.autosubmit_version)
        as_conf.set_version(Autosubmit.autosubmit_version)
        update_experiment_descrip_version(expid, version=Autosubmit.autosubmit_version)

        return True

    @staticmethod
    def update_description(expid, new_description):
        Log.info("Checking if experiment exists...")
        check_experiment_exists(expid)
        Log.info("Experiment found.")
        Log.info("Setting {0} description to '{1}'".format(
            expid, new_description))
        result = update_experiment_descrip_version(
            expid, description=new_description)
        if result:
            Log.info("Update completed successfully.")
        else:
            Log.critical("Update failed.")
        return True

    # fastlook
    @staticmethod
    def update_old_script(root_dir, template_path, as_conf):
        # Do a backup and tries to update
        warn = ""
        substituted = ""
        Log.info("Checking {0}".format(template_path))
        if template_path.exists():
            backup_path = root_dir / Path(template_path.name + "_AS_v3_backup_placeholders")
            if not backup_path.exists():
                Log.info("Backup stored at {0}".format(backup_path))
                shutil.copyfile(template_path, backup_path)
            template_content = open(template_path, 'r', encoding=locale.getlocale()[1]).read()
            # Look for %_%
            variables = re.findall('%(?<!%%)[a-zA-Z0-9_.]+%(?!%%)', template_content)
            variables = [variable[1:-1].upper() for variable in variables]
            results = {}
            # Change format
            for old_format_key in variables:
                for key in as_conf.load_parameters().keys():
                    key_affix = key.split(".")[-1]
                    if key_affix == old_format_key:
                        if old_format_key not in results:
                            results[old_format_key] = set()

                        results[old_format_key].add("%" + key.strip("'") + "%")
            for key, new_key in results.items():
                if len(new_key) > 1:
                    if list(new_key)[0].find("JOBS") > -1 or list(new_key)[0].find("PLATFORMS") > -1:
                        pass
                    else:
                        warn += "{0} couldn't translate to {1} since it is a duplicate variable. Please chose one of the keys value.\n".format(
                            key, new_key)
                else:
                    new_key = new_key.pop().upper()
                    substituted += "{0} translated to {1}\n".format(key.upper(), new_key)
                    template_content = re.sub('%(?<!%%)' + key + '%(?!%%)', new_key, template_content, flags=re.I)
            # write_it
            # Deletes unused keys from confs
            if template_path.name.lower().find("autosubmit") > -1:
                template_content = re.sub('(?m)^( )*(EXPID:)( )*[a-zA-Z0-9]*(\n)*', "", template_content, flags=re.I)
            # Write final result
            open(template_path, "w").write(template_content)

        if warn == "" and substituted == "":
            Log.result("Completed check for {0}.\nNo %_% variables found.".format(template_path))
        else:
            Log.result("Completed check for {0}".format(template_path))

        return warn, substituted

    @staticmethod
    def upgrade_scripts(expid,files=""):
        def get_files(root_dir_, extensions,files=""):
            all_files = []
            if len(files) > 0:
                for ext in extensions:
                    all_files.extend(root_dir_.rglob(ext))
            else:
                if ',' in files:
                    files = files.split(',')
                elif ' ' in files:
                    files = files.split(' ')
                for file in files:
                    all_files.append(file)
            return all_files

        Log.info("Checking if experiment exists...")
        try:
            # Check that the user is the owner and the configuration is well configured
            Autosubmit._check_ownership(expid, raise_error=True)
            folder = Path(BasicConfig.LOCAL_ROOT_DIR) / expid / "conf"
            factory = YAMLParserFactory()
            # update scripts to yml format
            for f in folder.rglob("*.yml"):
                # Tries to convert an invalid yml to correct one
                try:
                    parser = factory.create_parser()
                    parser.load(Path(f))
                except BaseException as e:
                    try:
                        AutosubmitConfig.ini_to_yaml(f.parent, Path(f))
                    except BaseException:
                        Log.warning("Couldn't convert conf file to yml: {0}", f.parent)

            # Converts all ini into yaml
            Log.info("Converting all .conf files into .yml.")
            for f in folder.rglob("*.conf"):
                if not Path(f.stem + ".yml").exists():
                    try:
                        AutosubmitConfig.ini_to_yaml(Path(f).parent, Path(f))
                    except Exception as e:
                        Log.warning("Couldn't convert conf file to yml: {0}", Path(f).parent)
            as_conf = AutosubmitConfig(expid, BasicConfig, YAMLParserFactory())
            as_conf.reload(force_load=True)
            # Load current variables
            as_conf.check_conf_files()
            # Load current parameters ( this doesn't read job parameters)
            parameters = as_conf.load_parameters()

        except (AutosubmitError, AutosubmitCritical):
            raise
        # Update configuration files
        template_path = Path()
        warn = ""
        substituted = ""
        root_dir = Path(as_conf.basic_config.LOCAL_ROOT_DIR) / expid / "conf"
        Log.info("Looking for %_% variables inside conf files")
        for f in get_files(root_dir, ('*.yml', '*.yaml', '*.conf')):
            template_path = root_dir / Path(f).name
            try:
                w, s = Autosubmit.update_old_script(root_dir, template_path, as_conf)
                if w != "":
                    warn += "Warnings for: {0}\n{1}\n".format(template_path.name, w)
                if s != "":
                    substituted += "Variables changed for: {0}\n{1}\n".format(template_path.name, s)
            except BaseException as e:
                Log.printlog("Couldn't read {0} template.\ntrace:{1}".format(template_path, str(e)))
        if substituted == "" and warn == "":
            pass
        else:
            Log.result(substituted)
            Log.result(warn)
        # Update templates
        root_dir = Path(as_conf.get_project_dir())
        template_path = Path()
        warn = ""
        substituted = ""
        Log.info("Looking for %_% variables inside templates")
        for section, value in as_conf.jobs_data.items():
            try:
                template_path = root_dir / Path(value.get("FILE", ""))
                w, s = Autosubmit.update_old_script(template_path.parent, template_path, as_conf)
                if w != "":
                    warn += "Warnings for: {0}\n{1}\n".format(template_path.name, w)
                if s != "":
                    substituted += "Variables changed for: {0}\n{1}\n".format(template_path.name, s)
            except BaseException as e:
                Log.printlog("Couldn't read {0} template.\ntrace:{1}".format(template_path, str(e)))
        if substituted != "":
            Log.printlog(substituted, Log.RESULT)
        if warn != "":
            Log.printlog(warn, Log.ERROR)
        Log.info("Changing {0} experiment version from {1} to {2}",
                 expid, as_conf.get_version(), Autosubmit.autosubmit_version)
        as_conf.set_version(Autosubmit.autosubmit_version)
        update_experiment_descrip_version(expid, version=Autosubmit.autosubmit_version)

    @staticmethod
    def pkl_fix(expid):
        """
        Tries to find a backup of the pkl file and restores it. Verifies that autosubmit is not running on this experiment.  

        :param expid: experiment identifier
        :type expid: str
        :return:
        :rtype: 
        """
        exp_path = os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid)
        tmp_path = os.path.join(exp_path, BasicConfig.LOCAL_TMP_DIR)
        pkl_folder_path = os.path.join(exp_path, "pkl")
        current_pkl_path = os.path.join(
            pkl_folder_path, "job_list_{}.pkl".format(expid))
        backup_pkl_path = os.path.join(
            pkl_folder_path, "job_list_{}_backup.pkl".format(expid))
        try:
            with portalocker.Lock(os.path.join(tmp_path, 'autosubmit.lock'), timeout=1):
                # Not locked
                Log.info("Looking for backup file {}".format(backup_pkl_path))
                if os.path.exists(backup_pkl_path):
                    # Backup file exists
                    Log.info("Backup file found.")
                    # Make sure backup file is not empty
                    _stat_b = os.stat(backup_pkl_path)
                    if _stat_b.st_size <= 6:
                        # It is empty -> Return
                        Log.info(
                            "The backup file {} is empty. Pkl restore operation stopped. No changes have been made.".format(
                                backup_pkl_path))
                        return
                    if os.path.exists(current_pkl_path):
                        # Pkl file exists
                        Log.info("Current pkl file {} found.".format(
                            current_pkl_path))
                        _stat = os.stat(current_pkl_path)
                        if _stat.st_size > 6:
                            # Greater than 6 bytes -> Not empty
                            if not Autosubmit._user_yes_no_query(
                                    "The current pkl file {0} is not empty. Do you want to continue?".format(
                                        current_pkl_path)):
                                # The user chooses not to continue. Operation stopped.
                                Log.info(
                                    "Pkl restore operation stopped. No changes have been made.")
                                return
                        result = None
                        if _stat.st_size > 6:
                            # File not empty: Archive
                            archive_pkl_name = os.path.join(pkl_folder_path, "{0}_job_list_{1}.pkl".format(
                                datetime.datetime.today().strftime("%d%m%Y%H%M%S"), expid))
                            # Waiting for completion
                            subprocess.call(
                                ["cp", current_pkl_path, archive_pkl_name])

                            if os.path.exists(archive_pkl_name):
                                Log.result("File {0} archived as {1}.".format(
                                    current_pkl_path, archive_pkl_name))
                        else:
                            # File empty: Delete
                            result = os.popen("rm {}".format(current_pkl_path))
                            if result is not None:
                                Log.info("File {0} deleted.".format(
                                    current_pkl_path))
                    # Restore backup file
                    Log.info("Restoring {0} into {1}".format(
                        backup_pkl_path, current_pkl_path))
                    subprocess.call(["mv", backup_pkl_path, current_pkl_path])

                    if os.path.exists(current_pkl_path):
                        Log.result("Pkl restored.")
                else:
                    Log.info(
                        "Backup file not found. Pkl restore operation stopped. No changes have been made.")
        except (portalocker.AlreadyLocked, portalocker.LockException) as e:
            message = "Another Autosubmit instance using the experiment\n. Stop other Autosubmit instances that are using the experiment or delete autosubmit.lock file located on the /tmp folder."
            raise AutosubmitCritical(message, 7000)
        except AutosubmitCritical as e:
            raise AutosubmitCritical(e.message, e.code, e.trace)
        except BaseException as e:
            raise

    @staticmethod
    def database_backup(expid):
        try:
            database_path = os.path.join(BasicConfig.JOBDATA_DIR, "job_data_{0}.db".format(expid))
            backup_path = os.path.join(BasicConfig.JOBDATA_DIR, "job_data_{0}.sql".format(expid))
            tmp_backup_path = os.path.join(BasicConfig.JOBDATA_DIR, "job_data_{0}_tmp.sql".format(expid))
            command = "sqlite3 {0} .dump > {1} ".format(database_path, tmp_backup_path)
            Log.debug("Backing up jobs_data...")
            out = subprocess.call(command, shell=True)
            Log.debug("Jobs_data database backup completed.")
        except BaseException as e:
            Log.debug("Jobs_data database backup failed.")

    @staticmethod
    def database_fix(expid):
        """
        Database methods. Performs a sql dump of the database and restores it.

        :param expid: experiment identifier
        :type expid: str
        :return:
        :rtype:        
        """
        os.umask(0)  # Overrides user permissions
        current_time = int(time.time())
        corrupted_db_path = os.path.join(BasicConfig.JOBDATA_DIR, "job_data_{0}_corrupted.db".format(expid))

        database_path = os.path.join(BasicConfig.JOBDATA_DIR, "job_data_{0}.db".format(expid))
        database_backup_path = os.path.join(BasicConfig.JOBDATA_DIR, "job_data_{0}.sql".format(expid))
        dump_file_name = 'job_data_{0}.sql'.format(expid, current_time)
        dump_file_path = os.path.join(BasicConfig.JOBDATA_DIR, dump_file_name)
        bash_command = 'cat {1} | sqlite3 {0}'.format(database_path, dump_file_path)
        try:
            if os.path.exists(database_path):
                result = os.popen("mv {0} {1}".format(database_path, corrupted_db_path)).read()
                time.sleep(1)
                Log.info("Original database moved.")
            try:
                exp_history = ExperimentHistory(expid, jobdata_dir_path=BasicConfig.JOBDATA_DIR,
                                                historiclog_dir_path=BasicConfig.HISTORICAL_LOG_DIR)
                Log.info("Restoring from sql")
                result = os.popen(bash_command).read()
                exp_history.initialize_database()

            except:
                Log.warning("It was not possible to restore the jobs_data.db file... , a new blank db will be created")
                result = os.popen("rm {0}".format(database_path)).read()

                exp_history = ExperimentHistory(expid, jobdata_dir_path=BasicConfig.JOBDATA_DIR,
                                                historiclog_dir_path=BasicConfig.HISTORICAL_LOG_DIR)
                exp_history.initialize_database()
        except Exception as exp:
            Log.warning(str(exp))

    @staticmethod
    def archive(expid, noclean=True, uncompress=True):
        """
        Archives an experiment: call clean (if experiment is of version 3 or later), compress folder
        to tar.gz and moves to year's folder

        :param expid: experiment identifier
        :type expid: str
        :param noclean: flag telling it whether to clean the experiment or not.
        :type noclean: bool
        :param uncompress: flag telling it whether to decompress or not.
        :type uncompress: bool
        :return: ``True`` if the experiment has been successfully archived. ``False`` otherwise.
        :rtype: bool

        """

        exp_path = os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid)

        exp_folder = os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid)

        if not noclean:
            # Cleaning to reduce file size.
            version = get_autosubmit_version(expid)
            if version is not None and version.startswith('3') and not Autosubmit.clean(expid, True, True, True):
                raise AutosubmitCritical(
                    "Can not archive project. Clean not successful", 7012)

        # Getting year of last completed. If not, year of expid folder
        year = None
        tmp_folder = os.path.join(exp_folder, BasicConfig.LOCAL_TMP_DIR)
        if os.path.isdir(tmp_folder):
            for filename in os.listdir(tmp_folder):
                if filename.endswith("COMPLETED"):
                    file_year = time.localtime(os.path.getmtime(
                        os.path.join(tmp_folder, filename))).tm_year
                    if year is None or year < file_year:
                        year = file_year

        if year is None:
            year = time.localtime(os.path.getmtime(exp_folder)).tm_year
        Log.info("Archiving in year {0}", year)

        # Creating tar file
        Log.info("Creating tar file ... ")
        try:
            year_path = os.path.join(BasicConfig.LOCAL_ROOT_DIR, str(year))
            if not os.path.exists(year_path):
                os.mkdir(year_path)
                os.chmod(year_path, 0o775)
            if not uncompress:
                compress_type = "w:gz"
                output_filepath = '{0}.tar.gz'.format(expid)
            else:
                compress_type = "w"
                output_filepath = '{0}.tar'.format(expid)
            with tarfile.open(os.path.join(year_path, output_filepath), compress_type) as tar:
                tar.add(exp_folder, arcname='')
                tar.close()
                os.chmod(os.path.join(year_path, output_filepath), 0o775)
        except Exception as e:
            raise AutosubmitCritical("Can not write tar file", 7012, str(e))

        Log.info("Tar file created!")

        try:
            shutil.rmtree(exp_folder)
        except Exception as e:
            Log.warning(
                "Can not fully remove experiments folder: {0}".format(str(e)))
            if os.stat(exp_folder):
                try:
                    tmp_folder = os.path.join(
                        BasicConfig.LOCAL_ROOT_DIR, "tmp")
                    tmp_expid = os.path.join(tmp_folder, expid + "_to_delete")
                    os.rename(exp_folder, tmp_expid)
                    Log.warning("Experiment folder renamed to: {0}".format(
                        exp_folder + "_to_delete "))
                except Exception as e:
                    Autosubmit.unarchive(expid, uncompressed=False)
                    raise AutosubmitCritical(
                        "Can not remove or rename experiments folder", 7012, str(e))

        Log.result("Experiment archived successfully")
        return True

    @staticmethod
    def unarchive(experiment_id, uncompressed=True):
        """
        Unarchives an experiment: uncompress folder from tar.gz and moves to experiment root folder

        :param experiment_id: experiment identifier
        :type experiment_id: str
        :param uncompressed: if True, the tar file is uncompressed
        :type uncompressed: bool

        """
        exp_folder = os.path.join(BasicConfig.LOCAL_ROOT_DIR, experiment_id)

        # Searching by year. We will store it on database
        year = datetime.datetime.today().year
        archive_path = None
        if not uncompressed:
            compress_type = "r:gz"
            output_pathfile = '{0}.tar.gz'.format(experiment_id)
        else:
            compress_type = "r:"
            output_pathfile = '{0}.tar'.format(experiment_id)
        while year > 2000:
            archive_path = os.path.join(
                BasicConfig.LOCAL_ROOT_DIR, str(year), output_pathfile)
            if os.path.exists(archive_path):
                break
            year -= 1

        if year == 2000:
            Log.error("Experiment {0} is not archived", experiment_id)
            return False
        Log.info("Experiment located in {0} archive", year)

        # Creating tar file
        Log.info("Unpacking tar file ... ")
        if not os.path.isdir(exp_folder):
            os.mkdir(exp_folder)
        try:
            with tarfile.open(os.path.join(archive_path), compress_type) as tar:
                tar.extractall(exp_folder)
                tar.close()
        except Exception as e:
            shutil.rmtree(exp_folder, ignore_errors=True)
            Log.printlog("Can not extract tar file: {0}".format(str(e)), 6012)
            return False

        Log.info("Unpacking finished")

        try:
            os.remove(archive_path)
        except Exception as e:
            Log.printlog(
                "Can not remove archived file folder: {0}".format(str(e)), 7012)
            Log.result("Experiment {0} unarchived successfully", experiment_id)
            return True

        Log.result("Experiment {0} unarchived successfully", experiment_id)
        return True

    @staticmethod
    def _create_project_associated_conf(as_conf, force_model_conf, force_jobs_conf):
        project_destiny = as_conf.get_file_project_conf()
        jobs_destiny = as_conf.get_file_jobs_conf()

        if as_conf.get_project_type() != 'none':
            if as_conf.get_file_project_conf():
                copy = True
                if os.path.exists(os.path.join(as_conf.get_project_dir(), as_conf.get_file_project_conf())):
                    if os.path.exists(project_destiny):
                        if force_model_conf:
                            os.rename(project_destiny, str(project_destiny) + "_backup")
                        else:
                            copy = False
                    if copy:
                        shutil.copyfile(os.path.join(as_conf.get_project_dir(), as_conf.get_file_project_conf()),
                                        project_destiny)

            if as_conf.get_file_jobs_conf():
                copy = True
                if os.path.exists(os.path.join(as_conf.get_project_dir(), as_conf.get_file_jobs_conf())):
                    if os.path.exists(jobs_destiny):
                        if force_jobs_conf:
                            os.rename(jobs_destiny, str(jobs_destiny) + "_backup")
                        else:
                            copy = False
                    if copy:
                        shutil.copyfile(os.path.join(as_conf.get_project_dir(), as_conf.get_file_jobs_conf()),
                                        jobs_destiny)

    @staticmethod
    def create(expid, noplot, hide, output='pdf', group_by=None, expand=list(), expand_status=list(),
               notransitive=False, check_wrappers=False, detail=False):
        """
        Creates job list for given experiment. Configuration files must be valid before executing this process.

        :param detail:
        :param check_wrappers:
        :param notransitive:
        :param expand_status:
        :param expand:
        :param group_by:
        :param expid: experiment identifier
        :type expid: str
        :param noplot: if True, method omits final plotting of the jobs list. Only needed on large experiments when
            plotting time can be much larger than creation time.
        :type noplot: bool
        :return: True if successful, False if not
        :rtype: bool
        :param hide: hides plot window
        :type hide: bool
        :param hide: hides plot window
        :type hide: bool
        :param output: plot's file format. It can be pdf, png, ps or svg
        :type output: str
        """

        # checking if there is a lock file to avoid multiple running on the same expid
        try:
            Autosubmit._check_ownership(expid, raise_error=True)
            exp_path = os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid)
            tmp_path = os.path.join(exp_path, BasicConfig.LOCAL_TMP_DIR)
            # Encapsulating the lock
            with portalocker.Lock(os.path.join(tmp_path, 'autosubmit.lock'), timeout=1) as fh:
                try:
                    Log.info(
                        "Preparing .lock file to avoid multiple instances with same expid.")

                    as_conf = AutosubmitConfig(expid, BasicConfig, YAMLParserFactory())
                    # Get original configuration
                    as_conf.check_conf_files(False, only_experiment_data=True, no_log=True)
                    # Getting output type provided by the user in config, 'pdf' as default
                    try:
                        if not Autosubmit._copy_code(as_conf, expid, as_conf.experiment_data.get("PROJECT",{}).get("PROJECT_TYPE","none"), False):
                            return False
                    except:
                        raise AutosubmitCritical("Error obtaining the project data, check the parameters related to PROJECT and GIT/SVN or LOCAL sections", code=7014)
                    # Update configuration with the new config in the dist ( if any )
                    as_conf.check_conf_files(False,force_load=True, only_experiment_data=False, no_log=False)
                    output_type = as_conf.get_output_type()

                    if not os.path.exists(os.path.join(exp_path, "pkl")):
                        raise AutosubmitCritical(
                            "The pkl folder doesn't exists. Make sure that the 'pkl' folder exists in the following path: {}".format(
                                exp_path), code=6013)
                    if not os.path.exists(os.path.join(exp_path, "plot")):
                        raise AutosubmitCritical(
                            "The plot folder doesn't exists. Make sure that the 'plot' folder exists in the following path: {}".format(
                                exp_path), code=6013)

                    update_job = not os.path.exists(os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid, "pkl",
                                                                 "job_list_" + expid + ".pkl"))
                    Autosubmit._create_project_associated_conf(
                        as_conf, False, update_job)

                    # Load parameters
                    Log.info("Loading parameters...")
                    parameters = as_conf.load_parameters()

                    date_list = as_conf.get_date_list()
                    if len(date_list) != len(set(date_list)):
                        raise AutosubmitCritical('There are repeated start dates!', 7014)
                    num_chunks = as_conf.get_num_chunks()
                    chunk_ini = as_conf.get_chunk_ini()
                    member_list = as_conf.get_member_list()
                    run_only_members = as_conf.get_member_list(run_only=True)
                    # print("Run only members {0}".format(run_only_members))
                    if len(member_list) != len(set(member_list)):
                        raise AutosubmitCritical(
                            "There are repeated member names!")
                    rerun = as_conf.get_rerun()

                    Log.info("\nCreating the jobs list...")
                    job_list = JobList(expid, BasicConfig, YAMLParserFactory(),
                                       Autosubmit._get_job_list_persistence(expid, as_conf), as_conf)
                    prev_job_list = Autosubmit.load_job_list(
                        expid, as_conf, notransitive=notransitive)

                    date_format = ''
                    if as_conf.get_chunk_size_unit() == 'hour':
                        date_format = 'H'
                    for date in date_list:
                        if date.hour > 1:
                            date_format = 'H'
                        if date.minute > 1:
                            date_format = 'M'
                    wrapper_jobs = dict()

                    for wrapper_name, wrapper_parameters in as_conf.get_wrappers().items():
                        #continue if it is a global option (non-dict)
                        if type(wrapper_parameters) is not dict:
                            continue
                        wrapper_jobs[wrapper_name] = as_conf.get_wrapper_jobs(wrapper_parameters)

                    job_list.generate(date_list, member_list, num_chunks, chunk_ini, parameters, date_format,
                                      as_conf.get_retrials(),
                                      as_conf.get_default_job_type(),
                                      as_conf.get_wrapper_type(), wrapper_jobs, notransitive=notransitive,
                                      update_structure=True, run_only_members=run_only_members,
                                      jobs_data=as_conf.experiment_data, as_conf=as_conf)

                    if str(rerun).lower() == "true":
                        job_list.rerun(as_conf.get_rerun_jobs(),as_conf)
                    else:
                        job_list.remove_rerun_only_jobs(notransitive)
                    Log.info("\nSaving the jobs list...")
                    job_list.add_logs(prev_job_list.get_logs())
                    job_list.save()
                    JobPackagePersistence(os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid, "pkl"),
                                          "job_packages_" + expid).reset_table()
                    groups_dict = dict()

                    # Setting up job historical database header. Must create a new run.
                    # Historical Database: Setup new run
                    try:
                        exp_history = ExperimentHistory(expid, jobdata_dir_path=BasicConfig.JOBDATA_DIR,
                                                        historiclog_dir_path=BasicConfig.HISTORICAL_LOG_DIR)
                        exp_history.initialize_database()

                        # exp_history.create_new_experiment_run(as_conf.get_chunk_size_unit(), as_conf.get_chunk_size(), as_conf.get_full_config_as_json(), job_list.get_job_list())
                        exp_history.process_status_changes(job_list.get_job_list(),
                                                           chunk_unit=as_conf.get_chunk_size_unit(),
                                                           chunk_size=as_conf.get_chunk_size(),
                                                           current_config=as_conf.get_full_config_as_json(),
                                                           create=True)
                        Autosubmit.database_backup(expid)
                    except BaseException as e:
                        Log.printlog("Historic database seems corrupted, AS will repair it and resume the run",
                                     Log.INFO)
                        try:
                            Autosubmit.database_fix(expid)
                        except Exception as e:
                            Log.warning(
                                "Couldn't recover the Historical database, AS will continue without it, GUI may be affected")
                    if not noplot:
                        if group_by:
                            status = list()
                            if expand_status:
                                for s in expand_status.split():
                                    status.append(
                                        Autosubmit._get_status(s.upper()))

                            job_grouping = JobGrouping(group_by, copy.deepcopy(job_list.get_job_list()), job_list,
                                                       expand_list=expand, expanded_status=status)
                            groups_dict = job_grouping.group_jobs()
                        # WRAPPERS

                        if len(as_conf.experiment_data.get("WRAPPERS", {})) > 0 and check_wrappers:
                            as_conf.check_conf_files(True)
                            packages_persistence = JobPackagePersistence(
                                os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid, "pkl"), "job_packages_" + expid)
                            packages_persistence.reset_table(True)
                            referenced_jobs_to_remove = set()
                            job_list_wrappers = copy.deepcopy(job_list)
                            jobs_wr = job_list_wrappers.get_job_list()
                            for job in jobs_wr:
                                for child in job.children:
                                    if child not in jobs_wr:
                                        referenced_jobs_to_remove.add(child)
                                for parent in job.parents:
                                    if parent not in jobs_wr:
                                        referenced_jobs_to_remove.add(parent)

                            for job in jobs_wr:
                                job.children = job.children - referenced_jobs_to_remove
                                job.parents = job.parents - referenced_jobs_to_remove
                            Autosubmit.generate_scripts_andor_wrappers(
                                as_conf, job_list_wrappers, jobs_wr, packages_persistence, True)

                            packages = packages_persistence.load(True)
                        else:
                            packages = None

                        Log.info("\nPlotting the jobs list...")
                        monitor_exp = Monitor()
                        # if output is set, use output
                        monitor_exp.generate_output(expid, job_list.get_job_list(),
                                                    os.path.join(
                                                        exp_path, "/tmp/LOG_", expid),
                                                    output if output is not None else output_type,
                                                    packages,
                                                    not hide,
                                                    groups=groups_dict,
                                                    job_list_object=job_list)
                    Log.result("\nJob list created successfully")
                    Log.warning(
                        "Remember to MODIFY the MODEL config files!")
                    fh.flush()
                    os.fsync(fh.fileno())

                    # Detail after lock has been closed.
                    if detail is True:
                        current_length = len(job_list.get_job_list())
                        if current_length > 1000:
                            Log.warning(
                                "-d option: Experiment has too many jobs to be printed in the terminal. Maximum job quantity is 1000, your experiment has " + str(
                                    current_length) + " jobs.")
                        else:
                            Log.info(job_list.print_with_status())
                            Log.status(job_list.print_with_status())
                    return True
                # catching Exception
                except KeyboardInterrupt as e:
                    # Setting signal handler to handle subsequent CTRL-C
                    signal.signal(signal.SIGINT, signal_handler_create)
                    fh.flush()
                    os.fsync(fh.fileno())
                    raise AutosubmitCritical("Stopped by user input", 7010)
                except BaseException as e:
                    raise
        except (portalocker.AlreadyLocked, portalocker.LockException) as e:
            message = "We have detected that there is another Autosubmit instance using the experiment\n. Stop other Autosubmit instances that are using the experiment or delete autosubmit.lock file located on tmp folder"
            raise AutosubmitCritical(message, 7000)
        except AutosubmitError as e:
            if e.trace == "":
                e.trace = traceback.format_exc()
            raise AutosubmitError(e.message, e.code, e.trace)
        except AutosubmitCritical as e:
            if e.trace == "":
                e.trace = traceback.format_exc()
            raise AutosubmitCritical(e.message, e.code, e.trace)
        except BaseException as e:
            raise AutosubmitCritical(str(e), 7070)

    @staticmethod
    def _copy_code(as_conf, expid, project_type, force):
        """
        Method to copy code from experiment repository to project directory.

        :param as_conf: experiment configuration class
        :type as_conf: AutosubmitConfig
        :param expid: experiment identifier
        :type expid: str
        :param project_type: project type (git, svn, local)
        :type project_type: str
        :param force: if True, overwrites current data
        :return: True if successful, False if not
        :rtype: bool
        """

        project_destination = as_conf.get_project_destination()
        if project_destination is None or len(project_destination) == 0:
            if project_type.lower() != "none":
                raise AutosubmitCritical("Autosubmit couldn't identify the project destination.", 7014)

        if project_type == "git":
            submitter = Autosubmit._get_submitter(as_conf)
            submitter.load_platforms(as_conf)
            try:
                hpcarch = submitter.platforms[as_conf.get_platform()]
            except BaseException as e:
                error = str(e)
                try:
                    hpcarch = submitter.platforms[as_conf.get_platform()]
                except Exception as e:
                    hpcarch = "local"
                Log.warning("Remote clone may be disabled due to: " + error)
            return AutosubmitGit.clone_repository(as_conf, force, hpcarch)
        elif project_type == "svn":
            svn_project_url = as_conf.get_svn_project_url()
            svn_project_revision = as_conf.get_svn_project_revision()
            project_path = os.path.join(
                BasicConfig.LOCAL_ROOT_DIR, expid, BasicConfig.LOCAL_PROJ_DIR)
            if os.path.exists(project_path):
                Log.info("Using project folder: {0}", project_path)
                if not force:
                    Log.debug("The project folder exists. SKIPPING...")
                    return True
                else:
                    shutil.rmtree(project_path, ignore_errors=True)
            try:
                os.mkdir(project_path)
            except BaseException as e:
                raise AutosubmitCritical(
                    "Project path:{0} can't be created. Revise that the path is the correct one.".format(project_path),
                    7014, str(e))

            Log.debug("The project folder {0} has been created.", project_path)
            Log.info("Checking out revision {0} into {1}",
                     svn_project_revision + " " + svn_project_url, project_path)
            try:
                output = subprocess.check_output("cd " + project_path + "; svn --force-interactive checkout -r " +
                                                 svn_project_revision + " " + svn_project_url + " " +
                                                 project_destination, shell=True)
            except subprocess.CalledProcessError:
                try:
                    shutil.rmtree(project_path, ignore_errors=True)
                except Exception as e:
                    pass
                raise AutosubmitCritical(
                    "Can not check out revision {0} into {1}".format(svn_project_revision + " " + svn_project_url,
                                                                     project_path), 7062)
            Log.debug("{0}", output)

        elif project_type == "local":
            local_project_path = as_conf.get_local_project_path()
            if local_project_path is None or len(local_project_path) == 0:
                raise AutosubmitCritical("Empty project path! please change this parameter to a valid one.", 7014)
            project_path = os.path.join(
                BasicConfig.LOCAL_ROOT_DIR, expid, BasicConfig.LOCAL_PROJ_DIR)
            local_destination = os.path.join(project_path, project_destination)

            if os.path.exists(project_path):
                Log.info("Using project folder: {0}", project_path)
                if os.path.exists(local_destination):
                    if force:
                        try:
                            cmd = ["rsync -ach --info=progress2 " +
                                   local_project_path + "/* " + local_destination]
                            subprocess.call(cmd, shell=True)
                        except (subprocess.CalledProcessError, IOError):
                            raise AutosubmitCritical("Can not rsync {0} into {1}. Exiting...".format(
                                local_project_path, project_path), 7063)
                else:
                    os.mkdir(local_destination)
                    try:
                        output = subprocess.check_output(
                            "cp -R " + local_project_path + "/* " + local_destination, shell=True)
                    except subprocess.CalledProcessError:
                        try:
                            shutil.rmtree(project_path)
                        except Exception as e:
                            pass
                        raise AutosubmitCritical("Can not copy {0} into {1}. Exiting...".format(
                            local_project_path, project_path), 7063)
            else:
                os.mkdir(project_path)
                os.mkdir(local_destination)
                Log.debug(
                    "The project folder {0} has been created.", project_path)
                Log.info("Copying {0} into {1}",
                         local_project_path, project_path)
                try:
                    output = subprocess.check_output(
                        "cp -R " + local_project_path + "/* " + local_destination, shell=True)
                except subprocess.CalledProcessError:
                    try:
                        shutil.rmtree(project_path)
                    except Exception as e:
                        pass
                    raise AutosubmitCritical(
                        "Can not copy {0} into {1}. Exiting...".format(local_project_path, project_path), 7063)
                Log.debug("{0}", output)
        return True

    @staticmethod
    def change_status(final, final_status, job, save):
        """
        Set job status to final

        :param save:
        :param final:
        :param final_status:
        :param job:
        """
        if save:
            if job.status in [Status.SUBMITTED, Status.QUEUING, Status.HELD] and final_status not in [Status.QUEUING,
                                                                                                      Status.HELD,
                                                                                                      Status.SUSPENDED]:
                job.hold = False
                if job.platform_name and job.platform_name.upper() != "LOCAL":
                    job.platform.send_command(job.platform.cancel_cmd + " " + str(job.id), ignore_log=True)
            elif job.status in [Status.QUEUING, Status.RUNNING, Status.SUBMITTED] and final_status == Status.SUSPENDED:
                if job.platform_name and job.platform_name.upper() != "LOCAL":
                    job.platform.send_command("scontrol hold " + "{0}".format(job.id), ignore_log=True)
            elif final_status in [Status.QUEUING, Status.RUNNING] and (job.status == Status.SUSPENDED):
                if job.platform_name and job.platform_name.upper() != "LOCAL":
                    job.platform.send_command("scontrol release " + "{0}".format(job.id), ignore_log=True)
        job.status = final_status
        Log.info("CHANGED: job: " + job.name + " status to: " + final)
        Log.status("CHANGED: job: " + job.name + " status to: " + final)

    @staticmethod
    def set_status(expid, noplot, save, final, lst, filter_chunks, filter_status, filter_section, filter_type_chunk,
                   hide, group_by=None,
                   expand=list(), expand_status=list(), notransitive=False, check_wrapper=False, detail=False):
        """
        Set status

        :param detail:
        :param check_wrapper:
        :param notransitive:
        :param expand_status:
        :param expand:
        :param group_by:
        :param filter_type_chunk:
        :param noplot:
        :param expid: experiment identifier
        :type expid: str
        :param save: if true, saves the new jobs list
        :type save: bool
        :param final: status to set on jobs
        :type final: str
        :param lst: list of jobs to change status
        :type lst: str
        :param filter_chunks: chunks to change status
        :type filter_chunks: str
        :param filter_status: current status of the jobs to change status
        :type filter_status: str
        :param filter_section: sections to change status
        :type filter_section: str
        :param hide: hides plot window
        :type hide: bool
        """
        Autosubmit._check_ownership(expid, raise_error=True)
        exp_path = os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid)
        tmp_path = os.path.join(exp_path, BasicConfig.LOCAL_TMP_DIR)
        section_validation_message = " "
        job_validation_message = " "
        # checking if there is a lock file to avoid multiple running on the same expid
        try:
            with portalocker.Lock(os.path.join(tmp_path, 'autosubmit.lock'), timeout=1):
                Log.info(
                    "Preparing .lock file to avoid multiple instances with same expid.")

                Log.debug('Exp ID: {0}', expid)
                Log.debug('Save: {0}', save)
                Log.debug('Final status: {0}', final)
                Log.debug('List of jobs to change: {0}', lst)
                Log.debug('Chunks to change: {0}', filter_chunks)
                Log.debug('Status of jobs to change: {0}', filter_status)
                Log.debug('Sections to change: {0}', filter_section)
                wrongExpid = 0
                as_conf = AutosubmitConfig(
                    expid, BasicConfig, YAMLParserFactory())
                as_conf.check_conf_files(True)

                # Getting output type from configuration
                output_type = as_conf.get_output_type()
                # Getting db connections

                # Validating job sections, if filter_section -ft has been set:
                if filter_section is not None:
                    section_validation_error = False
                    section_error = False
                    section_not_foundList = list()
                    section_validation_message = "\n## Section Validation Message ##"
                    countStart = filter_section.count('[')
                    countEnd = filter_section.count(']')
                    if countStart > 1 or countEnd > 1:
                        section_validation_error = True
                        section_validation_message += "\n\tList of sections has a format error. Perhaps you were trying to use -fc instead."
                    # countUnderscore =  filter_section.count('_')
                    # if countUnderscore > 1:
                    #    section_validation_error = True
                    #    section_validation_message += "\n\tList of sections provided has a format error. Perhaps you were trying to use -fl instead."
                    if section_validation_error is False:
                        if len(str(filter_section).strip()) > 0:
                            if len(filter_section.split()) > 0:
                                jobSections = as_conf.jobs_data
                                for section in filter_section.split():
                                    # print(section)
                                    # Provided section is not an existing section, or it is not the keyword 'Any'
                                    if section not in jobSections and (section != "Any"):
                                        section_error = True
                                        section_not_foundList.append(section)
                        else:
                            section_validation_error = True
                            section_validation_message += "\n\tEmpty input. No changes performed."
                    if section_validation_error is True or section_error is True:
                        if section_error is True:
                            section_validation_message += "\n\tSpecified section(s) : [" + str(section_not_foundList) + \
                                                          "] not found in the experiment " + str(expid) + \
                                                          ".\n\tProcess stopped. Review the format of the provided input. Comparison is case sensitive." + \
                                                          "\n\tRemember that this option expects section names separated by a blank space as input."

                        raise AutosubmitCritical(
                            "Error in the supplied input for -ft.", 7011, section_validation_message+job_validation_message)
                job_list = Autosubmit.load_job_list(
                    expid, as_conf, notransitive=notransitive)
                submitter = Autosubmit._get_submitter(as_conf)
                submitter.load_platforms(as_conf)
                hpcarch = as_conf.get_platform()
                for job in job_list.get_job_list():
                    if job.platform_name is None or job.platform_name.upper() == "":
                        job.platform_name = hpcarch
                    # noinspection PyTypeChecker
                    job.platform = submitter.platforms[job.platform_name]
                platforms_to_test = set()
                platforms = submitter.platforms
                for job in job_list.get_job_list():
                    job.submitter = submitter
                    if job.platform_name is None:
                        job.platform_name = hpcarch
                    # noinspection PyTypeChecker
                    job.platform = platforms[job.platform_name]
                    # noinspection PyTypeChecker
                    if job.status in [Status.QUEUING, Status.SUBMITTED, Status.RUNNING]:
                        platforms_to_test.add(
                            platforms[job.platform_name])
                # establish the connection to all platforms
                definitive_platforms = list()
                for platform in platforms_to_test:
                    try:
                        Autosubmit.restore_platforms([platform])
                        definitive_platforms.append(platform.name)
                    except Exception as e:
                        pass

                # Validating list of jobs, if filter_list -fl has been set:
                # Seems that Autosubmit.load_job_list call is necessary before verification is executed
                if job_list is not None and lst is not None:
                    job_validation_error = False
                    job_error = False
                    job_not_foundList = list()
                    job_validation_message = "\n## Job Validation Message ##"
                    jobs = list()
                    countStart = lst.count('[')
                    countEnd = lst.count(']')
                    if countStart > 1 or countEnd > 1:
                        job_validation_error = True
                        job_validation_message += "\n\tList of jobs has a format error. Perhaps you were trying to use -fc instead."

                    if job_validation_error is False:
                        for job in job_list.get_job_list():
                            jobs.append(job.name)
                        if len(str(lst).strip()) > 0:
                            if len(lst.split()) > 0:
                                for sentJob in lst.split():
                                    # Provided job does not exist, or it is not the keyword 'Any'
                                    if sentJob not in jobs and (sentJob != "Any"):
                                        job_error = True
                                        job_not_foundList.append(sentJob)
                        else:
                            job_validation_error = True
                            job_validation_message += "\n\tEmpty input. No changes performed."

                    if job_validation_error is True or job_error is True:
                        if job_error is True:
                            job_validation_message += "\n\tSpecified job(s) : [" + str(
                                job_not_foundList) + "] not found in the experiment " + \
                                                      str(expid) + ". \n\tProcess stopped. Review the format of the provided input. Comparison is case sensitive." + \
                                                      "\n\tRemember that this option expects job names separated by a blank space as input."
                        raise AutosubmitCritical(
                            "Error in the supplied input for -ft.", 7011, section_validation_message+job_validation_message)

                # Validating fc if filter_chunks -fc has been set:
                if filter_chunks is not None:
                    fc_validation_message = "## -fc Validation Message ##"
                    fc_filter_is_correct = True
                    selected_sections = filter_chunks.split(",")[1:]
                    selected_formula = filter_chunks.split(",")[0]
                    current_sections = as_conf.jobs_data
                    fc_deserializedJson = object()
                    # Starting Validation
                    if len(str(selected_sections).strip()) == 0:
                        fc_filter_is_correct = False
                        fc_validation_message += "\n\tMust include a section (job type)."
                    else:
                        for section in selected_sections:
                            # section = section.strip()
                            # Validating empty sections
                            if len(str(section).strip()) == 0:
                                fc_filter_is_correct = False
                                fc_validation_message += "\n\tEmpty sections are not accepted."
                                break
                            # Validating existing sections
                            # Retrieve experiment data

                            if section not in current_sections:
                                fc_filter_is_correct = False
                                fc_validation_message += "\n\tSection " + section + \
                                                         " does not exist in experiment. Remember not to include blank spaces."

                    # Validating chunk formula
                    if len(selected_formula) == 0:
                        fc_filter_is_correct = False
                        fc_validation_message += "\n\tA formula for chunk filtering has not been provided."

                    # If everything is fine until this point
                    if fc_filter_is_correct is True:
                        # Retrieve experiment data
                        current_dates = as_conf.experiment_data["EXPERIMENT"]["DATELIST"].split()
                        current_members = as_conf.get_member_list()
                        # Parse json
                        try:
                            fc_deserializedJson = json.loads(
                                Autosubmit._create_json(selected_formula))
                        except Exception as e:
                            fc_filter_is_correct = False
                            fc_validation_message += "\n\tProvided chunk formula does not have the right format. Were you trying to use another option?"
                        if fc_filter_is_correct is True:
                            for startingDate in fc_deserializedJson['sds']:
                                if startingDate['sd'] not in current_dates:
                                    fc_filter_is_correct = False
                                    fc_validation_message += "\n\tStarting date " + \
                                                             startingDate['sd'] + \
                                                             " does not exist in experiment."
                                for member in startingDate['ms']:
                                    if member['m'] not in current_members and member['m'].lower() != "any":
                                        fc_filter_is_correct = False
                                        fc_validation_message += "\n\tMember " + \
                                                                 member['m'] + \
                                                                 " does not exist in experiment."

                    # Ending validation
                    if fc_filter_is_correct is False:
                        section_validation_message = fc_validation_message
                        raise AutosubmitCritical(
                            "Error in the supplied input for -fc.", 7011, section_validation_message+job_validation_message)
                # Validating status, if filter_status -fs has been set:
                # At this point we already have job_list from where we are getting the allows STATUS
                if filter_status is not None:
                    status_validation_error = False
                    status_validation_message = "\n## Status Validation Message ##"
                    # Trying to identify chunk formula
                    countStart = filter_status.count('[')
                    countEnd = filter_status.count(']')
                    if countStart > 1 or countEnd > 1:
                        status_validation_error = True
                        status_validation_message += "\n\tList of status provided has a format error. Perhaps you were trying to use -fc instead."
                    # Trying to identify job names, implying status names won't use more than 1 underscore _
                    # countUnderscore = filter_status.count('_')
                    # if countUnderscore > 1:
                    #    status_validation_error = True
                    #    status_validation_message += "\n\tList of status provided has a format error. Perhaps you were trying to use -fl instead."
                    # If everything is fine until this point
                    if status_validation_error is False:
                        status_filter = filter_status.split()
                        status_reference = Status()
                        status_list = list()
                        for job in job_list.get_job_list():
                            reference = status_reference.VALUE_TO_KEY[job.status]
                            if reference not in status_list:
                                status_list.append(reference)
                        for status in status_filter:
                            if status not in status_list:
                                status_validation_error = True
                                status_validation_message += "\n\t There are no jobs with status " + \
                                                             status + " in this experiment."
                    if status_validation_error is True:
                        raise AutosubmitCritical("Error in the supplied input for -fs.{0}".format(
                            status_validation_message), 7011, section_validation_message+job_validation_message)

                jobs_filtered = []
                final_status = Autosubmit._get_status(final)
                if filter_section or filter_chunks:
                    if filter_section:
                        ft = filter_section.split()
                    else:
                        ft = filter_chunks.split(",")[1:]
                    if ft == 'Any':
                        for job in job_list.get_job_list():
                            Autosubmit.change_status(
                                final, final_status, job, save)
                    else:
                        for section in ft:
                            for job in job_list.get_job_list():
                                if job.section == section:
                                    if filter_chunks:
                                        jobs_filtered.append(job)
                                    else:
                                        Autosubmit.change_status(
                                            final, final_status, job, save)

                # New feature : Change status by section, member, and chunk; freely.
                # Including inner validation. Trying to make it independent.
                # 19601101 [ fc0 [1 2 3 4] Any [1] ] 19651101 [ fc0 [16-30] ] ],SIM,SIM2,SIM3
                if filter_type_chunk:
                    validation_message = "## -ftc Validation Message ##"
                    filter_is_correct = True
                    selected_sections = filter_type_chunk.split(",")[1:]
                    selected_formula = filter_type_chunk.split(",")[0]
                    deserializedJson = object()
                    performed_changes = dict()

                    # Starting Validation
                    if len(str(selected_sections).strip()) == 0:
                        filter_is_correct = False
                        validation_message += "\n\tMust include a section (job type). If you want to apply the changes to all sections, include 'Any'."
                    else:
                        for section in selected_sections:
                            # Validating empty sections
                            if len(str(section).strip()) == 0:
                                filter_is_correct = False
                                validation_message += "\n\tEmpty sections are not accepted."
                                break
                            # Validating existing sections
                            # Retrieve experiment data
                            current_sections = as_conf.jobs_data
                            if section not in current_sections and section != "Any":
                                filter_is_correct = False
                                validation_message += "\n\tSection " + \
                                                      section + " does not exist in experiment."

                    # Validating chunk formula
                    if len(selected_formula) == 0:
                        filter_is_correct = False
                        validation_message += "\n\tA formula for chunk filtering has not been provided. If you want to change all chunks, include 'Any'."

                    # If everything is fine until this point
                    if filter_is_correct is True:
                        # Retrieve experiment data
                        current_dates = as_conf.experiment_data["EXPERIMENT"]["DATELIST"].split()
                        current_members = as_conf.get_member_list()
                        # Parse json
                        try:
                            deserializedJson = json.loads(
                                Autosubmit._create_json(selected_formula))
                        except Exception as e:
                            filter_is_correct = False
                            validation_message += "\n\tProvided chunk formula does not have the right format. Were you trying to use another option?"
                        if filter_is_correct is True:
                            for startingDate in deserializedJson['sds']:
                                if startingDate['sd'] not in current_dates:
                                    filter_is_correct = False
                                    validation_message += "\n\tStarting date " + \
                                                          startingDate['sd'] + \
                                                          " does not exist in experiment."
                                for member in startingDate['ms']:
                                    if member['m'] not in current_members and member['m'] != "Any":
                                        filter_is_correct_ = False
                                        validation_message += "\n\tMember " + \
                                                              member['m'] + \
                                                              " does not exist in experiment."

                    # Ending validation
                    if filter_is_correct is False:
                        raise AutosubmitCritical(
                            "Error in the supplied input for -ftc.", 7011, section_validation_message+job_validation_message)

                    # If input is valid, continue.
                    record = dict()
                    final_list = []
                    # Get current list
                    working_list = job_list.get_job_list()
                    for section in selected_sections:
                        if section == "Any":
                            # Any section
                            section_selection = working_list
                            # Go through start dates
                            for starting_date in deserializedJson['sds']:
                                date = starting_date['sd']
                                date_selection = [j for j in section_selection if date2str(
                                    j.date) == date]
                                # Members for given start date
                                for member_group in starting_date['ms']:
                                    member = member_group['m']
                                    if member == "Any":
                                        # Any member
                                        member_selection = date_selection
                                        chunk_group = member_group['cs']
                                        for chunk in chunk_group:
                                            filtered_job = [j for j in member_selection if j.chunk == int(chunk)]
                                            for job in filtered_job:
                                                final_list.append(job)
                                            # From date filter and sync is not None
                                            for job in [j for j in date_selection if
                                                        j.chunk == int(chunk) and j.synchronize is not None]:
                                                final_list.append(job)
                                    else:
                                        # Selected members
                                        member_selection = [j for j in date_selection if j.member == member]
                                        chunk_group = member_group['cs']
                                        for chunk in chunk_group:
                                            filtered_job = [j for j in member_selection if j.chunk == int(chunk)]
                                            for job in filtered_job:
                                                final_list.append(job)
                                            # From date filter and sync is not None
                                            for job in [j for j in date_selection if
                                                        j.chunk == int(chunk) and j.synchronize is not None]:
                                                final_list.append(job)
                        else:
                            # Only given section
                            section_selection = [j for j in working_list if j.section == section]
                            # Go through start dates
                            for starting_date in deserializedJson['sds']:
                                date = starting_date['sd']
                                date_selection = [j for j in section_selection if date2str(
                                    j.date) == date]
                                # Members for given start date
                                for member_group in starting_date['ms']:
                                    member = member_group['m']
                                    if member == "Any":
                                        # Any member
                                        member_selection = date_selection
                                        chunk_group = member_group['cs']
                                        for chunk in chunk_group:
                                            filtered_job = [j for j in member_selection if
                                                            j.chunk is None or j.chunk == int(chunk)]
                                            for job in filtered_job:
                                                final_list.append(job)
                                            # From date filter and sync is not None
                                            for job in [j for j in date_selection if
                                                        j.chunk == int(chunk) and j.synchronize is not None]:
                                                final_list.append(job)
                                    else:
                                        # Selected members
                                        member_selection = [j for j in date_selection if j.member == member]
                                        chunk_group = member_group['cs']
                                        for chunk in chunk_group:
                                            filtered_job = [j for j in member_selection if j.chunk == int(chunk)]
                                            for job in filtered_job:
                                                final_list.append(job)
                                            # From date filter and sync is not None
                                            for job in [j for j in date_selection if
                                                        j.chunk == int(chunk) and j.synchronize is not None]:
                                                final_list.append(job)
                    status = Status()
                    for job in final_list:
                        if job.status in [Status.QUEUING, Status.RUNNING,
                                          Status.SUBMITTED] and job.platform.name not in definitive_platforms:
                            Log.printlog("JOB: [{1}] is ignored as the [{0}] platform is currently offline".format(
                                job.platform.name, job.name), 6000)
                            continue
                        if job.status != final_status:
                            # Only real changes
                            performed_changes[job.name] = str(
                                Status.VALUE_TO_KEY[job.status]) + " -> " + str(final)
                            Autosubmit.change_status(
                                final, final_status, job, save)
                    # If changes have been performed
                    if len(list(performed_changes.keys())) > 0:
                        if detail is True:
                            current_length = len(job_list.get_job_list())
                            if current_length > 1000:
                                Log.warning(
                                    "-d option: Experiment has too many jobs to be printed in the terminal. Maximum job quantity is 1000, your experiment has " + str(
                                        current_length) + " jobs.")
                            else:
                                Log.info(job_list.print_with_status(
                                    statusChange=performed_changes))
                    else:
                        Log.warning("No changes were performed.")
                # End of New Feature

                if filter_chunks:
                    if len(jobs_filtered) == 0:
                        jobs_filtered = job_list.get_job_list()

                    fc = filter_chunks
                    Log.debug(fc)

                    if fc == 'Any':
                        for job in jobs_filtered:
                            Autosubmit.change_status(
                                final, final_status, job, save)
                    else:
                        # noinspection PyTypeChecker
                        data = json.loads(Autosubmit._create_json(fc))
                        for date_json in data['sds']:
                            date = date_json['sd']
                            if len(str(date)) < 9:
                                format_ = "D"
                            elif len(str(date)) < 11:
                                format_ = "H"
                            elif len(str(date)) < 13:
                                format_ = "M"
                            elif len(str(date)) < 15:
                                format_ = "S"
                            else:
                                format_ = "D"
                            jobs_date = [j for j in jobs_filtered if date2str(
                                j.date, format_) == date]

                            for member_json in date_json['ms']:
                                member = member_json['m']
                                jobs_member = [j for j in jobs_date if j.member == member]

                                for chunk_json in member_json['cs']:
                                    chunk = int(chunk_json)
                                    for job in [j for j in jobs_date if j.chunk == chunk and j.synchronize is not None]:
                                        Autosubmit.change_status(
                                            final, final_status, job, save)

                                    for job in [j for j in jobs_member if j.chunk == chunk]:
                                        Autosubmit.change_status(
                                            final, final_status, job, save)

                if filter_status:
                    status_list = filter_status.split()

                    Log.debug("Filtering jobs with status {0}", filter_status)
                    if status_list == 'Any':
                        for job in job_list.get_job_list():
                            Autosubmit.change_status(
                                final, final_status, job, save)
                    else:
                        for status in status_list:
                            fs = Autosubmit._get_status(status)
                            for job in [j for j in job_list.get_job_list() if j.status == fs]:
                                Autosubmit.change_status(
                                    final, final_status, job, save)

                if lst:
                    jobs = lst.split()
                    expidJoblist = defaultdict(int)
                    for x in lst.split():
                        expidJoblist[str(x[0:4])] += 1

                    if str(expid) in expidJoblist:
                        wrongExpid = jobs.__len__() - expidJoblist[expid]
                    if wrongExpid > 0:
                        Log.warning(
                            "There are {0} job.name with an invalid Expid", wrongExpid)

                    if jobs == 'Any':
                        for job in job_list.get_job_list():
                            Autosubmit.change_status(
                                final, final_status, job, save)
                    else:
                        for job in job_list.get_job_list():
                            if job.name in jobs:
                                Autosubmit.change_status(
                                    final, final_status, job, save)

                job_list.update_list(as_conf, False, True)

                if save and wrongExpid == 0:
                    job_list.save()
                    exp_history = ExperimentHistory(expid, jobdata_dir_path=BasicConfig.JOBDATA_DIR,
                                                    historiclog_dir_path=BasicConfig.HISTORICAL_LOG_DIR)
                    exp_history.initialize_database()
                    exp_history.process_status_changes(job_list.get_job_list(),
                                                       chunk_unit=as_conf.get_chunk_size_unit(),
                                                       chunk_size=as_conf.get_chunk_size(),
                                                       current_config=as_conf.get_full_config_as_json())
                    Autosubmit.database_backup(expid)
                else:
                    Log.printlog(
                        "Changes NOT saved to the JobList!!!!:  use -s option to save", 3000)

                if as_conf.get_wrapper_type() != 'none' and check_wrapper:
                    packages_persistence = JobPackagePersistence(os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid, "pkl"),
                                                                 "job_packages_" + expid)
                    os.chmod(os.path.join(BasicConfig.LOCAL_ROOT_DIR,
                                          expid, "pkl", "job_packages_" + expid + ".db"), 0o775)
                    packages_persistence.reset_table(True)
                    referenced_jobs_to_remove = set()
                    job_list_wrappers = copy.deepcopy(job_list)
                    jobs_wr = copy.deepcopy(job_list.get_job_list())
                    [job for job in jobs_wr if (
                            job.status != Status.COMPLETED)]
                    for job in jobs_wr:
                        for child in job.children:
                            if child not in jobs_wr:
                                referenced_jobs_to_remove.add(child)
                        for parent in job.parents:
                            if parent not in jobs_wr:
                                referenced_jobs_to_remove.add(parent)

                    for job in jobs_wr:
                        job.children = job.children - referenced_jobs_to_remove
                        job.parents = job.parents - referenced_jobs_to_remove
                    Autosubmit.generate_scripts_andor_wrappers(as_conf, job_list_wrappers, jobs_wr,
                                                               packages_persistence, True)

                    packages = packages_persistence.load(True)
                else:
                    packages = JobPackagePersistence(os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid, "pkl"),
                                                     "job_packages_" + expid).load()
                if not noplot:
                    groups_dict = dict()
                    if group_by:
                        status = list()
                        if expand_status:
                            for s in expand_status.split():
                                status.append(
                                    Autosubmit._get_status(s.upper()))

                        job_grouping = JobGrouping(group_by, copy.deepcopy(job_list.get_job_list()), job_list,
                                                   expand_list=expand,
                                                   expanded_status=status)
                        groups_dict = job_grouping.group_jobs()
                    Log.info("\nPlotting joblist...")
                    monitor_exp = Monitor()
                    monitor_exp.generate_output(expid,
                                                job_list.get_job_list(),
                                                os.path.join(
                                                    exp_path, "/tmp/LOG_", expid),
                                                output_format=output_type,
                                                packages=packages,
                                                show=not hide,
                                                groups=groups_dict,
                                                job_list_object=job_list)

                if not filter_type_chunk and detail is True:
                    Log.warning("-d option only works with -ftc.")
                return True

        except (portalocker.AlreadyLocked, portalocker.LockException) as e:
            message = "We have detected that there is another Autosubmit instance using the experiment\n. Stop other Autosubmit instances that are using the experiment or delete autosubmit.lock file located on tmp folder"
            raise AutosubmitCritical(message, 7000)
        except (AutosubmitError, AutosubmitCritical):
            raise
        except BaseException as e:
            raise AutosubmitCritical(
                "An Error has occurred while setting some of the workflow jobs, no changes were made", 7040, str(e))

    @staticmethod
    def _user_yes_no_query(question):
        """
        Utility function to ask user a yes/no question

        :param question: question to ask
        :type question: str
        :return: True if answer is yes, False if it is no
        :rtype: bool
        """
        sys.stdout.write('{0} [y/n]\n'.format(question))
        while True:
            try:
                if sys.version_info[0] == 3:
                    answer = input()
                else:
                    # noinspection PyCompatibility
                    answer = input()
                return strtobool(answer.lower())
            except EOFError as e:
                raise AutosubmitCritical("No input detected, the experiment won't be erased.", 7011, str(e))
            except ValueError:
                sys.stdout.write('Please respond with \'y\' or \'n\'.\n')

    @staticmethod
    def _get_status(s):
        """
        Convert job status from str to Status

        :param s: status string
        :type s: str
        :return: status instance
        :rtype: Status
        """
        s = s.upper()
        if s == 'READY':
            return Status.READY
        elif s == 'COMPLETED':
            return Status.COMPLETED
        elif s == 'WAITING':
            return Status.WAITING
        elif s == 'HELD':
            return Status.HELD
        elif s == 'SUSPENDED':
            return Status.SUSPENDED
        elif s == 'FAILED':
            return Status.FAILED
        elif s == 'RUNNING':
            return Status.RUNNING
        elif s == 'QUEUING':
            return Status.QUEUING
        elif s == 'UNKNOWN':
            return Status.UNKNOWN

    @staticmethod
    def _get_members(out):
        """
        Function to get a list of members from json

        :param out: json member definition
        :type out: str
        :return: list of members
        :rtype: list
        """
        count = 0
        data = []
        # noinspection PyUnusedLocal
        for element in out:
            if count % 2 == 0:
                ms = {'m': out[count],
                      'cs': Autosubmit._get_chunks(out[count + 1])}
                data.append(ms)
                count += 1
            else:
                count += 1

        return data

    @staticmethod
    def _get_chunks(out):
        """
        Function to get a list of chunks from json

        :param out: json member definition
        :type out: str
        :return: list of chunks
        :rtype: list
        """
        data = []
        for element in out:
            if element.find("-") != -1:
                numbers = element.split("-")
                for count in range(int(numbers[0]), int(numbers[1]) + 1):
                    data.append(str(count))
            else:
                data.append(element)

        return data

    @staticmethod
    def _get_submitter(as_conf):
        """
        Returns the submitter corresponding to the communication defined on autosubmit's config file

        :return: submitter
        :rtype: Submitter
        """
        try:
            communications_library = as_conf.get_communications_library()
        except Exception as e:
            communications_library = 'paramiko'
        if communications_library == 'paramiko':
            return ParamikoSubmitter()
        else:
            # only paramiko is available right now.
            return ParamikoSubmitter()

    @staticmethod
    def _get_job_list_persistence(expid, as_conf):
        """
        Returns the JobListPersistence corresponding to the storage type defined on autosubmit's config file

        :return: job_list_persistence
        :rtype: JobListPersistence
        """
        storage_type = as_conf.get_storage_type()
        if storage_type == 'pkl':
            return JobListPersistencePkl()
        elif storage_type == 'db':
            return JobListPersistenceDb(os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid, "pkl"),
                                        "job_list_" + expid)
        raise AutosubmitCritical('Storage type not known', 7014)

    @staticmethod
    def _create_json(text):
        """
        Function to parse rerun specification from json format

        :param text: text to parse
        :type text: str
        :return: parsed output
        """
        count = 0
        data = []

        # text = "[ 19601101 [ fc0 [1 2 3 4] fc1 [1] ] 16651101 [ fc0 [1-30 31 32] ] ]"

        def parse_date(datestring):
            result = []
            startindex = datestring.find('(')
            endindex = datestring.find(')')
            if startindex > 0 and endindex > 0:
                try:
                    startstring = datestring[:startindex]
                    startrange = datestring[startindex + 1:].split('-')[0]
                    endrange = datestring[startindex:-1].split('-')[1]
                    startday = int(startrange[-2:])
                    endday = int(endrange[-2:])

                    frommonth = int(startrange[:2])
                    tomonth = int(endrange[:2])

                    for i in range(frommonth, tomonth + 1):
                        for j in range(startday, endday + 1):
                            result.append(startstring + "%02d" %
                                          i + "%02d" % j)
                except Exception as exp:
                    raise AutosubmitCritical(
                        "Autosubmit couldn't parse your input format. Exception: {0}".format(exp))

            else:
                result = [datestring]
            return result

        out = nestedExpr('[', ']').parseString(text).asList()

        # noinspection PyUnusedLocal
        for element in out[0]:
            if count % 2 == 0:
                datelist = parse_date(out[0][count])
                for item in datelist:
                    sd = {'sd': item, 'ms': Autosubmit._get_members(
                        out[0][count + 1])}
                    data.append(sd)
                count += 1
            else:
                count += 1

        sds = {'sds': data}
        result = json.dumps(sds)
        return result

    @staticmethod
    def testcase(copy_id, description, chunks=None, member=None, start_date=None, hpc=None, branch=None):
        """
        Method to create a test case. It creates a new experiment whose id starts by 't'.


        :param copy_id: experiment identifier
        :type copy_id: str
        :param description: test case experiment description
        :type description: str
        :param chunks: number of chunks to be run by the experiment. If None, it uses configured chunk(s).
        :type chunks: int
        :param member: member to be used by the test. If None, it uses configured member(s).
        :type member: str
        :param start_date: start date to be used by the test. If None, it uses configured start date(s).
        :type start_date: str
        :param hpc: HPC to be used by the test. If None, it uses configured HPC.
        :type hpc: str
        :param branch: branch or revision to be used by the test. If None, it uses configured branch.
        :type branch: str
        :return: test case id
        :rtype: str
        """

        testcaseid = Autosubmit.expid(hpc, description, copy_id, False, True)
        if testcaseid == '':
            return False

        Autosubmit._change_conf(
            testcaseid, hpc, start_date, member, chunks, branch, False)

        return testcaseid

    @staticmethod
    def test(expid, chunks, member=None, start_date=None, hpc=None, branch=None):
        """
        Method to conduct a test for a given experiment. It creates a new experiment for a given experiment with a
        given number of chunks with a random start date and a random member to be run on a random HPC.


        :param expid: experiment identifier
        :type expid: str
        :param chunks: number of chunks to be run by the experiment
        :type chunks: int
        :param member: member to be used by the test. If None, it uses a random one from which are defined on
                       the experiment.
        :type member: str
        :param start_date: start date to be used by the test. If None, it uses a random one from which are defined on
                         the experiment.
        :type start_date: str
        :param hpc: HPC to be used by the test. If None, it uses a random one from which are defined on
                    the experiment.
        :type hpc: str
        :param branch: branch or revision to be used by the test. If None, it uses configured branch.
        :type branch: str
        :return: True if test was successful, False otherwise
        :rtype: bool
        """
        testid = Autosubmit.expid(
            'test', 'test experiment for {0}'.format(expid), expid, False, True)
        if testid == '':
            return False

        Autosubmit._change_conf(testid, hpc, start_date,
                                member, chunks, branch, True)

        Autosubmit.create(testid, False, True)
        if not Autosubmit.run_experiment(testid):
            return False
        return True

    @staticmethod
    def _change_conf(testid, hpc, start_date, member, chunks, branch, random_select=False):
        as_conf = AutosubmitConfig(testid, BasicConfig, YAMLParserFactory())

        if as_conf.experiment_data.get("RERUN", False):
            if str(as_conf.experiment_data["RERUN"].get("RERUN", "False")).lower() != "true":
                raise AutosubmitCritical('Can not test a RERUN experiment', 7014)

        content = open(as_conf.experiment_file).read()
        if random_select:
            if hpc is None:
                platforms_parser = as_conf.get_parser(
                    YAMLParserFactory(), as_conf.platforms_file)
                test_platforms = list()
                for section in platforms_parser.sections():
                    if as_conf.experiment_data["PLATFORMS"][section].get('TEST_SUITE', 'false').lower() == 'true':
                        test_platforms.append(section)
                if len(test_platforms) == 0:
                    raise AutosubmitCritical(
                        "Missing hpcarch setting in expdef", 7014)

                hpc = random.choice(test_platforms)
            if member is None:
                member = random.choice(str(as_conf.experiment_data['EXPERIMENT'].get('MEMBERS')).split(' '))
            if start_date is None:
                start_date = random.choice(str(as_conf.experiment_data['EXPERIMENT'].get('DATELIST')).split(' '))
            if chunks is None:
                chunks = 1

        # Experiment
        content = content.replace(re.search('EXPID:.*', content, re.MULTILINE).group(0),
                                  "EXPID: " + testid)
        if start_date is not None:
            content = content.replace(re.search('DATELIST:.*', content, re.MULTILINE).group(0),
                                      "DATELIST: " + start_date)
        if member is not None:
            content = content.replace(re.search('MEMBERS:.*', content, re.MULTILINE).group(0),
                                      "MEMBERS: " + member)
        if chunks is not None:
            # noinspection PyTypeChecker
            content = content.replace(re.search('NUMCHUNKS:.*', content, re.MULTILINE).group(0),
                                      "NUMCHUNKS: " + chunks)
        if hpc is not None:
            content = content.replace(re.search('HPCARCH:.*', content, re.MULTILINE).group(0),
                                      "HPCARCH: " + hpc)
        if branch is not None:
            content = content.replace(re.search('PROJECT_BRANCH:.*', content, re.MULTILINE).group(0),
                                      "PROJECT_BRANCH: " + branch)
            content = content.replace(re.search('PROJECT_REVISION:.*', content, re.MULTILINE).group(0),
                                      "PROJECT_REVISION: " + branch)

        open(as_conf.experiment_file, 'wb').write(content)

    @staticmethod
    def load_job_list(expid, as_conf, notransitive=False, monitor=False):
        rerun = as_conf.get_rerun()

        job_list = JobList(expid, BasicConfig, YAMLParserFactory(),
                           Autosubmit._get_job_list_persistence(expid, as_conf), as_conf)
        run_only_members = as_conf.get_member_list(run_only=True)
        date_list = as_conf.get_date_list()
        date_format = ''
        if as_conf.get_chunk_size_unit() == 'hour':
            date_format = 'H'
        for date in date_list:
            if date.hour > 1:
                date_format = 'H'
            if date.minute > 1:
                date_format = 'M'
        wrapper_jobs = dict()
        for wrapper_section, wrapper_data in as_conf.experiment_data.get("WRAPPERS", {}).items():
            if isinstance(wrapper_data, collections.abc.Mapping):
                wrapper_jobs[wrapper_section] = wrapper_data.get("JOBS_IN_WRAPPER", "")

        job_list.generate(date_list, as_conf.get_member_list(), as_conf.get_num_chunks(), as_conf.get_chunk_ini(),
                          as_conf.experiment_data, date_format, as_conf.get_retrials(),
                          as_conf.get_default_job_type(), as_conf.get_wrapper_type(), wrapper_jobs,
                          new=False, notransitive=notransitive, run_only_members=run_only_members,
                          jobs_data=as_conf.experiment_data, as_conf=as_conf)
        if str(rerun).lower() == "true":
            rerun_jobs = as_conf.get_rerun_jobs()
            job_list.rerun(rerun_jobs,as_conf, monitor=monitor)
        else:
            job_list.remove_rerun_only_jobs(notransitive)

        return job_list

    @staticmethod
    def rerun_recovery(expid, job_list, rerun_list, as_conf):
        """
        Method to check all active jobs. If COMPLETED file is found, job status will be changed to COMPLETED,
        otherwise it will be set to WAITING. It will also update the jobs list.

        :param expid: identifier of the experiment to recover
        :type expid: str
        :param job_list: job list to update
        :type job_list: JobList
        :param rerun_list: list of jobs to rerun
        :type rerun_list: list
        :param as_conf: AutosubmitConfig object
        :type as_conf: AutosubmitConfig
        :return:


        """

        hpcarch = as_conf.get_platform()
        submitter = Autosubmit._get_submitter(as_conf)
        try:
            submitter.load_platforms(as_conf)
            if submitter.platforms is None:
                raise AutosubmitCritical("platforms couldn't be loaded", 7014)
        except Exception as e:
            raise AutosubmitCritical("platforms couldn't be loaded", 7014)
        platforms = submitter.platforms

        platforms_to_test = set()
        for job in job_list.get_job_list():
            if job.platform_name is None:
                job.platform_name = hpcarch
            # noinspection PyTypeChecker
            job.platform = platforms[job.platform_name]
            # noinspection PyTypeChecker
            platforms_to_test.add(platforms[job.platform_name])
        rerun_names = []

        [rerun_names.append(job.name) for job in rerun_list.get_job_list()]
        jobs_to_recover = [
            i for i in job_list.get_job_list() if i.name not in rerun_names]

        Log.info("Looking for COMPLETED files")
        start = datetime.datetime.now()
        for job in jobs_to_recover:
            if job.platform_name is None:
                job.platform_name = hpcarch
            # noinspection PyTypeChecker
            job.platform = platforms[job.platform_name.upper()]

            if job.platform.get_completed_files(job.name, 0):
                job.status = Status.COMPLETED
                Log.info(
                    "CHANGED job '{0}' status to COMPLETED".format(job.name))

            job.platform.get_logs_files(expid, job.remote_logs)
        return job_list
