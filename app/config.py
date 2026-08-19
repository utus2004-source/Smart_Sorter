import yaml
from pathlib import Path

# Project root, used so that paths do not depend on the current working directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"
DEFAULT_CLASSES_PATH = PROJECT_ROOT / "config" / "classes.yaml"


class Config:
    # Responsibilities:
    # - Load the configuration files
    # - Expose every section to the components
    # - Resolve file paths against the project root

    def __init__(self, config_path=DEFAULT_CONFIG_PATH, classes_path=DEFAULT_CLASSES_PATH):

        with open(config_path, "r") as config_file:
            data = yaml.safe_load(config_file)

        with open(classes_path, "r") as classes_file:
            classes_data = yaml.safe_load(classes_file)

        self.camera = data["camera"]
        self.model = data["model"]
        self.roi = data["roi"]
        self.stabilization = data["stabilization"]
        self.decision_filter = data["decision_filter"]
        self.display = data["display"]
        self.communication = data["communication"]

        # Class name -> bin number
        self.classes = classes_data["classes"]

        # Make the model path independent of the working directory
        self.model["path"] = str(PROJECT_ROOT / self.model["path"])
