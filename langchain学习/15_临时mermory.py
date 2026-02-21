from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate, prompt
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import history
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from requests import session

model = ChatTongyi(model="qwen3-max")
prompt = PromptTemplate.from_template(
    "你需要根据用户的历史对话内容，来生成下一个对话内容。对话历史:{chat_history},用户提问:{input},请回答"
    )
str_parser = StrOutputParser()

base_chain = prompt | model | str_parser

store = {}
def get_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    
    return store[session_id]

#  创建一个新的链，对原有链增强功能：自动附加历史消息
conversation_chain = RunnableWithMessageHistory(
    base_chain,
    get_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

if __name__ == "__main__":
    # 固定格式，添加LangChain的配置，为当前程序配置所属的session_id
    session_config = {
        "configurable" : {
            "session_id":"user_001"
        }
    }
    res = conversation_chain.invoke({"input":"小明有两个猫"}, session_config)
    print("第一次执行",res)
    res = conversation_chain.invoke({"input":"小刚有一个狗"}, session_config)
    print("第二次执行",res)
    res = conversation_chain.invoke({"input":"总共有几个宠物"}, session_config)
    print("第三次执行",res)
