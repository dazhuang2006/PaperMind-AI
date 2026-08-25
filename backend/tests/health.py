# 自动化测试：验证 /api/health 接口是否正常
import sys
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

# 把项目根目录加入导入路径，这样不管从哪个目录运行测试都能找到 backend 包
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.main import app

client = TestClient(app)


class HealthTest(unittest.TestCase):

    def test_health(self):
        resp = client.get("/api/health")
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["status"], "ok")
        self.assertIn("PaperMind", body["app"])


if __name__ == "__main__":
    unittest.main()
