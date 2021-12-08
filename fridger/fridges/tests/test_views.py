from decimal import Decimal

import pytest
from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from fridger.fridges.models import FridgeOwnership
from fridger.utils.enums import FridgeProductStatus


@pytest.mark.django_db
class TestFridgesViews:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.test_user = baker.make("users.User")
        self.url = reverse("fridge-list")

    def _get_detail_url(self, id):
        return reverse("fridge-detail", args=[id])

    def test_create_fridge_with_ownership(self):
        client = APIClient()
        client.force_authenticate(self.test_user)

        data = {"name": "Moja lodowka"}
        response = client.post(self.url, data)

        fridge_ownerships = FridgeOwnership.objects.filter(user=self.test_user)
        fridge_ownership = fridge_ownerships.first()

        assert response.status_code == 201
        assert len(fridge_ownerships) == 1
        assert str(fridge_ownership.fridge.id) == response.data["id"]

    def test_update_fridge_do_not_create_ownership(self):
        client = APIClient()
        client.force_authenticate(self.test_user)
        fridge_ownership = baker.make("fridges.FridgeOwnership", user=self.test_user)
        fridge_id = fridge_ownership.fridge.id

        data = {"name": "Moja lodowka2"}
        response = client.put(self._get_detail_url(fridge_id), data)

        fridge_ownership_db = FridgeOwnership.objects.get(user=self.test_user)

        assert response.status_code == 200
        assert fridge_ownership_db == fridge_ownership
        assert FridgeOwnership.objects.count() == 1

    def test_detail_fridge_product_stats(self):
        client = APIClient()
        client.force_authenticate(self.test_user)
        fridge_ownership = baker.make("fridges.FridgeOwnership", user=self.test_user)
        fridge = fridge_ownership.fridge
        baker.make("fridges.FridgeOwnership", fridge=fridge)
        product = baker.make("products.FridgeProduct", fridge=fridge)
        baker.make(
            "products.FridgeProductHistory",
            product=product,
            status=FridgeProductStatus.UNUSED,
            quantity=Decimal(7),
        )
        baker.make(
            "products.FridgeProductHistory",
            product=product,
            status=FridgeProductStatus.USED,
            quantity=Decimal(3),
        )
        baker.make(
            "products.FridgeProductHistory",
            product=product,
            status=FridgeProductStatus.UNUSED,
            quantity=Decimal(5),
        )

        response = client.get(self._get_detail_url(fridge.id))
        json_response = response.json()

        assert json_response["shared_with_count"] == 1
        assert json_response["products_count"] == 1
        assert json_response["products"][0]["quantity_base"] == Decimal(12)
        assert json_response["products"][0]["quantity_left"] == Decimal(9)
