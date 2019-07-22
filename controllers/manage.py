# import string, datetime


T_DB = DAL('sqlite:memory:')
# T_DB = DAL('sqlite://storage.sqlite')


@AUTH.requires(is_user() or is_admin())
# caching for simple performance reasons
@cache.action(time_expire=300, cache_model=cache.ram, prefix='factory')
def factory():
    class_name = request.get_vars['class']
    class_uri = ''

    view_by_id = request.get_vars.pop('id', None)
    
    class_uri = TBOXI.get_model(class_name, 'identifier')
    
    result_list = ABOXI.get_instances(class_uri)

    if isinstance(result_list, Exception):
        response.flash = T("Exception: " + str(result_list))
        result_list = []

    fields = get_table_fields(class_uri)

    # Gracefully fail in case no fields have matched
    if fields == []:
        object_list = [Field('none')]
        response.flash('Field or table not found in domain model.')

    global T_DB

    T_DB.define_table(class_name, *fields)
    T_DB[class_name].id.readable = False
    T_DB[class_name].truncate()
    for k in result_list:
        T_DB[class_name].insert(**k)

    query = T_DB[class_name]

    if view_by_id:
        query = T_DB(T_DB[class_name].identifier == view_by_id)
    
    form = SQLFORM.grid(query, csv=False, maxtextlength=70,
                        links_in_grid=False, oncreate=on_create,
                        onupdate=on_update, ondelete=on_delete,
                        searchable=True)

    try:
        form.element(_id='delete_record__row')['_class'] = 'hidden'
    except Exception:
        pass

    try:
        form.element(_id='delete_record__label')['_class'] = 'hidden'
    except Exception:
        pass

    return dict(form=form,
                extra=TBOXI.get_model(class_name))


def on_create(form):
    # For disabling refresh on form re-submission
    if session.on_create == form.vars:
        return

    session.on_create = form.vars
    payload = dict(form.vars)
    payload.pop('id', None)

    print 'in on create'

    class_name = request.get_vars['class']

    if class_name is not None:
        class_type = TBOXI.get_model(class_name, 'identifier')
        ABOXI.create(payload, class_type)  

    cache.ram.clear('factory*')


def on_update(form):
    class_name = request.get_vars['class']
    try:
        payload = dict(T_DB[class_name][form.vars.id])
    except Exception:
        print ("Temporary Table name not found!", class_name)
    else:
        # payload=dict(form.vars)
        del_rec = payload.pop('delete_this_record', None)
        payload.pop('id', None)
        payload.pop('update_record', None)
        payload.pop('delete_record', None)

        if del_rec != 'on':
            result = ABOXI.update(payload)
            response.flash = T(str(result))
        # else:
            #   return on_update_delete(json_payload)

    cache.ram.clear('factory*')


def on_delete(table, record_id):
    payload = dict(T_DB[table][record_id])
    payload.pop('delete_record', None)
    payload.pop('update_record', None)
    payload.pop('id', None)

    cache.ram.clear('factory*')

    return ABOXI.delete(payload)
