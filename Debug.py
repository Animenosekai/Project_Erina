print("Initializing Erina configuration")
from Erina.config import Server as ServerConfig
print("Initializing the server")
from ErinaServer.Server import ErinaServer

## RECORDING Endpoints
print("Initializing Static")
from ErinaServer.Erina import Static
print("Initializing API")
from ErinaServer.Erina.api import API
print("Initializing Admin")
from ErinaServer.Erina.admin import Admin
print("Initializing Auth")
from ErinaServer.Erina.auth import Auth
print("Initializing Config")
from ErinaServer.Erina.admin import Config
print("Initializing Custom")
from ErinaServer import Custom


print("Running the server")
## RUNNING ErinaServer (HTTP)
ErinaServer.run(ServerConfig.host, ServerConfig.port, True)