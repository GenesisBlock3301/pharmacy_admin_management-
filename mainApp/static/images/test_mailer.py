from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from core.mailer import Mailer


class MailerTestCase(APITestCase):
    def test_send_mail(self):
        """
            Ensures we can send email from our mailer
        """
        url = reverse('email-sent')
        data = {
            'subject': 'Test subject',
            'body': 'Test body',
            'to': 'test_user@example.com',
            'from_email': 'eden@example.com'
            }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Mailer.send())
