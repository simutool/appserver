
AUTH.settings.allow_basic_login = True
@AUTH.requires(is_admin() or is_user())
@request.restful()
def api():
    response.view = 'generic.json'

    def PUT(*args, **vars):
        if isinstance(vars, dict) is not True:
            raise HTTP(400)
        
        eml = vars.pop('email', '')
        pwd = vars.pop('password', '')

        # Get id of user
        identifier = ABOXI.get_id_by_email(eml)
        
        # Authenticate user
        login = program_login(eml, pwd)
        
        if login is False \
           or identifier is None:
            raise HTTP(401)

        response = {
            "user_identifier": identifier,
            "object_storage_host": SETTINGS.object_storage_host,
            "object_storage_username": SETTINGS.object_storage_username,
            "object_storage_password": SETTINGS.object_storage_password,
            "document_endpoint": SETTINGS.document_endpoint,
            "id_gen_endpoint": SETTINGS.id_gen_endpoint,
            "inheritance_query_endpoint": SETTINGS.inheritance_query_endpoint,
            "create_activity_endpoint": SETTINGS.create_activity_endpoint
        }
        
        return response

    return locals()
