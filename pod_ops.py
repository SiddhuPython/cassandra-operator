import shutil
import json
import logging
import logging.handlers
from kubernetes import client, config
from kubernetes.client.rest import ApiException
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('%s' % 'pod_ops.log', 'w', 'utf-8')
file_handler.setLevel(logging.DEBUG)
file_format = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s: %(lineno)d in %(funcName)s]')
file_handler.setFormatter(file_format)
logger.addHandler(file_handler)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter('%(message)s')
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)

def create_namespaced_role(namespace, r_json_path):
    """Function to create cluster role"""
    config.load_kube_config()
    # config.load_incluster_config()
    configuration = client.Configuration()
    logger.info("creating role")
    api_instance = client.RbacAuthorizationV1Api(
        client.ApiClient(configuration))
    with open(r_json_path, 'r') as role_out:
        body = json.load(role_out)
    try:
        logger.info("creating role .........")
        api_response = api_instance.create_namespaced_role(namespace, body)
        logger.info(
            "role for cluster created successfully\n ")
    except ApiException as e:
        logger.error("Failed to create namespaced role\n %s " % e)


def delete_namespaced_role(cluster_name, namespace):
    config.load_kube_config()
    # config.load_incluster_config()
    configuration = client.Configuration()
    api_instance = client.RbacAuthorizationV1Api(
        client.ApiClient(configuration))
    name = cluster_name
    pretty = 'true'
    dry_run = 'All'
    grace_period_seconds = 56
    orphan_dependents = True
    body = client.V1DeleteOptions()  # V1DeleteOptions |  (optional)
    try:
        logger.info("Deleting namespaced roles..........")
        api_response = api_instance.delete_namespaced_role(
            name,
            namespace,
            pretty=pretty,
            dry_run=dry_run,
            grace_period_seconds=grace_period_seconds,
            orphan_dependents=orphan_dependents,
            body=body)
        logger.info("roles are deleted successfully")
    except ApiException as e:
        logger.error(
            "Exception when calling RbacAuthorizationV1Api->delete_namespaced_role: %s\n" %
            e)


def create_namespaced_rolebinding(namespace, rb_json_path):
    """
    Function to create namespaced role binding for a cluster
    """
    # create an instance of the API class
    config.load_kube_config()
    # config.load_incluster_config()
    configuration = client.Configuration()
    api_instance = client.RbacAuthorizationV1Api(
        client.ApiClient(configuration))
    namespace = namespace  # str | object name and auth scope, such as for teams and projects
    #body = client.V1RoleBinding()
    with open(rb_json_path, 'r') as jsfile:
        body = json.load(jsfile)
    try:
        logger.info("create namespaced rolebinding......")
        api_instance.create_namespaced_role_binding(
            namespace, body)
        logger.info("rolebinding created successfully")
    except ApiException as e:
        logger.error(
            "Exception when calling RbacAuthorizationV1Api->create_namespaced_role_binding\n: %s" %
            e)


def delete_namespaced_rolebinding(name, namespace):
    config.load_kube_config()
    # config.load_incluster_config()
    configuration = client.Configuration()
    api_instance = client.RbacAuthorizationV1Api(
        client.ApiClient(configuration))
    limit = 56
    pretty = 'true'
    allow_watch_bookmarks = True

    dry_run = '- All'  # str | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an err
    timeout_seconds = 56
    watch = True  # bool | Watch for changes to the described resources and return them as a stream of add, update, and remove notifications. Specify resourceVersio
    grace_period_seconds = 56
    orphan_dependents = True
    propagation_policy = 'Background'
    body = client.V1DeleteOptions()  # V1DeleteOptions |  (optional)
    try:
        logger.info("Namespaced deleting ............")
        api_response = api_instance.delete_collection_namespaced_role_binding(
            namespace, pretty=pretty, limit=limit, timeout_seconds=timeout_seconds, watch=watch)
        logger.info("namespaced rolebinding deleted successfully")
    except ApiException as e:
        logger.error(
            "Exception when calling RbacAuthorizationV1Api->delete_namespaced_role_binding: %s\n" %
            e)


def create_namespaced_service_account(namespace, json_file_path):
    """
    Function to create service account
    """
    #service_accounts = get_service_accounts(namespace)
    config.load_kube_config()
    # config.load_incluster_config()
    configuration = client.Configuration()
    api_instance = client.CoreV1Api(client.ApiClient(configuration))
    #pretty = 'true'
    with open(json_file_path, 'r') as jfile:
        body = json.load(jfile)
    try:
        logger.info("creating service account.............")
        api_instance.create_namespaced_service_account(
            namespace, body)
        logger.info("service account created successfully %s" % namespace)
    except ApiException as e:
        logger.error(
            "Exception when calling CoreV1Api->create_namespaced_service_account: %s\n" %
            e)


def get_service_accounts(namespace):
    sas = []
    config.load_kube_config()
    # config.load_incluster_config()
    configuration = client.Configuration()
    api_instance = client.CoreV1Api(client.ApiClient(configuration))
    pretty = 'true'
    try:
        api_response = api_instance.list_namespaced_service_account(
            namespace, pretty=pretty)
        for item in api_response.items:
            for secret in item.secrets:
                sas.append(secret.name.split('-token')[0])
        return sas
    except ApiException as e:
        return "Exception when calling CoreV1Api->create_namespaced_service_account: %s\n" % e


def delete_service_account(service_acc_name, namespace):
    # Function to delete service account
    config.load_kube_config()
    # config.load_incluster_config()
    configuration = client.Configuration()
    api_instance = client.CoreV1Api(client.ApiClient(configuration))
    pretty = 'true'
    try:
        logger.info("deleting service account.......")
        api_instance.delete_namespaced_service_account(
            service_acc_name, namespace, pretty=pretty)
        logger.info("service account deleted successfully")
    except ApiException as e:
        logger.error(
            "Exception when calling CoreV1Api->create_namespaced_service_account: %s\n" %
            e)


def create_custom_resource_object(
        namespace,
        json_file_path,
        service_account_jpath, rb_json_path, r_json_path):
    """
    Function to create custom resource object
    """
    config.load_kube_config()
    # config.load_incluster_config()
    configuration = client.Configuration()
    api_instance = client.CustomObjectsApi(client.ApiClient(configuration))
    group = 'cassandra.rook.io'  # str | The custom resource's group name
    version = 'v1alpha1'  # str | The custom resource's version
    # str | The custom resource's plural name. For TPRs this would be
    # lowercase plural kind.
    plural = 'clusters'
    pretty = 'true'
    with open(json_file_path, 'r') as jfile:
        data = json.load(jfile)
    try:
        create_namespaced_role(namespace, r_json_path)
        create_namespaced_service_account(namespace, service_account_jpath)
        create_namespaced_rolebinding(namespace, rb_json_path)
        api_response = api_instance.create_namespaced_custom_object(
            group, version, namespace, plural, body=data, pretty=pretty)
        logging.info("New cassandra operator cluster created successfully")

        return api_response
    except ApiException as e:
        logging.error(
            "Exception when calling CustomObjectsApi->create_namespaced_custom_object: %s\n" %
            e)


def update_cluster(name, namespace, crd_path):
    config.load_kube_config()
    configuration = client.Configuration()
    api_instance = client.CustomObjectsApi(client.ApiClient(configuration))
    plural = 'clusters'
    group = 'cassandra.rook.io'
    version = 'v1alpha1'
    pretty = 'true'
    logging.info(crd_path)
    with open(crd_path, 'r') as jfile:
        body = json.load(jfile)
    try:
        api_response = api_instance.patch_namespaced_custom_object(group, version, namespace, plural, name, body)
        return api_response
    except ApiException as e:
        logging.error("Failed to scaleup/scaledown resource")


def delete_custom_resource_object(cluster_name):
    """
    Function to delete custom resource object
    """
    # config.load_incluster_config()
    config.load_kube_config()
    configuration = client.Configuration()
    api_instance = client.CustomObjectsApi(client.ApiClient(configuration))
    group = 'cassandra.rook.io'  # str | The custom resource's group name
    version = 'v1alpha1'  # str | The custom resource's version
    plural = 'clusters'
    name = cluster_name
    namespace = 'rook-cassandra'
    grace_period_seconds = 56
    orphan_dependents = True
    body = client.V1DeleteOptions()

    try:
        logger.info("deleting namespaced custom object ......................")
        api_response = api_instance.delete_namespaced_custom_object(
            group,
            version,
            namespace,
            plural,
            name,
            body,
            grace_period_seconds=grace_period_seconds,
            orphan_dependents=orphan_dependents)
        logger.info(api_response)
        logger.info("custom resource object deleted successfully")
        service_account_name = name + "-member"
        delete_namespaced_role(service_account_name, namespace)
        delete_service_account(service_account_name, namespace)
        delete_namespaced_rolebinding(service_account_name, namespace)
        shutil.rmtree(cluster_name)
        return api_response
    except ApiException as e:
        return(
            "Exception when calling CustomObjectsApi->delete_namespaced_custom_object: %s\n" %
            e)


def get_pods_info(namespace, cluster_name):
    """
    Function to get pods status
    """
    config.load_kube_config()
    # config.load_incluster_config()
    configuration = client.Configuration()
    api_instance = client.CoreV1Api(client.ApiClient(configuration))
    limit = 56
    pretty = 'true'
    all_pods = []
    pods = {}
    try:
        api_response = api_instance.list_namespaced_pod(
            namespace, limit=limit, pretty=pretty)
        for item in api_response.items:
            if cluster_name+'-' in item.metadata.name:
                pods['name'] = item.metadata.name
                pods['status'] = item.status.conditions[0].status
                if  pods['status']:
                    msg = "pod created successfully"
                else:
                    msg = item.status.conditions[0].message
                pods['msg'] = msg
                all_pods.append(pods.copy())
        return all_pods
    except ApiException as e:
        logger.error("Exception when calling CoreV1Api->list_node: %s\n" % e)


def get_clusters_info(namespace):
    """
    Function to get clusters info
    """
    clusters_info = []
    clusters = {}
    config.load_kube_config()
    configuration = client.Configuration()
    api_instance = client.AppsV1beta2Api(client.ApiClient(configuration))
    pretty = 'true'
    try:
        api_response = api_instance.list_namespaced_stateful_set(
            namespace, pretty=pretty)
        for cluster in api_response.items:
            clusters['name'] = cluster.metadata.labels['cassandra.rook.io/cluster']
            clusters_info.append(clusters.copy())
        return clusters_info
    except ApiException as e:
        return(
            "Exception when calling AppsV1beta2Api->patch_namespaced_stateful_set_status: %s\n" %
            e)


