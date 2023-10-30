from src.tests.unitests import *


class ResourceIndexTest(ProjectTest):
    def test_index_302(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, "text/html; charset=utf-8")
