from langchain_chroma import Chroma
import config_data as config

class VectorStoreService(object):
    def __init__(self, embedding):
         # 嵌入模型的传入
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory,
        )
    
    def get_retriever(self):
        """

        返回向量检索器，方便加入chain
        search_type: 检索类型，默认相似度检索
        k: 返回的文档数量，默认4个
        """
        return self.vector_store.as_retriever(
            search_kwargs={"k": config.similarity_threshold},
        )

if __name__ == "__main__":
    from langchain_community.embeddings import DashScopeEmbeddings
    embedding = DashScopeEmbeddings(model="text-embedding-v4")
    service = VectorStoreService(embedding)
    retriever = service.get_retriever()
    results = retriever.invoke("我的体重为180斤，提供尺码推荐")
    print(results)
    


    # print(retriever)