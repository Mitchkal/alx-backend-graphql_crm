#!/bin/env python3
"""
module for query schema
"""
from graphene import ObjectType, String, relay


class Query(ObjectType):
    """
    query class
    """

    all_customers = DjangoFilterConnectionField(CustomerNode)
    all_products = DjangoFilterConnectionField(ProductNode)
    hello = String()

    def resolve_greeting(parent, info):
        """
        returns greeting wehen called
        """
        return "Hello, GraphQl!"


schema = graphene.Schema(query=Query)
