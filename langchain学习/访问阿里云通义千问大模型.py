# langchain_community
from langchain_community.llms.tongyi import Tongyi

Tongyi = Tongyi(model="qwen-max")

response = Tongyi.invoke("请用中文介绍一下阿里云通义千问大模型。")
print(response)