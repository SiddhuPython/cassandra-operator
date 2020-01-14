import os
import shutil
import logging
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from pod_ops import create_custom_resource_object, get_pods_info, delete_custom_resource_object, get_clusters_info

import yaml
import json
import config
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/api/cluster_info', methods=['GET'])
def cluster_info():
    if 'namespace' in request.args:
        cluster_info = get_clusters_info(request.args['namespace'])
        return jsonify({'cluster_info': cluster_info})
    return jsonify({'Error': 'Enter namespace'})


@app.route('/api/resource', methods=['POST'])
def create_cluster():
    cluster_data = request.get_json()
    cluster_name = cluster_data['cluster_name']
    data_center_name = cluster_data['data_center_name']
    name_space = cluster_data['name_space']
    rack_name = cluster_data['rack_name']
    rack_members = cluster_data['rack_members']
    request_cpu = cluster_data['cpu']
    request_memory = cluster_data['memory']
    logging.info("creating role json for cluster role")
    if not os.path.exists(cluster_name):
        os.makedirs(cluster_name)
    ROLE_PATH = os.path.join(cluster_name,'role.json')
    ROLEBINDING_PATH = os.path.join(cluster_name, 'rolebinding.json')
    SA_PATH = os.path.join(cluster_name, 'sa.json')
    CRD_PATH = os.path.join(cluster_name,'crd.json')
    with open('role.yml', 'r') as rolefile, open(ROLE_PATH, 'w') as r_json_out:
        for i in yaml.safe_load_all(rolefile):
            i['metadata']['name'] = cluster_name+'-member'
            json.dump(i, r_json_out, ensure_ascii=False, indent="\t")
    logging.info("creating rolebinding for %s cluster "%cluster_name)
    with open('rolebinding_temp.yml', 'r') as rbf, open(ROLEBINDING_PATH, 'w') as rb_json_out:
        for i in yaml.safe_load_all(rbf):
            i["metadata"]["name"] = cluster_name + '-member'
            i["roleRef"]["name"] =  cluster_name + '-member'
            i["subjects"][0]["name"] = cluster_name + '-member'
            json.dump(i, rb_json_out, ensure_ascii=False, indent="\t")
    logging.info("creating service account for new cluster")
    with open('service_account.yml', 'r') as saf, open(SA_PATH, 'w') as json_out:
        for i in yaml.safe_load_all(saf):
            if i['kind'] == 'ServiceAccount':
                i['metadata']['name'] = cluster_name + '-member'
            json.dump(i, json_out, ensure_ascii=False, indent="\t")
    logging.info("creating custom resource object for %s cluster "%cluster_name)
    with open('crd.yml', 'r') as f, open(CRD_PATH, 'w') as json_out:
        for i in yaml.safe_load_all(f):
            if i['kind'] == 'Cluster':
                i['metadata']['name'] = cluster_name
                i['spec']['datacenter']['name'] = data_center_name
                i['spec']['datacenter']['racks'][0]['name'] = rack_name
                i['spec']['datacenter']['racks'][0]['members'] = int(
                    rack_members)
                i['spec']['datacenter']['racks'][0]['resources']['requests']['cpu'] = int(
                    request_cpu)
                i['spec']['datacenter']['racks'][0]['resources']['requests']['memory'] = request_memory
            json.dump(i, json_out, ensure_ascii=False, indent="\t")
    logging.info("Creating new cluster %s"%cluster_name)
    resp = create_custom_resource_object(
        name_space,
        CRD_PATH,
        SA_PATH,
        ROLEBINDING_PATH,
        ROLE_PATH)
    return jsonify({'result': resp})


@app.route('/api/delete', methods=['DELETE'])
def delete_pod():
    if 'cluster_name' in request.args:
        cluster_name = request.args['cluster_name']
        resp = delete_custom_resource_object(cluster_name)
        return {"Message": "Cluster deleted successfully"}
    return jsonify({'result': resp})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=config.PORT, debug=config.DEBUG_MODE)
