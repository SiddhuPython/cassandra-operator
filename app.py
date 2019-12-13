from flask import Flask, jsonify
from flask import request
from pod_ops import create_custom_resource_object, get_nodes_info, delete_custom_resource_object
import yaml, json
app = Flask(__name__)



@app.route('/api/cluster_info', methods=['GET'])
def cluster_info():
    if 'namespace' in request.args:
        cluster_info = get_nodes_info(request.args['namespace'])
        return jsonify({'cluster_info':cluster_info})
    return jsonify({'Error':'Enter namespace'})

@app.route('/api/resource', methods=['POST'])
def create_cluster():
    cluster_name = request.args['cluster_name']
    data_center_name = request.args['data_center_name']
    name_space = request.args['name_space']
    rack_name = request.args['rack_name']
    rack_members = request.args['rack_members']
    request_cpu = request.args['cpu']
    request_memory = request.args['memory']
    with open('temp.yml', 'r') as f, open('sample.json','w') as json_out:
        for i in yaml.safe_load_all(f):
            if i['kind']=='Cluster':
                i['spec']['datacenter']['name']=cluster_name
                i['spec']['datacenter']['racks'][0]['name']=rack_name
                i['spec']['datacenter']['racks'][0]['members']=int(rack_members)
                i['spec']['datacenter']['racks'][0]['resources']['requests']['cpu']=int(request_cpu)
                i['spec']['datacenter']['racks'][0]['resources']['requests']['memory']=request_memory
            json.dump(i, json_out, ensure_ascii=False,indent=2)
    resp = create_custom_resource_object(name_space, 'sample.json')
    return jsonify({'result':'%s'%resp})

@app.route('/api/delete', methods=['DELETE'])
def delete_pod():
    namespace = request.args['namespace']
    return jsonify({'result':delete_custom_resource_object(namespace,'sample.json')})

if __name__=="__main__":
    app.run(debug=True)
