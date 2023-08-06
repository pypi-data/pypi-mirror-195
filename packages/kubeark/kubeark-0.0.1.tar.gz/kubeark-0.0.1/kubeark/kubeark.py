#coding=utf-8

from kubernetes import client, config

try:
    # 尝试从集群内部读取 kubeconfig 文件
    config.load_incluster_config()
except config.ConfigException:
    # 如果从集群内部读取 kubeconfig 文件失败，则尝试从环境变量中读取 kubeconfig 文件路径
    config.load_kube_config()

v1 = client.CoreV1Api()

try:
    # 列出所有节点
    nodes = v1.list_node()
except Exception as e:
    print(f"Error: {e}")
else:
    if len(nodes.items) == 0:
        # 如果集群中没有节点，则说明集群不存在
        print("Kubernetes cluster does not exist.")
    else:
        # 集群存在，继续处理
        print("Kubernetes cluster exists. Continuing with processing.")
