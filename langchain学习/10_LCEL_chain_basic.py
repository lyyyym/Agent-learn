import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser



# 1. 定义组件
# ------------------------------------------
# 组件 A: 提示词模板
prompt = ChatPromptTemplate.from_template("请用非常简短的一句话介绍：{topic}")

# 组件 B: 聊天模型
from langchain_community.chat_models.tongyi import ChatTongyi
model = ChatTongyi(model="qwen3-max")

# 组件 C: 输出解析器 (将 ChatMessage 转为 str)
output_parser = StrOutputParser()


# 2. 构建链 (LCEL)
# ------------------------------------------
# 语法糖 `|` (管道符)
# 流程：输入 -> prompt -> model -> output_parser -> 结果
chain = prompt | model | output_parser


# 3. 调用链
# ------------------------------------------
print("--- 单次调用 (invoke) ---")
result = chain.invoke({"topic": "大语言模型"})
print(result)


print("\n--- 批处理 (batch) ---")
# 并行处理多个输入，效率更高
results = chain.batch([
    {"topic": "Python"},
    {"topic": "LangChain"},
    {"topic": "Agent"}
])
for r in results:
    print(r)


print("\n--- 流式输出 (stream) ---")
# 像打字机一样逐字输出 (适合 Web 实时展示)
# 注意：模拟的 Lambda 可能不支持流式，如果是真实 ChatOpenAI 会看到效果
for chunk in chain.stream({"topic": "未来科技"}):
    print(chunk, end="|", flush=True)
print()
