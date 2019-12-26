import json
import logging
import subprocess
from kubernetes import client, config
from kubernetes.client.rest import ApiException

def create_custom_resource_object(namespace,json_file_path):
    config.load_kube_config()
    #config.load_incluster_config()
    configuration = client.Configuration()
    api_instance = client.CustomObjectsApi(client.ApiClient(configuration))
    group = 'cassandra.rook.io' # str | The custom resource's group name
    version = 'v1alpha1' # str | The custom resource's version
    plural = 'clusters' # str | The custom resource's plural name. For TPRs this would be lowercase plural kind.
    pretty = 'true'
    with open(json_file_path,'r') as jfile:
        data = json.load(jfile)
    try:
        api_response = api_instance.create_namespaced_custom_object(group, version, namespace, plural,body=data, pretty=pretty)
        return api_response
    except ApiException as e:
        return ("Exception when calling CustomObjectsApi->create_namespaced_custom_object: %s\n" % e)

def delete_custom_resource_object(cluster_name):
    #config.load_incluster_config()
    config.load_kube_config()
    configuration = client.Configuration()
    api_instance = client.CustomObjectsApi(client.ApiClient(configuration))
    group = 'cassandra.rook.io' # str | The custom resource's group name
    version = 'v1alpha1' # str | The custom resource's version
    plural = 'clusters' # str | The custom resource's plural name. For TPRs this would be lowercase plural kind.
    pretty = 'true'
    name = cluster_name
    namespace = 'rook-cassandra'
    body = client.V1DeleteOptions()

    try:
        api_response = api_instance.delete_namespaced_custom_object(group, version, namespace, plural, name, body)
        return api_response
    except ApiException as e:
        return ("Exception when calling CustomObjectsApi->delete_namespaced_custom_object: %s\n" % e)
def get_pods_info(namespace):
    config.load_kube_config()
    #config.load_incluster_config()
    configuration = client.Configuration()
    api_instance = client.CoreV1Api(client.ApiClient(configuration))
    allow_watch_bookmarks = True 
    field_selector = 'node_info'
    label_selector = 'node_info'
    limit = 56
    pretty='true'
    all_pods = []
    d1 = {}
    try:
        api_response = api_instance.list_namespaced_pod(namespace, limit=limit, pretty=pretty)
        for item in api_response.items:
            d1['name']=item.metadata.name
            d1['status']=item.status.phase
            all_pods.append(d1.copy())
        return all_pods
    except ApiException as e:
        return "Exception when calling CoreV1Api->list_node: %s\n" % e
def get_clusters_info(namespace):
    clusters_info = []
    d1  = {}
    config.load_kube_config()
    #config.load_incluster_config()
    configuration = client.Configuration()
    api_instance = client.AppsV1beta2Api(client.ApiClient(configuration))
    try:
       api_response = api_instance.list_namespaced_stateful_set(namespace)
       for cluster in api_response.items:
           d1['name']=cluster.metadata.labels['cassandra.rook.io/cluster']
           clusters_info.append(d1.copy())
       return clusters_info
    except ApiException as e:
       return "Exception when calling AppsV1beta2Api->patch_namespaced_stateful_set_status: %s\n" % e

if __name__=="__main__":
    #print(create_custom_resource_object('rook-cassandra','sample.json'))
    print(delete_custom_resource_object('rook-cassandra2'))

