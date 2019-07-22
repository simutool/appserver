
logger = None

class MailBroadcaster:

    def __init__(self, actor, instances, action, subscribed_mails, parent_logger_name):
        self.initialize_logger(parent_logger_name, 'mail_broadcaster')
        self.actor = actor
        self.instances = instances
        self.action = action
        self.subscribed_emails = subscribed_mails

        self.mail = AUTH.settings.mailer
        self.subject = ''
        self.body = ''
        self.set_action_verb()
        self.generate_content()
        self.broadcast_event()

    def set_action_verb(self):
        if self.action == 'c':
            self.action = 'created'
        if self.action == 'u':
            self.action = 'modified'
        if self.action == 'd':
            self.action = 'deleted'

    def generate_content(self):
        name = self.actor['title']
        mbox = self.actor['mbox']
        
        self.subject = '[SIMUTOOL KMS] Notification'

        salut = 'Dear User,\n\n'
        main_statement = '%s (%s) has %s the following items in the Knowledge Base:\n\n' % (name, mbox, self.action)

        reports = self.gen_all_reports()
        pre_separator = '\n\nYou have received this message because you have subscribed to changes.'
        separator = '\n_________________\n\n'
        last = 'This is an automated message, please do not reply to this email.'
        
        self.body = salut +\
                    main_statement +\
                    reports +\
                    pre_separator +\
                    separator +\
                    last

        print self.body


    def broadcast_event(self):       
        logger.info('Broadcasting event to the following e-mails: %s' % emls)
        for eml in emls:
            self.send_email(eml)


    def gen_all_reports(self):
        reports = ""
        for instance in self.instances:
            reports = reports + self.gen_one_report(instance)
        return reports


    def gen_one_report(self, instance):
        typ_title = instance['type_title']
        title = instance['title']
        # type_id = instance['type_identifier']
        report = '  - %s [%s].' % (title, typ_title.capitalize())
        if self.action == 'd' or self.action == 'deleted':
            return report + '\n'
        url = self.make_view_url(instance['identifier'], typ_title)
        report = '%s For more info visit %s.\n' % (report, url)
        return report
            

    def send_email(self, mbox):
        return self.mail.send(
                 to=[mbox], 
                 subject=self.subject,
                 message=self.body)


    def make_view_url(self, identifier, type_title):
        manage_address = "manage/factory"
        url = "%s/%s/%s?class=%s&id=%s" % (SETTINGS.base_url, SETTINGS.app_name, manage_address, type_title, identifier)
        return url


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

# pld =  {
#      "actor":{
#         "mbox":"xyz@abc.d",
#         "title":"Black Schwarz"
#      },
#      "instances":[
#         {
#            "type":"Part",
#            "title":"AGI Part",
#            "identifier": "http://example.org/abox/02d67d9d-a279-4150-8558-1292341b7485"
#         },
#         {
#            "type":"Part",
#            "title":"AGI Part",
#            "identifier": "http://asd6565ffg324234"
#         }
#      ],
#      "action":"c"
#   }

# MailBroadcaster(
#   pld['actor'],
#   pld['instances'],
#   pld['action']).broadcast_event()