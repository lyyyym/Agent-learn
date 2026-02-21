from langchain_core.prompts import FewShotPromptTemplate,PromptTemplate
from langchain_community.llms.tongyi import Tongyi
# 示例模板
example_template = PromptTemplate.from_template("单词：{word}，反义词：{antonym}")

# 示例数据注入，要求为list内部套字典
example_data = [
    {"word": "快乐", "antonym": "悲伤"},
    {"word": "高兴", "antonym": "难过"}
]

few_shot_prompt = FewShotPromptTemplate(
    example_prompt = example_template, #示例数据模板
    examples = example_data,        #示例数据
    prefix = "请根据以下示例，生成对应的反义词：",        #前缀
    suffix = "请生成单词“{input}”的反义词。",        #后缀
    input_variables = ['input'], #输入变量 声明在前缀或者后缀中所需要注入的变量名
)

prompt_text = few_shot_prompt.invoke(input={"input": "幸福"}).to_string()
print(prompt_text)

model = Tongyi(model="qwen-max")

print(model.invoke(input=prompt_text))