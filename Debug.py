print("Initializing the server")
from ErinaWebsite.Server import ErinaServer

## RECORDING Endpoints
print("Importing Static")
from ErinaWebsite.Erina import Static
#print("Importing API")
#from ErinaWebsite.Erina.api import API
print("Importing Admin")
from ErinaWebsite.Erina.admin import Admin
print("Importing Auth")
from ErinaWebsite.Erina.auth import Auth
print("Importing Custom")
from ErinaWebsite import Custom

print("Running the server")
## RUNNING ErinaServer (HTTP)
ErinaServer.run("127.0.0.1", "5000", True)