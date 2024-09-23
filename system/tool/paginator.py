class Paginated:
    def __init__(self, current_page: int, total_pages: int, content: list):
        self.current_page = current_page
        self.total_pages = total_pages
        self.content = content

