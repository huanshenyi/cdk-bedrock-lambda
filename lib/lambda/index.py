import json
import requests
from bs4 import BeautifulSoup

def handler(event, context):
    url = "https://aws.amazon.com/jp/blogs/aws/"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.select("article.blog-post")[:1]

    result = []
    for article in articles:
        title = article.select_one("h2.blog-post-title").text.strip()
        link = article.select_one("h2.blog-post-title a")["href"]
        date = article.select_one("footer.blog-post-meta").text.strip()

        result .append({"title": title, "link": link, "date": date})

    contents = json.dumps(result, ensure_ascii=False)

    response_body = {"application/json": {"body": contents}}
    action_response = {
        "actionGroup": event.get("actionGroup", "default_action_group"),
        "apiPath": event.get("apiPath", "/default_path"),
        "httpMethod": event.get("httpMethod", "GET"),
        "httpStatusCode": 200,
        "responseBody": response_body,
    }
    api_response = {"messageVersion": "1.0", "response": action_response}

    return api_response
    
    # API Gatewayから呼び出す場合のレスポンス
    # return {
    #     "statusCode": 200,
    #     "body": contents,
    #     "headers": {
    #         "Content-Type": "application/json"
    #     }
    # }