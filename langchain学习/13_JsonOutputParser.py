from itertools import chain
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate, prompt

str_parser = StrOutputParser()
json_parser = JsonOutputParser()
model = ChatTongyi(model="qwen3-max")

first_prompt = PromptTemplate.from_template(
    "我的邻居姓{lasename}, 刚生了{gender}, 我想给他起个名字，名字要和姓氏搭配，名字的性别要和孩子的性别一致,仅回复名字，无需其他内容。"
    "并将名字封装为json格式，key为name，value为姓名，请严格遵守json格式要求。"
)

second_prompt = PromptTemplate.from_template(
    "姓名：{name}，请帮我解析含义"
)

chain = first_prompt | model | json_parser | second_prompt | model | str_parser

res = chain.invoke({"lasename":"王", "gender":"男"})
print(res)
print(type(res))