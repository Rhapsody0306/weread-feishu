import requests
import os

# 微信读书数据获取
def get_weread_notes():
    cookie = os.getenv("WEREAD_COOKIE")
    headers = {"Cookie": cookie, "User-Agent": "Mozilla/5.0"}
    response = requests.get("https://i.weread.qq.com/user/notebooks", headers=headers)
    return response.json().get("books", [])

# 飞书API工具
class FeishuTool:
    def __init__(self):
        self.app_id = os.getenv("FEISHU_APP_ID")
        self.app_secret = os.getenv("FEISHU_APP_SECRET")
        self.token = self._get_token()
    
    def _get_token(self):
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        res = requests.post(url, json={"app_id": self.app_id, "app_secret": self.app_secret})
        return res.json().get("tenant_access_token")
    
    def add_to_table(self, app_token, table_id, data):
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
        headers = {"Authorization": f"Bearer {self.token}"}
        requests.post(url, headers=headers, json={"fields": data})

# 主函数
if __name__ == "__main__":
    notes = get_weread_notes()
    feishu = FeishuTool()
    for book in notes:
        feishu.add_to_table(
            app_token="你的多维表格App Token",  # 在飞书表格URL中查找
            table_id="你的表格ID",
            data={
                "书名": book.get("title"),
                "作者": book.get("author"),
                "进度": book.get("progress"),
                "笔记": "\n".join([highlight.get("markText") for highlight in book.get("highlights")])
            }
        )
