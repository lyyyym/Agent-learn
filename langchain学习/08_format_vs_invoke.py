from langchain_core.prompts import PromptTemplate

# 1. 定义一个简单的提示词模板
template = PromptTemplate.from_template("请给我讲一个关于{topic}的笑话。")

print("--- 1. format 方法演示 ---")
# format: 仅进行字符串替换，返回的是标准的 Python 字符串 (str)
formatted_string = template.format(topic="程序员")
print(f"类型: {type(formatted_string)}")
print(f"内容: {formatted_string}")

print("\n--- 2. invoke 方法演示 ---")
# invoke: 遵循 Runnable 协议，返回的是 PromptValue 对象
# 这种对象可以方便地转换为字符串 (to_string) 或 消息列表 (to_messages，用于 ChatModel)
invoke_result = template.invoke({"topic": "程序员"})
print(f"类型: {type(invoke_result)}")
print(f"内容: {invoke_result}")
print(f"转为字符串: {invoke_result.to_string()}")
print(f"转为消息(用于ChatModel): {invoke_result.to_messages()}")

print("\n--- 3. 为什么这很重要？ ---")
# 如果你是直接看字符串，觉得没区别。
# 但 invoke 的返回值通用性更强。
# 例如，如果是 ChatPromptTemplate，invoke 会生成 Message 对象列表，而 format 可能会报错或生成不符合 ChatModel 预期的字符串。

from langchain_core.prompts import ChatPromptTemplate

chat_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个幽默大师。"),
    ("user", "讲一个关于{topic}的笑话")
])

print("\n[ChatPromptTemplate 对比]")
# format_messages 是旧版常用方法，现在推荐用 invoke
chat_invoke_result = chat_template.invoke({"topic": "AI"})
print(f"Chat invoke 结果类型: {type(chat_invoke_result)}")
print(f"Chat invoke 结果内容: {chat_invoke_result.to_messages()}")
