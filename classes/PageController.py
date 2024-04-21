from functions.rest_api import controller, get
from repos.PageRepo import PageRepo
from entities.Page import Page
@controller('/')
class PageController:

    def __init__(self):
        self.repo = PageRepo()

    @get('/')
    def test(self):
        self.repo = PageRepo()

        self.repo.insert_page(Page(link='test', data='data'))
        return {
                'message': 'GEEEEEET /',
                'method': 'GET',
            }
    @get('/get')
    def testX(self):
        self.repo = PageRepo()

        records = self.repo.get_pages()
        return {
                'message': 'testX',
                'method': 'GET',
                'data': records
            }