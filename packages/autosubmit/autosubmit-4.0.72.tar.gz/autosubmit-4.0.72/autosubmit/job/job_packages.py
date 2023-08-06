#!/usr/bin/env python3

# Copyright 2017-2020 Earth Sciences Department, BSC-CNS

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



import os
from datetime import timedelta

import time
import random
from autosubmit.job.job_common import Status
from log.log import Log,AutosubmitCritical,AutosubmitError
Log.get_logger("Autosubmit")
from autosubmit.job.job import Job
from bscearth.utils.date import sum_str_hours
from threading import Thread, Lock
from typing import List
import multiprocessing
import tarfile
import datetime
import re
import locale
lock = Lock()
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.name = "data_processing"
        thread.start()
        return thread
    return wrapper
class JobPackageBase(object):
    """
    Class to manage the package of jobs to be submitted by autosubmit
    """

    def __init__(self, jobs):
        # type: (List[Job]) -> None
        self._common_script = None
        self._jobs = jobs # type: List[Job]
        self._expid = jobs[0].expid # type: str
        self.hold = False # type: bool
        self.export = jobs[0].export 
        self.x11 = jobs[0].x11
        try:
            self._tmp_path = jobs[0]._tmp_path
            self._platform = jobs[0]._platform
            self._custom_directives = set()
            for job in jobs:
                if job._platform.name != self._platform.name or job.platform is None:
                    raise Exception('Only one valid platform per package')
        except IndexError:
            raise Exception('No jobs given')

    def __len__(self):
        return self._jobs.__len__()

    @property
    def jobs(self):
        # type: () -> List[Job]
        """
        Returns the jobs

        :return: jobs
        :rtype: List[Job]
        """
        return self._jobs

    @property
    def platform(self):
        """
        Returns the platform

        :return: platform
        :rtype: Platform
        """
        return self._platform

    @threaded
    def check_scripts(self,jobs,configuration, parameters,only_generate,hold):
        for job in jobs:
            if job.check.lower() == Job.CHECK_ON_SUBMISSION.lower():
                if only_generate:
                    exit_ = True
                    break
                if not os.path.exists(os.path.join(configuration.get_project_dir(), job.file)):
                    lock.acquire()
                    if configuration.get_project_type().lower() != "none" and len(configuration.get_project_type()) > 0:
                        raise AutosubmitCritical(
                            "Template [ {0} ] using CHECK=On_submission has some empty variable {0}".format(
                                job.name), 7014)
                    lock.release()
                if not job.check_script(configuration, parameters, show_logs=job.check_warnings):
                    Log.warning("Script {0} check failed", job.name)
                    Log.warning("On submission script has  some empty variables")
                else:
                    Log.result("Script {0} OK", job.name)
            lock.acquire()
            job.update_parameters(configuration, parameters)
            lock.release()
            # looking for directives on jobs
            self._custom_directives = self._custom_directives | set(job.custom_directives)
    @threaded
    def _create_scripts_threaded(self,jobs,configuration):
        for i in range(0, len(jobs)):
            self._job_scripts[jobs[i].name] = jobs[i].create_script(configuration)

    def _create_common_script(self,filename=""):
        pass

    def submit(self, configuration, parameters,only_generate=False,hold=False):
        """
        :param hold:
        :para configuration: Autosubmit basic configuration \n
        :type configuration: AutosubmitConfig object \n
        :param parameters; Parameters from joblist \n
        :type parameters: JobList,parameters \n
        :param only_generate: True if coming from generate_scripts_andor_wrappers(). If true, only generates scripts; otherwise, submits. \n
        :type only_generate: Boolean 
        """
        job = None
        exit_=False
        thread_number = multiprocessing.cpu_count()
        if len(self.jobs) > 2500:
            thread_number = thread_number * 2
        elif len(self.jobs) > 5000:
            thread_number = thread_number * 3
        elif len(self.jobs) > 7500:
            thread_number = thread_number * 4
        elif len(self.jobs) > 10000:
            thread_number = thread_number * 5
        chunksize = int((len(self.jobs) + thread_number - 1) / thread_number)
        try:
            if len(self.jobs) < thread_number:
                for job in self.jobs:
                    if job.check == Job.CHECK_ON_SUBMISSION.lower():
                        if only_generate:
                            exit_=True
                            break
                        if not os.path.exists(os.path.join(configuration.get_project_dir(), job.file)):
                            if configuration.get_project_type().lower() != "none" and len(configuration.get_project_type()) > 0:
                                raise AutosubmitCritical("Template [ {0} ] using CHECK=On_submission has some empty variable {0}".format(job.name),7014)
                        if not job.check_script(configuration, parameters,show_logs=job.check_warnings):
                            Log.warning("Script {0} check failed",job.name)
                            Log.warning("On submission script has some empty variables")
                        else:
                            Log.result("Script {0} OK",job.name)
                    job.update_parameters(configuration, parameters)
                    # looking for directives on jobs
                    self._custom_directives = self._custom_directives | set(job.custom_directives)
            else:
                Lhandle = list()
                for i in range(0, len(self.jobs), chunksize):
                    Lhandle.append(self.check_scripts(self.jobs[i:i + chunksize], configuration, parameters, only_generate, hold))
                for dataThread in Lhandle:
                    dataThread.join()
        except AutosubmitCritical : #Raise the intended message
            raise
        except BaseException as e: #should be IOERROR
            raise AutosubmitCritical(
                "Error on {1}, template [{0}] still does not exists in running time(check=on_submission activated) ".format(job.file,job.name), 7014)
        Log.debug("Creating Scripts")
        if not exit_:
            if len(self.jobs) < thread_number:
                self._create_scripts(configuration)
            else:
                Lhandle = list()
                for i in range(0, len(self.jobs), chunksize):
                    Lhandle.append(self._create_scripts_threaded(self.jobs[i:i + chunksize],configuration))
                for dataThread in Lhandle:
                    dataThread.join()
                self._common_script = self._create_common_script()
            if not only_generate:
                Log.debug("Sending Files")
                self._send_files()
                Log.debug("Submitting")
                self._do_submission(hold=hold)


    def _create_scripts(self, configuration):
        raise Exception('Not implemented')

    def _send_files(self):
        """ Send local files to the platform. """

    def _do_submission(self,job_scripts=None, hold=False):
        """ Submit package to the platform. """



class JobPackageSimple(JobPackageBase):
    """
    Class to manage a group of simple jobs, not packaged, to be submitted by autosubmit
    """

    def __init__(self, jobs):
        super(JobPackageSimple, self).__init__(jobs)
        self._job_scripts = {}
        self.export = jobs[0].export

    def _create_scripts(self, configuration):
        for job in self.jobs:
            self._job_scripts[job.name] = job.create_script(configuration)

    def _send_files(self):
        for job in self.jobs:
            self.platform.send_file(self._job_scripts[job.name])
            # TODO Ugly fix quick fix until figure another option, this is to avoid to delete the Additional file in local before sending it due sharing the same directory
            if self.platform.type.upper() != "LOCAL":
                for file_n in range(len(job.additional_files)):
                    filename = os.path.basename(os.path.splitext(job.additional_files[file_n])[0])
                    full_path = os.path.join(self._tmp_path,filename ) + "_" + job.name[5:]
                    self.platform.send_file(os.path.join(self._tmp_path, full_path))

    def _do_submission(self, job_scripts="", hold=False):
        if len(job_scripts) == 0:
            job_scripts = self._job_scripts
        for job in self.jobs:
            #CLEANS PREVIOUS RUN ON LOCAL
            log_completed = os.path.join(self._tmp_path, job.name + '_COMPLETED')
            log_stat = os.path.join(self._tmp_path, job.name + '_STAT')
            if os.path.exists(log_completed):
                os.remove(log_completed)
            if os.path.exists(log_stat):
                os.remove(log_stat)
            self.platform.remove_stat_file(job.name)
            self.platform.remove_completed_file(job.name)
            job.id = self.platform.submit_job(job, job_scripts[job.name], hold=hold, export = self.export)
            if job.id is None or not job.id:
                continue
            Log.info("{0} submitted", job.name)
            job.status = Status.SUBMITTED            
            job.write_submit_time(hold=self.hold)


class JobPackageSimpleWrapped(JobPackageSimple):
    """
    Class to manage a group of simple wrapped jobs, not packaged, to be submitted by autosubmit
    """

    def __init__(self, jobs):
        super(JobPackageSimpleWrapped, self).__init__(jobs)
        self._job_wrapped_scripts = {}

    def _create_scripts(self, configuration):
        super(JobPackageSimpleWrapped, self)._create_scripts(configuration)
        for job in self.jobs:
            self._job_wrapped_scripts[job.name] = job.create_wrapped_script(configuration)

    def _send_files(self):
        super(JobPackageSimpleWrapped, self)._send_files()
        for job in self.jobs:
            self.platform.send_file(self._job_wrapped_scripts[job.name])

    def _do_submission(self, job_scripts=None, hold=False):
        if job_scripts is None or not job_scripts:
            job_scripts = self._job_wrapped_scripts
        super(JobPackageSimpleWrapped, self)._do_submission(job_scripts, hold=hold)


class JobPackageArray(JobPackageBase):
    """
    Class to manage an array-based package of jobs to be submitted by autosubmit
    """

    def __init__(self, jobs):
        self._job_inputs = {}
        self._job_scripts = {}
        self._common_script = None
        self._array_size_id = "[1-" + str(len(jobs)) + "]"
        self._wallclock = '00:00'
        self._num_processors = '0'
        for job in jobs:
            if job.wallclock > self._wallclock:
                self._wallclock = job.wallclock
            if job.processors > self._num_processors:
                self._num_processors = job.processors
        super(JobPackageArray, self).__init__(jobs)

    def _create_scripts(self, configuration):
        timestamp = str(int(time.time()))
        for i in range(0, len(self.jobs)):
            self._job_scripts[self.jobs[i].name] = self.jobs[i].create_script(configuration)
            self._job_inputs[self.jobs[i].name] = self._create_i_input(timestamp, i)
        self._common_script = self._create_common_script(timestamp)

    def _create_i_input(self, filename, index):
        filename += '.{0}'.format(index)
        input_content = self._job_scripts[self.jobs[index].name]
        open(os.path.join(self._tmp_path, filename), 'wb').write(input_content)
        os.chmod(os.path.join(self._tmp_path, filename), 0o755)
        return filename

    def _create_common_script(self, filename =""):
        script_content = self.platform.header.array_header(filename, self._array_size_id, self._wallclock,
                                                           self._num_processors,
                                                           directives=self.platform.custom_directives)
        filename += '.cmd'
        open(os.path.join(self._tmp_path, filename), 'wb').write(script_content)
        os.chmod(os.path.join(self._tmp_path, filename), 0o755)
        return filename

    def _send_files(self):
        for job in self.jobs:
            self.platform.send_file(self._job_scripts[job.name])
            self.platform.send_file(self._job_inputs[job.name])
        self.platform.send_file(self._common_script)

    def _do_submission(self, job_scripts=None, hold=False):
        for job in self.jobs:
            self.platform.remove_stat_file(job.name)
            self.platform.remove_completed_file(job.name)

        package_id = self.platform.submit_job(None, self._common_script, hold=hold, export = self.export)

        if package_id is None or not package_id:
            return

        for i in range(0, len(self.jobs)):
            Log.info("{0} submitted", self.jobs[i].name)
            self.jobs[i].id = str(package_id) + '[{0}]'.format(i)
            self.jobs[i].status = Status.SUBMITTED            
            self.jobs[i].write_submit_time(hold=hold)


class JobPackageThread(JobPackageBase):
    """
    Class to manage a thread-based package of jobs to be submitted by autosubmit

    :param dependency: Name of potential dependency
    :type dependency: String
    """
    FILE_PREFIX = 'ASThread'

    def __init__(self, jobs, dependency=None, jobs_resources=dict(),method='ASThread',configuration=None,wrapper_section="WRAPPERS", wrapper_info= {}):
        super(JobPackageThread, self).__init__(jobs)
        if len(wrapper_info) > 0 :
            self.wrapper_type = wrapper_info[0]
            self.wrapper_policy = wrapper_info[1]
            self.wrapper_method = wrapper_info[2]
            self.jobs_in_wrapper = wrapper_info[3]
            self.extensible_wallclock = wrapper_info[4]
        else:
            self.wrapper_type = None
            self.wrapper_policy = None
            self.wrapper_method = None
            self.jobs_in_wrapper = None
            self.extensible_wallclock = 0

        self._job_scripts = {}
        # Seems like this one is not used at all in the class
        self._job_dependency = dependency
        self._common_script = None
        self._wallclock = '00:00'
        self._num_processors = '0'
        self._jobs_resources = jobs_resources
        self._wrapper_factory = self.platform.wrapper
        self.current_wrapper_section = wrapper_section
        self.inner_retrials = 0
        if configuration is not None:
            self.inner_retrials = configuration.get_retrials()
            self.export = configuration.get_wrapper_export(configuration.experiment_data["WRAPPERS"][self.current_wrapper_section])
            if self.export.lower() != "none" and len(self.export) > 0:
                for job in self.jobs:
                    if job.export.lower() != "none" and len(job.export) > 0:
                        self.export == job.export
                        break
            wr_queue = configuration.get_wrapper_queue(configuration.experiment_data["WRAPPERS"][self.current_wrapper_section])
            if wr_queue is not None and len(str(wr_queue)) > 0:
                self.queue = wr_queue
            else:
                self.queue = jobs[0].queue
            wr_partition = configuration.get_wrapper_partition(configuration.experiment_data["WRAPPERS"][self.current_wrapper_section])
            if wr_partition is not None and len(str(wr_partition)) > 0:
                self.partition = wr_partition
            else:
                self.partition = jobs[0].partition
        else:
            self.queue = jobs[0].queue
            self.partition = jobs[0].partition
        self.method = method
#pipeline
    @property
    def name(self):
        return self._name
    @property
    def _jobs_scripts(self):
        self._jobs_resources['PROCESSORS_PER_NODE'] = self.platform.processors_per_node
        jobs_scripts = []
        for job in self.jobs:
            if job.section not in self._jobs_resources:
                self._jobs_resources[job.section] = dict()
                self._jobs_resources[job.section]['PROCESSORS'] = job.processors
                self._jobs_resources[job.section]['TASKS'] = job.tasks
            try:
                jobs_scripts.append(self._job_scripts[job.name])
            except BaseException as e:
                pass
        return jobs_scripts
    @property
    def queue(self):
        if str(self._num_processors) == '1' or str(self._num_processors) == '0':
            return self.platform.serial_platform.serial_queue
        else:
            return self._queue
    @queue.setter
    def queue(self,value):
        self._queue = value
    @property
    def _project(self):
        return self._platform.project
    def set_job_dependency(self, dependency):
        self._job_dependency = dependency
    def _create_scripts(self, configuration):
        for i in range(0, len(self.jobs)):
            self._job_scripts[self.jobs[i].name] = self.jobs[i].create_script(configuration)
        self._common_script = self._create_common_script()
    def _create_common_script(self,filename=""):
        lang = locale.getlocale()[1]
        if lang is None:
            lang = locale.getdefaultlocale()[1]
            if lang is None:
                lang = 'UTF-8'
        script_content = self._common_script_content()
        script_file = self.name + '.cmd'
        open(os.path.join(self._tmp_path, script_file), 'wb').write(script_content.encode(lang))
        os.chmod(os.path.join(self._tmp_path, script_file), 0o755)
        return script_file

    def _send_files(self):
        Log.debug("Check remote dir")
        self.platform.check_remote_log_dir()
        compress_type = "w"
        output_filepath = '{0}.tar'.format("wrapper_scripts")
        if callable(getattr(self.platform, 'remove_multiple_files')):
            filenames = str()
            for job in self.jobs:
                filenames += " " + self.platform.remote_log_dir + "/" + job.name + ".cmd"
            self.platform.remove_multiple_files(filenames)
        tar_path = os.path.join(self._tmp_path, output_filepath)
        Log.debug("Compressing multiple_files")
        with tarfile.open(tar_path, compress_type) as tar:
            for job in self.jobs:
                jfile = os.path.join(self._tmp_path,self._job_scripts[job.name])
                with open(jfile, 'rb') as f:
                    info = tar.gettarinfo(jfile,self._job_scripts[job.name])
                    tar.addfile(info, f)
        tar.close()
        os.chmod(tar_path, 0o755)
        self.platform.send_file(tar_path, check=False)
        Log.debug("Uncompress - send_command")
        self.platform.send_command("cd {0}; tar -xvf {1}".format(self.platform.get_files_path(),output_filepath))
        Log.debug("Send_file: common_script")
        self.platform.send_file(self._common_script)


    def _do_submission(self, job_scripts=None, hold=False):
        if callable(getattr(self.platform, 'remove_multiple_files')):
            filenames = str()
            for job in self.jobs:
                filenames += " " + self.platform.remote_log_dir + "/" + job.name + "_STAT " + \
                             self.platform.remote_log_dir + "/" + job.name + "_COMPLETED"
            self.platform.remove_multiple_files(filenames)
        else:
            for job in self.jobs:
                self.platform.remove_stat_file(job.name)
                self.platform.remove_completed_file(job.name)
                if hold:
                    job.hold = hold

        package_id = self.platform.submit_job(None, self._common_script, hold=hold, export = self.export)

        if package_id is None or not package_id:
            return

        for i in range(0, len(self.jobs) ):
            Log.info("{0} submitted", self.jobs[i].name)
            self.jobs[i].id = str(package_id)
            self.jobs[i].status = Status.SUBMITTED            
            self.jobs[i].write_submit_time(hold=hold)

    def _common_script_content(self):
        pass
class JobPackageThreadWrapped(JobPackageThread):
    """
    Class to manage a thread-based package of jobs to be submitted by autosubmit
    """
    FILE_PREFIX = 'ASThread'

    def __init__(self, jobs, dependency=None,configuration=None,wrapper_section="WRAPPERS"):
        super(JobPackageThreadWrapped, self).__init__(jobs,configuration)
        self._job_scripts = {}
        self._job_dependency = dependency
        self._common_script = None
        self._wallclock = '00:00'
        self._num_processors = '0'
        self.threads = '1'
        self.current_wrapper_section = wrapper_section


    @property
    def name(self):
        return self._name

    @property
    def _jobs_scripts(self):
        jobs_scripts = []
        for job in self.jobs:
            jobs_scripts.append(self._job_scripts[job.name])
        return jobs_scripts

    @property
    def queue(self):
        if str(self._num_processors) == '1' or str(self._num_processors) == '0':
            return self.platform.serial_platform.serial_queue
        else:
            return self.platform.queue
    @queue.setter
    def queue(self,value):
        self._queue = value
    @property
    def _project(self):
        return self._platform.project

    def _create_scripts(self, configuration):
        for i in range(0, len(self.jobs)):
            self._job_scripts[self.jobs[i].name] = self.jobs[i].create_script(configuration)
        self._common_script = self._create_common_script()

    def _create_common_script(self,filename=""):
        script_content = self._common_script_content()
        script_file = self.name + '.cmd'
        open(os.path.join(self._tmp_path, script_file), 'wb').write(script_content)
        os.chmod(os.path.join(self._tmp_path, script_file), 0o755)
        return script_file

    def _send_files(self):
        for job in self.jobs:
            self.platform.send_file(self._job_scripts[job.name])
        self.platform.send_file(self._common_script)

    def _do_submission(self, job_scripts=None, hold=False):
        for job in self.jobs:
            self.platform.remove_stat_file(job.name)
            self.platform.remove_completed_file(job.name)
            if hold:
                job.hold = hold

        package_id = self.platform.submit_job(None, self._common_script, hold=hold, export = self.export)

        if package_id is None or not package_id:
            raise Exception('Submission failed')

        for i in range(0, len(self.jobs)):
            Log.info("{0} submitted", self.jobs[i].name)
            self.jobs[i].id = str(package_id)
            self.jobs[i].status = Status.SUBMITTED            
            self.jobs[i].write_submit_time(hold=hold)
class JobPackageVertical(JobPackageThread):
    """
    Class to manage a vertical thread-based package of jobs to be submitted by autosubmit
    :param jobs: 
    :type jobs:
    :param: dependency:
    """
    def __init__(self, jobs, dependency=None,configuration=None,wrapper_section="WRAPPERS", wrapper_info = {}):
        super(JobPackageVertical, self).__init__(jobs, dependency,configuration=configuration,wrapper_section=wrapper_section, wrapper_info = wrapper_info)
        for job in jobs:
            if int(job.processors) >= int(self._num_processors):
                self._num_processors = job.processors
            self._threads = job.threads

            self._wallclock = sum_str_hours(self._wallclock, job.wallclock)
        self._name = self._expid + '_' + self.FILE_PREFIX + "_{0}_{1}_{2}".format(str(int(time.time())) +
                                                                                  str(random.randint(1, 10000)),
                                                                                  self._num_processors,
                                                                                  len(self._jobs))

    def parse_time(self):
        format_ = "minute"
        # noinspection Annotator
        regex = re.compile(r'(((?P<hours>\d+):)((?P<minutes>\d+)))(:(?P<seconds>\d+))?')
        parts = regex.match(self._wallclock)
        if not parts:
            return
        parts = parts.groupdict()
        if int(parts['hours']) > 0 :
            format_ = "hour"
        else:
            format_ = "minute"
        time_params = {}
        for name, param in parts.items():
            if param:
                time_params[name] = int(param)
        return timedelta(**time_params),format_
    def _common_script_content(self):
        if self.jobs[0].wrapper_type == "vertical":
            #wallclock = datetime.datetime.strptime(self._wallclock, '%H:%M')
            wallclock,format_ = self.parse_time()
            if format_ == "hour":
                total = wallclock.days * 24 + wallclock.seconds / 60 / 60
            else:
                total = wallclock.days * 24 + wallclock.seconds / 60
            total = total * 1.15
            if format_ == "hour":
                hour = int(total )
                minute = int((total - int(total)) * 60.0)
                second = int(((total - int(total)) * 60 -
                              int((total - int(total)) * 60.0)) * 60.0)
            else:
                hour = 0
                minute = int(total)
                second = int((total - int(total)) * 60.0)
            wallclock_delta = datetime.timedelta(hours=hour, minutes=minute,seconds=second)
            wallclock_seconds = wallclock_delta.days * 24 * 60 * 60 + wallclock_delta.seconds
            wallclock_by_level = wallclock_seconds/(self.jobs[-1].level+1)
            if self.extensible_wallclock > 0:
                original_wallclock_to_seconds = wallclock.days * 86400.0 + wallclock.seconds
                wallclock_seconds = int(original_wallclock_to_seconds + wallclock_by_level * self.extensible_wallclock)
                wallclock_delta = datetime.timedelta(hours=0, minutes=0, seconds=wallclock_seconds)
                total = wallclock.days * 24 + wallclock.seconds / 60 / 60
                hh = int(total)
                mm = int((total - int(total)) * 60.0)
                ss = int(((total - int(total)) * 60 -
                              int((total - int(total)) * 60.0)) * 60.0)
                if hh < 10:
                    hh_str='0'+str(hh)
                else:
                    hh_str = str(hh)
                if mm < 10:
                    mm_str='0'+str(mm)
                else:
                    mm_str = str(mm)
                self._wallclock = "{0}:{1}".format(hh_str,mm_str)
                Log.info("Submitting {2} with wallclock {0}:{1}".format(hh_str,mm_str,self._name))
        else:
            wallclock_by_level = None

        return self._wrapper_factory.get_wrapper(self._wrapper_factory.vertical_wrapper, name=self._name,
                                                 queue=self._queue, project=self._project, wallclock=self._wallclock,
                                                 num_processors=self._num_processors, jobs_scripts=self._jobs_scripts,
                                                 dependency=self._job_dependency, jobs_resources=self._jobs_resources,
                                                 expid=self._expid, rootdir=self.platform.root_dir,
                                                 directives=self._custom_directives,threads=self._threads,method=self.method.lower(),retrials=self.inner_retrials, wallclock_by_level=wallclock_by_level,partition=self.partition)


class JobPackageHorizontal(JobPackageThread):
    """
    Class to manage a horizontal thread-based package of jobs to be submitted by autosubmit
    """

    def __init__(self, jobs, dependency=None, jobs_resources=dict(),method='ASThread',configuration=None,wrapper_section="WRAPPERS"):
        super(JobPackageHorizontal, self).__init__(jobs, dependency, jobs_resources,configuration=configuration,wrapper_section=wrapper_section)
        self.method = method

        self._queue = self.queue
        for job in jobs:
            if job.wallclock > self._wallclock:
                self._wallclock = job.wallclock
            self._num_processors = str(int(self._num_processors) + int(job.processors))
            self._threads = job.threads
        self._name = self._expid + '_' + self.FILE_PREFIX + "_{0}_{1}_{2}".format(str(int(time.time())) +
                                                                                  str(random.randint(1, 10000)),
                                                                                  self._num_processors,
                                                                                  len(self._jobs))
        self._jobs_resources = jobs_resources

    def _common_script_content(self):
        return self._wrapper_factory.get_wrapper(self._wrapper_factory.horizontal_wrapper, name=self._name,
                                                 queue=self._queue, project=self._project, wallclock=self._wallclock,
                                                 num_processors=self._num_processors, jobs_scripts=self._jobs_scripts,
                                                 dependency=self._job_dependency, jobs_resources=self._jobs_resources,
                                                 expid=self._expid, rootdir=self.platform.root_dir,
                                                 directives=self._custom_directives,threads=self._threads,method=self.method.lower(),partition=self.partition)

class JobPackageHybrid(JobPackageThread):
    """
        Class to manage a hybrid (horizontal and vertical) thread-based package of jobs to be submitted by autosubmit
        """

    def __init__(self, jobs, num_processors, total_wallclock, dependency=None, jobs_resources=dict(),method="ASThread",configuration=None,wrapper_section="WRAPPERS"):
        all_jobs = [item for sublist in jobs for item in sublist] #flatten list
        super(JobPackageHybrid, self).__init__(all_jobs, dependency, jobs_resources,method,configuration=configuration,wrapper_section=wrapper_section)
        self.jobs_lists = jobs
        self.method=method
        self._num_processors = int(num_processors)
        self._threads = all_jobs[0].threads
        self._wallclock = total_wallclock
        self._name = self._expid + '_' + self.FILE_PREFIX + "_{0}_{1}_{2}".format(str(int(time.time())) +
                                                                                  str(random.randint(1, 10000)),
                                                                                  self._num_processors,
                                                                                  len(self._jobs))

    @property
    def _jobs_scripts(self):
        self._jobs_resources['PROCESSORS_PER_NODE'] = self.platform.processors_per_node

        jobs_scripts = []
        for job_list in self.jobs_lists:
            inner_jobs = list()
            for job in job_list:
                inner_jobs.append(job.name + '.cmd')
                if job.section not in self._jobs_resources:
                    self._jobs_resources[job.section] = dict()
                    self._jobs_resources[job.section]['PROCESSORS'] = job.processors
                    self._jobs_resources[job.section]['TASKS'] = job.tasks
            jobs_scripts.append(inner_jobs)
        return jobs_scripts


class JobPackageVerticalHorizontal(JobPackageHybrid):

    def _common_script_content(self):
        return self._wrapper_factory.get_wrapper(self._wrapper_factory.hybrid_wrapper_vertical_horizontal,
                                                 name=self._name, queue=self._queue, project=self._project,
                                                 wallclock=self._wallclock, num_processors=self._num_processors,
                                                 jobs_scripts=self._jobs_scripts, dependency=self._job_dependency,
                                                 jobs_resources=self._jobs_resources, expid=self._expid,
                                                 rootdir=self.platform.root_dir, directives=self._custom_directives,threads=self._threads,method=self.method.lower(),partition=self.partition)


class JobPackageHorizontalVertical(JobPackageHybrid):

    def _common_script_content(self):
        return self._wrapper_factory.get_wrapper(self._wrapper_factory.hybrid_wrapper_horizontal_vertical,
                                                 name=self._name, queue=self._queue, project=self._project,
                                                 wallclock=self._wallclock, num_processors=self._num_processors,
                                                 jobs_scripts=self._jobs_scripts, dependency=self._job_dependency,
                                                 jobs_resources=self._jobs_resources, expid=self._expid,
                                                 rootdir=self.platform.root_dir, directives=self._custom_directives,threads=self._threads,method=self.method.lower(),partition=self.partition)

