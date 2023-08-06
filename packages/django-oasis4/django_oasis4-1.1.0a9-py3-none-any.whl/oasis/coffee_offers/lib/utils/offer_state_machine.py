# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         6/03/23 16:24
# Project:      CFHL Transactional Backend
# Module Name:  offer_state_machine
# Description:
# ****************************************************************
from datetime import datetime
from django.conf import settings
from oasis.coffee_offers.lib.choices import CoffeeOffersStates
from oasis.models import Operation
from oasis.models import StateMachine


class OfferStateMachine:
    def __init__(self, offer, operation):
        self.__offer = offer
        self.__operation = operation
        self.__from_status = offer.status

    def run(self):
        oasis_state = self.__operation.state
        oasis_status = self.__operation.status
        machine_qs = StateMachine.objects.filter(from_state__exact=self.__from_status, oasis_state__exact=oasis_state,
                                                 oasis_status__exact=oasis_status, update_oasis__exact=False)
        states = machine_qs.all()
        for state in states:
            self.__offer.status = state.state
            # Change kg received
            if self.__offer.kg_received != self.__operation.quantity:
                self.__offer.kg_received = self.__operation.quantity

            if state.is_changed:
                # Change kg offered
                if self.__offer.kg_offered != self.__operation.otherif:
                    self.__offer.kg_offered = self.__operation.otherif
                # Change delivery date
                if self.__offer.delivery_Date != self.__operation.finaldate:
                    self.__offer.delivery_date = self.__operation.finaldate

            self.__offer.save()
