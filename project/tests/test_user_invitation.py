
from random import randint

from django.contrib.auth.models import User
from invitations.models import Invitation


class TestUserInvitationBackEnd:

    def test_send_invitation(self, db, rf, mailoutbox):
        invite = Invitation.create('{0}@example.com'.format(
            randint(11111111, 99999999)))
        mails_before = len(mailoutbox)
        invite.send_invitation(rf.get(''))
        assert len(mailoutbox) == mails_before+1
        assert invite.key in mailoutbox[-1].body
        invite.delete()


class TestInvitationFrontEnd:

    def test_invitation_user(self, logined_admin_browser,
                             live_server, mailoutbox):
        mails_before = len(mailoutbox)
        logined_admin_browser.find_by_css('.clickable-row').first.click()
        email = logined_admin_browser.find_by_name('email')[0]
        test_email = '{0}@example.com'.format(randint(11111111, 99999999))
        email.value = test_email
        button = logined_admin_browser.find_by_name('submit')[0]
        button.click()
        assert logined_admin_browser.is_text_present(
            'Successfully invited {0}'.format(test_email))
        button.click()
        assert logined_admin_browser.is_text_present(
            '{0} already invited'.format(test_email))
        assert len(mailoutbox) == mails_before + 1
        invite = Invitation.objects.get(email=test_email)
        assert invite
        logined_admin_browser.visit(
            live_server + '/invitations/accept-invite/' + invite.key)
        usr = logined_admin_browser.find_by_id('id_username')[0]
        usr.value = 'test'
        logined_admin_browser.find_by_id('id_password1')[0].value = 'Start123'
        logined_admin_browser.find_by_id('id_password2')[0].value = 'Start123'
        logined_admin_browser.find_by_value('Login')[0].click()
        assert User.objects.get(username='test')

    def test_block_registration(self, live_server, browser):
        browser.visit(live_server + '/accept-invite/register/')
        assert browser.is_text_present('Page Not Found')
