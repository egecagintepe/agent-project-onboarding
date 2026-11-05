import unittest
from main import healthcheck

class TestShopApi(unittest.TestCase):
    def test_healthcheck(self):
        self.assertEqual(healthcheck(), {"status": "ok", "service": "shop-api"})

if __name__ == "__main__":
    unittest.main()
