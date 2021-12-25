import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from exponent_server_sdk import PushClient, PushMessage

from fridger.products.models import FridgeProduct

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        products = FridgeProduct.objects.exclude(expiration_date__isnull=True).exclude(is_available=False)
        for product in products:
            fridge = product.fridge
            mobile_tokens = list(
                fridge.fridge_ownership.exclude(user__mobile_token="").values_list("user__mobile_token", flat=True)
            )
            days_difference = (product.expiration_date - datetime.date.today()).days

            if days_difference < 3 and len(mobile_tokens) > 0:
                self._send_bulk_products_push_messages(mobile_tokens, fridge, product, days_difference)

    def _send_bulk_products_push_messages(self, mobile_tokens, fridge, product, days_difference):
        if days_difference > 0:
            title = _("%(product_name)s is going to expire") % {"product_name": product.name}
            body = ngettext(
                "%(product_name)s from fridge %(fridge_name)s is going to expire tomorrow.",
                "%(product_name)s from fridge %(fridge_name)s is going to expire in the next %(days_difference)s days.",
                days_difference,
            ) % {
                "fridge_name": fridge.name,
                "product_name": product.name,
                "days_difference": days_difference,
            }
        elif days_difference == 0:
            title = _("%(product_name)s is going to expire") % {"product_name": product.name}
            body = _("%(product_name)s from fridge %(fridge_name)s today ends its expiration date") % {
                "fridge_name": fridge.name,
                "product_name": product.name,
                "days_difference": days_difference,
            }
        else:
            title = _("%(product_name)s has expired") % {"product_name": product.name}
            body = ngettext(
                "%(product_name)s from fridge %(fridge_name)s has expired yesterday.",
                "%(product_name)s from fridge %(fridge_name)s has expired %(days_difference)s days ago.",
                abs(days_difference),
            ) % {
                "fridge_name": fridge.name,
                "product_name": product.name,
                "days_difference": abs(days_difference),
            }

        PushClient().publish(
            PushMessage(
                to=mobile_tokens,
                title=title,
                body=body,
                data={"fridge_id": fridge.id, "product_id": product.id},
            )
        )
