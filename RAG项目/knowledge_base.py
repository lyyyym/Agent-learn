
from importlib import metadata
import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime


"""
知识库
"""
def check_md5(md5_str:str):
    """
    检查文件的MD5值是否已经被处理过
    Flase:未处理，True:已处理
    """
    if not os.path.exists(config.md5_path):
        # if进入表示文件不存在，那肯定没有处理这个md5值了
        open(config.md5_path, "w", encoding="utf-8").close() # 创建该文件
        return False
    else:
        for line in open(config.md5_path,'r',encoding='utf-8').readlines():
            line = line.strip() #处理字符串前后的空格和回车
            if line == md5_str:
                return True
        return False

    
def save_md5(md5_str:str):
    """
    保存文件的MD5值到数据库
    """
    with open(config.md5_path, "a", encoding="utf-8") as f:
        f.write(md5_str + "\n")



def get_string_md5(input_str:str, encoding:str="utf-8"):
    """将传入的字符串转为md5字符串"""
    # 将字符串转换为二进制
    input_bytes = input_str.encode(encoding)

    # 计算MD5值
    md5_hash = hashlib.md5()
    md5_hash.update(input_bytes) # 更新内容，传入即将要转换的字节数组
    md5_str = md5_hash.hexdigest() # 得到md5的十六进制字符串

    return md5_str 


class KnowledgeBaseService(object):
    """知识库服务类"""
    def __init__(self):
        # 如果文件夹不存在则创建否则跳过
        os.makedirs(config.persist_directory, exist_ok=True) # 确保目录存在
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory, # 数据库本地存储文件夹
        ) # 向量存储的实例 Chroma数据库
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,  # 分割后的文本段最大长度
            chunk_overlap=config.chunk_overlap, # 连续文本段之间的重叠长度
            separators=config.separators, # 文本分割时使用的分隔符列表
            length_function=len, # 用于计算文本长度的函数
        ) # 文本分割器的对象
    
    def upload_by_str(self, data, filename):
        """
        上传字符串进行向量化，存入向量数据库
        """
        md5_str = get_string_md5(data)
        if check_md5(md5_str):
            print("该字符串的MD5值已经被处理过，无需重复处理")
            return
        
        # 对字符串进行分割
        if len(data) > config.max_split_char_num:
            knowledge_chunks: list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]
        
        metadata = {
            "source": filename,
            "create_time": datatime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": config.operator,
        }

        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for _ in range(len(knowledge_chunks))],
        )



        save_md5(md5_str)
        return "success"

if __name__ == "__main__":
    kb_service = KnowledgeBaseService()
    kb_service.upload_by_str("你好", "persist_directory")