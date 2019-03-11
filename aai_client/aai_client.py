#!/usr/bin/python

import argparse
import json
import sys
import requests
import time

class key_error:
    def __init__(self, error):
   	 self.error = error
	 print "Requires an attribute %s" % self.error
	 sys.exit(2)

def geturlconstruct(**kwargs):
    url = 'https://' + kwargs["ip"] + ":" + kwargs["port"] + kwargs["version"] + kwargs["url_part"]
    return url

class Makerelationship:
    #def __init__(self, relationship_key, related_to, relationship_value, customer_id="Demonstration", cloud_owner="CloudOwner", complex_name="clli1"):
    def __init__(self, relationship_key, property_key=[], **kwargs):
	self.slash = "/"
	self.relationship_key = relationship_key
	self.property_key = property_key
	if "related-to" in kwargs:
		self.related_to = kwargs["related-to"]
	try:
	   if "relationship-value" in kwargs:
		self.relationship_value = kwargs["relationship-value"]
	except AttributeError as e:
		pass
	print self.relationship_value
	if "customer_id" in kwargs:
	        self.customer_id = kwargs["customer_id"]
	if "cloud_owner" in kwargs:
	        self.cloud_owner = kwargs["cloud_owner"]
	if "cloud_name" in kwargs:
	        self.cloud_name = kwargs["cloud_name"]
	if "tenant_id" in kwargs:
	        self.tenant_id = kwargs["tenant_id"]
	if "tenant_name" in kwargs:
	        self.tenant_name = kwargs["tenant_name"]
    def make_relationship(self):
	relationship_list = {}
	try:
		for value in self.relationship_value:
			relationship = {}
			relationship_data = []
			if self.related_to == "service-subscription":
				relationship["related-to"] = self.related_to
				relationship["related-link"] = "/aai/v11/business/customers/customer/Demonstration/service-subscriptions/service-subscription/" + value
				relationship_data.append(dict({"relationship-key": self.relationship_key[0], "relationship-value": self.customer_id}))
				relationship_data.append(dict({"relationship-key": self.relationship_key[1], "relationship-value": value}))
				relationship["relationship-data"] = relationship_data
				relationship_list.setdefault("relationship", []).append(relationship)
			elif self.related_to == "cloud-region":
				relationship_list["related-to"] = self.related_to
				relationship_list["related-link"] = "/aai/v11/cloud-infrastructure/cloud-regions/cloud-region/" + self.cloud_owner + self.slash + self.cloud_name
				relationship_data.append(dict({"relationship-key": self.relationship_key[0], "relationship-value": self.cloud_owner}))
				relationship_data.append(dict({"relationship-key": self.relationship_key[1], "relationship-value": value}))	
				relationship_list["relationship-data"] = relationship_data
	except AttributeError as e:
		relationship_list = {}
		relationship = {}
                relationship_data = []
		related_to_property = []
		if self.related_to == "tenant":
			relationship["related-to"] = self.related_to
			relationship["related-link"] = "/aai/v11/cloud-infrastructure/cloud-regions/cloud-region/" + self.cloud_owner + self.slash + self.cloud_name + "/tenants/tenant/" + self.tenant_id
			relationship_data.append(dict({"relationship-key": self.relationship_key[0], "relationship-value":  self.cloud_owner}))
			relationship_data.append(dict({"relationship-key": self.relationship_key[1], "relationship-value": self.cloud_name}))
			relationship_data.append(dict({"relationship-key": self.relationship_key[2], "relationship-value": self.tenant_id}))
			relationship["relationship-data"] = relationship_data
			related_to_property.append(dict({"property-key": self.property_key[0], "property-value": self.tenant_name}))
			relationship["related-to-property"] = related_to_property
			relationship_list.setdefault("relationship", []).append(relationship)
	#print json.dumps(relationship_list, indent=4, sort_keys=True)
	return relationship_list

def construct_patch_body(resource, patch, **kwargs):
    """
    construct the body for patching a resource based on arguments
    """
    if patch == "relationship" and resource == "complex":
    	try:
		jsonPayload = {}
		related_to_property = []
		related_to_property.append(dict({"property-key": "cloud-region.owner-defined-type", "property-value": "OwnerType"}))		
		jsonPayload["related-to-property"] = related_to_property
	except KeyError as e:
                key_error(str(e))				    
    	if "related-to" in kwargs:
       		try:
                        relationship_key = ["cloud-region.cloud-owner", "cloud-region.cloud-region-id"]
                        #complex_relation = Makerelationship(relationship_key, kwargs["related-to"], kwargs["relationship-value"], kwargs["cloud_name"], kwargs["cloud_owner"])
                        complex_relation = Makerelationship(relationship_key, **kwargs)
                        relationship = complex_relation.make_relationship()
			jsonPayload.update(relationship)
			print json.dumps(jsonPayload, indent=4, sort_keys=True)
			jsonPayload = json.dumps(jsonPayload)
		except KeyError as e:
			key_error(str(e))
    else:
	print TBD
    return jsonPayload

def construct_body(resource, **kwargs):
    """
    construct the body based on resource and arguments
    """
    if resource == "service-subscription":
	try:
		jsonPayload = json.dumps({"service-type": kwargs["service_type"]})	
	except KeyError as e:
		key_error(str(e))
    elif resource == "customer":
	try:
		jsonPayload = {}
		jsonPayload["global-customer-id"] = kwargs["customer_id"]
		jsonPayload["subscriber-name"] = kwargs["customer_id"]
		try:
			jsonPayload["subscriber-type"] = kwargs["customer_type"]
		except KeyError:
			jsonPayload["subscriber-type"] = "INFRA"
	except KeyError as e:
                key_error(str(e))
 	if "related-to" in kwargs:
		try:
			relationship_list = {}
			relationship_key = ["cloud-region.cloud-owner", "cloud-region.cloud-region-id", "tenant.tenant-id"]
			property_key = ["tenant.tenant-name"]
			tenant_relation = Makerelationship(relationship_key, property_key, **kwargs)
			jsonPayload["relationship-list"] = tenant_relation.make_relationship()
                        print json.dumps(jsonPayload, indent=4, sort_keys=True)
                        jsonPayload = json.dumps(jsonPayload)		
		except KeyError as e:
                        key_error(str(e))
	else:
                print json.dumps(jsonPayload, indent=4, sort_keys=True)
                jsonPayload = json.dumps(jsonPayload)
    elif resource == "cloud-region":
	try:
		jsonPayload = {}
		tenant = {}
		jsonPayload["cloud-owner"] = kwargs["cloud_owner"]
	  	jsonPayload["cloud-region-id"] = kwargs["cloud_name"]	
		jsonPayload["cloud-type"] = kwargs["cloud_type"]
		jsonPayload["owner-defined-type"] = "owner type"
		jsonPayload["cloud-region-version"] = "v2.5"
		jsonPayload["cloud-zone"] = kwargs["cloud_zone"]
		tenant["tenant-id"] = kwargs["tenant_id"]
		tenant["tenant-name"] = kwargs["tenant_name"]
	except KeyError as e:
        	key_error(str(e))
	if "related-to" in kwargs:
		try:
			relationship_list = {}
			relationship_key = ["customer.global-customer-id", "service-subscription.service-type"]
			#service_subscription_relation = Makerelationship(relationship_key, kwargs["related-to"],kwargs["relationship-value"],kwargs["customer_id"])
			service_subscription_relation = Makerelationship(relationship_key, **kwargs)
			tenant["relationship-list"] = service_subscription_relation.make_relationship()
			jsonPayload["tenants"] = tenant
			print json.dumps(jsonPayload, indent=4, sort_keys=True)
			jsonPayload = json.dumps(jsonPayload)
		except KeyError as e:
                        key_error(str(e))
	else:
		jsonPayload["tenants"] = tenant
        	print json.dumps(jsonPayload, indent=4, sort_keys=True)
                jsonPayload = json.dumps(jsonPayload)
    elif resource == "tenant":
	try:
		jsonPayload = {}
	        jsonPayload["tenant-id"] = kwargs["tenant_id"]
	        jsonPayload["tenant-name"] = kwargs["tenant_name"]
	except KeyError as e:
                key_error(str(e))
	if "related-to" in kwargs:
		try:
			relationship_list = {}
			relationship_key = ["customer.global-customer-id", "service-subscription.service-type"]
			#tenant_relation = Makerelationship(relationship_key, kwargs["related-to"],kwargs["relationship-value"],kwargs["customer_id"])
			tenant_relation = Makerelationship(relationship_key, **kwargs)
			jsonPayload["relationship-list"] = tenant_relation.make_relationship()
			print json.dumps(jsonPayload, indent=4, sort_keys=True)
                        jsonPayload = json.dumps(jsonPayload)
		except KeyError as e:
	        	key_error(str(e))
	else:
		print json.dumps(jsonPayload, indent=4, sort_keys=True)
		jsonPayload = json.dumps(jsonPayload)
    return jsonPayload

def aaidelete(url, resource_version, resource):
    """
    delete a resource in AAI
    """
    url = url + "?resource-version=" + resource_version
    print url
    response = requests.delete(url, headers=headers, verify=False)
    if response.status_code == 204:
    	print "resource %s deleted successfully" % resource
    else:
	print response.status_code
        print response.text
    return response

def aaiput(url, payload, update, **kwargs):

    """
    put a new resource into AAI
    """
    response = requests.put(url, payload, headers=headers, verify=False)
    response_headers = response.headers
    if response.status_code == 201:
	print "Object created successfully\n"
    elif response.status_code == 200:
	print "Object patched successfully\n"
    elif response.status_code == 412 and update is True:
	if "Precondition Required:resource-version not passed" in response.text:
		print "Update is True, fetching the resource-version for the resource %s" % args.resource 
		getdict = {"ip":args.ip, "port":args.port, "version":"/aai/v11/"}
		url_part = resource2url_part(args.resource, **args.my_dict)
		getdict["url_part"] = url_part
	        url = geturlconstruct(**getdict)
	        response = aaiget(url)
		try:
			resource_version = response["resource-version"]
			print resource_version
		except KeyError as e:
                        key_error(str(e))
	        #print json.dumps(response, indent=4, sort_keys=True)	
		payload = json.loads(payload)
		payload["resource-version"] = resource_version
		payload = json.dumps(payload)
		response = requests.put(url, payload, headers=headers, verify=False)
		response_headers = response.headers
		if response.status_code == 200:
			print "resource %s updated successfully" % args.resource
		else:
			print response.status_code
			print response.text
    else:
	print "Received resopnse code %s\n" % response.status_code
	print "Message: %s\n" % response.text
    return response_headers

def aaiget(url):
    """
    get a resource details 
    """
    response = requests.get(url, headers=headers, verify=False)
    response_headers = response.headers
    response_code=response.status_code
    #print response.encoding
    if response_code is 200:
	return json.loads(response.text)

def patch_url(url_part, patch):
    """
    Construct the url_part based on the pacthing resource
    """
    slash="/"
    if patch == "relationship":
	url_part = url_part + slash + "relationship-list/" + patch
    return url_part
	

def resource2url_part(resource, **kwargs):
    """
    Construct the url based on resource and arguments given for GET calls
    """
    slash="/"
    if resource == "cloud-region":
	try:
		url_part = "cloud-infrastructure/cloud-regions/cloud-region/" + kwargs["cloud_owner"] + slash +  kwargs["cloud_name"]
	except KeyError as e:
		key_error(str(e))
    elif resource == "tenants":
	try:
		url_part = "cloud-infrastructure/cloud-regions/cloud-region/" + kwargs["cloud_owner"] + slash + kwargs["cloud_name"] + slash + "tenants"
	except KeyError as e:
		key_error(str(e))
    elif resource == "tenant":
 	try:
		url_part = "cloud-infrastructure/cloud-regions/cloud-region/" + kwargs["cloud_owner"] + slash + kwargs["cloud_name"] + slash + "tenants/tenant/" + kwargs["tenant_id"]
	except KeyError as e:
		key_error(str(e))
    elif resource == "customer":
	try:
		url_part = "business/customers/customer/" + kwargs["customer_id"]
	except KeyError as e:
		key_error(str(e))
    elif resource == "service-subscriptions":
	try:
		url_part = "business/customers/customer/" + kwargs["customer_id"] + slash + "service-subscriptions"
	except KeyError as e:
		key_error(str(e))
    elif resource == "service-subscription":
	try:
		url_part = "business/customers/customer/" + kwargs["customer_id"] + slash + "service-subscriptions/service-subscription/" + kwargs["service_type"]
	except KeyError as e:
		key_error(str(e))
    elif resource == "generic-vnf":
	try:
		url_part = "network/generic-vnfs/generic-vnf/" + kwargs["vnf_id"]
	except KeyError as e:	
		key_error(str(e))
    elif resource == "zone":
	try:
	    	url_part = "network/zones/zone/" + kwargs["zone_id"]
	except KeyError as e:
		key_error(str(e))
    elif resource == "service":
	try:
	    	url_part = "service-design-and-creation/services/service/" + kwargs["service_id"]
	except KeyError as e:
		key_error(str(e))
    elif resource == "services":
	try:
	    	url_part = "service-design-and-creation/services"
	except KeyError as e:
		key_error(str(e))
    elif resource == "complex":
	try:
		url_part = "cloud-infrastructure/complexes/complex/" + kwargs["complex_name"]
	except KeyError as e:
		key_error(str(e))
    else:
	resource_list = {"cloud-regions":"cloud-infrastructure/cloud-regions/", "customers":"business/customers", "generic-vnfs":"network/generic-vnfs", "zones":"network/zones", "complexes":"cloud-infrastructure/complexes"}
	url_part = resource_list.get(resource)
    return url_part

# Build our required arguments list
parser = argparse.ArgumentParser(description='Will also parse key pairs into a dictionary along with traditional arguments')
my_dict = {}
class StoreDictKeyPair(argparse.Action):
     def __call__(self, parser, namespace, values, option_string=None):
         for kv in values.split(","):
             k,v = kv.split("=")
	     if k == "relationship-value":
	     	my_dict.setdefault(k, []).append(v)
	     else:
	        my_dict[k] = v
         setattr(namespace, self.dest, my_dict)

#resource = parser.add_argument_group("resource")
#context = parser.add_argument_group("context")
#patch = parser.add_argument_group("patch")
#debug = parser.add_argument_group("debug")
#update = parser.add_argument_group("update")
#force = parser.add_argument_group("force")
#resource.add_argument("-i", "--ip", help="The AAI ip address", type=str, required=True)
#resource.add_argument("-p", "--port", help="The AAI port", type=str, default="8443")
#context.add_argument("--context", help="CREATE/DEKETE/GET a resource", type=str, required=True)
#patch.add_argument("--patch", help="PATCH/UPDATE a resource", type=str)
#resource.add_argument("-r", "--resource", help="resource name", type=str, required=True)
#debug.add_argument("--debug", help="debug logging", action='store_true')
#update.add_argument("--update", help="update a resource based on resource version", action='store_true')
#force.add_argument("--force", help="delete a resource forcefully along with it dependencies", action='store_true')
#parser.add_argument("--key_pairs", help="customer_id=Demonstration,cloud_owner=CloudOwner,tenant_name=admin,tenant_id=<id>,service-subscription=vFWCL,cloud_name=<name> ..etc", dest="my_dict", action=StoreDictKeyPair, metavar="KEY1=VAL1,KEY2=VAL2...")

#args = parser.parse_args()
#print args.my_dict

headers = {"Accept":"application/json", "Content-type":"application/json","X-FromAppId":"AAI","X-TransactionId":"get_aai_cloud_region","Authorization":"Basic QUFJOkFBSQ=="}
list_of_resources = ["cloud-regions", "cloud-region", "tenants", "tenant", "customers", "customer", "service-subscriptions", "service-subscription", "generic-vnfs", "generic-vnf", "zones", "zone", "complexes", "complex"]
list_of_specific_resource = ["cloud-region", "tenants", "tenant", "customer", "service-subscriptions", "service-subscription", "generic-vnf", "zone", "complex"]

