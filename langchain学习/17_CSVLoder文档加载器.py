from langchain_community.document_loaders.csv_loader import CSVLoader

import os

# 获取当前脚本的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 拼接 csv 文件的绝对路径
csv_file_path = os.path.join(current_dir, "data.csv")

# ==========================================
# 1. 基础用法：加载所有列
# ==========================================
print("--- 1. 基础加载 (每一行作为一个 Document) ---")

# file_path: CSV 文件的路径
loader = CSVLoader(file_path=csv_file_path)
docs = loader.load()

# 查看结果
print(f"加载了 {len(docs)} 个文档。")
print(f"第一个文档内容:\n{docs[0].page_content}")
print(f"第一个文档元数据:\n{docs[0].metadata}")
print("-" * 30)


# ==========================================
# 2. 进阶用法：指定列作为 content
# ==========================================
print("\n--- 2. 指定 content 列 (source_column) ---")
# 默认情况下，CSVLoader 会把所有列拼接成 page_content。
# 如果你只想用某一列作为主要内容（例如 'description'），可以使用 source_column 参数。
# 这样 metadata 中会保留 source 信息，便于溯源。

loader_specific = CSVLoader(
    file_path=csv_file_path,
    source_column="description" # 指定这一列为主要内容
)

docs_specific = loader_specific.load()

print(f"第一个文档内容 (只包含 description):\n{docs_specific[0].page_content}")
print(f"第一个文档元数据:\n{docs_specific[0].metadata}")
print("-" * 30)


# ==========================================
# 3. 进阶用法：自定义 CSV 解析参数 (csv_args)
# ==========================================
print("\n--- 3. 自定义解析参数 (例如修改分隔符) ---")
# 有时候 CSV 文件不是逗号分隔，或者是其他特殊格式，可以传递 csv_args
# 这些参数会直接传给 Python 内置的 csv.DictReader

loader_custom = CSVLoader(
    file_path=csv_file_path,
    csv_args={
        "delimiter": ",",      # 分隔符
        "quotechar": '"',      # 引号字符
        "fieldnames": ["姓名", "部门", "薪资", "描述"] # 重命名列名 (如果文件没有表头，或者想覆盖表头)
    }
)

# 注意：如果指定了 fieldnames 且文件本身有表头，表头会被当成第一行数据读出来
# 这里为了演示，我们假设它会读取所有行
docs_custom = loader_custom.load()

# 因为重命名了列，所以第一行（原本的表头）现在变成了数据
print(f"读取到的第一条数据 (原表头):\n{docs_custom[0].page_content}")
# print(docs_custom)
# 懒加载， .lazy_load(),迭代器[document]
for doc in loader_custom.lazy_load():
    print(doc.page_content)
    print(f"元数据 (metadata): {doc.metadata}")  # 包含数据源路径、行号等元信息
    print(f"内容 (page_content): {doc.page_content}")  # 实际的文本内容，即 CSV 行转换后的字符串
    print(f"类型 (type): {doc.type}")  # 对象的类型，通常为 'Document'
    print("-" * 30)
