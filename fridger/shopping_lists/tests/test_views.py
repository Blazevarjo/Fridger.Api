import pytest
from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from fridger.shopping_lists.models import ShoppingListOwnership
from fridger.utils.enums import UserPermission


@pytest.mark.django_db
class TestShoppingListsViews:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.test_user = baker.make("users.User")
        self.url = reverse("shopping-list-list")

    def _get_detail_url(self, id):
        return reverse("shopping-list-detail", args=[id])

    def test_create_shopping_list_with_ownership(self):
        client = APIClient()
        client.force_authenticate(self.test_user)

        data = {"name": "Moja lista zakupowa"}
        response = client.post(self.url, data)

        shopping_list_ownerships = ShoppingListOwnership.objects.filter(user=self.test_user)
        shopping_list_ownership = shopping_list_ownerships.first()

        assert response.status_code == 201
        assert len(shopping_list_ownerships) == 1
        assert str(shopping_list_ownership.shopping_list.id) == response.data["id"]
        assert shopping_list_ownership.permission == UserPermission.CREATOR

    def test_update_shopping_list_do_not_create_ownership(self):
        client = APIClient()
        client.force_authenticate(self.test_user)
        shopping_list_ownership = baker.make("shopping_lists.ShoppingListOwnership", user=self.test_user)
        shopping_list_id = shopping_list_ownership.shopping_list.id

        data = {"name": "Moja lista zakupowa"}
        response = client.patch(self._get_detail_url(shopping_list_id), data)

        shopping_list_ownership_db = ShoppingListOwnership.objects.get(user=self.test_user)

        assert response.status_code == 200
        assert shopping_list_ownership_db == shopping_list_ownership
        assert ShoppingListOwnership.objects.count() == 1

    def test_list_fridge_ownerships(self):
        client = APIClient()
        client.force_authenticate(self.test_user)
        shopping_list = baker.make("shopping_lists.ShoppingList")
        baker.make("shopping_lists.ShoppingListOwnership", shopping_list=shopping_list, user=self.test_user)
        baker.make("shopping_lists.ShoppingListOwnership", shopping_list=shopping_list)
        baker.make("shopping_lists.ShoppingListOwnership")
        url = reverse("shopping-list-ownerships", args=[shopping_list.id])

        response = client.get(url)
        json_response = response.json()

        assert response.status_code == 200
        assert len(json_response) == 2


@pytest.mark.django_db
class TestShoppingListsOwnershipsViews:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.test_user = baker.make("users.User")
        self.client = APIClient()
        self.client.force_authenticate(self.test_user)

    def _get_detail_url(self, id):
        return reverse("shopping-list-ownership-detail", args=[id])

    def test_create_ownership(self):
        url = reverse("shopping-list-ownership-list")
        shopping_list = baker.make("shopping_lists.ShoppingList")

        data = {
            "user": str(self.test_user.id),
            "shopping_list": str(shopping_list.id),
            "permission": UserPermission.READ,
        }
        response = self.client.post(url, data=data)
        response_data = response.json()
        response_id = response_data.pop("id")

        assert response.status_code == 201
        assert response_id
        assert response_data == data
        assert ShoppingListOwnership.objects.count() == 1

    def test_update_ownership(self):
        shopping_list_ownership = baker.make("shopping_lists.ShoppingListOwnership", user=self.test_user)

        data = {
            "permission": UserPermission.READ,
        }

        response = self.client.patch(self._get_detail_url(shopping_list_ownership.id), data=data)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data == data
        assert ShoppingListOwnership.objects.count() == 1

    def test_delete_ownership(self):
        shopping_list_ownership = baker.make("shopping_lists.ShoppingListOwnership", user=self.test_user)

        response = self.client.delete(self._get_detail_url(shopping_list_ownership.id))

        assert response.status_code == 204
        assert not ShoppingListOwnership.objects.filter(id=shopping_list_ownership.id).exists()
