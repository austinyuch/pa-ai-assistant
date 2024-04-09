import requests

# 您的Instagram頁面ID和訪問令牌
page_id = "<your-page-id>"
access_token = "<your-access-token>"

# 發送GET請求到Instagram Graph API
url = f"https://graph.instagram.com/{page_id}/media?access_token={access_token}"
response = requests.get(url)

# 解析響應
data = response.json()

# 遍歷每個媒體項目
for item in data["data"]:
    # 獲取媒體項目的詳細信息
    media_id = item["id"]
    url = f"https://graph.instagram.com/{media_id}?fields=id,media_type,media_url,username,timestamp,caption&access_token={access_token}"
    response = requests.get(url)
    media_data = response.json()

    # 打印媒體項目的詳細信息
    print(media_data)
