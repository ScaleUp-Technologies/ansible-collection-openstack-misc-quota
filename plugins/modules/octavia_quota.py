from ansible.module_utils.basic import *

DOCUMENTATION = r'''
author:
- Freerk-Ole Zakfeld, ScaleUp Technologies GmbH & Co. KG (@fzakfeld)
description: Set Octavia LBAAS Quota
module: octavia_quota
options:
    cloud:
        description:
            - Cloud auth config
        type: dict
        required: true
    project_id:
        description:
            - ID of the project where to set the quota
        type: str
        required: true
    load_balancer:
        description:
            - Number of load_balancer resources
        type: int
        required: true
    listener:
        description:
            - Number of listener resources
        type: int
        required: true
    pool:
        description:
            - Number of pool resources
        type: int
        required: true
    health_monitor:
        description:
            - Number of health_monitor resources
        type: int
        required: true
'''

EXAMPLES = r'''
name: Set the Octavia quota
octavia_quota:
    cloud:
        auth:
            auth_url: https://keystone.cloud.example.com
            username: admin
            password: xxx
            project_id: xxx
            project_name: admin
    project_id: xyz
    load_balancer: 10
    listener: 20
    pool: 30
    health_monitor: 40
'''

def main():
    module = AnsibleModule(argument_spec={
        'cloud': {
            'type': 'dict',
            'required': True,
        },
        'project_id': {
            'type': 'str',
            'required': True,
        },
        'load_balancer': {
            'type': 'int',
            'required': True
        },
        'listener': {
            'type': 'int',
            'required': True
        },
        'pool': {
            'type': 'int',
            'required': True
        },
        'health_monitor': {
            'type': 'int',
            'required': True
        }
    }, supports_check_mode=True)

    changed = False

    import openstack

    auth = module.params['cloud']['auth']

    project_id = module.params['project_id']

    conn = openstack.connect(
        **auth
    )

    new_quotas = {
        'load_balancer': module.params['load_balancer'],
        'listener': module.params['listener'],
        'pool': module.params['pool'],
        'health_monitor': module.params['health_monitor'],
    }

    quotas = conn.load_balancer.get_quota(project_id)

    for quota_key in new_quotas:
        if new_quotas[quota_key] != quotas[quota_key]:
            changed = True
            break

    if changed and not module.check_mode:
        quotas = conn.load_balancer.update_quota(project_id, **new_quotas)

    module.exit_json(changed=changed, new_quotas=new_quotas)

if __name__ == '__main__':
    main()