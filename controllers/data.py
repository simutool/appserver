import uuid
import os
from gluon.streamer import DEFAULT_CHUNK_SIZE

BASE_DOWN_URL = SETTINGS.base_url + SETTINGS.fs_download_url

AUTH.settings.allow_basic_login = True
@AUTH.requires(is_admin() or is_user())
@request.restful()
def api():
    response.view = 'generic.json'

    def GET(*args, **vars):
        if vars == {} \
           or args == ():
            raise HTTP(400)
        
        endpoint = args[0]
        filename = vars.values()[0]

        # remove surrounding quotes, in case the user
        # mistakingly enclosed the filename in " or '
        filename = filename.strip('\'\"')

        if filename == "":
            raise HTTP(400)

        if endpoint == 'unique-name':
            ext = os.path.splitext(filename)[1]
            uuid4 = str(uuid.uuid4())
            unique_name = uuid4 + ext
            down_url = BASE_DOWN_URL + unique_name
            result = {'unique_name': unique_name,
                      'url': down_url}

            record = DB.fs.insert(
                #uploadfield=None,
                unique_name=unique_name,
                original_filename=filename)

            return result
        
        elif endpoint == 'document':
            rec = DB(DB.fs.unique_name == filename).select().first()
            if rec == None:
                raise HTTP(404)
            original_fn = rec.original_filename
            path = os.path.join(request.folder, 'uploads/', filename)
            return response.stream(path,
                                   4096, 
                                   request=request, 
                                   attachment=True, 
                                   filename=original_fn)
        else:
            raise HTTP(400)


    def PUT(*args, **vars):
        # print request.body
        # record = DB.fs.insert()
        # print record
        content_type = request.env.HTTP_CONTENT_TYPE
        filename = request.env.HTTP_FILENAME
        print (filename, content_type)
        # record =  DB.fs.insert(uploadfield=request.body)
        # with open(request.body, 'rb') as stream:

        # We shorten the filename because of os filename limit,
        # see https://groups.google.com/forum/#!topic/web2py/ee6NBnj_TyU
        short_name = get_short_name(filename)

        record = DB.fs.insert(
            uploadfield=DB.fs.uploadfield.store(
                file=request.body,
                filename=short_name),
            original_filename=filename)


    return locals()


def get_short_name(filename):
    fname = filename.split('.')
    extension = fname[-1]
    short_name = '.'.join(fname[0:-1])
    short_name = short_name[0:40]
    short_name = '%s.%s' % (short_name, extension)
    return short_name

def get_uuid(filename):
    return uuid.uuid5(uuid.NAMESPACE_DNS, filename)

# with open(filename, 'rb') as stream:
#     db.myfile.insert(image=DB.fs.uploadfield.store(stream, filename),
#                      image_file=stream.read())

# uploadfs allows you specify a different file system where to upload files,
# including an Amazon S3 storage or a remote SFTP storage.
# You need to have PyFileSystem installed for this to work
# uploadfs must point to PyFileSystem.'


# def upload():
#      table =  db.tablename
#      record =  db.tablename[request.args(0)]
#      record.update_record(uploadfield=record.store(file=request.body,filename=request.args(1))
#      return 'done'
