import os
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings

# 1. 准备工作：设置环境
current_dir = os.path.dirname(os.path.abspath(__file__))
txt_file_path = os.path.join(current_dir, "long_text.txt")
persist_directory = os.path.join(current_dir, "chroma_db") # 向量数据库的持久化路径

# 2. 加载文档
print("--- 1. 加载文档 ---")
loader = TextLoader(txt_file_path, encoding="utf-8")
docs = loader.load()
print(f"原始文档长度: {len(docs[0].page_content)}")

# 3. 文本分割
print("\n--- 2. 文本分割 ---")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,    # 块大小
    chunk_overlap=50,  # 重叠
)
chunks = text_splitter.split_documents(docs)
print(f"分割成 {len(chunks)} 个块")

# 4. 初始化 Embedding 模型
# 注意：你需要确保 DASHSCOPE_API_KEY 环境变量已经设置
embeddings = DashScopeEmbeddings()

# 5. 创建/加载 Chroma 向量数据库
print("\n--- 3. 向量化并存储 (这可能需要一点时间) ---")
# from_documents 会做两件事：
# 1. 调用 embeddings 模型把 chunks 变成向量
# 2. 把向量和文本存到 persist_directory 指定的目录中
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=persist_directory, # 指定持久化目录
    collection_name="langchain_intro"    # 集合名称，类似 SQL 的表名
)
# 在旧版 Chroma 中需要手动调用 .persist()，新版通常会自动保存

print(f"成功保存到: {persist_directory}")

# 6. 验证：进行一次相似度检索
print("\n--- 4. 尝试检索 ---")
query = "TextLoader 是什么？"
results = vector_store.similarity_search(query, k=2) # 找最相似的 2 个

for i, doc in enumerate(results):
    print(f"\n[结果 {i+1}] (Source: {doc.metadata.get('source')})")
    print(doc.page_content)
