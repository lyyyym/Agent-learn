from typing import List

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableWithMessageHistory

import config_data as config
from file_history_store import get_history
from vector_stores import VectorStoreService


def print_prompt(prompt):
    """打印提示模板"""
    print("=" * 20)
    print(prompt.to_string())
    print("=" * 20)
    return prompt


class RagService(object):
    def __init__(self):
        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model),
        )
        # Tongyi 只允许最多一条 system message
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "以我提供的参考资料为主，简洁且专业地回答用户问题。"
                    "\n参考资料如下：\n{context}"
                    "\n请结合下面的历史对话保持上下文一致。",
                ),
                MessagesPlaceholder("history"),
                ("user", "请回答用户提问：{input}"),
            ]
        )
        self.chat_model = ChatTongyi(model=config.chat_model)
        self.chain = self._get_chain()

    def _get_chain(self):
        """内部方法，用于获取 RAG 链"""
        retriever = self.vector_service.get_retriever()

        def format_document(docs: List[Document]):
            if not docs:
                return "没有相关文档。"

            formatted_str = ""
            for doc in docs:
                formatted_str += (
                    f"文档片段: {doc.page_content}\n"
                    f"文档元数据: {doc.metadata}\n\n"
                )
            return formatted_str

        def pick_user_input(value: dict) -> str:
            return value["input"]

        def build_prompt_input(value):
            return {
                "input": value["input"]["input"],
                "context": value["context"],
                "history": value["input"]["history"],
            }

        chain = (
            {
                "input": RunnablePassthrough(),
                "context": RunnableLambda(pick_user_input) | retriever | format_document,
            }
            | RunnableLambda(build_prompt_input)
            | self.prompt_template
            | print_prompt
            | self.chat_model
            | StrOutputParser()
        )

        return RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )


if __name__ == "__main__":
    session_config = {"configurable": {"session_id": "user_001"}}
    service = RagService()
    result = service.chain.invoke({"input": "春天穿什么衣服？"}, session_config)
    print(result)
