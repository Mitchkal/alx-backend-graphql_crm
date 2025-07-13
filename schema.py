#!/usr/bin/env python3
"""
modulw for query schema
"""
from graphene import ObjectType, Schema

from crm.schema import Query as CRMQuery, Mutation as CRMMutation


class Query(CRMQuery, ObjectType):
    """
    Query class that combines CRM queries
    """

    pass

    # hello = String()

    # def resolve_hello(parent, info):
    #     """
    #     Returns a greeting when called
    #     """
    #     return "Hello, GraphQL!"


class Mutation(CRMMutation, ObjectType):
    pass


schema = Schema(query=Query, mutation=CRMMutation)
