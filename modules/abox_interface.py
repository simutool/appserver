# This file contains all the functions that interface with the TBox
# It is the only middle-man between TBox and front-end.
import logging
from kgservice import ABox

class ABoxInterface(object):

    def __init__(self, graph_url, usr, pswd, path, parent_logger_name):
        logger_name = self.initialize_logger(parent_logger_name, 'abox_interface')
        self.kgs = ABox.ABoxService(graph_url, usr, pswd, path, logger_name)


    def initialize_logger(self, parent_logger_name, module_name):
        global logger
        logger_name = parent_logger_name + '.' + module_name
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s' +
                            ' %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename='logfile.log')
        return logger_name


    def create(self, payload, class_type):
        # payload = json.dumps(payload, default=kbms_converter)

        # class_type = TBOXI.get_model(class_name, 'identifier')

        if 'payload' in payload.keys():
            payload['payload'][0]['type'] = class_type
        else:
            payload['type'] = class_type
            payload = {'payload': [payload]}

        print 'In create interface with the following payload:'
        print payload

        response = self.kgs.create(payload, 'http://example.org/abox/dd5e8c90-123c-42fc-aa44-d322111df5b7')

        print 'response of create:'
        print response

        return response

    def get(payload):
        res = self.kgs.get(payload)
        if len(res['payload']) != 0:
            return res
        return None


    # return True if there is an instance in the DB with this uri.
    # must return false if a class has this uri
    def is_instance(uri):
        return False


    def get_instances(self, class_type):
        # class_type = TBOXI.get_model(class_name, 'identifier')
        result = self.kgs.get_instances(class_type)
        if not isinstance(result, Exception):
            result = result['payload']
        return result


    def get_subscribed_users(self):
        return self.kgs.get_subscribed_users()


    def query(self, graph_query):
        # kgservice_result = '{"payload":"[]"}'
        # dict_result = dict(kgservice_result)
        # dummy result foir testing purposes
        pass


    def get_id_by_email(self, email):
        q = 'MATCH (n {mbox:"%s"}) RETURN n.identifier' % email
        res = self.kgs.query(q)['payload']        
        try:
            res = res[0]['n.identifier']
        except Exception as e:
            return None
        return res


    def update(self, payload):
        # payload = json.dumps(payload, default=kbms_converter)

        if 'payload' not in payload.keys():
            payload = {'payload': [payload]}

        print 'In update interface with the following payload:'
        print payload

        response = self.kgs.update(payload)

        print 'response of update:'
        print response

        return response


    def delete(self, payload):
        if 'payload' not in payload.keys():
            payload = {'payload': [payload]}
        #payload = json.dumps(payload, default=kbms_converter)
        response = self.kgs.delete(payload)
        print ('Delete response:', response)
        return response
