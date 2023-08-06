from zoho_books_python_sdk.resources import SalesOrders

from prefect import Task
from prefect.utilities.tasks import defaults_from_attrs
from typing import Any


class Create(Task):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @defaults_from_attrs()
    def run(self, path_params: dict = None, query: dict = None, body: dict = None, **task_kwargs: Any):

        if body is None:
            raise ValueError("An object must be provided")

        try:
            sales_orders = SalesOrders()

            response = sales_orders.create(path_params=path_params, query=query, body=body, **task_kwargs)
            return response
        except Exception as error:
            print(error)
            raise error


class List(Task):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @defaults_from_attrs()
    def run(self, **task_kwargs: Any):

        try:
            sales_orders = SalesOrders()

            response = sales_orders.list(**task_kwargs)
            return response
        except Exception as error:
            print(error)
            raise error


class Fetch(Task):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @defaults_from_attrs()
    def run(self, id_: str = None, path_params: dict = None, query: dict = None, **task_kwargs: Any):

        if id_ is None:
            raise ValueError("An id must be provided")

        try:
            sales_orders = SalesOrders()

            response = sales_orders.get(id_=id_, path_params=path_params, query=query, **task_kwargs)
            return response
        except Exception as error:
            print(error)
            raise error


class Update(Task):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @defaults_from_attrs()
    def run(self, id_: str = None, path_params: dict = None, query: dict = None, body: dict = None, **task_kwargs: Any):

        if id_ is None:
            raise ValueError("An id must be provided")

        if body is None:
            raise ValueError("An object must be provided")

        try:
            sales_orders = SalesOrders()

            response = sales_orders.update(id_=id_, path_params=path_params, query=query, body=body, **task_kwargs)
            return response
        except Exception as error:
            print(error)
            raise error


class Delete(Task):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @defaults_from_attrs()
    def run(self, id_: str = None, path_params: dict = None, query: dict = None, **task_kwargs: Any):

        if id_ is None:
            raise ValueError("An object must be provided")

        try:
            sales_orders = SalesOrders()

            response = sales_orders.delete(id_=id_, path_params=path_params, query=query, **task_kwargs)
            return response
        except Exception as error:
            print(error)
            raise error


class Void(Task):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @defaults_from_attrs()
    def run(self, id_: str = None, body: dict = None, **task_kwargs: Any):

        if id_ is None:
            raise ValueError("An object must be provided")

        try:
            sales_orders = SalesOrders()

            response = sales_orders.void(id_=id_, body=body)
            return response
        except Exception as error:
            print(error)
            raise error


class Open(Task):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @defaults_from_attrs()
    def run(self, id_: str = None, **task_kwargs: Any):

        if id_ is None:
            raise ValueError("An object must be provided")

        try:
            sales_orders = SalesOrders()

            response = sales_orders.open(id_=id_)
            return response
        except Exception as error:
            print(error)
            raise error


class Submit(Task):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @defaults_from_attrs()
    def run(self, id_: str = None, **task_kwargs: Any):

        if id_ is None:
            raise ValueError("An object must be provided")

        try:
            sales_orders = SalesOrders()

            response = sales_orders.submit(id_=id_)
            return response
        except Exception as error:
            print(error)
            raise error


class Approve(Task):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @defaults_from_attrs()
    def run(self, id_: str = None, **task_kwargs: Any):

        if id_ is None:
            raise ValueError("An object must be provided")

        try:
            sales_orders = SalesOrders()

            response = sales_orders.approve(id_=id_)
            return response
        except Exception as error:
            print(error)
            raise error


class BulkExport(Task):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @defaults_from_attrs()
    def run(self, body: dict = None, **task_kwargs: Any):

        if body is None:
            raise ValueError("An object must be provided")

        try:
            sales_orders = SalesOrders()

            response = sales_orders.bulk_export(body=body)
            return response
        except Exception as error:
            print(error)
            raise error


class BulkPrint(Task):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @defaults_from_attrs()
    def run(self, body: dict = None, **task_kwargs: Any):

        if body is None:
            raise ValueError("An object must be provided")

        try:
            sales_orders = SalesOrders()

            response = sales_orders.bulk_print(body=body)
            return response
        except Exception as error:
            print(error)
            raise error


class UpdateBillingAddress(Task):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @defaults_from_attrs()
    def run(self, id_: str = None, body: dict = None, **task_kwargs: Any):

        if id_ is None:
            raise ValueError("An object must be provided")

        if body is None:
            raise ValueError("An object must be provided")

        try:
            sales_orders = SalesOrders()

            response = sales_orders.update_billing_address(id_=id_, body=body)
            return response
        except Exception as error:
            print(error)
            raise error


class UpdateShippingAddress(Task):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @defaults_from_attrs()
    def run(self, id_: str = None, body: dict = None, **task_kwargs: Any):

        if id_ is None:
            raise ValueError("An object must be provided")

        if body is None:
            raise ValueError("An object must be provided")

        try:
            sales_orders = SalesOrders()

            response = sales_orders.update_shipping_address(id_=id_, body=body)
            return response
        except Exception as error:
            print(error)
            raise error
