# Copyright (c) 2017-2021, NVIDIA CORPORATION.  All rights reserved.

"""TAO Toolkit instance handler for launching jobs on Whl based non-docker instances."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os
import sys
import subprocess

from tlt.components.instance_handler.base_instance import TLTInstance
from tlt.components.instance_handler.utils import (
    load_config_file,
)
from tlt.components.types.task import Task

logger = logging.getLogger(__name__)


class WHLInstance(TLTInstance):
    """Instance handler class to define a TAO Toolkit instance."""

    def __init__(self, task_map, config_path):
        """Initialize a Wheel based TAO Toolkit instance.

        Args:
            task_map(dict): Dictionary of task name to Task data structure.
        """
        super(WHLInstance, self).__init__(
            task_map=task_map,
        )
        self.current_config_path = config_path
        logger.debug("Current config file imported from: {}".format(
            self.current_config_path
        ))

    @staticmethod
    def load_config(config_path):
        """Function to load the json config file.

        Args:
            config_path(str): Unix style path to the config file.

        Returns:
            config_data(dict): Parsed config data.
        """
        data = load_config_file(config_path)
        return data

    @staticmethod
    def parse_launcher_config(config_data):
        """Parse launcher configuration data based on format version.

        Args:
            data(dict): Data containing configuration parameters for the launcher instance

        Returns:
            task_map(dict): Dictionary of tasks mapped to the respective dockers.
        """
        if "format_version" not in config_data.keys():
            raise KeyError("format is a required key in the launcher config.")

        task_map = {}
        if config_data["format_version"] == 1.0:
            for image in list(config_data["dockers"].keys()):
                logger.debug("Processing {}".format(image))
                docker_data = config_data["dockers"][image]
                if "tasks" not in list(docker_data.keys()):
                    raise NotImplementedError(
                        "The config data must contain tasks associated with the "
                        "respective docker."
                    )
                task_map.update({
                    task: Task(
                        name=task,
                    ) for task in docker_data["tasks"]
                })
        elif config_data["format_version"] == 2.0:
            for image in list(config_data["dockers"].keys()):
                logger.debug("Processing {}".format(image))
                docker_data = config_data["dockers"][image]
                if not isinstance(docker_data, dict):
                    raise("Invalid format.")
                task_map.update({
                    task: Task(
                        name=task,
                    ) for tag in docker_data.keys() for task in docker_data[tag]["tasks"]
                })
        else:
            raise NotImplementedError("Invalid format type: {}".format(config_data["format_version"]))
        return task_map

    @classmethod
    def from_config(cls, config_path):
        """Instantiate a TAO Toolkit instance from a config file.

        Args:
            config_path(str): Path to the launcher config file.

        Returns:
            Initialized WHLInstance object.
        """
        config_data = cls.load_config(config_path)
        task_map = cls.parse_launcher_config(config_data)
        debug_string = ""
        for task_name, task in task_map.items():
            debug_string += f"{task_name}: {str(task)}\n"
        logger.debug(debug_string)
        return WHLInstance(
            task_map,
            config_path
        )

    def launch_command(self, task, args):
        """Launch command for tasks.

        Args:
            task(str): Name of the task from the entrypoint.
            args(list): List of args to the task.

        Returns:
            No explicit returns.
        """
        if task in list(self.task_map.keys()):
            assert isinstance(args, list), (
                "The arguments must be given as a list to be passed. "
                "Got a {} instead".format(
                    type(args)
                )
            )
            if args:
                command = ""
                if args[0] == "run":
                    args.pop(0)
                else:
                    command = "{} ".format(task)
                command += " ".join(args)
            else:
                logger.info(
                    "No commands provided to the launcher\n"
                    "Listing the help options "
                    "when you exit."
                )
                command += " -h"
            try:
                subprocess.check_call(
                    command,
                    shell=True,
                    stdout=sys.stdout,
                    env=os.environ
                )
            except subprocess.CalledProcessError as e:
                if e.output is not None:
                    print("TLT command run failed with error: {}".format(e.output))
                    sys.exit(-1)
        else:
            raise NotImplementedError(
                "Task asked for wasn't implemented to run on WHL instance. {}".format(task))
