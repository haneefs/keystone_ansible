from keystone_v3 import process_module_action
import sys
import json


class TestModule(object):

    def __init__(self):
        self.params = {}

    def exit_json(self, **kwargs):
        ''' return from the module, without error '''

        if not 'changed' in kwargs:
            kwargs['changed'] = False

        print self.jsonify(kwargs)

    def fail_json(self, **kwargs):
        ''' return from the module, with an error message '''

        assert 'msg' in kwargs, "implementation error -- msg to explain the error is required"
        kwargs['failed'] = True

        print self.jsonify(kwargs)

    def jsonify(self, data):
        for encoding in ("utf-8", "latin-1", "unicode_escape"):
            try:
                return json.dumps(data, encoding=encoding)
            # Old systems using simplejson module does not support encoding
            # keyword.
            except TypeError, e:
                return json.dumps(data)
            except UnicodeDecodeError, e:
                continue
        self.fail_json(msg='Invalid unicode encoding encountered')


def test_process(module):
    import os

    os.environ["no_proxy"] = "localhost"

    print "Testing %s" % module.params["action"]
    process_module_action(module)


def get_login_cred(module):

    module.params["login_username"] = "admin1"
    module.params["login_project_name"] = "admin"
    module.params["login_user_domain_name"] = "Default"
    module.params["login_project_domain_name"] = "Default"
    module.params["login_password"] = "password"
    module.params["endpoint"] = "http://localhost:35357/v3"


def get_token_cred(module):
    module.params["auth_url"] = "http://localhost:35357/v3"
    module.params["token"] = "ADMIN"


def test_find_domain(module):
    module.params["action"] = "find_domain"
    module.params["domain_name"] = "Invalid_domain"
    test_process(module)

    module.params["domain_name"] = "Default"
    test_process(module)


def test_create_domain(module):
    module.params["action"] = "create_domain"
    module.params["domain_name"] = "TestDomain"
    module.params["description"] = "TestDescription"

    test_process(module)


def test_delete_domain(module):
    module.params["action"] = "delete_domain"
    module.params["domain_name"] = "TestDomain"

    test_process(module)


def test_find_user(module):
    module.params["action"] = "find_user"
    module.params["domain_name"] = "Invalid_domain"
    module.params["user_name"] = "admin"
    test_process(module)

    module.params["user_domain_name"] = "Default"
    test_process(module)

    module.params["user_name"] = "Invalid_user"
    test_process(module)


def test_create_user(module):
    module.params["action"] = "create_user"
    module.params["user_domain_name"] = "Default"
    module.params["description"] = "TestDescription"
    module.params["user_name"] = "TestUser"
    module.params["user_password"] = "TestUserPwd"

    test_process(module)


def test_delete_user(module):
    module.params["action"] = "delete_user"
    module.params["domain_name"] = "Default"
    module.params["user_domain_name"] = "Default"

    test_process(module)


def test_find_project(module):
    module.params["action"] = "find_project"
    module.params["project_domain_name"] = "Invalid_domain"
    module.params["project_name"] = "admin"
    test_process(module)

    module.params["project_domain_name"] = "Default"
    test_process(module)

    module.params["project_name"] = "Invalid_project"
    test_process(module)


def test_create_project(module):
    module.params["action"] = "create_project"
    module.params["project_domain_name"] = "Default"
    module.params["description"] = "TestDescription"
    module.params["project_name"] = "Testproject"

    test_process(module)


def test_delete_project(module):
    module.params["action"] = "delete_project"
    module.params["project_domain_name"] = "Default"
    module.params["project_name"] = "Testproject"

    test_process(module)


def test_find_role(module):
    module.params["action"] = "find_role"
    module.params["role_name"] = "Invalid Role"
    test_process(module)

    module.params["role_name"] = "admin"
    test_process(module)


def test_create_role(module):
    module.params["action"] = "create_role"
    module.params["role_name"] = "Testrole"
    module.params["description"] = "TestDescription"

    test_process(module)


def test_delete_role(module):
    module.params["action"] = "delete_role"
    module.params["role_name"] = "Testrole"

    test_process(module)


def test_grant_revoke_project_role(module):

    test_create_role(module)

    module.params["action"] = "grant_project_role"
    module.params["role_name"] = "Testrole"
    module.params["project_name"] = "admin"
    module.params["project_domain_name"] = "Default"
    module.params["user_name"] = "admin"
    module.params["user_domain_name"] = "Default"

    test_process(module)

    module.params["action"] = "revoke_project_role"
    test_process(module)


def test_grant_revoke_domain_role(module):

    test_create_role(module)

    module.params["action"] = "grant_domain_role"
    module.params["role_name"] = "Testrole"

    module.params["domain_name"] = "Default"
    module.params["user_name"] = "admin"
    module.params["user_domain_name"] = "Default"

    test_process(module)

    module.params["action"] = "revoke_domain_role"
    test_process(module)

    test_delete_role(module)


def test_create_service(module):

    module.params["action"] = "create_service"
    module.params["service_name"] = "TestService"

    module.params["service_type"] = "TestServiceType"
    module.params["description"] = "TestServiceDescription"
    

    test_process(module)


def test_create_endpoint(module):

    module.params["action"] = "create_endpoint"
    module.params["service_name"] = "TestService"

    module.params["region"] = "regiona_a"
    module.params["internal_url"] = "http://internalurl/"
    module.params["admin_url"] = "http://internalurl/"
    module.params["public_url"] = "http://internalurl/"
    

    test_process(module)


if __name__ == '__main__':

    try:
        '''
        module = TestModule()
        get_login_cred(module)
        test_find_domain(module)

        module = TestModule()
        get_login_cred(module)
        test_create_domain(module)

        module = TestModule()
        get_login_cred(module)
        test_delete_domain(module)

        module = TestModule()
        get_login_cred(module)
        test_find_user(module)

        module = TestModule()
        get_login_cred(module)
        test_create_user(module)

        module = TestModule()
        get_login_cred(module)
        test_delete_user(module)

        module = TestModule()
        get_login_cred(module)
        test_find_project(module)

        module = TestModule()
        get_login_cred(module)
        test_create_project(module)

        module = TestModule()
        get_login_cred(module)
        test_delete_project(module)

        module = TestModule()
        get_login_cred(module)
        test_find_role(module)

        module = TestModule()
        get_login_cred(module)
        test_create_role(module)

        module = TestModule()
        get_login_cred(module)
        test_delete_role(module)

        module = TestModule()
        get_login_cred(module)
        test_grant_revoke_project_role(module)

        module = TestModule()
        get_login_cred(module)
        test_grant_revoke_domain_role(module)
        
        module = TestModule()
        get_login_cred(module)
        test_create_service(module)
        
        '''
        module = TestModule()
        get_login_cred(module)
        test_create_endpoint(module)

    except Exception as e:
        print e
