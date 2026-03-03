import streamlit as st
import time

from rag import RagService
import config_data as config   

st.title("智能客服")
st.divider()  # 添加分割线


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "你好！我是智能客服，有什么我可以帮助你的吗？"}]  # 初始化消息列表

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()  # 初始化RAG服务


for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])  # 显示历史消息



# 用户输入
prompt = st.chat_input()

if prompt:
    # 显示用户输入
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})  # 将用户消息添加到会话状态中

    ai_res_list = []

    with st.spinner("智能客服正在生成回复..."):


        res_stream = st.session_state["rag"].chain.stream(
            {"input": prompt},
            config.session_config,
        )
        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk
        # 显示生成回复的提示
        st.chat_message("assistant").write_stream(capture(res_stream, ai_res_list))
        st.session_state["messages"].append({"role": "assistant", "content": "".join(ai_res_list)})  # 将AI回复添加到会话状态中


