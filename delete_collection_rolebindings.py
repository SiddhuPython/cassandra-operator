
from kubernetes import config, client
config.load_kube_config()
# config.load_incluster_config()
configuration = client.Configuration()
api_instance = client.RbacAuthorizationV1Api(client.ApiClient(configuration))
namespace = 'rook-cassandra' # str | object name and auth scope, such as for teams and projects
pretty = 'true' # str | If 'true', then the output is pretty printed. (optional)
allow_watch_bookmarks = True # bool | allowWatchBookmarks requests watch events with type \"BOOKMARK\". Servers that do not implement bookmarks may ignore this
dry_run = '- All' # str | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an err
grace_period_seconds = 56 # int | The duration in seconds before the object should be deleted. Value must be non-negative integer. The value zero indicates del
limit = 56 # int | limit is a maximum number of responses to return for a list call. If more items exist, the server will set the `continue` field on the list
orphan_dependents = True # bool | Deprecated: please use the PropagationPolicy, this field will be deprecated in 1.7. Should the dependent objects be orphaned.
propagation_policy = 'Background' # str | Whether and how garbage collection will be performed. Either this field or OrphanDependents may be set, but not both.
timeout_seconds = 56 # int | Timeout for the list/watch call. This limits the duration of the call, regardless of any activity or inactivity. (optional)
watch = True # bool | Watch for changes to the described resources and return them as a stream of add, update, and remove notifications. Specify resourceVersio
body = client.V1DeleteOptions() # V1DeleteOptions |  (optional)
api_response = api_instance.delete_collection_namespaced_role_binding(namespace, pretty=pretty,limit=limit, timeout_seconds=timeout_seconds, watch=watch)
