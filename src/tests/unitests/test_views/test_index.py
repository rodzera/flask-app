from src.tests.unitests import *


class ViewsIndexTest(ProjectTest):
    def test_index_302(self):
        response = self.client.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "text/html; charset=utf-8")
