from src.tests.unitests import *


class ResourceUsersTest(ProjectTest):
    def test_index_302(self):
        response = self.client.get("/api/users", headers={"Accept": "application/json", **self.api_auth})
        self.assertEqual(response.status_code, 200)
