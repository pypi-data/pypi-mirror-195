# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         3/03/23 8:29
# Project:      CFHL Transactional Backend
# Module Name:  oasis_actions
# Description:
# ****************************************************************
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from oasis.models import Operation
from oasis.models import Product
from typing import Any


class OasisActions:
    def __init__(self, data_cache: dict):
        if data_cache is not None and {"data", "action"} <= data_cache.keys():
            self.__data = data_cache.get("data")
            self.__action = data_cache.get("action")
            self.__user = data_cache.get("user", None)
        else:
            raise ValueError(_("Invalid initialization data."))

    def __get_method(self) -> str:
        return "_" + self.__action

    def do_action(self) -> Any:
        if hasattr(self, self.__get_method()):
            # Get the method name
            method = getattr(self, self.__get_method())
            # Invoke the method
            return method()
        else:
            raise ValidationError(_("Action does not have an associated method."))

    def _save_offer(self):
        data = self.__data
        user = self.__user

        saved = Operation.objects.operation_insert(user, data.get("product"), data.get("location"), data.get("amount"),
                                                   data.get("price"), data.get("to_date"))
        print(saved)
