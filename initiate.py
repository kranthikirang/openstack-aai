#!/usr/bin/python

import sys
import json
from aai_client import *
from openstack_client import *

data = {"domain_id": "default", "user_name": "admin", "password": "password", "project_name": "onap"}
keystone_token = keystone_auth("keystone.openstack.svc.cluster.local", "80", "v3", **data)
payload = keystone_token.auth_body()
token = keystone_token.get_token(payload)
print json.dumps(token, indent=4, sort_keys=True)

openstack_projects = openstack_keystone("keystone.openstack.svc.cluster.local", "80", "v3", token)
projects = openstack_projects.get_projects()
#default_project_list = ["service", "6380aaf753714bed8409769337900f4f-4ef2c3df-6792-4071-9e24-ac7e7ea"] #We don't need service and heat stack projects to be in AAI but we can make that also happen
default_project_list = ["services"] #We don't need service and heat stack projects to be in AAI but we can make that also happen
#print json.dumps(projects, indent=4, sort_keys=True)
filtered_projects = []
for project in projects:
	if not project["name"] in default_project_list:
		filtered_projects.append(project)
print json.dumps(filtered_projects, indent=4, sort_keys=True)

getdict = {"ip":"10.10.230.4", "port":"30233", "version":"/aai/v11/"}
tenant_dict={"cloud_name":"RegionOne", "cloud_owner":"CloudOwner", "customer_id": "Demonstration"}

url_part = resource2url_part("tenants", **tenant_dict)
getdict["url_part"] = url_part
url = geturlconstruct(**getdict)
print url
response = aaiget(url)
#print json.dumps(response, indent=4, sort_keys=True)
aai_project_list=[]
for tenant in response["tenant"]:
       #aai_project_list[tenant["tenant-name"]] = tenant["tenant-id"]
       aai_project_list.append(dict({"name": tenant["tenant-name"], "id": tenant["tenant-id"], "resource-version": tenant["resource-version"]})) 
print json.dumps(aai_project_list, indent=4, sort_keys=True)

projects_to_add = []
for project in filtered_projects:
	y = project["id"]
	if filter(lambda project: project["id"] == y, aai_project_list):
		print "Project %s exists in AAI" % project["name"]
	else:
		projects_to_add.append(dict({"name": project["name"], "id": project["id"]}))
print "Projects to be added are %s" % json.dumps(projects_to_add, indent=4, sort_keys=True)

projects_to_delete = []
for project in aai_project_list:
	y = project["id"]
	if filter(lambda project: project["id"] == y, filtered_projects):
		print "Project %s is up to date" % project["name"]
	else:
		projects_to_delete.append(dict({"name": project["name"], "id": project["id"], "resource-version": project["resource-version"]}))
print "Project to be deleted are %s" % json.dumps(projects_to_delete, indent=4, sort_keys=True)

#get the AAI services
getdict = {"ip":"10.10.230.4", "port":"30233", "version":"/aai/v11/"}
tenant_dict={"cloud_name":"RegionOne", "cloud_owner":"CloudOwner", "customer_id": "Demonstration"}
url_part = resource2url_part("services", **tenant_dict)
getdict["url_part"] = url_part
url = geturlconstruct(**getdict)
print url
response = aaiget(url)
service_list=[]
for service in response["service"]:
  service_list.append(service["service-description"])
print json.dumps(service_list)

for project in projects_to_add:
	print project
        tenant_dict={"cloud_name":"RegionOne", "cloud_owner":"CloudOwner", "customer_id": "Demonstration", "tenant_name": project["name"], "tenant_id": project["id"], "related-to": "service-subscription", "relationship-value": service_list}
	url_part = resource2url_part("tenant", **tenant_dict)
	getdict["url_part"] = url_part
	url = geturlconstruct(**getdict)
	print url
	payload = construct_body("tenant", **tenant_dict)
	response = aaiput(url, payload, update=False, **tenant_dict)
	print response
print "Following list of tenants uploded to AAI %s" % projects_to_add

for project in projects_to_delete:
	tenant_dict={"cloud_name":"RegionOne", "cloud_owner":"CloudOwner", "customer_id": "Demonstration", "tenant_name": project["name"], "tenant_id": project["id"]}
	url_part = resource2url_part("tenant", **tenant_dict)
        getdict["url_part"] = url_part
        url = geturlconstruct(**getdict)
        print url
	payload = construct_body("tenant", **tenant_dict)
	response = aaidelete(url, project["resource-version"], "tenant")
        print response
print "Following list of tenants deleted in AAI %s" % projects_to_delete


#def get_openstackendpoints():
#   openstack_endpoints = openstack_keystone("keystone.openstack.svc.kubespray.byond.com", "80", "v3", token)
#   endpoints = openstack_endpoints.get_endpoints()
#   return endpoints
   #print json.dumps(endpoints, indent=4, sort_keys=True)

#endpoints = get_openstackendpoints()
#print endpoints
#for endpoint in endpoints:
#	print endpoint["url"]
