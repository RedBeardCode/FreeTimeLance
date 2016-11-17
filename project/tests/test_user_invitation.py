from random import randint
from django.core import mail
from invitations.models import Invitation


class TestUserInvitationBackEnd:
     def test_send_invitation(self, db, rf):
         invite = Invitation.create('{0}@example.com'.format(randint(11111111, 99999999)))
         mails_before = len(mail.outbox)
         invite.send_invitation(rf.get(''))
         assert len(mail.outbox) == mails_before+1
         assert invite.key in mail.outbox[-1].body
         invite.delete()
