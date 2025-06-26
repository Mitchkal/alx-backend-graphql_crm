#!/bin/env python3
"""
modulw for query schema
"""
from graphene import ObjectType, String, Schema


class Query(ObjectType):
    """
    query class
    """
    hello = String()

    def resolve_hello(parent, info):
        """
        returns greeting wehen called
        """
        return "Hello, GraphQl!"


schema = Schema(query=Query)
