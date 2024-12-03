# import json
# import requests
# from bs4 import BeautifulSoup

# def handler(event, context):
#     url = "https://aws.amazon.com/jp/blogs/aws/"

#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")

#     articles = soup.select("article.blog-post")[:1]

#     result = []
#     for article in articles:
#         title = article.select_one("h2.blog-post-title").text.strip()
#         link = article.select_one("h2.blog-post-title a")["href"]
#         date = article.select_one("footer.blog-post-meta").text.strip()

#         result .append({"title": title, "link": link, "date": date})

#     contents = json.dumps(result, ensure_ascii=False)

#     response_body = {"application/json": {"body": contents}}
#     action_response = {
#         "actionGroup": event.get("actionGroup", "default_action_group"),
#         "apiPath": event.get("apiPath", "/default_path"),
#         "httpMethod": event.get("httpMethod", "GET"),
#         "httpStatusCode": 200,
#         "responseBody": response_body,
#     }
#     api_response = {"messageVersion": "1.0", "response": action_response}

#     return api_response
    
    # API Gatewayから呼び出す場合のレスポンス
    # return {
    #     "statusCode": 200,
    #     "body": contents,
    #     "headers": {
    #         "Content-Type": "application/json"
    #     }
    # }
import requests
import json
from bs4 import BeautifulSoup

# URLの指定
def handler(event, context):
    q = event.get('queryStringParameters', {}).get('q', None)
    print("q=", q)
    url = "https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=ja&source=gcsc&cselibv=8fa85d58e016b414&cx=014740152999584300951%3Acwjxl5ottau&q={0}&safe=off&cse_tok=AB-tC_4sYPYLzv88oenOvCrc1XGV%3A1728627859233&sort=&exp=cc&oq={1}&gs_l=partner-generic.12...0.0.1.16225.0.0.0.0.0.0.0.0..0.0.csems%2Cnrl%3D10...0.....34.partner-generic..1.3.216.7R-VAnp2ufE&callback=google.search.cse.api5000&rurl=http%3A%2F%2Fwww.sns-g.com%2F".format(q, q)
          
    print("url=", url)
    response = requests.get(url)

    if response.status_code == 200:
        text = response.text
        
        prefix = "/*O_o*/\ngoogle.search"
        prefixlen = "/*O_o*/\ngoogle.search.cse.api5000("
        suffix = ");"
        
        if text.startswith(prefix) and text.endswith(suffix):
            # 前後の文字列を取り除き、純粋なJSON部分を取り出す
            json_text = text[len(prefixlen):-len(suffix)]
            
            # JSONとして読み込み
            try:
                data = json.loads(json_text)
                
                # results部分だけを取り出す
                results = data.get("results", [])
                body = []
                
                for result in results:
                    # content, title, visibleUrlを取得
                    content = result.get("content", "N/A")
                    title = result.get("title", "N/A")
                    visible_url = result.get("visibleUrl", "N/A")
                    
                    body.append({"content": content, "title": title, "visibleUrl": visible_url})
                return {
                    "statusCode": 200,
                    "body": json.dumps(body),
                    "headers": {
                        "Content-Type": "application/json"
                    }
                }
            except json.JSONDecodeError as e:
                return {
                    "statusCode": 500,
                    "body": {},
                    "headers": {
                        "Content-Type": "application/json"
                    }
                }
        else:
            return {
                "statusCode": 500,
                "body": {},
                "headers": {
                    "Content-Type": "application/json"
                }
            }
    else:
        return {
            "statusCode": 500,
            "body": {},
            "headers": {
                "Content-Type": "application/json"
            }
        }