# Copyright (c) 2017-2021, NVIDIA CORPORATION.  All rights reserved.

"""Returns Docker or WHL instance with their supported tasks."""

import os

from tlt.components.instance_handler.base_instance import INSTANCE_HANDLER_TASKS as CLI_TASKS

if os.environ.get('TAO_DOCKER_DISABLE', '0') != '0':
    from tlt.components.instance_handler.whl_instance import WHLInstance
else:
    from tlt.components.instance_handler.local_instance import LocalInstance


def get_launcher(launcher_config_file):
    """Choose between WHL and Docker based instance.

    Args: launcher_config_file.
    Returns: Instance along with the supported tasks.
    """
    assert os.environ.get('TAO_DOCKER_DISABLE', '0') in ['0', '1'], 'Invalid value for TAO_DOCKER_DISABLE'
    if os.environ.get('TAO_DOCKER_DISABLE', '0') == '1':
        instance = WHLInstance.from_config(launcher_config_file)
        supported_tasks = [*instance.dl_tasks]
    else:
        instance = LocalInstance.from_config(launcher_config_file)
        supported_tasks = [*CLI_TASKS, *instance.dl_tasks]
    return instance, supported_tasks
