from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from cards.models import Card
from categories.models import Category


class CardTestCase(TestCase):
    test_cards = list()

    def setUp(self):
        """Set up test scenario
        """
        test_category = Category.objects.create(name='Category 1', description='Description 1')

        for i in range(1, 11):
            test_card = Card.objects.create(
                question='Question {}'.format(i),
                answer='Answer {}'.format(i),
                hint='Hint {}'.format(i),
                category=test_category,
            )
            self.test_cards.append(test_card)

    def test_card_list(self):
        """Test if the card list is displayed sucessfully
        """
        url = reverse('card-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_card_detail(self):
        """Test if the card list is displayed sucessfully
        """
        test_card = self.test_cards[0]

        url = reverse('card-detail', args=(test_card.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_card_in_area_1(self):
        """Test if the new card is in area 1
        """
        test_card = self.test_cards[0]
        self.assertEqual(test_card.area, 1)

    def test_card_move_forward(self):
        """Test if the card can be moved forward in the next area
        """
        test_card = self.test_cards[1]
        test_card.area = 1
        test_card.save()

        for i in range(2, 7):
            test_card.move_forward()
            refreshed_test_card = Card.objects.get(pk=test_card.pk)
            self.assertEqual(refreshed_test_card.area, i)

    def test_card_move_too_much_forward(self):
        """Test if the card cannot be moved to area 7 which doesn't exist
        """
        test_card = self.test_cards[1]
        test_card.area = 1
        test_card.save()

        for i in range(2, 8):
            test_card.move_forward()

        refreshed_test_card = Card.objects.get(pk=test_card.pk)
        self.assertEqual(refreshed_test_card.area, 6)

    def test_card_move_backward(self):
        """Test if the card can be moved backward in the next area
        """
        test_card = self.test_cards[2]
        test_card.area = 6
        test_card.save()

        for i in reversed(range(1, 6)):
            test_card.move_backward()
            refreshed_test_card = Card.objects.get(pk=test_card.pk)
            self.assertEqual(refreshed_test_card.area, i)

    def test_card_move_too_much_backward(self):
        """Test if the card cannot be moved to area 0 which doesn't exist
        """
        test_card = self.test_cards[2]
        test_card.area = 6
        test_card.save()

        for _ in reversed(range(0, 6)):
            test_card.move_backward()

        refreshed_test_card = Card.objects.get(pk=test_card.pk)
        self.assertEqual(refreshed_test_card.area, 1)

    def test_card_reset(self):
        """Test if the "Reset" button works
        """
        test_card = self.test_cards[1]
        test_card.area = 3
        test_card.save()

        url = reverse('card-reset', args=(test_card.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        refreshed_test_card = Card.objects.get(pk=test_card.pk)
        self.assertEqual(refreshed_test_card.area, 1)

    def test_card_set_area_4(self):
        """Test if the card can be set to area 4
        """
        test_card = self.test_cards[1]
        test_card.area = 4
        test_card.save()

        url = reverse('card-set-area', args=(test_card.pk, 4))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        refreshed_test_card = Card.objects.get(pk=test_card.pk)
        self.assertEqual(refreshed_test_card.area, 4)

    def test_card_set_area_1337(self):
        """Test if the card cannot be set to area 1337
        """
        test_card = self.test_cards[1]
        test_card.area = 4
        test_card.save()

        # Set the URL manually instead of reverse(), because the URL regex wouldn't allow this test
        url = '/card/{}/set-area/{}/'.format(test_card.pk, 1337)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        refreshed_test_card = Card.objects.get(pk=test_card.pk)
        self.assertEqual(refreshed_test_card.area, 4)

    def test_card_delete(self):
        """Test if the "Delete" button works
        """
        test_card = self.test_cards[3]

        url = reverse('card-delete', args=(test_card.pk,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        with self.assertRaises(ObjectDoesNotExist):
            Card.objects.get(pk=test_card.pk)
