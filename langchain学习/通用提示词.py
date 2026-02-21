from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi
# zero-shot思想
prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lasename}, 刚生了{gender}, 我想给他起个名字，名字要和姓氏搭配，名字的性别要和孩子的性别一致,简单回答。"
)

# prompt_txt = prompt_template.format(lasename="李", gender="男孩")

model = Tongyi(model="qwen-max")
# res = model.invoke(input=prompt_txt)
# print(res) 


# 加入链

chain = prompt_template | model
chain_res = chain.invoke(input={"lasename": "李", "gender": "男孩"})
print(chain_res)