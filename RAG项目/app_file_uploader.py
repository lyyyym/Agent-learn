# 基于streamlit完成WEB网页上传服务
from fileinput import filename
import streamlit as st

# 添加网页标题
st.title("文件上传服务")

# 文件上传
uploaded_file = st.file_uploader("请上传一个txt文件", 
                                type=["txt"],
                                accept_multiple_files=False) # 表示仅接受一个文件的上传
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
    file_content = uploaded_file.read().decode("utf-8")
    # 显示文件内容
    st.text_area("文件内容预览", file_content, height=300)

