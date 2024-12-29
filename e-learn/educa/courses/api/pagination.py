from rest_framework.pagination import PageNumberPagination

class StandardPagination(PageNumberPagination):
    """
    Custom pagination class that extends PageNumberPagination from DRF.

    This pagination class allows for controlling the number of items per page
    in API responses. It provides the following features:
    - A default page size of 10 items per page.
    - A query parameter (`page_size`) that can be used to specify the number of 
      items per page dynamically.
    - A maximum page size limit of 50 to prevent excessively large responses.

    Attributes:
        page_size (int): The default number of items to return per page (10).
        page_size_query_param (str): The query parameter name to allow clients
                                      to specify a custom page size ('page_size').
        max_page_size (int): The maximum number of items allowed per page (50).
    """
    # Default page size
    page_size = 10
    # Query parameter to allow users to override the page size
    page_size_query_param = 'page_size'
    # Maximum allowed page size
    max_page_size = 50
