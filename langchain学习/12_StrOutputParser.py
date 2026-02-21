from itertools import chain
from turtle import mode
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate, prompt

parser = StrOutputParser()
model = ChatTongyi(model="qwen3-max")
prompt = PromptTemplate.from_template(
    "我的邻居姓{lasename}, 刚生了{gender}, 我想给他起个名字，名字要和姓氏搭配，名字的性别要和孩子的性别一致,简单回答。"
)

chain = prompt | model | parser | model | parser

res: AIMessage = chain.invoke({"lasename":"王", "gender":"男"})
print(res)
print(type(res))