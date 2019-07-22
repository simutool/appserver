# import tzlocal
from datetime import datetime


def is_admin():
    return AUTH.has_membership(SETTINGS.admn_grp)


def is_user():
    return AUTH.has_membership(SETTINGS.non_admn_grp)


def format_res(res_list):
    """
    returns something of this format:
     {'http://example.org/tbox/kbmsthing': 'kbmsthing',
      'http://example.org/tbox/user': 'User',
      'http://example.org/tbox/productdesign': 'Product Design',
      'http://example.org/tbox/data': 'Data'}
    """        
    final_dict = {}
    for res in res_list:
        try:
            final_dict[res['identifier']] = res['title']
        except KeyError as exception:
            print exception
    return final_dict


def get_table_fields(class_uri):
    """
    returns a list of web2py Field objects, possible types:
        - ref [class_uri]
        - type
        - identifier
        - datetime (temporarily disabled)
        - upload (temporarily disabled)
        - string
        - any other value defaults to string too
    """
    object_list = []
    fields = get_fields_and_types(class_uri)
    for field in fields:
        field_type = field[1].lower()
        field = field[0]
        if field_type.startswith('ref '):
            class_title = field_type.lstrip('ref ')
            class_id = TBOXI.get_model(class_title, 'identifier')
            instances = format_res(ABOXI.get_instances(class_id))
            fld = Field(field, requires=IS_IN_SET(instances, multiple=True,
                                                  zero=T('Please select all relevant items:')))
            object_list.append(fld)
        elif field_type == 'type':
            # sub_self = get_subtypes_title(referenced_class,
            #                               include_self=True,
            #                               direct_children=False)
            # fld = Field(field, requires=IS_IN_SET(sub_self,
            #                                       zero=T('Select one:')))
            object_list.append(Field(field,
                                     readable=False, writable=False))
        elif field_type == 'identifier':
            object_list.append(Field(field,
                                     readable=True, writable=False))
        elif field_type == 'datetime':
            object_list.append(Field(field, type='datetime',
                                     format=T('%Y-%m-%d %H:%M:%S')))
            # object_list.append(Field(field))
        elif field_type == 'upload':
            object_list.append(Field(field, type='upload'))
        else:
            object_list.append(Field(field))

    return object_list





def get_fields_and_types(class_uri):
    """returns a dict of {'field1_name': 'field1_type',
                          'field2_name': 'field2_type'}

    'field_type' is one of the folowing formats:
        'ref [class_uri]' a reference/relation to instance of another class
        'type' a type attribute, which should be a list of class uris
               fetched using the function subtypes_self(class_uri)
        'identifier' an id that cannot be writable or editable by the user
        'datetime'
        anything else defaults to string
    """
    p_r_list = TBOXI.get_peoperties_relations(class_uri)
    p_r_list2 = []
    for p_r in p_r_list:
        p_r_list2.append([p_r, get_type(p_r)])
    return p_r_list2


def get_type(field_name):
    """Takes a field name and returns its type by looking up
       the TBOXI. If the field is not
       found in the dict then it's type is a string."""
    try:
        return TBOXI.get_type(field_name)
    except KeyError:
        return 'string'


def gen_rel_path(item):
    return 'factory?class=%s' % item


def get_menu_item(item_name):
    item_url = gen_rel_path(item_name)
    return (T(item_name.capitalize()),
            URL('manage', item_url) == URL(),
            URL('manage', item_url), [])


def kbms_converter(obj):
    if isinstance(obj, datetime):
        # add time zone info
        # obj = obj.replace(tzinfo=tzlocal.get_localzone())
        # convert to iso
        obj = obj.isoformat()
        split = obj.__str__().split('T')
        sqlite_f = "%s %s" % (split[0], split[1])
        return sqlite_f
    return None


# Generates a web2py menu based on domain model
def get_sub_menu(root_class_uri, root_class_name):
    menu = [(T('Home'),
             URL('default', 'index') == URL(),
             URL('default', 'index'), [])]

    isadmin = TBOXI.get_model(root_class_name, 'admin')
    
    if isadmin and isadmin.lower() == "false":
        menu.append(get_menu_item(root_class_name))
    elif is_admin():
        menu.append(get_menu_item(root_class_name))

    direct_children = TBOXI.get_subtypes(root_class_uri,
                                         include_self=False,
                                         direct_children=True)

    # skip the root class item, we have already included it in the menu
    # direct_children=direct_children_self.pop(root_class_uri, None)

    for c_uri, c_name in direct_children.iteritems():
        c_uri = str(c_uri)
        c_name = str(c_name.lower())

        decendants_of_children = TBOXI.get_subtypes(c_uri,
                                              include_self=True,
                                              direct_children=False)

        # remove the parent class to add it at the
        # end of the list for usability reasons
        decendants_of_children.pop(c_uri, None)

        sub_list = []
        for c_c_uri, c_c_name in decendants_of_children.iteritems():
            c_c_uri = str(c_c_uri)
            c_c_name = str(c_c_name.lower())
            if TBOXI.get_model(c_c_name, 'admin').lower() == "false":
                sub_list.append(get_menu_item(c_c_name))
            elif is_admin():
                sub_list.append(get_menu_item(c_c_name))

        if TBOXI.get_model(c_name, 'admin').lower() == "false":
            sub_list.append(get_menu_item(c_name))
        elif is_admin():
            sub_list.append(get_menu_item(c_name))

        if sub_list:
            menu.append((T(c_name.capitalize()),
                         URL('manage', gen_rel_path(c_name)) == URL(),
                         URL('manage', gen_rel_path(c_name)), sub_list))
    menu.append((T('Feedback?'),
                 URL('default', 'feedback') == URL(),
                 URL('default', 'feedback'), []))
    return menu
