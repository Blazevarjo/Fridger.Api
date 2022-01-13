import pytest
from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from fridger.utils.enums import FridgeProductStatus, QuantityType, UserPermission


@pytest.mark.django_db
class TestShoppingListProductPemissions:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user = baker.make("users.User")

        self.url = reverse("shopping-list-product-list")
        self.url_detail = lambda id: reverse("shopping-list-product-detail", args=[id])

    def test_create_product_user_read_no_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        shopping_list = baker.make(
            "shopping_lists.ShoppingListOwnership", user=self.user, permission=UserPermission.READ
        ).shopping_list

        data = {
            "shopping_list": shopping_list.id,
            "taken_by": self.user.id,
            "name": "test name",
            "note": "Test note",
            "price": "123.00",
            "quantity_type": QuantityType.KG,
            "quantity": "2.00",
        }
        response = client.post(self.url, data=data)

        assert response.status_code == 403

    def test_create_product_user_admin_has_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        shopping_list = baker.make(
            "shopping_lists.ShoppingListOwnership",
            user=self.user,
            permission=UserPermission.ADMIN,
        ).shopping_list

        data = {
            "shopping_list": shopping_list.id,
            "taken_by": self.user.id,
            "name": "test name",
            "note": "Test note",
            "price": "123.00",
            "quantity_type": QuantityType.KG,
            "quantity": "2.00",
        }
        response = client.post(self.url, data=data)

        assert response.status_code == 201

    def test_update_product_user_read_no_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        shopping_list = baker.make(
            "shopping_lists.ShoppingListOwnership",
            user=self.user,
            permission=UserPermission.READ,
        ).shopping_list
        product = baker.make("products.ShoppingListProduct", shopping_list=shopping_list)
        data = {
            "name": "new name",
        }
        response = client.patch(self.url_detail(product.id), data=data)

        assert response.status_code == 403

    def test_update_product_user_admin_has_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        shopping_list = baker.make(
            "shopping_lists.ShoppingListOwnership",
            user=self.user,
            permission=UserPermission.ADMIN,
        ).shopping_list
        product = baker.make("products.ShoppingListProduct", shopping_list=shopping_list)
        data = {
            "name": "new name",
        }
        response = client.patch(self.url_detail(product.id), data=data)

        assert response.status_code == 200

    def test_delete_product_user_read_no_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        shopping_list = baker.make(
            "shopping_lists.ShoppingListOwnership",
            user=self.user,
            permission=UserPermission.READ,
        ).shopping_list
        product = baker.make("products.ShoppingListProduct", shopping_list=shopping_list)

        response = client.delete(self.url_detail(product.id))

        assert response.status_code == 403

    def test_delete_product_user_admin_has_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        shopping_list = baker.make(
            "shopping_lists.ShoppingListOwnership",
            user=self.user,
            permission=UserPermission.ADMIN,
        ).shopping_list
        product = baker.make("products.ShoppingListProduct", shopping_list=shopping_list)

        response = client.delete(self.url_detail(product.id))

        assert response.status_code == 204


@pytest.mark.django_db
class TestFridgeProductPemissions:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user = baker.make("users.User")

        self.url = reverse("fridge-product-list")
        self.url_detail = lambda id: reverse("fridge-product-detail", args=[id])

    def test_create_product_user_read_no_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        fridge = baker.make("fridges.FridgeOwnership", user=self.user, permission=UserPermission.READ).fridge

        data = {
            "fridge": fridge.id,
            "name": "test name",
            "quantity_type": QuantityType.KG,
            "product_history": {"status": FridgeProductStatus.UNUSED, "quantity": "2.00"},
        }
        response = client.post(self.url, data=data, format="json")

        assert response.status_code == 403

    def test_create_product_user_admin_has_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        fridge = baker.make("fridges.FridgeOwnership", user=self.user, permission=UserPermission.ADMIN).fridge

        data = {
            "fridge": fridge.id,
            "name": "test name",
            "quantity_type": QuantityType.KG,
            "product_history": {"status": FridgeProductStatus.UNUSED, "quantity": "2.00"},
        }
        response = client.post(self.url, data=data, format="json")

        assert response.status_code == 201

    def test_update_product_user_read_no_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        fridge = baker.make("fridges.FridgeOwnership", user=self.user, permission=UserPermission.READ).fridge
        product = baker.make("products.FridgeProduct", fridge=fridge)

        data = {
            "name": "new name",
        }
        response = client.patch(self.url_detail(product.id), data=data)

        assert response.status_code == 403

    def test_update_product_user_admin_has_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        fridge = baker.make("fridges.FridgeOwnership", user=self.user, permission=UserPermission.ADMIN).fridge
        product = baker.make("products.FridgeProduct", fridge=fridge)

        data = {
            "name": "new name",
        }
        response = client.patch(self.url_detail(product.id), data=data)

        assert response.status_code == 200

    def test_delete_product_user_read_no_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        fridge = baker.make(
            "fridges.FridgeOwnership",
            user=self.user,
            permission=UserPermission.READ,
        ).fridge
        product = baker.make("products.FridgeProduct", fridge=fridge)

        response = client.delete(self.url_detail(product.id))

        assert response.status_code == 403

    def test_delete_product_user_admin_has_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        fridge = baker.make(
            "fridges.FridgeOwnership",
            user=self.user,
            permission=UserPermission.ADMIN,
        ).fridge
        product = baker.make("products.FridgeProduct", fridge=fridge)

        response = client.delete(self.url_detail(product.id))

        assert response.status_code == 204


@pytest.mark.django_db
class TestFridgeProductHistoryPemissions:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user = baker.make("users.User")

        self.url = reverse("fridge-history-product-list")

    def test_create_product_history_user_read_no_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        fridge = baker.make("fridges.FridgeOwnership", user=self.user, permission=UserPermission.READ).fridge
        product = baker.make("products.FridgeProduct", fridge=fridge)
        data = {
            "product": product.id,
            "status": FridgeProductStatus.USED,
            "quantity": 2.00,
        }
        response = client.post(self.url, data=data)

        assert response.status_code == 403

    def test_create_product_history_user_admin_has_access(self):
        client = APIClient()
        client.force_authenticate(self.user)
        fridge = baker.make("fridges.FridgeOwnership", user=self.user, permission=UserPermission.ADMIN).fridge
        product = baker.make("products.FridgeProduct", fridge=fridge)
        data = {
            "product": product.id,
            "status": FridgeProductStatus.USED,
            "quantity": 2.00,
        }
        response = client.post(self.url, data=data)

        assert response.status_code == 201
