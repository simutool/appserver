# -*- coding: utf-8 -*-
from gluon.tools import Auth, Service, PluginManager, Crud
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
MYCONF = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    DB = DAL(SETTINGS.db_url_login,
             pool_size=MYCONF.get('DB.pool_size'),
             # migrate_enabled=False,
             migrate=SETTINGS.migrate,
             lazy_tables=True,
             fake_migrate_all=SETTINGS.fake_migrate_all,
             check_reserved=['postgres', 'sqlite'])
    
#   DB = DAL(MYCONF.get('DB.uri'),
#        pool_size=MYCONF.get('DB.pool_size'),
#        migrate_enabled=False,
#        fake_migrate_all=True,
#        migrate_enabled=MYCONF.get('DB.migrate'),
#        check_reserved=['all'])

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*']
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = MYCONF.get('forms.formstyle')
# or 'bootstrap3_stacked' or 'bootstrap2' or other

response.form_label_separator = MYCONF.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - AUTHentication (registration, login, logout, ... )
# - AUTHorization (role based AUTHorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
AUTH = Auth(DB, host_names=MYCONF.get('host.names'))
SERVICE = Service()
PLUGINS = PluginManager()

# -------------------------------------------------------------------------
# create all tables needed by AUTH if not custom tables
# -------------------------------------------------------------------------

# Auth Table Creation code moved to db_wizard.py
# because it contains references other tables

CRUD = Crud(DB)

CRUD.settings.auth = AUTH

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
MAIL = AUTH.settings.mailer
# if request.is_local:
#     MAIL.settings.server = 'logging'
# else:
#     MAIL.settings.server = MYCONF.get('smtp.server')

MAIL.settings.server = MYCONF.get('smtp.server')

MAIL.settings.sender = MYCONF.get('smtp.sender')
MAIL.settings.login = MYCONF.get('smtp.login')
MAIL.settings.tls = MYCONF.get('smtp.tls') or False
MAIL.settings.ssl = MYCONF.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure AUTH policy
# -------------------------------------------------------------------------
AUTH.settings.registration_requires_verification = False
AUTH.settings.registration_requires_approval = False
AUTH.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> DB.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#     'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> DB.mytable.insert(myfield='value')
# >>> rows = db(DB.mytable.myfield == 'value').select(DB.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# AUTH.enable_record_versioning(db)


# -------------------------------------------------------------------------
# Define User table and rename the deafault web2py auth_user to t_user
# -------------------------------------------------------------------------
AUTH.settings.table_user_name = 't_user'

AUTH.settings.extra_fields['t_user'] = [
    Field('f_label', type='string', label=T('Title'),
          readable=False),
    # Field('kms_id', label=T('KMS ID')),
    Field('f_description', type='text', label=T('Description'))]

AUTH.define_tables(username=False, signature=False)

CUSTOM_AUTH_TABLE = DB[AUTH.settings.table_user_name]

AUTH.settings.table_user = CUSTOM_AUTH_TABLE

AUTH.settings.email_case_sensitive = False



DB.t_user._extra = TBOXI.get_model('user')
# DB.t_user.singular = TBOXI.get_model('user', 'sing')
# DB.t_user.plural = TBOXI.get_model('user', 'pl')

# -------------------------------------------------------------------------
# End of User table definition code
# -------------------------------------------------------------------------



# -------------------------------------------------------------------------
# Define File System table
# -------------------------------------------------------------------------

DB.define_table(
  'fs',
  Field('uploadfield', type='upload'),
  Field('original_filename'),
  Field('download_url'),
  # TODO: make a unique constraint when changing DB to postgres
  Field('unique_name', unique=True),
  Field('uploader'))


NUM_USERS = len(DB().select(AUTH.settings.table_user.ALL))
if NUM_USERS == 0 and SETTINGS.first_user_email and SETTINGS.first_user_pass:
    register_first_admin_user_bare(
        SETTINGS.first_user_email,
        SETTINGS.first_user_pass)


def program_login(email, password):
    # DB.t_user.password.requires = None
    return AUTH.login_bare(email, password)


ABOXI.query('')