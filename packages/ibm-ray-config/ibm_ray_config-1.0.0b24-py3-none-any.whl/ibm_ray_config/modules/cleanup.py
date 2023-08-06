import time
import ibm_cloud_sdk_core
import ibm_vpc
import yaml
from ibm_ray_config.modules.config_builder import ConfigBuilder
from ibm_ray_config.modules.utils import Color, color_msg
ibm_vpc_client = None

def get_vpc_data(vpc_id):
    
    if not vpc_id: return None
    try:
        vpc_data = ibm_vpc_client.get_vpc(vpc_id).result
        return vpc_data
    except ibm_cloud_sdk_core.ApiException as e:
        if e.code == 404:
            print(("VPC doesn't exist."))
            return None
        else: raise 

def delete_subnets(vpc_data):
    def _poll_subnet_exists(subnet_id):
        tries = 30 # waits up to 5 min with 10 sec interval
        sleep_interval = 10
        while tries:
            try:
                subnet_data = ibm_vpc_client.get_subnet(subnet_id).result
            except Exception:
                print(color_msg(f"Deleted subnet id: '{subnet_id}'",color=Color.PURPLE))
                return True
            tries -= 1
            time.sleep(sleep_interval)
        print(f"Failed to delete instance within expected time frame of {tries*sleep_interval/60} minutes.")
        return False

    subnets_attached_to_routing_table = ibm_vpc_client.list_subnets(routing_table_id = vpc_data['default_routing_table']['id']).get_result()['subnets']
    subnets_ids = [subnet['id'] for subnet in subnets_attached_to_routing_table]
    for id in subnets_ids:
        try:
            ibm_vpc_client.delete_subnet(id).get_result()
            _poll_subnet_exists(id)
        except ibm_cloud_sdk_core.ApiException as e:
            if e.code == 404:
                print("subnet doesn't exist.")

def delete_gateways(vpc_id):
    gateways = ibm_vpc_client.list_public_gateways(resource_group_id=RESOURCE_GROUP_ID).get_result()['public_gateways']
    gateways_ids_of_vpc = [gateway['id'] for gateway in gateways if gateway['vpc']['id']== vpc_id]
    for gateway_id in gateways_ids_of_vpc:
        deleting_resource = True
        while deleting_resource:
            try:
                ibm_vpc_client.delete_public_gateway(gateway_id).get_result()
                deleting_resource = False
                print(color_msg(f"Deleted gateway with id: '{gateway_id}'",Color.PURPLE))
            except ibm_cloud_sdk_core.ApiException as e:
                if e.code == 404:
                    print("gateway doesn't exist.") 
                    deleting_resource = False
                if e.code == 409:
                    print("gateway still in use.")
                    # will retry until cloud functions timeout. 
                    time.sleep(5) 

def delete_instances(vpc_id):
    def _poll_instance_exists(instance_id):
        tries = 20
        sleep_interval = 3
        while tries:
            try:
                instance_data = ibm_vpc_client.get_instance(instance_id).get_result()
            except Exception:
                print(color_msg(f"Deleted VM instance with id: '{instance_id}'",Color.PURPLE))
                return True
            tries -= 1
            time.sleep(sleep_interval)
        print(f"Failed to delete instance within expected time frame of {(tries*sleep_interval)/60} minutes.")
        return False

    instances = ibm_vpc_client.list_instances(vpc_id=vpc_id).get_result()['instances']
    instances_ids = [instance['id'] for instance in instances]
    for id in instances_ids:
        ibm_vpc_client.delete_instance(id=id).get_result()
        _poll_instance_exists(id)

def delete_unbound_vpc(vpc_id):
    deleting_resource = True
    while deleting_resource:
        try:
            ibm_vpc_client.delete_vpc(vpc_id).get_result()
            deleting_resource = False
            print(color_msg(f"VPC '{vpc_id}' and its attached resources were deleted successfully",Color.PURPLE))
        except ibm_cloud_sdk_core.ApiException as e:
            if e.code == 404:
                print("VPC doesn't exist.") 
                deleting_resource = False
            if e.code == 409:
                print("VPC still in use.")
                # will retry until cloud functions timeout. 
                time.sleep(5)

def delete_vpc(vpc_id):
    vpc_data = get_vpc_data(vpc_id)
    if not vpc_data:
        print((f"Failed to find a VPC with id={vpc_id}"))
        return
    print(color_msg(f"Deleting vpc: '{vpc_data['name']}' with id: '{vpc_id}'",Color.YELLOW))
    delete_instances(vpc_data['id'])
    delete_subnets(vpc_data)
    delete_gateways(vpc_id)
    delete_unbound_vpc(vpc_id)
    


def clean_cluster(config_file):
    global ibm_vpc_client, RESOURCE_GROUP_ID
    with open(config_file) as f:
        config = yaml.safe_load(f)
    node_config = config['available_node_types'][ConfigBuilder.DEFAULT_NODE_TYPE]['node_config']
    iam_api_key, RESOURCE_GROUP_ID, vpc_id, region = (config['provider']['iam_api_key'], node_config['resource_group_id'],
                                                       node_config['vpc_id'], config['provider']['region'])

    authenticator = ibm_cloud_sdk_core.authenticators.IAMAuthenticator(iam_api_key, url=None)
    ibm_vpc_client = ibm_vpc.VpcV1('2022-06-30',authenticator=authenticator)

    if not region:
        raise Exception("VPC not found in any region")

    ibm_vpc_client.set_service_url(f'https://{region}.iaas.cloud.ibm.com/v1')
    
    delete_vpc(vpc_id=vpc_id)
    return {"Status": "Success"}