#!/usr/bin/python
from suds.client import Client
from suds.wsse import Security, UsernameToken
#
import sys
#For basic logging
import logging
logging.basicConfig()
#Uncomment to debug SOAP XML
#logging.getLogger('suds.client').setLevel(logging.DEBUG)
#logging.getLogger('suds.transport').setLevel(logging.DEBUG)
#
#getFileContents result requires decompress and decoding
import base64, zlib
#
# -----------------------------------------------------------------------------
class WebServiceClient:
    def __init__(self, webservice_type, host, port, ssl, username, password):
        url = ''
        if (ssl):
            url = 'https://' + host + ':' + port
        else:
            url = 'http://' + host + ':' + port
        if webservice_type == 'configuration':
            self.wsdlFile = url + '/ws/v9/configurationservice?wsdl'
        elif webservice_type == 'defect':
            self.wsdlFile = url + '/ws/v9/defectservice?wsdl'
        else:
            raise "unknown web service type: " + webservice_type

        self.client = Client(self.wsdlFile)
        self.security = Security()
        self.token = UsernameToken(username, password)
        self.security.tokens.append(self.token)
        self.client.set_options(wsse=self.security)

    def getwsdl(self):
        print(self.client)

# -----------------------------------------------------------------------------
class DefectServiceClient(WebServiceClient):
    def __init__(self, host, port, ssl, username, password):
        WebServiceClient.__init__(self, 'defect', host, port, ssl, username, password)

# -----------------------------------------------------------------------------
class ConfigServiceClient(WebServiceClient):
    def __init__(self, host, port, ssl, username, password):
        WebServiceClient.__init__(self, 'configuration', host, port, ssl, username, password)
    def getProjects(self):
        return self.client.service.getProjects()

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    host = '<hostname>'
    port = '<port on hostname>'
    ssl = False #True
    username = '<username>' #sys.argv[1]
    password = '<password>' #sys.argv[2]
    #
    #cid=<id number>

    #defectServiceClient = DefectServiceClient(host, port, ssl, username, password)
    configServiceClient = ConfigServiceClient(host, port, ssl, username, password)

#
#--------configservice calls---------------------------
#
configServiceClient.client.service.createProject({"description": description , "name": name })
    type = sys.argv[3]
    if(type == '-p' or type == '--project'):
        name = sys.argv[4]
        description = sys.argv[5]
        if not description:
            description = 'project created using script'

        if name:
            configServiceClient.client.service.createProject({'description': description, 'name': name})
        else:
            print('Error : invalid project name passed to script')
            print('script usage : ')
            print('python [scriptname] [user] [password] [-p|--project for project] [project name to be created] [description of the project]')
            #p = configServiceClient.client.service.getProjects(name)
            #print(v)
    elif(type == '-s' or type == '--stream'):
        projectName = sys.argv[4]
        streamName = sys.argv[5]
        description = sys.argv[5]
        if not description:
           description = 'stream created using script'

        language = sys.argv[6]
        if not language:
           language = "MIXED"

        triageStoreName = sys.argv[7]
        if not triageStoreName:
           triageStoreName = 'Default Triage Store'

        triageStoreIdVal = configServiceClient.client.service.getTriageStores({'namePattern': triageStoreName})
        project = configServiceClient.client.service.getProjects({'namePattern': projectName})
        configServiceClient.client.service.createStreamInProject({'name': project[0].id.name}, {'name': streamName, 'language': language, 'description': description, 'triageStoreId': triageStoreIdVal[0].id})
    else:
        print("Error: invalid input type")
