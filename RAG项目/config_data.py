
md5_path = "C:\\Users\\31949\\Desktop\\agent_learn\\RAG项目\\md5.txt"


# Chroma
collection_name = "rag"
persist_directory = "C:\\Users\\31949\\Desktop\\agent_learn\\RAG项目\\chroma_db"


#spliter
chunk_size = 1000 # 分割后的文本段最大长度
chunk_overlap = 100 # 连续文本段之间的重叠长度
separators = ["\n\n", "\n", " ", ".", "。","?","？","!","！",""]
max_split_char_num = 1000 # 最大分割次数


operator = "agent" # 操作人