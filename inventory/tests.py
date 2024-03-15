from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Item
from django.urls import reverse

# Create your tests here.

class ItemModelTests(TestCase):
    def test_was_added_recently_with_future_item(self):
        time=timezone.now()+datetime.timedelta(days=30)
        future_item = Item(add_date=time)
        self.assertIs(future_item.was_added_recently(),False)

    def test_was_added_rencently_with_old_item(self):
        time = timezone.now() - datetime.timedelta(days=1,seconds=1)
        old_item = Item(add_date=time)
        self.assertIs(old_item.was_added_recently(), False)

    def test_was_added_rencently_with_recent_item(self):
        time = timezone.now() - datetime.timedelta(hours=23,minutes=59,seconds=29)
        recent_item = Item(add_date=time)
        self.assertIs(recent_item.was_added_recently(), True)

class ItemDetailViewTests(TestCase):
    def test_future_item(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_item = create_item(title="Future item.", days=5)
        url = reverse("inventory:detail", args=(future_item.id))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
