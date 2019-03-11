# aai_client

aai client script to PUT/GET/DELETE the data to AAI REST API

## getting started

This script will be useful to make AAI REST API calls based on a command line arguments

python aai_client.py --help

## GET calls

Exmaples:

python aai_client.py -i <ip> --context get --resource complexes

python aai_client.py -i <ip> --context get --resource tenants --key_pairs cloud_name=ec0,cloud_owner=CloudOwner

python aai_client.py -i <ip> --context get -r tenant --key_pairs tenant_id=840d2b141ddf466988eea28f38c84d9d,cloud_owner=CloudOwner,cloud_name=ec3

python aai_client.py -i <ip> --context get -r cloud-region --key_pairs cloud_owner=CloudOwner,cloud_name=ec3

## PUT calls

Exmaples:

python aai_client.py -i <ip> --context create -r cloud-region --key_pair cloud_name=ec4,cloud_owner=CloudOwner,cloud_type=openstack,cloud_zone=nova,tenant_id=840d2b141ddf466988eea28f38c84d9d,tenant_name=admin,customer_id=Demonstration

python aai_client.py -i <ip> --context create -r tenant --key_pairs tenant_name=admin,tenant_id=840d2b141ddf466988eea28f38c84d9d,cloud_owner=CloudOwner,cloud_name=ec4,customer_id=Demonstration

python aai_client.py -i <ip> --context create -r cloud-region --key_pair cloud_name=ec3,cloud_owner=CloudOwner,cloud_type=openstack,cloud_zone=nova,tenant_id=840d2b141ddf466988eea28f38c84d9d,tenant_name=admin,related-to=service-subcription,relationship-value=vFWCL,relationship-value=vIMS,relationship-value=vCPE,realtionship-value=vLB,customer_id=Demonstration

python aai_client.py -i <ip> --context create -r tenant --key_pairs related-to=service-subscription,realationship-vlaue=vFWCL,relationship-value=vIMS,relationship-value=vCPE,realtionship-value=vLB,tenant_name=admin,tenant_id=840d2b141ddf466988eea28f38c84d9d,cloud_owner=CloudOwner,cloud_name=ec3,customer_id=Demonstration

### --update flag

Exmaples:

python aai_client.py -i <ip> --context create -r cloud-region --key_pair cloud_name=ec8,cloud_owner=CloudOwner,cloud_type=openstack,cloud_zone=nova,tenant_id=840d2b141ddf466988eea28f38c84d9d,tenant_name=admin,related-to=service-subcription,relationship-value=vFWCL,relationship-value=vIMS,relationship-value=vCPE,relationship-value=vLB,relationship-value=wordpress1 --update

## DELETE calls

Examples:

python aai_client.py -i <ip> --context delete -r cloud-region --key_pairs cloud_name=ec8,cloud_owner=CloudOwner
python aai_client.py -i <ip> --context delete -r tenant --key_pairs clustomer_id=Demonstration,cloud_owner=CloudOwner,cloud_name=ec8,tenant_id=840d2b141ddf466988eea28f38c84d9d
