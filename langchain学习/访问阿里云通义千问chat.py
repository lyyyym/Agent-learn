from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

llm = ChatTongyi(model="qwen3-max")

messages = [
    SystemMessage(content="你是一位边塞诗人。"),
    HumanMessage(content="给我写一首唐诗。"),
    AIMessage(content="边塞风光好，\n长城蜿蜒绕。\n烽火连三月，\n家书抵万金。"),
    HumanMessage(content="按照你上一首的格式，再来一首宋词。"),
]

for chunk in llm.stream(messages):
    # Some stream chunks can be empty.
    if chunk.content:
        print(chunk.content, end="", flush=True)

