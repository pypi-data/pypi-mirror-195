#!/usr/bin/env python3

# Copyright 2014 Climate Forecasting Unit, IC3

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
# along with Autosubmit.  If not, see <http: www.gnu.org / licenses / >.


import os

from log.log import Log,AutosubmitCritical,AutosubmitError
from autosubmitconfigparser.config.basicconfig import BasicConfig
from autosubmitconfigparser.config.configcommon import AutosubmitConfig
from .submitter import Submitter
from autosubmit.platforms.psplatform import PsPlatform
from autosubmit.platforms.lsfplatform import LsfPlatform
from autosubmit.platforms.pbsplatform import PBSPlatform
from autosubmit.platforms.sgeplatform import SgePlatform
from autosubmit.platforms.ecplatform import EcPlatform
from autosubmit.platforms.slurmplatform import SlurmPlatform
from autosubmit.platforms.locplatform import LocalPlatform
from autosubmit.platforms.paramiko_platform import ParamikoPlatformException


class ParamikoSubmitter(Submitter):
    """
    Class to manage the experiments platform
    """

    def __init__(self):
        self.platforms = None

    def load_platforms_migrate(self, asconf, retries=5):
        pass  # Add all info related to migrate

    def load_local_platform(self, asconf):
        platforms = dict()
        # Build Local Platform Object
        local_platform = LocalPlatform(asconf.expid, 'local', BasicConfig)
        local_platform.max_wallclock = asconf.get_max_wallclock()
        local_platform.max_processors = asconf.get_max_processors()
        local_platform.max_waiting_jobs = asconf.get_max_waiting_jobs()
        local_platform.total_jobs = asconf.get_total_jobs()
        local_platform.scratch = os.path.join(
            BasicConfig.LOCAL_ROOT_DIR, asconf.expid, BasicConfig.LOCAL_TMP_DIR)
        local_platform.temp_dir = os.path.join(
            BasicConfig.LOCAL_ROOT_DIR, 'ASlogs')
        local_platform.root_dir = os.path.join(
            BasicConfig.LOCAL_ROOT_DIR, local_platform.expid)
        local_platform.host = 'localhost'
        # Add object to entry in dictionary
        platforms['local'] = local_platform
        platforms['LOCAL'] = local_platform
        self.platforms = platforms

    def load_platforms(self, asconf, retries=5):
        """
        Create all the platforms object that will be used by the experiment

        :param retries: retries in case creation of service fails
        :param asconf: autosubmit config to use
        :type asconf: AutosubmitConfig
        :return: platforms used by the experiment
        :rtype: dict
        """
        exp_data = asconf.experiment_data
        raise_message=""
        platforms_used = list()
        hpcarch = asconf.get_platform()
        platforms_used.append(hpcarch)

        # Traverse jobs defined in jobs_.conf and add platforms found if not already included
        jobs_data = exp_data.get('JOBS', {})
        for job in jobs_data:
            hpc = jobs_data[job].get('PLATFORM', hpcarch).upper()
            if hpc not in platforms_used:
                platforms_used.append(hpc)

        platform_data = exp_data.get('PLATFORMS', {})
        # Declare platforms dictionary, key: Platform Name, Value: Platform Object
        platforms = dict()

        # Build Local Platform Object
        local_platform = LocalPlatform(asconf.expid, 'local', BasicConfig)
        local_platform.max_wallclock = asconf.get_max_wallclock()
        local_platform.max_processors = asconf.get_max_processors()
        local_platform.max_waiting_jobs = asconf.get_max_waiting_jobs()
        local_platform.total_jobs = asconf.get_total_jobs()
        local_platform.scratch = os.path.join(
            BasicConfig.LOCAL_ROOT_DIR, asconf.expid, BasicConfig.LOCAL_TMP_DIR)
        local_platform.temp_dir = os.path.join(
            BasicConfig.LOCAL_ROOT_DIR, 'ASlogs')
        local_platform.root_dir = os.path.join(
            BasicConfig.LOCAL_ROOT_DIR, local_platform.expid)
        local_platform.host = 'localhost'
        # Add object to entry in dictionary
        platforms['LOCAL'] = local_platform

        # parser is the platform's parser that represents platforms_.conf
        # Traverse sections []
        for section in platform_data:
            # Consider only those included in the list of jobs
            if section not in platforms_used:
                continue

            platform_type = platform_data[section].get('TYPE', '').lower()
            platform_version = platform_data[section].get('VERSION', '')
            try:
                if platform_type == 'pbs':
                    remote_platform = PBSPlatform(
                        asconf.expid, section, BasicConfig, platform_version)
                elif platform_type == 'sge':
                    remote_platform = SgePlatform(
                        asconf.expid, section, BasicConfig)
                elif platform_type == 'ps':
                    remote_platform = PsPlatform(
                        asconf.expid, section, BasicConfig)
                elif platform_type == 'lsf':
                    remote_platform = LsfPlatform(
                        asconf.expid, section, BasicConfig)
                elif platform_type == 'ecaccess':
                    remote_platform = EcPlatform(
                        asconf.expid, section, BasicConfig, platform_version)
                elif platform_type == 'slurm':
                    remote_platform = SlurmPlatform(
                        asconf.expid, section, BasicConfig)
                else:
                    raise Exception(
                        "Queue type not specified on platform {0}".format(section))

            except ParamikoPlatformException as e:
                Log.error("Queue exception: {0}".format(str(e)))
                return None
            # Set the type and version of the platform found
            remote_platform.type = platform_type
            remote_platform._version = platform_version

            # Concatenating host + project and adding to the object
            add_project_to_host = platform_data[section].get('ADD_PROJECT_TO_HOST', False)
            if str(add_project_to_host).lower() != "false":
                host = '{0}'.format(platform_data[section].get('HOST', ""))
                if host.find(",") == -1:
                    host = '{0}-{1}'.format(host,platform_data[section].get('PROJECT', ""))
                else:
                    host_list = host.split(",")
                    host_aux = ""
                    for ip in host_list:
                        host_aux += '{0}-{1},'.format(ip,platform_data[section].get('PROJECT', ""))
                    host = host_aux[:-1]

            else:
                host = platform_data[section].get('HOST', "")

            remote_platform.host = host
            # Retrieve more configurations settings and save them in the object
            remote_platform.max_wallclock = platform_data[section].get('MAX_WALLCLOCK',"2:00")
            remote_platform.max_processors = platform_data[section].get('MAX_PROCESSORS',asconf.get_max_processors())
            remote_platform.max_waiting_jobs = platform_data[section].get('MAX_WAITING_JOBS',asconf.get_max_waiting_jobs())
            remote_platform.total_jobs = platform_data[section].get('TOTAL_JOBS',asconf.get_total_jobs())
            remote_platform.hyperthreading = str(platform_data[section].get('HYPERTHREADING',False)).lower()
            remote_platform.project = platform_data[section].get('PROJECT',"")
            remote_platform.budget = platform_data[section].get('BUDGET', "")
            remote_platform.reservation = platform_data[section].get('RESERVATION', "")
            remote_platform.exclusivity = platform_data[section].get('EXCLUSIVITY', "")
            remote_platform.user = platform_data[section].get('USER', "")
            remote_platform.scratch = platform_data[section].get('SCRATCH_DIR', "")
            remote_platform.project_dir = platform_data[section].get('SCRATCH_PROJECT_DIR', remote_platform.project)
            remote_platform.temp_dir = platform_data[section].get('TEMP_DIR', "")
            remote_platform._default_queue = platform_data[section].get('QUEUE', "")
            remote_platform._serial_queue = platform_data[section].get('SERIAL_QUEUE', "")
            remote_platform.ec_queue = platform_data[section].get('EC_QUEUE', "hpc")

            remote_platform.ec_queue = platform_data[section].get('EC_QUEUE', "hpc")

            remote_platform.processors_per_node = platform_data[section].get('PROCESSORS_PER_NODE',"1")
            remote_platform.custom_directives = platform_data[section].get('CUSTOM_DIRECTIVES',"")
            if len(remote_platform.custom_directives) > 0:
                Log.debug("Custom directives from platform.conf: {0}".format(
                    remote_platform.custom_directives))
            remote_platform.scratch_free_space = str(platform_data[section].get('SCRATCH_FREE_SPACE', False)).lower()
            try:
                remote_platform.root_dir = os.path.join(remote_platform.scratch, remote_platform.project,remote_platform.user, remote_platform.expid)
                remote_platform.update_cmds()

                platforms[section] = remote_platform
            except Exception as e:
                raise_message = "Error in platform.conf: SCRATCH_DIR, PROJECT, USER, EXPID must be defined for platform {0}".format(section)
            # Executes update_cmds() from corresponding Platform Object
            # Save platform into result dictionary

            serial = platform_data[section].get('SERIAL_PLATFORM',None)
            if serial is not None and len(str(serial)) > 0:
                platforms[section].serial_platform = serial.upper()


        self.platforms = platforms
        if raise_message != "":
            raise AutosubmitError(raise_message)
