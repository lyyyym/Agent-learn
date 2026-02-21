import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter

# 获取当前脚本的绝对路径，避免路径错误
current_dir = os.path.dirname(os.path.abspath(__file__))
txt_file_path = os.path.join(current_dir, "long_text.txt")

# ==========================================
# 1. TextLoader: 加载整个文件
# ==========================================
print("--- 1. TextLoader 加载 ---")
# encoding="utf-8" 非常重要，防止中文乱码
loader = TextLoader(txt_file_path, encoding="utf-8")
docs = loader.load()

print(f"加载了 {len(docs)} 个文档 (TextLoader 默认把整个文件当成 1 个文档)")
print(f"文档总长度: {len(docs[0].page_content)} 字符")
print("-" * 30)


# ==========================================
# 2. CharacterTextSplitter: 简单字符分割
# ==========================================
print("\n--- 2. CharacterTextSplitter (基于分隔符的简单分割) ---")
# 这种分割器比较死板，它只会在指定的分隔符处切断。
# 如果一段话中间没有分隔符，即使超过 chunk_size 它可能也不会切断（除非强制），或者会切得很难看。

c_splitter = CharacterTextSplitter(
    separator="\n\n", # 仅在双换行处分割
    chunk_size=100,   # 期望每个块 100 字符
    chunk_overlap=20, # 重叠 20 字符
    length_function=len,
    is_separator_regex=False,
)

c_docs = c_splitter.split_documents(docs)
print(f"分割成了 {len(c_docs)} 个块")
for i, doc in enumerate(c_docs):
    print(f"[块 {i+1}] 长度: {len(doc.page_content)}")
    # print(doc.page_content[:50] + "...") # 打印前50个字预览
print("-" * 30)


# ==========================================
# 3. RecursiveCharacterTextSplitter: 递归字符分割 (推荐!)
# ==========================================
print("\n--- 3. RecursiveCharacterTextSplitter (智能递归分割) ---")
# 这是最常用的分割器。它会尝试按顺序使用 ["\n\n", "\n", " ", ""] 进行分割。
# 它的策略是：
# 1. 先试着用 "\n\n" 切，如果切出来的块太小，就合并；如果太大，就进入下一步。
# 2. 再试着用 "\n" 切...
# 3. 这样能最大程度保证段落、句子的完整性。

r_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,   # 每个块约 100 字符
    chunk_overlap=20, # 重叠 20 字符，防止上下文丢失
    separators=["\n\n", "\n", " ", ""] # 默认分隔符列表
)

r_docs = r_splitter.split_documents(docs)
print(f"分割成了 {len(r_docs)} 个块")

# 打印前几个块看看效果
for i, doc in enumerate(r_docs[:3]):
    print(f"\n[块 {i+1}] (长度 {len(doc.page_content)}):")
    print(f"\"{doc.page_content}\"")

print("-" * 30)
