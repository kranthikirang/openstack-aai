#!/usr/bin/python

import sys
import json
import requests
from aai_client import *
#import logging

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
#try:
#    import http.client as http_client
#except ImportError:
    # Python 2
#    import httplib as http_client
#http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
#logging.basicConfig()
#logging.getLogger().setLevel(logging.DEBUG)
#requests_log = logging.getLogger("requests.packages.urllib3")
#requests_log.setLevel(logging.DEBUG)
#requests_log.propagate = True

class keystone_auth:
     def __init__(self, host, port, version, **kwargs):
        self.host = host
	self.port = port
 	self.version = version
	self.kwargs = kwargs
	self.headers = {"Accept":"application/json", "Content-type":"application/json"}
	if version == "v3":
		#self.url = "http://keystone.openstack.svc.kubespray.byond.com:80/v3/auth/tokens"
		#self.url = "https://" + self.host + ":" + self.port + "/v3/auth/tokens"
		self.url = "http://" + self.host + ":" + self.port + "/v3/auth/tokens"
	else:
		#self.url = "https://" + self.host + ":" + self.port + "/v2.0/tokens"
		self.url = "http://" + self.host + ":" + self.port + "/v2.0/tokens"
	
     def auth_body(self):
        if self.version == "v3":
	  payload = {}
	  domain = {}
	  #domain["id"] = "default"
	  domain["id"] = self.kwargs["domain_id"]
	  password = {}
	  user = {}
	  #user["name"] = "admin"
	  user["name"] = self.kwargs["user_name"]
	  #user["password"] = "password"
	  user["password"] = self.kwargs["password"]
	  user["domain"] = domain
	  password["user"] = user

	  identity = {}
	  methods_list=["password"]
	  identity["methods"] = methods_list
	  identity["password"] = password
	  project = {}
	  #project["name"] = "admin"
	  project["name"] = self.kwargs["project_name"]
	  project["domain"] = domain
	  scope = {}
	  scope["project"] = project
	  auth = {}
	  auth["identity"] = identity
	  auth["scope"] = scope
	  payload["auth"] = auth
	  payload = json.dumps(payload)
 	  print payload
	  return payload
	  #sys.exit(2)

	  #payload = { "auth": { "identity": { "methods": ["password"], "password": { "user": { "name": "admin", "domain": { "id": "default" }, "password": "password" } } } } }
	  #payload = json.dumps(payload)
	  #print payload
        else:
          payload = {}
          credentials = {}
          credentials["username"] = self.kwargs["user_name"]
          credentials["password"] = self.kwargs["password"]
          auth = {}
          auth["passwordCredentials"] = credentials
          auth["tenantName"] = self.kwargs["project_name"]
          payload["auth"] = auth
          #payload = {"auth": {"tenantName": "onap", "passwordCredentials": {"username": "m19866", "password": "p3MQ7X4C94z2aE"}}}
          payload = json.dumps(payload)
          print payload
          return payload
          

     def get_token(self, payload):
        if self.version == "v3":
          response = requests.post(self.url, payload, headers=self.headers, verify=False)
	  response_headers = response.headers
	  response_code=response.status_code
	  print response_headers
          print response
	  response = json.loads(response.text)
	  token = response_headers["X-Subject-Token"]
	  #print token
	  #print response_code
	  return token
        else:
          response = requests.post(self.url, payload, headers=self.headers, verify=False)
          response = json.loads(response.text)
          token = response["access"]["token"]["id"]
          #print token
          return token

class openstack_keystone:
    def __init__(self, host, port, version, token, **kwargs):
	self.host = host
	self.port = port
	self.version = version
        self.kwargs = kwargs
        self.headers = {"Accept":"application/json", "Content-type":"application/json", "X-Auth-Token": token}
	#self.url = "https://" + self.host + ":" + self.port
	self.url = "http://" + self.host + ":" + self.port
        if version == "v3":
                self.url = self.url + "/v3"
        elif version == "v2.0":
                self.url = self.url + "/v2.0"
	else:
		self.url = self.url + version

    def get_projects(self):
	if self.version == "v3":
		self.url = self.url + "/projects"
                response = requests.get(self.url, headers=self.headers, verify=False)
	        response_headers = response.headers
        	response_code=response.status_code
	        print response_code
	        print response_headers
	        response = json.loads(response.text)
	        return response["projects"]
	else:
		self.url = self.url + "/tenants"
		response = requests.get(self.url, headers=self.headers, verify=False)
		response_headers = response.headers
		response_code=response.status_code
		print response_code
		print response_headers
		response = json.loads(response.text)
		return response["tenants"]
   
    def get_endpoints(self):
	self.url = self.url + "/endpoints"
	response = requests.get(self.url, headers=self.headers, verify=False)
        response_headers = response.headers
        response_code=response.status_code
        print response_code
        print response_headers
        response = json.loads(response.text)
        return response["endpoints"]

class openstack:
    def __init__(self, endpoint, resource, token, **kwargs):
	self.endpoint = endpoint
	self.resource = resource
        self.headers = {"Accept":"application/json", "Content-type":"application/json", "X-Auth-Token": token}
	self.kwargs = kwargs

    def get_vservers(self):
	response = requests.get(self.endpoint, headers=self.headers, verify=False)
        response_headers = response.headers
        response_code=response.status_code
        print response_code
        print response_headers
        response = json.loads(response.text)

