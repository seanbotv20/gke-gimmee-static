import requests
import googleapiclient.discovery as discovery
import os

IP_ADDRESS = os.environ['IP_ADDRESS']

def getMetadata(metadata):
    response = requests.get(f'http://metadata.google.internal/computeMetadata/v1/{metadata}', headers={"Metadata-Flavor": "Google"})
    response.raise_for_status()
    return response.text

def getMetadataOrVariable(metadata, variable):
    data = os.getenv(variable)

    if data == None:
        data = getMetadata(metadata)

    return data

def getInstanceId():
    return getMetadataOrVariable('instance/id', 'INSTANCE_ID')

def getInstanceProject():
    return getMetadataOrVariable('project/project-id', 'PROJECT')

def getInstanceZone():
    return getMetadataOrVariable('instance/zone', 'ZONE').split('/')[-1]

if __name__ == "__main__":

    instanceId = getInstanceId()
    print(f'InstanceId: {instanceId}')

    project = getInstanceProject()
    print(f'Project: {project}')

    zone = getInstanceZone()
    print(f'Zone: {zone}')


    compute = discovery.build('compute', 'v1')

    instances = compute.instances()
    
    instance = instances.get(project=project, zone=zone, instance=instanceId).execute()

    if len(instance['networkInterfaces']) == 1:
        networkInterface = instance['networkInterfaces'][0]

        if len(networkInterface['accessConfigs']) ==1:
            accessConfig = networkInterface['accessConfigs'][0]

            if (accessConfig['natIP'] != IP_ADDRESS):

                deleteResponse = instances.deleteAccessConfig(project=project, zone=zone, instance=instanceId, accessConfig=accessConfig['name'], networkInterface=networkInterface['name']).execute()
                print(deleteResponse)

                createResponse = instances.addAccessConfig(project=project, zone=zone, instance=instanceId, networkInterface=networkInterface['name'], body={
                    "kind": "compute#accessConfig",
                    "networkTier": "PREMIUM",
                    "natIP": IP_ADDRESS,
                    "type": "ONE_TO_ONE_NAT",
                }).execute()

                print(createResponse)

            else:
                print("This instance already has specified IP_ADDRESS, ignoring")

        else:
            raise Exception("Instance has multiple accessConfigs, not sure how to deal with that")
    else:
        raise Exception("Instance has multiple network interfaces, not sure how to deal with that")

