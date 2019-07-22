
from mail_broadcaster import MailBroadcaster

AUTH.settings.allow_basic_login = True
@AUTH.requires(is_admin() or is_user())
@request.restful()
def api():
    response.view = 'generic.json'

    def PUT(*args, **vars):
        """
        Sample input:
        {
           "payload":[
              {
                 "actor":{
                    "mbox":"xyz@abc.d",
                    "title":"Black Schwarz"
                 },
                 "instances":[
                   {
                      "type_title":"Part",
                      "type_identifier":"http://example.org/tbox/part",
                      "title":"AGI Part",
                      "identifier": "http://asdfdsffg324234"
                   },
                   {
                      "type_title":"Part",
                      "type_identifier":"http://example.org/tbox/part",
                      "title":"AGI Part",
                      "identifier": "http://asd6565ffg324234"
                   }
                 ],
                 "action":"c"
              }
           ]
        }

        """
        if vars == {} \
           or isinstance(vars, dict) is not True \
           or 'payload' not in vars.keys():
             raise HTTP(400)

        keys = vars['payload'][0].keys()

        if 'actor' not in keys \
           or 'instances' not in keys \
           or 'action' not in keys:
             raise HTTP(400)

        pld = vars.pop('payload', None)[0]
        
        subscribed_mails = ABOXI.get_subscribed_users()

        MailBroadcaster(
            pld['actor'],
            pld['instances'],
            pld['action'],
            subscribed_mails,
            SETTINGS.logger_name)

        return "Users have been notified."


    return locals()
