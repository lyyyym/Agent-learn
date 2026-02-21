import os,json
from typing import List, Sequence
from langchain_core.messages import message_to_dict, messages_from_dict
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate, prompt
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import history
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from requests import session
# message_to_dict 的作用是将 LangChain 的消息对象（如 HumanMessage, AIMessage 等）
# 转换为一个标准的 Python 字典格式，便于进行 JSON 序列化或持久化存储。
# 
# message_from_dict 的作用是将之前转换后的字典格式重新实例化为
# 对应的 LangChain 消息对象，从而恢复其原有的属性和方法。
class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self,session_id,storage_path):
        self.session_id = session_id
        self.storage_path = storage_path

        # 完整的文件路径
        self.file_path = os.path.join(self.storage_path, self.session_id)

        # 如果路径不存在，则创建
        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)

    def add_message(self, message: BaseMessage) -> None:
        """添加单条消息 (LangChain 核心接口要求)"""
        # 1. 读取现有消息
        current_messages = self.messages
        # 2. 追加新消息
        current_messages.append(message)
        # 3. 序列化
        serialized_messages = [message_to_dict(m) for m in current_messages]
        # 4. 写入文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(serialized_messages, f, ensure_ascii=False, indent=4)
    
    @property  #通过装饰器，将message方法变成成员属性
    def messages(self) -> List[BaseMessage]: 
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return messages_from_dict(data)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)





model = ChatTongyi(model="qwen3-max")
prompt = PromptTemplate.from_template(
    "你需要根据用户的历史对话内容，来生成下一个对话内容。对话历史:{chat_history},用户提问:{input},请回答"
    )
str_parser = StrOutputParser()

base_chain = prompt | model | str_parser


def get_history(session_id):
    return FileChatMessageHistory(session_id,storage_path="./chat_history")

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
    # res = conversation_chain.invoke({"input":"小明有两个猫"}, session_config)
    # print("第一次执行",res)
    # res = conversation_chain.invoke({"input":"小刚有一个狗"}, session_config)
    # print("第二次执行",res)
    res = conversation_chain.invoke({"input":"总共有几个宠物"}, session_config)
    print("第三次执行",res)