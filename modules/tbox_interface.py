# This file contains all the functions that interface with the TBox
# It is the only middle-man between TBox and front-end.
import logging
from kgservice import TBox

class TBoxInterface(object):

    def __init__(self, graph_url, usr, pswd, path, parent_logger_name):
        logger_name = self.initialize_logger(parent_logger_name, 'tbox_interface')
        self.kgs = TBox.TBoxService(graph_url, usr, pswd, path, logger_name)


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


    # returns all decendants (direct and indirect are included),
    # if true only direct children are included.
    def get_subtypes(self, class_uri, direct_children, include_self):
        """
        Retrurn format example:
        {'http://example.org/tbox/kbmsthing': 'kbmsthing',
         'http://example.org/tbox/user': 'User',
         'http://example.org/tbox/productdesign': 'Product Design',
         'http://example.org/tbox/data':'Data'}
        """
        payload_list = self.kgs.get_subtypes(class_uri,
                                         direct_children,
                                         include_self)['payload']
        return_dict = {}
        for payload in payload_list:
            # if include_self is not True and pl['identifier']==class_uri:
            #   continue
            return_dict[payload['identifier']] = payload['title']
        return return_dict


    def get_peoperties_relations(self, class_id):
        """ Takes a class uri a retuns a list of the names of all the
            properties and relations of theat class in the TBox."""
        return self.kgs.get_attributes(class_id)


    def get_type(self, att_name):
      """
        A function that takes a string name of a property or relationship and returns its type.
        get_att_type(att_title) -> string

        There are 4 cases:

        if att_title equals the value of self.identifier return "identifier"

        if att_title equals the value of self.instance_of return "type"

        if att_title a relation that points to class with title class_xyz, return "ref class_xyz"

        if att_title is the title of a property, return the value of the field "xsd_type" of that property (ex. xsd:string )
      """
      return self.kgs.get_att_type(att_name)

    # if prop_name == None, returns a dict (, or {"payload":[]} if faliure)
    # else returns a scalar (or None if faliure)
    def get_model(self, class_title, prop_name=None):

        class_title = class_title.lower()

        try:
          class_payload = self.kgs._get_tbox_node_by_title(class_title)["payload"][0]
        except IndexError as e:
          logger.warning(self._exception_class_title(class_title))
          if prop_name==None:
            return {"payload":[]}
          else:
            return None

        if prop_name is None:
            return class_payload
        else:
            return class_payload.pop(prop_name, None)


    def _exception_class_title(self, title):
        msg = ("Class (%s) cannot be found in model. Check spelling or define." % title)
        return KeyError(msg)
