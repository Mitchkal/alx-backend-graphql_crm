#!/bin/env python3
"""
modulw for query schema
"""
from graphene import ObjectType, String


class Query(ObjectType):
    """
    query class
    """
    hello = String()

    def resolve_greeting(parent, info):
        """
        returns greeting wehen called
        """
        return "Hello, GraphQl!"


schema = graphene.Schema(query=Query)
