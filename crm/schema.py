#!/usr/bin/env python3
"""
mutation classes
"""
from decimal import ROUND_HALF_UP, Decimal
import graphene
from graphql import GraphQLError
import re
from django.db import transaction
from graphene_django import DjangoObjectType
from .models import Customer, Product, Order

from graphene import ObjectType, String, relay
from graphene_django.filter import DjangoFilterConnectionField
from .filters import CustomerFilter, ProductFilter, OrderFilter


class CustomerNode(DjangoObjectType):
    """
    Node for customer model
    """

    class Meta:
        model = Customer
        filterset_class = CustomerFilter
        interfaces = (relay.Node,)


class ProductNode(DjangoObjectType):
    """
    Node for product model
    """

    class Meta:
        model = Product
        filterset_class = ProductFilter
        interfaces = (relay.Node,)


class CustomerFilterInput(graphene.InputObjectType):
    """
    Custom filter input
    """

    name_icontains = graphene.String(required=False)
    email_icontains = graphene.String(required=False)
    created_at_gte = graphene.DateTime()
    created_at_lte = graphene.DateTime()
    phone_starts_with = graphene.String(required=False)


class CustomerInput(graphene.InputObjectType):
    """
    input object type
    """

    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()


class CustomerType(DjangoObjectType):
    """
    Type definition for customer
    """

    class Meta:
        model = Customer
        fields = ("id", "name", "email", "phone", "created_at")


class CreateCustomer(graphene.Mutation):
    """
    graphene mutation for customer model
    """

    class Arguments:
        """
        input arguments for mutation
        """

        id = graphene.ID()
        input = CustomerInput(required=True)

        # name = graphene.String(required=True)
        # email = graphene.String(required=True)
        # phone = graphene.String()

    customer = graphene.Field(CustomerType)
    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, input, id=None):
        """
        Validation for email and phone
        email uniqueness, phone validity
        """
        name = input.name
        email = input.email
        phone = input.phone

        # for email uniqueness
        if Customer.objects.filter(email=email):
            raise GraphQLError("Customer with the same email already exists.")

        # for phone validation if provided
        if phone and not re.match(r"^(\+?\d{7,15}|\d{3}-\d{3}-\d{4})$", phone):
            raise GraphQLError("Invalid customer phone number.")

        # create a new customer instance
        customer = Customer(name=name, email=email, phone=phone)
        # save the customer instance
        customer.save()

        #  return mutation of created customer instance
        return CreateCustomer(
            customer=customer, success=True, message="Customer created successfully."
        )


class BulkCreateCustomers(graphene.Mutation):
    """
    Mutatation to create bulk customers
    """

    class Arguments:
        """
        input arguments for mutation
        """

        input = graphene.List(CustomerInput, required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, info, input):
        """
        create bulk customers in one transaction
        """
        customers = input
        created = []
        errors = []

        new_customers = []

        for index, data in enumerate(customers):
            name = data.name
            email = data.email
            phone = data.phone

            # Validate email uniqueness
            if Customer.objects.filter(email=email).exists():
                errors.append(
                    f"[{index}] Customer with email '{email}' already esists."
                )
                continue

            # Validate phone number
            if phone and not re.match(r"^(\+?\d{7,15}|\d{3}-\d{3}-\d{4})$", phone):
                errors.append(f"[{index}] Invalid phone number '{phone}'.")
                continue

            # create new customer instance
            new_customers.append(Customer(name=name, email=email, phone=phone))

        # save all customers in one transaction
        try:
            with transaction.atomic():
                created_objs = Customer.objects.bulk_create(new_customers)
                created.extend(created_objs)
        except Exception as e:
            errors.append(f"Bulk creation failed: {str(e)}")

        return BulkCreateCustomers(customers=created, errors=errors)


class ProductInput(graphene.InputObjectType):
    """
    Input object types for a product
    """

    name = graphene.String()
    # price = graphene.Float(required=True)
    price = graphene.Decimal(required=True)

    # price = graphene.Decimal(required=True)
    stock = graphene.Int()


class ProductType(DjangoObjectType):
    """
    Type definition for  a product
    """

    class Meta:
        model = Product
        fields = ("id", "name", "price", "stock")


class ProductFilterInput(graphene.InputObjectType):
    """
    custom filter input for products
    """

    price_gte = graphene.Float(required=False)
    price_lte = graphene.Float(required=False)
    stock_gte = graphene.Int(required=False)
    stock_lte = graphene.Int(required=False)
    name_icontains = graphene.String(required=False)


class CreateProduct(graphene.Mutation):
    """
    Mutation class for a product
    """

    class Arguments:
        """
        input arguments to the mutation
        """

        input = ProductInput(required=True)

    product = graphene.Field(ProductType)
    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, input):
        """
        create a new product instance
        """
        # from decimal import Decimal

        name = input.name
        # price = input.price
        price = Decimal(str(input.price)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        stock = input.stock

        if price < 0:
            raise GraphQLError("Price cannot be negative.")
        if stock < 0:
            raise GraphQLError("Stock cannot be negative.")
        # # Validate uniqueness of product name
        # if Product.objects.filter(name=name).exists():
        #     raise GraphQLError(f"A product with the name exists")

        product = Product(name=name, price=price, stock=stock)

        product.save()

        return CreateProduct(
            product=product,
            success=True,
            message=f"Product '{name}' created successfully.",
        )


class UpdateLowStockProducts(graphene.Mutation):
    """
    Mutation class that queries products with stock <10
    and increments the stock by ten to simulate restocking
    then returns a list of updated products and success message
    """

    class Arguments:
        """
        input arguments for the mutation
        """

        increment = graphene.Int(required=False, default_value=10)
        input = ProductInput(required=False)

    # attributes to return
    updated_products = graphene.List(ProductType)
    new_stock_level = graphene.Int()
    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, increment, input=None):
        """
        query product with stock less than 10 and increment
        also return the new stock level
        """
        from django.db import transaction

        products = Product.objects.filter(stock__lt=10)
        if not products.exists():
            raise GraphQLError("No products with low stock found.")
        updated_products = []
        try:
            with transaction.atomic():
                for prod in products:
                    prod.stock += increment
                    prod.save()
                    updated_products.append(prod)

        except Exception as e:
            raise GraphQLError(f"Failed to update products: {e}")

        return UpdateLowStockProducts(
            updated_products=updated_products,
            new_stock_level=sum(p.stock for p in updated_products),
            success=True,
            message=f"Successfully updated {len(updated_products)} products.",
        )


class OrderInput(graphene.InputObjectType):
    """
    Input object type for an order mutation
    """

    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)


class OrderFilterInput(graphene.InputObjectType):
    """
    Input object type for filtering orders
    """

    customer_name = graphene.String(required=False)
    order_date_lte = graphene.DateTime(required=False)
    order_date_gte = graphene.DateTime(required=False)
    total_amount_gte = graphene.Float(required=False)
    total_amount_lte = graphene.Float(required=False)
    product_name = graphene.String(required=False)
    product_id = graphene.ID(required=False)


class OrderType(DjangoObjectType):
    """
    Type definition for an order
    """

    total_amount = graphene.Decimal()
    customer = graphene.Field(CustomerType)
    product = graphene.List(ProductType)

    class Meta:
        model = Order
        fields = ("id", "order_date")

    def resolve_total_amount(self, info):
        return graphene.Decimal(self.total_price)

    def resolve_customer(self, info):
        return self.customer

    def resolve_products(self, info):
        return self.products.all()


class OrderNode(DjangoObjectType):
    """
    Node for order model
    """

    class Meta:
        model = Order
        filterset_class = OrderFilter
        interfaces = (relay.Node,)


class CreateOrder(graphene.Mutation):
    """
    Mutation class for creating an order
    """

    class Arguments:
        """
        Input arguments for the mutation
        """

        input = OrderInput(required=True)
        # total_price = graphene.Float()

    order = graphene.Field(OrderType)
    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, input, id=None):
        """
        Create a new order instance
        """
        customer_id = input.customer_id
        product_ids = input.product_ids
        if len(product_ids) == 0:
            raise GraphQLError("At least one product must be included")
        if not Customer.objects.filter(id=customer_id).exists():
            raise GraphQLError(f"Customer '{customer_id}' does not exist.")

        products = Product.objects.filter(id__in=product_ids)
        if len(products) != len(product_ids):
            missing_ids = set(product_ids) - set(products.values_list("id", flat=True))
            raise GraphQLError(f"Products with ids {missing_ids} do not exist.")
        if not products.exists():
            raise GraphQLError("The order does not contain any valid products.")

        total_price = sum(product.price for product in products)
        order = Order(customer_id=customer_id, total_price=total_price)
        order.save()
        order.products.set(products)
        return CreateOrder(
            order=order,
            success=True,
            message=f"Order '{order.id}' created successfully.",
        )


class Query(ObjectType):
    """
    query class
    """

    hello = String()

    all_customers = DjangoFilterConnectionField(
        CustomerNode, filter=CustomerFilterInput(required=False)
    )
    all_products = DjangoFilterConnectionField(
        ProductNode, filter=ProductFilterInput(required=False)
    )
    all_orders = DjangoFilterConnectionField(
        OrderNode, filter=OrderFilterInput(required=False)
    )
    # filtered_customers = graphene.List(
    #     CustomerType, filter=CustomerFilterInput(required=False)
    # )
    filtered_orders = DjangoFilterConnectionField(
        OrderNode, filter=OrderFilterInput(required=False)
    )
    filtered_customers = DjangoFilterConnectionField(
        CustomerNode, filter=CustomerFilterInput(required=False)
    )
    filtered_products = DjangoFilterConnectionField(
        ProductNode, filter=ProductFilterInput(required=False)
    )

    def resolve_hello(parent, info):
        """
        returns greeting wehen called
        """
        return "Hello, GraphQl!"


# register mutation
class Mutation(graphene.ObjectType):
    """
    registered mutations
    """

    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
    update_low_stock_products = UpdateLowStockProducts.Field()
