from safeIO import JSONFile
from Erina.env_information import erina_dir

configFile = JSONFile(erina_dir + "/Erina/_config/config.json")
defaultFile = JSONFile(erina_dir + "/Erina/_config/default.json")