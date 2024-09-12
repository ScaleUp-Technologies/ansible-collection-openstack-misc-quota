from ansible.module_utils.basic import *


DOCUMENTATION = r'''
author:
- Freerk-Ole Zakfeld, ScaleUp Technologies GmbH & Co. KG (@fzakfeld)
description: Set Designate DNS Quota
module: designate_quota
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
    zones:
        description:
            - Number of zone resources
        type: int
        required: true
    zone_recordsets:
        description:
            - Number of zone_recordset resources
        type: int
        required: true
    zone_records:
        description:
            - Number of zone_record resources
        type: int
        required: true
    recordset_records:
        description:
            - Number of recordset_record resources
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
    zone_recordsets: 500
    zone_records: 500
    recordset_records: 20
    zones: 10
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
        'zone_recordsets': {
            'type': 'int',
            'required': True
        },
        'zone_records': {
            'type': 'int',
            'required': True
        },
        'recordset_records': {
            'type': 'int',
            'required': True
        },
        'zones': {
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
        'zone_recordsets': (module.params['zone_recordsets']),
        'zone_records': (module.params['zone_records']),
        'recordset_records': (module.params['recordset_records']),
        'zones': (module.params['zones']),
    }

    dns_endpoint = conn.session.get_endpoint(service_type="dns")

    headers = {
        "X-Auth-All-Projects": "true"
    }

    resp = conn.session.get(dns_endpoint + f"/v2/quotas/{project_id}", headers=headers)
    quotas = resp.json()

    for quota_key in new_quotas:
        if new_quotas[quota_key] != quotas[quota_key]:
            changed = True
            break

    if changed and not module.check_mode:
        conn.session.patch(dns_endpoint + f"/v2/quotas/{project_id}", json=new_quotas, headers=headers)

    module.exit_json(changed=changed, new_quotas=new_quotas)

if __name__ == '__main__':
    main()
