

AUTH.settings.allow_basic_login = True
@AUTH.requires(is_admin() or is_user())
@request.restful()
def api():
    response.view = 'generic.json'

    # Read (if url query key == 'id' gets instance 
    #       else if it == 'type' calls get_instances)
    def GET(*args, **vars):
        if not vars:
            raise HTTP(400)
        # identifier = vars.values()[0]
        if 'id' in vars.keys():
            payload = {'payload': [{'identifier': vars.pop('id', None)}]}
            return get(payload)
        elif 'type' in vars.keys():
            class_name = vars.pop('type', None)
            response = get_instances(class_name)
            response = prep_response(response)
            return {'payload': response}
        else:
            raise HTTP(400)


    # Create
    def PUT(*args, **vars):
        if isinstance(vars, dict) is not True \
           or 'payload' not in vars.keys() \
           or 'type' not in vars.keys():
            raise HTTP(400)
        
        payload = {'payload': vars.pop('payload', None)}
        class_title = vars.pop('type', None)
        response = create(payload, class_title)
        response = prep_response(response)
        return response


    # Update
    def POST(*args, **vars):
        if isinstance(vars, dict) is not True or \
           'payload' not in vars.keys():
            raise HTTP(400)
        payload = {'payload': vars.pop('payload', None)}
        response = update(payload)
        response = prep_response(response)
        return response


    # Delete
    def DELETE(*args, **vars):
        if isinstance(vars, dict) is not True or \
           'id' not in vars.keys():
            raise HTTP(400)
        iden = vars.pop('id', None)

        # remove surrounding quotes, in case the user
        # mistakingly enclosed the uri in " or '
        iden = iden.strip('\'\"')
        payload = {'payload': [{'identifier': iden}]}
        response = delete(payload)
        response = prep_response(response)
        return response

    return locals()


def prep_response(result):
    if isinstance(result, Exception):
        result = {str(type(result)): str(result)}
    return result
