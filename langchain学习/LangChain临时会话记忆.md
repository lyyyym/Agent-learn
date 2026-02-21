## [LangChain 临时会话记忆 (In-Memory Session History)]

### 📌 概述
- **定义**：将用户的聊天记录暂时存储在**运行内存 (RAM)** 中，使 AI 在多轮对话中能够“记住”上下文。
- **生命周期**：**程序运行期间有效**。一旦程序关闭或重启，记忆就会消失。
- **核心组件**：
    - `InMemoryChatMessageHistory`: 实际存储消息列表的对象。
    - `RunnableWithMessageHistory`: 自动管理历史记录读写的 Chain 包装器。
- **适用场景**：
    - 开发调试 (Debug)
    - 简单的命令行聊天工具
    - 短期的临时对话任务

### 🔑 核心概念
| 术语 | 解释 | 代码对应 |
| :--- | :--- | :--- |
| **History Store** | 全局字典，用于存放所有用户的聊天记录对象。 | `store = {}` |
| **Session ID** | 会话的唯一身份证。用来区分不同用户（如 "user_001" vs "user_002"）。 | `session_id="user_001"` |
| **Get History** | 一个工厂函数。负责根据 Session ID 创建或获取对应的历史记录对象。 | `def get_history(session_id): ...` |
| **Configurable** | 运行时动态传参的机制。告诉 Chain 当前是谁在说话。 | `config={"configurable": {"session_id": "..."}}` |

### 📖 详细讲解

#### 工作原理：字典映射
LangChain 使用一个简单的 Python 字典 `store` 来管理所有会话：
- **Key**: `session_id` (字符串)
- **Value**: `InMemoryChatMessageHistory` 对象 (包含一个 `messages` 列表)

```python
store = {
    "user_001": InMemoryChatMessageHistory(messages=[...]),
    "user_002": InMemoryChatMessageHistory(messages=[...])
}
```

#### 流程图解
1.  **Invoke**: 用户调用 Chain，传入 `input` 和 `session_id`。
2.  **Get History**: `RunnableWithMessageHistory` 调用 `get_history(session_id)`。
3.  **Check Store**:
    *   **有记录**: 直接从 `store` 返回旧的 `History` 对象。
    *   **无记录**: 创建新的 `InMemoryChatMessageHistory`，存入 `store`，并返回。
4.  **Inject Prompt**: 将获取到的历史消息填充到 Prompt 的 `{chat_history}` 占位符中。
5.  **Model Run**: 模型基于“历史 + 当前问题”生成回答。
6.  **Save History**: 将“用户问题”和“AI 回答”追加到 `History` 对象中。

### 💻 代码示例

```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.output_parsers import StrOutputParser

# 1. 准备基础组件
model = ChatTongyi(model="qwen3-max")
# 注意：必须包含一个 {chat_history} 占位符
prompt = PromptTemplate.from_template(
    "对话历史:{chat_history}, 用户提问:{input}, 请回答"
)
base_chain = prompt | model | StrOutputParser()

# 2. 定义仓库 (Store) 和 管理员 (Factory Function)
store = {} 

def get_history(session_id: str):
    if session_id not in store:
        # 新用户：发新本子
        store[session_id] = InMemoryChatMessageHistory()
    # 老用户：给旧本子
    return store[session_id]

# 3. 包装 Chain (增强记忆功能)
conversation_chain = RunnableWithMessageHistory(
    base_chain,       # 原来的逻辑
    get_history,      # 管理员函数
    input_messages_key="input",        # 用户输入的变量名
    history_messages_key="chat_history" # 历史记录插到哪个变量里
)

# 4. 调用 (带着 Session ID)
config = {"configurable": {"session_id": "user_001"}}

# 第一轮：Store 为空 -> 创建新历史 -> 记录 "小明有两只猫"
conversation_chain.invoke({"input": "小明有两只猫"}, config)

# 第二轮：Store 有 user_001 -> 读取旧历史 -> AI 知道小明有猫
conversation_chain.invoke({"input": "他有几只猫？"}, config)
```

### ⚠️ 常见问题与避坑
1.  **Prompt 占位符缺失**：如果 Prompt 中没有 `{chat_history}`（或者你在 `history_messages_key` 指定的其他名字），程序会报错，因为它不知道把历史插在哪里。
2.  **内存爆炸**：因为所有记录都在内存里，如果用户量大或者对话极长，服务器内存会爆。**仅限测试使用！**
3.  **重启丢失**：服务器重启后，`store` 字典会被清空，所有人的记忆都没了。
4.  **Session ID 必须传**：如果不传 `config`，它不知道该存到哪，每次都会当成新对话。

### ✅ 小结
- **临时记忆 = 字典 (Store) + 对象 (History)**。
- 记住核心三要素：**Store (仓库)**、**Session ID (身份证)**、**Config (通行证)**。
- 它是理解 LangChain 记忆机制的基石，学会了它，切换到 Redis/Postgres 持久化记忆只需要改一行代码（把 `InMemoryChatMessageHistory` 换成 `RedisChatMessageHistory`）。
