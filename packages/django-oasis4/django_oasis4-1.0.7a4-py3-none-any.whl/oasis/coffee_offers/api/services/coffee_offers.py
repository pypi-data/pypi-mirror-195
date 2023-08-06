# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         1/03/23 10:10
# Project:      CFHL Transactional Backend
# Module Name:  coffee_offers
# Description:
# ****************************************************************
from coffee_price.models import Price
from coffee_price.api.serializers import PriceListSerializer
from datetime import datetime
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from oasis.coffee_offers import models
from oasis.coffee_offers.api.serializers import CoffeeWareHouseListSerializer
from oasis.lib.choices import CustomerType
from oasis.models import AssociateBalance
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from zibanu.django.rest_framework.exceptions import APIException
from zibanu.django.rest_framework import viewsets
from zibanu.django.utils import CodeGenerator


class CoffeeOffers(viewsets.ViewSet):
    """
    View set for rest service of CoffeOffers module
    """
    __cache_timeout = settings.OASIS_AUTH_CODE_TIMEOUT
    __cache_timeout_seconds = __cache_timeout * 60

    def _get_quota(self, user) -> float:
        """
        Method to get a quota from user profile
        :param user: user object from request
        :return: calculated quota
        """
        # Calculate QUOTA in Kg.
        if user.profile.segment == settings.COFFEE_OFFERS_TRADER_SEGMENT:
            quota = settings.COFFEE_OFFERS_TRADER_QUOTA
        else:
            if user.profile.type == CustomerType.PARTNER:
                quota = AssociateBalance.objects.get_quota(user.profile.document_id)
            else:
                quota = settings.COFFEE_OFFERS_DEFAULT_QUOTA

        if settings.COFFEE_OFFERS_CALCULATE_QUOTA:
            quota = quota - models.Offer.objects.get_balance(user)

        return quota

    def pre_load(self, request) -> Response:
        """
        Rest service for preload all data required for frontend operation.
        :param request: request object from HTTP
        :return: Response object
        """
        try:
            now = timezone.now()
            to_date = now + timedelta(days=settings.COFFEE_OFFERS_DAYS_DELTA)
            user = self._get_user(request)
            # Validate EXCLUDED
            if settings.COFFEE_OFFERS_LOCKED_SEGMENT != 0 and user.profile.segment == settings.COFFEE_OFFERS_LOCKED_SEGMENT:
                raise ValidationError(_("The partner/client is locked for coffee offers."))
            # Load Price List
            price_qs = Price.objects.get_products_price_by_date(date_to_search=now)
            price_serializer = PriceListSerializer(instance=price_qs, many=True, context={"kg": True})
            # Load Warehouse List
            warehouse_qs = models.CoffeeWareHouse.objects.order_by("location_name").all()
            warehouse_serializer = CoffeeWareHouseListSerializer(instance=warehouse_qs, many=True)

            # Calculate QUOTA in Kg.

            data_return = {
                "quota": self._get_quota(user),
                "percent": settings.COFFEE_OFFERS_PRICE_DELTA,
                "to_date": to_date,
                "offers": models.Offer.objects.get_active_offers(user),
                "prices": price_serializer.data,
                "warehouses": warehouse_serializer.data
            }
            status_return = status.HTTP_200_OK
        except ValidationError as exc:
            raise APIException(error=exc.detail[0], http_status=status.HTTP_406_NOT_ACCEPTABLE) from exc
        except Exception as exc:
            raise APIException(error=str(exc), http_status=status.HTTP_500_INTERNAL_SERVER_ERROR) from exc
        else:
            return Response(status=status_return, data=data_return)

    def load_offer(self, request) -> Response:
        try:
            if {"product", "price", "amount", "location", "to_date"} <= request.data.keys():
                user = self._get_user(request)

                # Validate user segment and user quota.
                # if request.data.get("amount") >= self._get_quota(user):
                #    raise ValidationError(_("The amount exceeds the quota available."))
                if user.profile.segment == settings.COFFEE_OFFERS_LOCKED_SEGMENT:
                    raise ValidationError(_("The partner/client is locked for coffee offers."))

                code_generator = CodeGenerator("save_offer")
                data_cache = code_generator.generate_dict()
                cache_key = data_cache.pop("uuid").hex
                data_cache["user"] = user
                data_cache["offer"] = {
                    "product": request.data.get("product"),
                    "price": request.data.get("price"),
                    "amount": request.data.get("amount"),
                    "location": request.data.get("location"),
                    "to_date": request.data.get("to_date")
                }
                data_return = {
                    "token": cache_key
                }
                status_return = status.HTTP_200_OK
            else:
                raise ValidationError(_("Data required at request not found."))
        except ValidationError as exc:
            raise APIException(error=exc.detail[0], http_status=status.HTTP_406_NOT_ACCEPTABLE) from exc
        except Exception as exc:
            raise APIException(error=str(exc), http_status=status.HTTP_500_INTERNAL_SERVER_ERROR) from exc
        else:
            return Response(status=status_return, data=data_return)
