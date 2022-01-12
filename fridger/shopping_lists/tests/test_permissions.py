import pytest
from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from fridger.utils.enums import UserPermission


@pytest.mark.django_db
class TestShoppingListPemissions:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user_read_in_shopping_list = baker.make("users.User")
        self.user_admin_in_shopping_list = baker.make("users.User")
        self.user_not_in_shopping_list = baker.make("users.User")

        shopping_list_to_delete = baker.make(
            "shopping_lists.ShoppingListOwnership", user=self.user_read_in_shopping_list, permission=UserPermission.READ
        ).shopping_list
        baker.make(
            "shopping_lists.ShoppingListOwnership",
            shopping_list=shopping_list_to_delete,
            user=self.user_admin_in_shopping_list,
            permission=UserPermission.ADMIN,
        )
        shopping_list_to_update = baker.make(
            "shopping_lists.ShoppingListOwnership", user=self.user_read_in_shopping_list, permission=UserPermission.READ
        ).shopping_list
        baker.make(
            "shopping_lists.ShoppingListOwnership",
            shopping_list=shopping_list_to_update,
            user=self.user_admin_in_shopping_list,
            permission=UserPermission.ADMIN,
        )

        self.url_delete = reverse("shopping-list-detail", args=[shopping_list_to_delete.id])
        self.url_update = reverse("shopping-list-detail", args=[shopping_list_to_update.id])

    def test_delete_user_not_in_shopping_list_has_no_access(self):
        client = APIClient()
        client.force_authenticate(self.user_not_in_shopping_list)

        response = client.delete(self.url_delete)

        assert response.status_code == 404

    def test_delete_user_read_in_shopping_list_has_no_access(self):
        client = APIClient()
        client.force_authenticate(self.user_read_in_shopping_list)

        response = client.delete(self.url_delete)

        assert response.status_code == 403

    def test_delete_user_admin_in_shopping_list_has_access(self):
        client = APIClient()
        client.force_authenticate(self.user_admin_in_shopping_list)

        response = client.delete(self.url_delete)

        assert response.status_code == 204

    def test_update_user_not_in_shopping_list_has_no_access(self):
        client = APIClient()
        client.force_authenticate(self.user_not_in_shopping_list)

        response = client.patch(self.url_delete, {"name": "test"})

        assert response.status_code == 404

    def test_update_user_read_in_shopping_list_has_no_access(self):
        client = APIClient()
        client.force_authenticate(self.user_read_in_shopping_list)

        response = client.patch(self.url_delete, {"name": "test"})

        assert response.status_code == 403

    def test_update_user_admin_in_shopping_list_has_access(self):
        client = APIClient()
        client.force_authenticate(self.user_admin_in_shopping_list)

        response = client.patch(self.url_delete, {"name": "test"})

        assert response.status_code == 200


@pytest.mark.django_db
class TestShoppingListOwnershipPermissions:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user = baker.make("users.User")
        self.url = reverse("shopping-list-ownership-list")

    def _get_detail_url(self, id):
        return reverse("shopping-list-ownership-detail", args=[id])

    def test_create_ownership_user_read_no_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        shopping_list = baker.make(
            "shopping_lists.ShoppingListOwnership", user=self.user, permission=UserPermission.READ
        ).shopping_list
        new_user = baker.make("users.User")
        data = {"shopping_list": shopping_list.id, "permission": UserPermission.READ, "user": new_user.id}
        response = client.post(self.url, data=data)

        assert response.status_code == 403

    def test_create_ownership_user_admin_has_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        shopping_list = baker.make(
            "shopping_lists.ShoppingListOwnership", user=self.user, permission=UserPermission.ADMIN
        ).shopping_list

        new_user = baker.make("users.User")
        data = {"shopping_list": shopping_list.id, "permission": UserPermission.READ, "user": new_user.id}
        response = client.post(self.url, data=data)

        assert response.status_code == 201

    def test_update_ownership_user_read_no_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        shopping_list_ownership = baker.make(
            "shopping_lists.ShoppingListOwnership", user=self.user, permission=UserPermission.READ
        )

        data = {
            "permission": UserPermission.READ,
        }
        response = client.patch(self._get_detail_url(shopping_list_ownership.id), data=data)

        assert response.status_code == 403

    def test_update_ownership_user_admin_has_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        shopping_list_ownership = baker.make(
            "shopping_lists.ShoppingListOwnership", user=self.user, permission=UserPermission.ADMIN
        )

        data = {
            "permission": UserPermission.READ,
        }
        response = client.patch(self._get_detail_url(shopping_list_ownership.id), data=data)

        assert response.status_code == 200

    def test_delete_ownership_user_read_has_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        shopping_list_ownership = baker.make(
            "shopping_lists.ShoppingListOwnership", user=self.user, permission=UserPermission.READ
        )

        response = client.delete(self._get_detail_url(shopping_list_ownership.id))

        assert response.status_code == 204

    def test_delete_ownership_user_admin_has_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        shopping_list_ownership = baker.make(
            "shopping_lists.ShoppingListOwnership", user=self.user, permission=UserPermission.ADMIN
        )

        response = client.delete(self._get_detail_url(shopping_list_ownership.id))

        assert response.status_code == 204

    def test_delete_ownership_random_user_has__no_access(self):
        random_user = baker.make("users.User")
        client = APIClient()
        client.force_authenticate(random_user)
        shopping_list_ownership = baker.make(
            "shopping_lists.ShoppingListOwnership", user=self.user, permission=UserPermission.ADMIN
        )

        response = client.delete(self._get_detail_url(shopping_list_ownership.id))

        assert response.status_code == 404
