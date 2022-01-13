from decimal import Decimal

import pytest
from model_bakery import baker

from fridger.utils.enums import FridgeProductStatus


@pytest.mark.django_db
class TestFridgeProductModels:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.product = baker.make("products.FridgeProduct")

    def test_fridge_product_has_correct_quantity_base(self):
        baker.make(
            "products.FridgeProductHistory",
            product=self.product,
            status=FridgeProductStatus.UNUSED,
            quantity=Decimal(5),
        )
        baker.make(
            "products.FridgeProductHistory",
            product=self.product,
            status=FridgeProductStatus.USED,
            quantity=Decimal(7),
        )
        baker.make(
            "products.FridgeProductHistory",
            product=self.product,
            status=FridgeProductStatus.UNUSED,
            quantity=Decimal(10),
        )

        assert self.product.quantity_base == 15

    def test_fridge_product_has_correct_quantity_left(self):
        baker.make(
            "products.FridgeProductHistory",
            product=self.product,
            status=FridgeProductStatus.UNUSED,
            quantity=Decimal(5),
        )
        baker.make(
            "products.FridgeProductHistory",
            product=self.product,
            status=FridgeProductStatus.USED,
            quantity=Decimal(7),
        )
        baker.make(
            "products.FridgeProductHistory",
            product=self.product,
            status=FridgeProductStatus.WASTED,
            quantity=Decimal(4),
        )
        baker.make(
            "products.FridgeProductHistory",
            product=self.product,
            status=FridgeProductStatus.UNUSED,
            quantity=Decimal(10),
        )

        assert self.product.quantity_left == 4

    def test_fridge_product_has_correct_quantity_used(self):
        baker.make(
            "products.FridgeProductHistory",
            product=self.product,
            status=FridgeProductStatus.UNUSED,
            quantity=Decimal(5),
        )
        baker.make(
            "products.FridgeProductHistory",
            product=self.product,
            status=FridgeProductStatus.USED,
            quantity=Decimal(7),
        )
        baker.make(
            "products.FridgeProductHistory",
            product=self.product,
            status=FridgeProductStatus.WASTED,
            quantity=Decimal(4),
        )
        baker.make(
            "products.FridgeProductHistory",
            product=self.product,
            status=FridgeProductStatus.UNUSED,
            quantity=Decimal(10),
        )

        assert self.product.quantity_used == 7

    def test_fridge_product_is_available(self):
        baker.make(
            "products.FridgeProductHistory",
            product=self.product,
            status=FridgeProductStatus.UNUSED,
            quantity=Decimal(5),
        )
        baker.make(
            "products.FridgeProductHistory",
            product=self.product,
            status=FridgeProductStatus.USED,
            quantity=Decimal(7),
        )
        baker.make(
            "products.FridgeProductHistory",
            product=self.product,
            status=FridgeProductStatus.WASTED,
            quantity=Decimal(4),
        )
        baker.make(
            "products.FridgeProductHistory",
            product=self.product,
            status=FridgeProductStatus.UNUSED,
            quantity=Decimal(10),
        )

        assert self.product.is_available

    def test_fridge_product_is_not_available(self):
        baker.make(
            "products.FridgeProductHistory",
            product=self.product,
            status=FridgeProductStatus.UNUSED,
            quantity=Decimal(5),
        )
        baker.make(
            "products.FridgeProductHistory",
            product=self.product,
            status=FridgeProductStatus.USED,
            quantity=Decimal(9),
        )
        baker.make(
            "products.FridgeProductHistory",
            product=self.product,
            status=FridgeProductStatus.WASTED,
            quantity=Decimal(6),
        )
        baker.make(
            "products.FridgeProductHistory",
            product=self.product,
            status=FridgeProductStatus.UNUSED,
            quantity=Decimal(10),
        )

        assert not self.product.is_available
