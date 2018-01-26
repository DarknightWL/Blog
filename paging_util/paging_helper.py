# coding: utf-8
# __author__ = "Darknight"
from django.utils.safestring import mark_safe


def try_int(arg, default=1):
    try:
        arg_int = int(arg)
    except Exception as error:
        arg_int = default
    return arg_int


class PagingInfo(object):
    '''
    生成分页功能所需要的参数：
        1、每页的数据开始的位置
        2、每页的数据结束的位置
        3、分页的总页数
    '''
    def __init__(self, cur_page, all_data_count, per_page_data_count=5):
        '''
        :param cur_page: 当前页
        :param all_data_count: 数据总量
        :param per_page_data_count: 每页显示的数据量
        '''
        self.CurrentPage = cur_page
        self.AllDataCount = all_data_count
        self.PerPageDataCount = per_page_data_count

    @property
    def start(self):
        # 单页数据开始位置
        return (self.CurrentPage-1) * self.PerPageDataCount

    @property
    def end(self):
        # 单页数据结束位置
        return self.CurrentPage * self.PerPageDataCount

    @property
    def all_page_count(self):
        # 总页数
        temp = divmod(self.AllDataCount, self.PerPageDataCount)
        if temp[1] == 0:
            all_page_count = temp[0]
        else:
            all_page_count = temp[0] + 1
        return all_page_count


def page_number(cur_page, all_page_count):
    '''
    :param cur_page: 当前页
    :param all_page_count: 总页数
    :return: 页码的开始和结束位置
    '''
    if all_page_count <= 11:
        paging_begin = 1
        paging_end = all_page_count + 1
    else:
        if cur_page <= 6:
            paging_begin = 1
            paging_end = cur_page + 5
        else:
            if cur_page + 5 > all_page_count:
                paging_begin = cur_page - 6
                paging_end = all_page_count
            else:
                paging_begin = cur_page - 6
                paging_end = cur_page + 5
    return paging_begin, paging_end


def paging_html(cur_page, all_page_count, url):
    '''
    @effect: 生成分页链接的html标签
    :param cur_page: 当前页
    :param all_page_count: 总页数
    :param url: 网址
    :return: html标签
    '''
    paging_html = []
    head_page = "<a href='{0}'>首页</a>".format(url)
    paging_html.append(head_page)
    if cur_page - 1 <= 0:
        last_page = "<a href=''>上一页</a>"
    else:
        last_page = "<a href='{0}{1}'>上一页</a>".format(url, cur_page - 1)
    paging_html.append(last_page)
    # 其他页码链接
    paging_begin, paging_end = page_number(cur_page, all_page_count)
    for i in range(paging_begin, paging_end):
        paging = "<a href='{0}{1}'>{2}</a>".format(url, i, i)
        paging_html.append(paging)

    if cur_page + 1 > all_page_count:
        next_page = "<a href='{0}{1}'>下一页</a>".format(url, all_page_count)
    else:
        next_page = "<a href='{0}{1}'>下一页</a>".format(url, cur_page + 1)
    paging_html.append(next_page)
    end_page = "<a href='{0}{1}'>尾页</a>".format(url, all_page_count)
    paging_html.append(end_page)

    return mark_safe(' '.join(paging_html))
