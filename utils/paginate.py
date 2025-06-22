from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.serializers import ValidationError

class LargeResultPagination(PageNumberPagination):
    page_size =100
    max_page_size = 1000

class StandardResultPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_query_param = 'page_size'



class CursorPagination(CursorPagination):
    page_size = 10
    ordering = 'name' #Use name occuring again and again


def paginate(data,paginator,page_number):
    if int(page_number)>paginator.num_pages:
        raise ValidationError("Not Enough pages",code=404)
    
    try:
        previous_page_number = paginator.page(page_number).previous_page_number()
    except:
        previous_page_number = None

    try:
        next_page_number = paginator.page(page_number).next_page_number()
    except:
        next_page_number = None

    data_to_show = paginator.page(page_number).object_list
    return {
        "Pagination":{
            "previous_page_number":previous_page_number,
            "is_previous_page" :  paginator.page(page_number).has_previous(),
            "next_page_number" :  next_page_number,
            "is_previous_page" :  paginator.page(page_number).has_next(),
            "start_index" :  paginator.page(page_number).start_index(),
            "end_index" :  paginator.page(page_number).end_index(),
            "total_entries" : paginator.count,
            "total_pages" : paginator.num_pages,
            "page" : page_number,
        },
        "result": data_to_show,
    }