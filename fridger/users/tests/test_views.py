import pytest
from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestFriendsQueryParams:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user = baker.make("users.User")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_friends_not_in_fridge_query(self):
        fridge = baker.make("fridges.Fridge")
        url = reverse("friend-list") + f"?not_in_fridge={fridge.id}"
        baker.make("fridges.FridgeOwnership", fridge=fridge, user=self.user)

        friend_in_1 = baker.make("fridges.FridgeOwnership", fridge=fridge).user
        friend_out_1 = baker.make("fridges.FridgeOwnership").user
        friend_in_2 = baker.make("fridges.FridgeOwnership", fridge=fridge).user
        friend_out_2 = baker.make("fridges.FridgeOwnership").user

        for i, friend in enumerate([friend_in_1, friend_in_2, friend_out_1, friend_out_2]):
            if i % 2 == 0:
                baker.make("users.Friend", friend_1=friend, friend_2=self.user)
            else:
                baker.make("users.Friend", friend_1=self.user, friend_2=friend)

        response = self.client.get(url)
        response_data = response.json()

        assert response.status_code == 200
        assert len(response_data) == 2
        assert any(item["friend"]["id"] == str(friend_out_1.id) for item in response_data)
        assert any(item["friend"]["id"] == str(friend_out_2.id) for item in response_data)
        assert not any(item["friend"]["id"] == str(friend_in_1.id) for item in response_data)
        assert not any(item["friend"]["id"] == str(friend_in_2.id) for item in response_data)

    def test_get_friends_not_in_shopping_list_query(self):
        shopping_list = baker.make("shopping_lists.ShoppingList")
        url = reverse("friend-list") + f"?not_in_shopping_list={shopping_list.id}"
        baker.make("shopping_lists.ShoppingListOwnership", shopping_list=shopping_list, user=self.user)

        friend_in_1 = baker.make("shopping_lists.ShoppingListOwnership", shopping_list=shopping_list).user
        friend_out_1 = baker.make("shopping_lists.ShoppingListOwnership").user
        friend_in_2 = baker.make("shopping_lists.ShoppingListOwnership", shopping_list=shopping_list).user
        friend_out_2 = baker.make("shopping_lists.ShoppingListOwnership").user

        for i, friend in enumerate([friend_in_1, friend_in_2, friend_out_1, friend_out_2]):
            if i % 2 == 0:
                baker.make("users.Friend", friend_1=friend, friend_2=self.user)
            else:
                baker.make("users.Friend", friend_1=self.user, friend_2=friend)

        response = self.client.get(url)
        response_data = response.json()

        assert response.status_code == 200
        assert len(response_data) == 2
        assert any(item["friend"]["id"] == str(friend_out_1.id) for item in response_data)
        assert any(item["friend"]["id"] == str(friend_out_2.id) for item in response_data)
        assert not any(item["friend"]["id"] == str(friend_in_1.id) for item in response_data)
        assert not any(item["friend"]["id"] == str(friend_in_2.id) for item in response_data)
