import pytest
from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from fridger.utils.enums import UserPermission


@pytest.mark.django_db
class TestFridgePemissions:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user_read_in_fridge = baker.make("users.User")
        self.user_admin_in_fridge = baker.make("users.User")
        self.user_not_in_fridge = baker.make("users.User")

        fridge_to_delete = baker.make(
            "fridges.FridgeOwnership", user=self.user_read_in_fridge, permission=UserPermission.READ
        ).fridge
        baker.make(
            "fridges.FridgeOwnership",
            fridge=fridge_to_delete,
            user=self.user_admin_in_fridge,
            permission=UserPermission.ADMIN,
        )
        fridge_to_update = baker.make(
            "fridges.FridgeOwnership", user=self.user_read_in_fridge, permission=UserPermission.READ
        ).fridge
        baker.make(
            "fridges.FridgeOwnership",
            fridge=fridge_to_update,
            user=self.user_admin_in_fridge,
            permission=UserPermission.ADMIN,
        )

        self.url_delete = reverse("fridge-detail", args=[fridge_to_delete.id])
        self.url_update = reverse("fridge-detail", args=[fridge_to_update.id])

    def test_delete_user_not_in_fridge_has_no_access(self):
        client = APIClient()
        client.force_authenticate(self.user_not_in_fridge)

        response = client.delete(self.url_delete)

        assert response.status_code == 404

    def test_delete_user_read_in_fridge_has_no_access(self):
        client = APIClient()
        client.force_authenticate(self.user_read_in_fridge)

        response = client.delete(self.url_delete)

        assert response.status_code == 403

    def test_delete_user_admin_in_fridge_has_access(self):
        client = APIClient()
        client.force_authenticate(self.user_admin_in_fridge)

        response = client.delete(self.url_delete)

        assert response.status_code == 204

    def test_update_user_not_in_fridge_has_no_access(self):
        client = APIClient()
        client.force_authenticate(self.user_not_in_fridge)

        response = client.put(self.url_delete, {"name": "test"})

        assert response.status_code == 404

    def test_update_user_read_in_fridge_has_no_access(self):
        client = APIClient()
        client.force_authenticate(self.user_read_in_fridge)

        response = client.put(self.url_delete, {"name": "test"})

        assert response.status_code == 403

    def test_update_user_admin_in_fridge_has_access(self):
        client = APIClient()
        client.force_authenticate(self.user_admin_in_fridge)

        response = client.put(self.url_delete, {"name": "test"})

        assert response.status_code == 200


@pytest.mark.django_db
class TestFridgeOwnershipPermissions:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user = baker.make("users.User")
        self.url = reverse("fridge-ownership-list")

    def _get_detail_url(self, id):
        return reverse("fridge-ownership-detail", args=[id])

    def test_create_ownership_user_read_no_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        fridge = baker.make("fridges.FridgeOwnership", user=self.user, permission=UserPermission.READ).fridge
        new_user = baker.make("users.User")
        data = {"fridge": fridge.id, "permission": UserPermission.READ, "user": new_user.id}
        response = client.post(self.url, data=data)

        assert response.status_code == 403

    def test_create_ownership_user_admin_has_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        fridge = baker.make("fridges.FridgeOwnership", user=self.user, permission=UserPermission.ADMIN).fridge

        new_user = baker.make("users.User")
        data = {"fridge": fridge.id, "permission": UserPermission.READ, "user": new_user.id}
        response = client.post(self.url, data=data)

        assert response.status_code == 201

    def test_update_ownership_user_read_no_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        fridge_ownership = baker.make("fridges.FridgeOwnership", user=self.user, permission=UserPermission.READ)

        data = {
            "permission": UserPermission.READ,
        }
        response = client.patch(self._get_detail_url(fridge_ownership.id), data=data)

        assert response.status_code == 403

    def test_update_ownership_user_admin_has_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        fridge_ownership = baker.make("fridges.FridgeOwnership", user=self.user, permission=UserPermission.ADMIN)

        data = {
            "permission": UserPermission.READ,
        }
        response = client.patch(self._get_detail_url(fridge_ownership.id), data=data)

        assert response.status_code == 200

    def test_delete_ownership_user_read_has_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        fridge_ownership = baker.make("fridges.FridgeOwnership", user=self.user, permission=UserPermission.READ)

        response = client.delete(self._get_detail_url(fridge_ownership.id))

        assert response.status_code == 204

    def test_delete_ownership_user_admin_has_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        fridge_ownership = baker.make("fridges.FridgeOwnership", user=self.user, permission=UserPermission.ADMIN)

        response = client.delete(self._get_detail_url(fridge_ownership.id))

        assert response.status_code == 204

    def test_delete_ownership_random_user_has__no_access(self):
        random_user = baker.make("users.User")
        client = APIClient()
        client.force_authenticate(random_user)
        fridge_ownership = baker.make("fridges.FridgeOwnership", user=self.user, permission=UserPermission.ADMIN)

        response = client.delete(self._get_detail_url(fridge_ownership.id))

        assert response.status_code == 404
