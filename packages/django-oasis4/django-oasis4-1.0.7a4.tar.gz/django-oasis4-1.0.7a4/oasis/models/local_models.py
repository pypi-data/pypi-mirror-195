# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2022. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2022. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         10/12/22 3:52 PM
# Project:      CFHL Transactional Backend
# Module Name:  own_models
# Description:
# ****************************************************************
from django.utils.translation import gettext_lazy as _
from oasis.lib import managers
from zibanu.django.db import models


class Company(models.Model):
    """
    Model class to represent entity Company.
    """
    company_id = models.IntegerField(blank=False, null=False, verbose_name=_("Company Id"))
    name = models.CharField(max_length=100, blank=False, null=False, verbose_name=_("Company Name"))
    tax_id = models.CharField(max_length=30, blank=False, null=False, verbose_name=_("Tax Id"))
    address = models.CharField(max_length=100, blank=False, null=False, verbose_name=_("Address"))
    phone = models.CharField(max_length=100, blank=False, null=False, verbose_name=_("Phone Number"))
    city = models.CharField(max_length=100, blank=False, null=False, verbose_name=_("City"))
    legal_representative = models.CharField(max_length=150, blank=False, null=False,
                                            verbose_name=_("Legal Representative"))
    enabled = models.BooleanField(default=True, blank=False, null=False, verbose_name=_("Enabled"))
    # Set default Manager
    objects = managers.Company()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["company_id"], name="UNQ_company_company_id")
        ]


class Product(models.Model):
    """
    Model class to represent Product entity.
    """
    product_id = models.IntegerField(blank=False, null=False, verbose_name=_("Product id"))
    name = models.CharField(max_length=250, blank=False, null=False, verbose_name=_("Product name"))
    enabled = models.BooleanField(default=True, blank=False, null=False, verbose_name=_("Is enabled"))
    # Set default manager
    objects = managers.Product()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("product_id",), name="ownproduct_productid_unique", )
        ]


class DocumentType(models.Model):
    """
    Model class to represent DocumentType entity
    """
    type_id = models.CharField(max_length=1, blank=False, null=False, verbose_name=_("Document type oasis id"))
    description = models.CharField(max_length=50, blank=False, null=False, verbose_name=_("Document type description"))
    # Set default manager
    objects = managers.DocumentType()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("type_id",), name="UNQ_document_type_id")
        ]


class CoffeeWareHouse(models.Model):
    """
    Model class to represent CoffeeWareHouse entity
    """
    location_id = models.IntegerField(null=False, blank=False, verbose_name=_("Location ID"))
    location_name = models.CharField(max_length=150, blank=False, null=False, verbose_name=_("Location Name"))
    # Default Manager
    objects = managers.CoffeeWareHouse()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("location_id", ), name="UNQ_coffee_ware_house_location_id")
        ]

        indexes = [
            models.Index(fields=("location_name", ), name="IDX_coffee_ware_house_location")
        ]

