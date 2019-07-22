# -*- coding: utf-8 -*-
import datetime

# required - do no delete
def user():
    return dict(form=AUTH())

@AUTH.requires(is_admin() or is_user())
def download():
    return response.download(request, DB)

def call():
    return SERVICE()
# end requires

@AUTH.requires(is_admin() or is_user())
def index():
    return dict()


@AUTH.requires_login()
def feedback():
    form = SQLFORM.factory(
        Field('Reason', requires=IS_IN_SET(['Bug', 'Feature Suggestion', 'Other']),
              default='Bug'),
        Field('Text', type='text', notnull=True))
    if form.process().accepted:
        if form.vars.Text == "":
            form.errors.Text = 'Please write something!'
        else:
            dev_email = SETTINGS.maintainer_eml
            reason = form.vars.Reason
            text = form.vars.Text
            user_email = AUTH.user.email
            time = str(datetime.datetime.now())
            mailto = 'mailto:%s?subject=%s&body=%s.\n\n______\n\nSent By: %s\nTime: %s' % (dev_email, reason, text, user_email, time)
            redirect(mailto)
    return dict(form=form)
