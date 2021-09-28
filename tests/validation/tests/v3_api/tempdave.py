import os
from .common import get_user_client
from .common import random_test_name
from .common import validate_cluster
from .common import wait_for_cluster_delete, get_admin_client, get_user_client_and_cluster
from .test_create_ha import resource_prefix
from lib.aws import AmazonWebServices
import pytest
import time

## Requires that the user has defined these env vars in shell first:
## .common.py and ..common.py
# CATTLE_TEST_URL
# ADMIN_TOKEN
# USER_TOKEN (standard user token)
## this test here
# USER_ID

USER_ID = os.environ.get("USER_ID")

def test_crb():
    client = get_admin_client()
    # for i in range(0,200):
    #     cluster = client.create_cluster(
    #         name=random_test_name("test"),
    #         driver="rancherKubernetesEngine",
    #         rancherKubernetesEngineConfig=rke_config)
    client, cluster = get_user_client_and_cluster()
    print("cluster:",cluster)
    # for cluster in cluster_existing:
    for i in range(0,4000):
         # create role template
        role_temp = client.create_role_template(name=random_test_name("role"),
                                                context="cluster",
                                                rules=[{"type": "policyRule", "verbs": ["create", "delete", "get", "list"], "apiGroups": ["*"], "resources": ["nodes"]}])
        time.sleep(.5)
        crtb = client.create_cluster_role_template_binding(
            clusterId=cluster.id,
            roleTemplateId=role_temp.id,
            subjectKind="User",
            userId=USER_ID) 
