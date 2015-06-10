# keystone_ansible

keystone_v3 provides support for keystone v3 api. 

This module doesn't attempt to provide all the keystone_v3 apis. Only those apis that are required for deploying keystone  are provoided

Supported actions:
   - create/find/delete user
   - create/find/delete domain
   - create/find/delete projects
   - create services
   - create endpoints
     create/delete roles
     grant both project and domain scoped roles

Few Implementation details
   - All the actions use name as parameter instead of id. Since names are unique only within its enclosing domain, the caller needs to qualify with domain name.
   - Supports both domain and project scoped tokens. Scope of the token is determined based in parameters
   - All the filters are send to keystone for filtering. e.g  find_user(name=joe, user_domain_name=default) sends the parameters to keystone and gets  the filtered results. This is main difference when compared with v2 modules, which  gets all the users and filters in the client side which doesn't work if there are more number of users ( keystone configured with ldap)
   - In keystone v3, you can't delete unless the status is disabled. Delete operations disables the resource before deleting it
   - By default uses insecure mode for ssl which can be overriden by passing cacerts
   - Uses explicit action instead of state="present/absent" for create/delete. Using state="absent" for delete makes parameter validation 
     difficult. e.g for deleting user need "username/user_domain_name". create_user needs username/user_domain_name/password.   
   - All the operations are idempotent 

Not supported:
    - check mode

Todo:
  - Parameter validation and checking of required parameters
  - Support for creating identity provider / service provider and configuring the same


