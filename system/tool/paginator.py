import math

class Paginated:
    def __init__(self, current_page: int, total_pages: int, content: list):
        self.current_page = current_page
        self.total_pages = total_pages
        self.content = content


def paginate(data: list, page=1, amount_per_page=10):
    pages = math.ceil(len(data) / amount_per_page)
    if page > pages or page < 1:
        raise IndexError("Invalid Page Number")
    c = (page - 1) * amount_per_page
    liw = data[c:c+amount_per_page]
    return Paginated(page, pages, liw)
