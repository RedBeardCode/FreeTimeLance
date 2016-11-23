
import pytest
from random import randint

from django.contrib.auth.models import User
from invitations.models import Invitation


@pytest.fixture
def invitation():
    invite = Invitation.create('{0}@example.com'.format(randint(11111111,
                                                                99999999)))
    yield invite
    invite.delete()


@pytest.fixture
def logined_admin_browser(browser, live_server, db, admin_user):
    browser.visit(live_server.url)
    browser.find_by_name('username')[0].value = 'admin'
    browser.find_by_name('password')[0].value = 'password'
    browser.find_by_value('Login')[0].click()
    yield browser
    browser.driver.close()


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

    @pytest.mark.django_db(transaction=True)
    def test_invitation_user(self, logined_admin_browser,
                             live_server, mailoutbox):
        mails_before = len(mailoutbox)
        logined_admin_browser.visit(live_server + '/1/')
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
