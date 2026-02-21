# 基于streamlit完成WEB网页上传服务
from fileinput import filename
import streamlit as st
from knowledge_base import KnowledgeBaseService


# 添加网页标题
st.title("文件上传服务")



# 文件上传
uploaded_file = st.file_uploader("请上传一个txt文件", 
                                type=["txt"],
                                accept_multiple_files=False) # 表示仅接受一个文件的上传



if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()
  
if uploaded_file is not None:
    # 提取文件信息
    file_name = uploaded_file.name
    file_type = uploaded_file.type
    file_size = uploaded_file.size / 1024  # 转换为KB

    st.subheader("文件信息")
    st.write(f"文件名: {file_name}")
    st.write(f"文件类型: {file_type}")
    st.write(f"文件大小: {file_size:.2f} KB")
    # 读取文件内容

    text = uploaded_file.read().decode("utf-8")
    
    st.session_state["service"].add_document(text, file_name)
    st.success(f"文件 {file_name} 已成功上传并添加到知识库！") 


