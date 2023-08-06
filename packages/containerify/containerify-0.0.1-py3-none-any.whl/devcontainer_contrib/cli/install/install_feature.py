from typing import Dict, Union, Optional
import os
from devcontainer_contrib.models.devcontainer_feature_definition import (
    FeatureDefinition,
)
import tempfile
from pathlib import Path
from devcontainer_contrib.settings import DContainerSettings
from devcontainer_contrib.utils.feature_oci import FeatureOCI
import psutil
import invoke


import logging
logger = logging.getLogger(__name__)


def install_feature(
    feature: str,
    options: Dict[str, str],
    remote_user: Optional[str] = None
) -> None:
    
    if remote_user not in psutil.users():

    with tempfile.TemporaryDirectory() as tempdir:
        tempdir_path = Path(tempdir)
        feature_dir = tempdir_path.joinpath("feature")
        feature_dir.mkdir(parents=True, exist_ok=True)    

        feature_obj = FeatureOCI(feature).get_devcontainer_feature_obj()

        feature_definition = FeatureDefinition.parse_obj(feature_obj)
    
        FeatureOCI(feature).download_and_extract(feature_dir)


        for option_name, option_obj in feature_definition.options.items():
            if option_name not in options:
                options[option_name] = option_obj.__root__.default

        env_variables_cmd = " ".join([f"{option_name.upper()}={option_value}" for option_name, option_value in options.items()])

        # resolve _REMOTE_USER and _REMOTE_USER_HOME
        # add env variables to /etc/environment (or another method to make sure its available in the final container)

        response = invoke.run(f"cd {feature_dir} && \
                              chmod +x ./install.sh && \
                              sudo {env_variables_cmd} bash -i ./install.sh")

    print(feature)
    print(args)
