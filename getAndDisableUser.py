#!/usr/bin/python
from suds.client import Client
from suds.wsse import Security, UsernameToken
import sys
import logging
logging.basicConfig()
#Uncomment to debug SOAP XML
#logging.getLogger('suds.client').setLevel(logging.DEBUG)
#logging.getLogger('suds.transport').setLevel(logging.DEBUG)
#
#getFileContents result requires decompress and decoding
import base64, zlib
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
    host = '<hostname>
    port = '<port>'
    ssl = True #False 
    username = sys.argv[1]
    password = sys.argv[2]
    #
    #cid=<cid number>

    #defectServiceClient = DefectServiceClient(host, port, ssl, username, password)
    configServiceClient = ConfigServiceClient(host, port, ssl, username, password)
    
#--------configservice calls---------------------------
    v = configServiceClient.client.service.getUser(sys.argv[3])
    print v.username
    if(v):
      v.__setattr__('disabled',True)
      configServiceClient.client.service.updateUser(v.username,v)

    #verify if the user has been disabled now
    u = configServiceClient.client.service.getUser(sys.argv[3])
    if(u.disabled):
       print "User disabled successfully :",sys.argv[3]
