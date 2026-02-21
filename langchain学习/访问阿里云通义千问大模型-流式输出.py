# langchain_community
from langchain_community.llms.tongyi import Tongyi

Tongyi = Tongyi(model="qwen-max")

response = Tongyi.stream("请用中文介绍一下阿里云通义千问大模型。")
for chunk in response:
    print(chunk, end="", flush=True)