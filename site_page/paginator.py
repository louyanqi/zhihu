def get_page_list(current_page, left, right, page_number):
    if current_page < 1:
        current_page = 1
    if current_page > page_number:
        current_page = page_number
    if current_page-1 < left:
        l = [i for i in range(current_page - left, current_page) if i > 0]
        m = [i for i in range(current_page, current_page + right+left+1-current_page) if i <= page_number]
        return l+m
    elif page_number - current_page < (right-1):
        l = [i for i in range(current_page - left - ((right-1) - (page_number - current_page)), current_page) if i > 0]
        m = [i for i in range(current_page, current_page + right) if i <= page_number]
        return l + m
    else:
        l = [i for i in range(current_page - left, current_page) if i > 0]
        m = [i for i in range(current_page, current_page + right) if i <= page_number]
        return l + m
