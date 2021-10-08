from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):
    def test_wait_for_db_ready(self):
        """Test waiting for database when it is available"""
        # If we get an OperationalError, then the DB isn't ready
        # If no OperationalError, DB is ready and we can continue
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    # `patch` as a decorator - speed up the tests - don't wait a full second
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for database"""
        # Management command will check for the OperationalError and then wait
        # a second before trying again
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # The first 5 times we call `gi` it will raise the OperationalError
            # and on the sixth time it will return
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
