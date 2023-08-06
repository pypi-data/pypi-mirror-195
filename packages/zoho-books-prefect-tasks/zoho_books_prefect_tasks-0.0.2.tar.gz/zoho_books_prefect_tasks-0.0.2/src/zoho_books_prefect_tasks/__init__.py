"""
Tasks for interacting with Zoho Inventory.
"""
try:
    from .tasks.bills import Create, List, Fetch, Update, Delete
    from .tasks.contact_persons import Create, List, Fetch, Update, Delete, Primary
    from .tasks.contacts import Create, List, Fetch, Update, Delete, ListComments, Active, Inactive, \
        GetEmailStatement, SendEmailStatement, SendEmail
    from .tasks.organizations import Create, List, Fetch, Update, Delete
    from .tasks.sales_orders import Create, List, Fetch, Update, Delete, Void, Open, Approve, Submit, BulkExport, \
        BulkPrint, UpdateBillingAddress, UpdateShippingAddress
except ImportError:
    raise ImportError(
        'Using `prefect.tasks.zoho_books` requires Prefect to be installed with the "zoho-books-python-sdk" extra. '
    )

from ._version import get_versions

__version__ = get_versions()['version']
del get_versions
