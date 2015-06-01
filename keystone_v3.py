#!/usr/bin/python
# -*- coding: utf-8 -*-
from duplicity.commandline import verify
from __builtin__ import False


DOCUMENTATION = '''
---
module: keystone_v3
version_added: "1.0"
short_description: Manage OpenStack Identity (keystone v3) users, tenants and roles
description:
   - Manage users,tenants, roles from OpenStack.
requirements: [ python-keystoneclient ]
author: Haneef Ali
'''

EXAMPLES = '''
# Create a tenant
- keystone_user: tenant=demo tenant_description="Default Tenant"

# Create a user
- keystone_user: user=john tenant=demo password=secrete

# Apply the admin role to the john user in the demo tenant
- keystone: role=admin user=john tenant=demo
'''


from keystoneclient.v3 import client as v3client
from keystoneclient.auth.identity import v3
from keystoneclient.auth import  token_endpoint
from keystoneclient import session


def _get_client(auth_url=None, token=None, login_username=None, login_password=None, login_project_name=None,
                login_project_domain_name=None, login_user_domain_name=None, login_domain_name=None,
                insecure=True, ca_cert=None):
    """Return a ks_client client object"""

    auth_plugin = None
    if token:
        auth_plugin = token_endpoint.Token(endpoint=auth_url, token=token)
    else:
        auth_plugin = v3.Password(auth_url=auth_url, username=login_username, password=login_password,
                                  project_name=login_project_name, project_domain_name=login_project_domain_name,
                                  user_domain_name=login_user_domain_name, domain_name=login_domain_name)

    # Force validation if ca_cert is provided
    if ca_cert:
        insecure = False
    auth_session = session.Session(
        auth=auth_plugin, verify=verify, cert=ca_cert)
    return v3client.Client(auth_url=auth_url, session=auth_session)


def _find_domain(ks_client, domain_name=None):
    domains = ks_client.domains.list(name=domain_name)
    return domains[0] if len(domains) else None


def _delete_domain(ks_client, domain=None):

    ks_client.domains.update(domain, enabled=False)
    return ks_client.domains.delete(domain)


def _create_domain(ks_client, domain_name=None, description=None):
    return ks_client.domains.create(name=domain_name, description=description)


def _find_user(ks_client, domain_name=None, user_name=None):
    domain = _find_domain(ks_client, domain_name=domain_name)

    if domain:
        users = ks_client.users.list(domain=domain, name=user_name)
        if len(users):
            return users[0]


def _create_user(ks_client, user_name=None, user_password=None, domain_name=None,
                 email=None, description=None):

    domain = _find_domain(ks_client, domain_name)
    return ks_client.users.create(name=user_name, password=user_password,
                                  description=description,
                                  email=email, domain=domain)


def _delete_user(ks_client, user=None):
    ks_client.users.update(user=user, enabled=False)
    ks_client.users.delete(user=user)


def _find_project(ks_client, domain_name=None, project_name=None):
    domain = _find_domain(ks_client, domain_name=domain_name)

    if domain:
        projects = ks_client.projects.list(domain=domain, name=project_name)
        if len(projects):
            return projects[0]


def _create_project(ks_client, project_name=None, domain_name=None,
                    description=None):

    domain = _find_domain(ks_client, domain_name)
    return ks_client.projects.create(name=project_name,
                                     description=description,
                                     domain=domain)


def _delete_project(ks_client, project=None):
    ks_client.projects.update(project=project, enabled=False)
    ks_client.projects.delete(project=project)


def _find_role(ks_client, role_name=None):
    roles = ks_client.roles.list(name=role_name)
    return roles[0] if len(roles) else None


def _delete_role(ks_client, role=None):
    return ks_client.roles.delete(role)


def _create_role(ks_client, role_name=None, description=None):
    return ks_client.roles.create(name=role_name, description=description)


def _grant_roles(ks_client, role=None, project=None, user=None, domain=None):
    return ks_client.roles.grant(role=role, project=project, user=user, domain=domain)


def _revoke_roles(ks_client, role=None, project=None, user=None, domain=None):
    return ks_client.roles.revoke(role=role, project=project, user=user, domain=domain)


def find_domain(ks_client, domain_name=None):
    domain = _find_domain(ks_client, domain_name=domain_name)
    result, domain = (True, domain) if (domain) else (False, None)
    return result, domain


def create_domain(ks_client, domain_name=None, description=None):

    domain = _find_domain(ks_client, domain_name=domain_name)

    if domain:
        return (False,  domain)

    # Domain with that name doesn't exist
    domain = _create_domain(
        ks_client, domain_name=domain_name, description=description)
    return (True, domain)


def delete_domain(ks_client, domain_name=None):

    domain = _find_domain(ks_client, domain_name=domain_name)

    if domain:
        _delete_domain(ks_client, domain=domain)
        return (True, domain)

     # Domain with that name doesn't exist
    return (False, None)


def find_user(ks_client, user_name=None, domain_name=None):
    user = _find_user(ks_client, domain_name=domain_name, user_name=user_name)
    result, user = (True, user) if user else (False, None)
    return result, user


def create_user(ks_client, user_name=None, user_password=None, domain_name=None,
                email=None, description=None):

    user = _find_user(ks_client, user_name=user_name, domain_name=domain_name)

    if user:
        return (False,  user)

    # Domain with that name doesn't exist
    user = _create_user(ks_client, user_name=user_name,
                        user_password=user_password, domain_name=domain_name,
                        email=email, description=description)
    return (True, user)


def delete_user(ks_client, user_name=None, domain_name=None):

    user = _find_user(ks_client, domain_name=domain_name, user_name=user_name)

    if user:
        _delete_user(ks_client, user=user)
        return (True, user)

     # Domain with that name doesn't exist
    return (False, None)


def find_project(ks_client, project_name=None, domain_name=None):
    project = _find_project(
        ks_client, domain_name=domain_name, project_name=project_name)
    result, project = (True, project) if project else (False, None)
    return result, project


def create_project(ks_client, project_name=None, domain_name=None,
                   description=None):

    project = _find_project(
        ks_client, project_name=project_name, domain_name=domain_name)

    if project:
        return (False,  project)

    # Domain with that name doesn't exist
    project = _create_project(ks_client, project_name=project_name,
                              domain_name=domain_name, description=description)
    return (True, project)


def delete_project(ks_client, project_name=None, domain_name=None):

    project = _find_project(
        ks_client, domain_name=domain_name, project_name=project_name)

    if project:
        _delete_project(ks_client, project=project)
        return (True, project)

     # Domain with that name doesn't exist
    return (False, None)


def find_role(ks_client, role_name=None):
    role = _find_role(ks_client, role_name=role_name)
    result, role = (True, role) if (role) else (False, None)
    return result, role


def create_role(ks_client, role_name=None, description=None):

    role = _find_role(ks_client, role_name=role_name)

    if role:
        return (False,  role)

    # role with that name doesn't exist
    role = _create_role(
        ks_client, role_name=role_name, description=description)
    return (True, role)


def delete_role(ks_client, role_name=None):

    role = _find_role(ks_client, role_name=role_name)

    if role:
        _delete_role(ks_client, role=role)
        return (True, role)

     # role with that name doesn't exist
    return (False, None)


def _grant_or_revoke_project_role(ks_client, role_name=None, user_name=None, project_name=None,
                                  user_domain_name=None, project_domain_name=None, grant=True):

    role = _find_role(ks_client, role_name=role_name)
    user = _find_user(
        ks_client, user_name=user_name, domain_name=user_domain_name)
    project = _find_project(
        ks_client, project_name=project_name, domain_name=project_domain_name)

    if (user and role and project):
        if (grant):
            _grant_roles(ks_client, role=role, project=project, user=user)
        else:
            _revoke_roles(ks_client, role=role, project=project, user=user)
        return (True, "OK")

    return (False, "Not able to find user/role/project with the given inputs")


def _grant_or_revoke_domain_role(ks_client, role_name=None, user_name=None,
                                 user_domain_name=None, domain_name=None, grant=True):

    role = _find_role(ks_client, role_name=role_name)
    user = _find_user(
        ks_client, user_name=user_name, domain_name=user_domain_name)
    domain = _find_domain(ks_client,  domain_name=domain_name)

    if (user and role and domain):
        if (grant):
            _grant_roles(ks_client, role=role, domain=domain, user=user)
        else:
            _revoke_roles(ks_client, role=role, domain=domain, user=user)
        return (True, "OK")

    return (False, "Not able to find user/role/domain with the given inputs")


def grant_project_role(ks_client, role_name=None, user_name=None, project_name=None,
                       user_domain_name=None, project_domain_name=None):

    return _grant_or_revoke_project_role(ks_client, role_name=role_name, user_name=user_name,
                                         project_name=project_name, user_domain_name=user_domain_name,
                                         project_domain_name=project_domain_name, grant=True)


def revoke_project_role(ks_client, role_name=None, user_name=None, project_name=None,
                        user_domain_name=None, project_domain_name=None):

    return _grant_or_revoke_project_role(ks_client, role_name=role_name, user_name=user_name,
                                         project_name=project_name, user_domain_name=user_domain_name,
                                         project_domain_name=project_domain_name, grant=False)


def grant_domain_role(ks_client, role_name=None, user_name=None, domain_name=None,
                      user_domain_name=None):

    return _grant_or_revoke_domain_role(ks_client, role_name=role_name, user_name=user_name,
                                        user_domain_name=user_domain_name,
                                        domain_name=domain_name, grant=True)


def revoke_domain_role(ks_client, role_name=None, user_name=None, domain_name=None,
                       user_domain_name=None):
    return _grant_or_revoke_domain_role(ks_client, role_name=role_name, user_name=user_name,
                                        user_domain_name=user_domain_name,
                                        domain_name=domain_name, grant=False)


def process_params(module):

    user_name = module.params.get("user_name", None)
    user_password = module.params.get("user_password", None)
    email = module.params.get("email", None)
    description = module.params.get("description", None)
    user_domain_name = module.params.get("user_domain_name", None)

    domain_name = module.params.get("domain_name", None)

    project_name = module.params.get("project_name", None)
    project_domain_name = module.params.get("project_domain_name", None)

    role_name = module.params.get("role_name", None)
    state = module.params.get("state", "present")

    action = module.params["action"]

    if (action == "find_domain" or action == "delete_domain"):
        kwargs = dict(domain_name=domain_name)
    elif (action == "create_domain"):
        kwargs = dict(domain_name=domain_name, description=description)
    elif (action == "find_user" or action == "delete_user"):
        kwargs = dict(domain_name=user_domain_name, user_name=user_name)
    elif (action == "create_user"):
        kwargs = dict(domain_name=user_domain_name, description=description, user_name=user_name,
                      email=email, user_password=user_password)
    elif (action == "find_project" or action == "delete_project"):
        kwargs = dict(
            domain_name=project_domain_name, project_name=project_name)
    elif (action == "create_project"):
        kwargs = dict(domain_name=project_domain_name, description=description,
                      project_name=project_name)
    elif (action == "find_role" or action == "delete_role"):
        kwargs = dict(role_name=role_name)
    elif (action == "create_role"):
        kwargs = dict(role_name=role_name, description=description)
    elif (action == "grant_project_role" or action == "revoke_project_role"):
        kwargs = dict(role_name=role_name, user_name=user_name,
                      user_domain_name=user_domain_name, project_name=project_name,
                      project_domain_name=project_domain_name)
    elif (action == "grant_domain_role" or action == "revoke_domain_role"):
        kwargs = dict(role_name=role_name, user_name=user_name,
                      user_domain_name=user_domain_name,
                      domain_name=domain_name)

    return kwargs

dispatch_map = {
    "find_domain": find_domain,
    "delete_domain": delete_domain,
    "create_domain": create_domain,

    "find_user": find_user,
    "delete_user": delete_user,
    "create_user": create_user,

    "find_project": find_project,
    "delete_project": delete_project,
    "create_project": create_project,

    "find_role": find_role,
    "delete_role": delete_role,
    "create_role": create_role,

    "grant_project_role": grant_project_role,
    "revoke_project_role": revoke_project_role,
    "grant_domain_role": grant_domain_role,
    "revoke_domain_role": revoke_domain_role

}


def get_client(module):

    login_username = module.params.get("login_username")
    login_project_name = module.params.get("login_project_name")
    login_user_domain_name = module.params.get("login_user_domain_name")
    login_project_domain_name = module.params.get("login_project_domain_name")
    login_password = module.params.get("login_password")
    auth_url = module.params.get("auth_url")
    token = module.params.get("token")

    ks_client = _get_client(login_username=login_username,
                            login_project_name=login_project_name,
                            login_user_domain_name=login_user_domain_name,
                            login_project_domain_name=login_project_domain_name,
                            login_password=login_password,
                            auth_url=auth_url,
                            token=token)

    return ks_client


def process_module_action(module):

    ks_client = get_client(module)

    action = module.params["action"]
    kwargs = process_params(module)

    try:
        result = dispatch_map[action](ks_client, **kwargs)
    except Exception as e:
        module.fail_json(msg="%s, failed" % e)
    else:
        status, resource_data = result
        data = dict(changed=status, result=str(resource_data))
        module.exit_json(**data)


def main():

    supported_actions = dispatch_map.keys()

    argument_spec = dict(
        login_username=dict(default=None),
        login_password=dict(default=None),
        login_project_name=dict(default=None),
        login_project_domain_name=dict(default=None),
        login_user_domain_name=dict(default=None),
        login_domain_name=dict(default=None),
        login_token=dict(default=None),

        user_name=dict(default=None),
        user_domain_name=dict(default=None),
        project_name=dict(default=None),
        project_domain_name=dict(default=None),
        domain_name=dict(default=None),
        role_name=dict(default=None),


        action=dict(default=None, required=True, choices=supported_actions)

    )

    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=False)
    process_module_action(module)

from ansible.module_utils.basic import *
from ansible.module_utils.database import *


if __name__ == '__main__':
    main()
