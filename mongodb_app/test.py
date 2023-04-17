import unittest

from app import app


class AppTestCase(unittest.TestCase):
    #this is for the setup of the todo-list app
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()
    
    
    #test for the update
    def test_update(self):
        response = self.client.post(
            '/update',
            data=dict(content='sport', degree='important'),
            follow_redirects=True
        )
        
        assert self.client.get('/update', query_string=dict(content='eat', degree='important'))
    
    #test for the delete
    def test_delete(self):
        response = self.client.post(
            '/delete',
            data=dict(content='sport', degree='important'),
            follow_redirects=True
        )
        
        assert self.client.get('/delete', query_string=dict(content='sport', degree='important'))
    
    #negative test for the update
    def test_update_negative(self):
        response = self.client.post(
            '/update',
            data=dict(content='gym', degree='not important'),
            follow_redirects=True
        )
        
        assert self.client.get('/update', query_string=dict(content='go walking', degree='important'))


if __name__ == "__main__":
    unittest.main()