from zoho_books_python_sdk.resources import ContactPersons

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
            contact_persons = ContactPersons()

            response = contact_persons.create(path_params=path_params, query=query, body=body, **task_kwargs)
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
            contact_persons = ContactPersons()

            response = contact_persons.list(**task_kwargs)
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
            contact_persons = ContactPersons()

            response = contact_persons.get(id_=id_, path_params=path_params, query=query, **task_kwargs)
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
            contact_persons = ContactPersons()

            response = contact_persons.update(id_=id_, path_params=path_params, query=query, body=body, **task_kwargs)
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
            contact_persons = ContactPersons()

            response = contact_persons.delete(id_=id_, path_params=path_params, query=query, **task_kwargs)
            return response
        except Exception as error:
            print(error)
            raise error


class Primary(Task):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @defaults_from_attrs()
    def run(self, id_: str = None):

        if id_ is None:
            raise ValueError("An id must be provided")

        try:
            contact_persons = ContactPersons()

            response = contact_persons.primary(id_=id_)
            return response
        except Exception as error:
            print(error)
            raise error
