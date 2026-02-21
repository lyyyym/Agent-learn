from pyexpat import model
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate
)

from langchain_community.chat_models.tongyi import ChatTongyi

chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system","你是一个边塞诗人，可以作诗"),
    MessagesPlaceholder(variable_name="history"),
    ("human","请再来一首唐诗")
])

history = [
    ("human","你来作一首唐诗"),
    ("ai","窗前明月光，疑是地上霜。举头望明月，低头思故乡。"),
    ("human","好诗好诗，请再来一首"),
    ("ai","锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。")
]

prompt_txt = chat_prompt_template.invoke({"history":history}).to_string()
# print(prompt_txt)

model = ChatTongyi(model="qwen3-max")
res = model.invoke(input=prompt_txt)
print(res.content, type(res))