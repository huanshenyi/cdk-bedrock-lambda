import os
import boto3
import json
import re

from linebot import LineBotApi
from linebot.models import TextSendMessage

LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']
AGENT_ID = os.environ['AGENT_ID']
AGENT_ALIAS_ID = os.environ['AGENT_ALIAS_ID']
LINE_BOT_API = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

def chat(message, session_id):

    # Agent用のSDKが用意されている
    client = boto3.client("bedrock-agent-runtime")
    
    # Agentを実行する
    response = client.invoke_agent(
        inputText=message,
        agentId=AGENT_ID,    # AgentのID
        agentAliasId=AGENT_ALIAS_ID,  # AgentのaliasのID
        sessionId=session_id,   # セッションのID
        enableTrace=False
    )
    
    # Agentの実行結果を取得し、返す
    results = response['completion']
    for result in results:        
        if 'chunk' in result:
            data = result['chunk']['bytes'].decode("utf-8")
    print(data)
    return data

def lambda_handler(event, context):
    body = json.loads(event['body'])

    if len(body['events']) > 0:
        if body['events'][0]['type'] == 'message':
            if body['events'][0]['message']['type'] == 'text':
                # Messaging APIのイベントからメッセージとuser idを取り出す
                message = body['events'][0]['message']['text']
                user = body['events'][0]['source']['userId']

                # Agentを実行し、回答を取得
                resp = chat(message, user)

                # Agentの回答を、返答の形でユーザーに返す
                LINE_BOT_API.reply_message(
                    body['events'][0]['replyToken'],
                    messages
                )

    return {
        "statusCode": 200,
        "body": json.dumps('Success!'),
    }
