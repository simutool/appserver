import logging
from gluon.contrib.appconfig import AppConfig
from gluon.storage import Storage

from tbox_interface import TBoxInterface
from abox_interface import ABoxInterface


# Doesn't work well anyway even for dev/testing 
# from gluon.custom_import import track_changes
# track_changes(True)

SETTINGS = Storage()
MYCONF = AppConfig(reload=False)

# read values from private/config.ini
SETTINGS.app_view_name = MYCONF.take('app.view_name', cast=str)
SETTINGS.app_name = MYCONF.take('app.app_name', cast=str)
SETTINGS.maintainer_eml = MYCONF.take('app.maintainer_eml', cast=str)
SETTINGS.base_url = MYCONF.take('app.base_url', cast=str)

SETTINGS.document_endpoint = MYCONF.take('app.document_endpoint', cast=str)
SETTINGS.id_gen_endpoint = MYCONF.take('app.id_gen_endpoint', cast=str)
SETTINGS.inheritance_query_endpoint = MYCONF.take('app.inheritance_query_endpoint', cast=str)
SETTINGS.create_activity_endpoint = MYCONF.take('app.create_activity_endpoint', cast=str)


SETTINGS.db_url_login = MYCONF.take('auth_db.db_url_login', cast=str)
SETTINGS.migrate = MYCONF.take('auth_db.migrate', cast=bool)
SETTINGS.fake_migrate_all = MYCONF.take('auth_db.fake_migrate_all', cast=bool)
SETTINGS.admn_grp = MYCONF.take('auth_db.admn_grp', cast=str)
SETTINGS.non_admn_grp = MYCONF.take('auth_db.non_admn_grp', cast=str)

SETTINGS.graph_url = MYCONF.take('garph_db.graph_url', cast=str)
SETTINGS.graph_user = MYCONF.take('garph_db.graph_user', cast=str)
SETTINGS.graph_pass = MYCONF.take('garph_db.graph_pass', cast=str)

SETTINGS.first_user_email = MYCONF.take('first_startup.admin_email', cast=str)
SETTINGS.first_user_pass = MYCONF.take('first_startup.admin_pass', cast=str)

SETTINGS.fs_download_url = MYCONF.take('file_server.fs_download_url', cast=str)
SETTINGS.object_storage_host = MYCONF.take('file_server.object_storage_host', cast=str)
SETTINGS.object_storage_username = MYCONF.take('file_server.object_storage_username', cast=str)
SETTINGS.object_storage_password = MYCONF.take('file_server.object_storage_password', cast=str)


# initialize logger
SETTINGS.logger_name = '%s.%s' % ('web2py.app', SETTINGS.app_name)
logger = logging.getLogger(SETTINGS.logger_name)
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s' +
                    ' %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logfile.log')


PATH = "applications/%s/modules/kgservice/" % SETTINGS.app_name

TBOXI = TBoxInterface(SETTINGS.graph_url,
                      SETTINGS.graph_user,
                      SETTINGS.graph_pass,
                      PATH,
                      SETTINGS.logger_name)

ABOXI = ABoxInterface(SETTINGS.graph_url,
                      SETTINGS.graph_user,
                      SETTINGS.graph_pass,
                      PATH,
                      SETTINGS.logger_name)



SETTINGS.baseURL = '%s://%s/%s' % (request.env.wsgi_url_scheme, request.env.http_host,
                                   request.application) 



def register_first_admin_user_bare(email, password):
    u_id = AUTH.register_bare(email=email, password=password).id
    try:
        AUTH.add_membership(SETTINGS.admn_grp,
                            AUTH.settings.table_user(u_id))
    except Exception:
        AUTH.add_group(SETTINGS.admn_grp,
                       ('Default automatically created admin group'
                        'by register_first_admin_user_bare function.'))
        AUTH.add_membership(SETTINGS.admn_grp,
                            AUTH.settings.table_user(u_id))
    try:
        AUTH.add_membership(SETTINGS.non_admn_grp,
                            AUTH.settings.table_user(u_id))
    except Exception:
        AUTH.add_group(SETTINGS.non_admn_grp,
                       ('Default automatically created user group'
                        'by register_first_admin_user_bare function.'))
        AUTH.add_membership(SETTINGS.non_admn_grp,
                            AUTH.settings.table_user(u_id))

