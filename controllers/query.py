# import json
# import requests

# @auth.requires(admin() or user())
# def query():

#   form = SQLFORM.factory(
# #    Field('uploader_name', label='Uploader', requires=IS_IN_DB(db, db.auth_user.email)),
# #    Field('upload_ipurpose', label='Purpose', requires=IS_IN_DB(db, db.upload_ipurpose.name)),
#     Field('upload_idate', label='Date of Upload',type='date'),
# #    Field('tags', label='Tags', requires=IS_IN_SET(all_tags.keys())),
#     Field('description', label='Description'))

#   on_search(request)

#   return dict(form=form)


# @auth.requires(admin() or user())
# def on_search(request):
#   query = {}
#   for rv in request.vars:
#     if request.vars[rv] is not '':
#       query[rv]=request.vars[rv]

#   if len(query.keys()) > 0:
    
#     logger.debug('Query submitted, the following json query has been generated  ('+str(query)+')')
#     logger.debug('Preparing to perform a HTTP post request to (xxx) with the json query')

#     #param={'query': query}
#     #print param

#     response = requests.post(settings.kr_pull_url, data=query)

#     session._json=json.dumps(response.json())
#     redirect(URL('query','display_results'))

# @auth.requires(admin() or user())
# def display_results():

#   json_str=session._json

#   response_dict= json.loads(json_str)
#   result_list=response_dict['results']

#   fields = []
#   for k in result_list[0].keys():
#     fields.extend([Field(k)])
  
#   # Changed to in-memory db to temporarily store query results 
#   # If this doesnt work remove the next line and rename all the occurences of 't_db' to 'db'
#   t_db=DAL('sqlite:memory:')
#   t_db.define_table('temp_table', *fields)
#   t_db.temp_table.truncate()
   
#   for k in result_list:
#     print k.values()
#     t_db.temp_table.insert(**k)

#   form = SQLFORM.grid(t_db.temp_table, deletable=False, editable=False)
#   return dict(form=form)


# #json_example = '{"results": [ {"doc_type": "Experiment Parameters", "modified_by": "1",   "description": "fg",     "upload_idate": "2016-09-06 16:51:14",     "data_file": "simutool_documents.data_file.ad5d3120e1211e8f.53637265656e73686f742066726f6d20323031362d30382d32392032332d30352d30382e706e67.png",     "attribute": "val",     "tags": "[2]",     "is_active": "True",     "visibility": "private",     "created_on": "2016-09-06 16:51:14",     "created_by": "1",     "download_link": "http://141.13.162.170:8000/kbwebclient/data/doc/37",     "uploader_name": "nasr.kasrin@uni-bamberg.de",     "modified_on": "2016-09-06 16:51:14",     "uploader": "1"   }  ]  }'

# #json_example_2 = '{"results": [ {"doc_type": "Experiment Parameters", "modified_by": "1"}]}'
