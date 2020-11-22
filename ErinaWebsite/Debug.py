from ErinaWebsite.Server import ErinaServer
from ErinaWebsite.Erina.api import API
from ErinaWebsite.Erina.admin import Admin
from ErinaWebsite.Erina.auth import Auth
from ErinaWebsite import Custom

ErinaServer.run("127.0.0.1", "5000", True)