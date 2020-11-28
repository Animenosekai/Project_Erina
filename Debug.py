print("Initializing the server")
from ErinaWebsite.Server import ErinaServer

## RECORDING Endpoints
print("Initializing Static")
from ErinaWebsite.Erina import Static
print("Initializing API")
from ErinaWebsite.Erina.api import API
print("Initializing Admin")
from ErinaWebsite.Erina.admin import Admin
print("Initializing Auth")
from ErinaWebsite.Erina.auth import Auth
print("Initializing Custom")
from ErinaWebsite import Custom


print("Running the server")
## RUNNING ErinaServer (HTTP)
ErinaServer.run("127.0.0.1", "5000", True)