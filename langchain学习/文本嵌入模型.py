from langchain_community.embeddings import DashScopeEmbeddings

embed = DashScopeEmbeddings()

print(embed.embed_query("hello world"))
print(embed.embed_documents(["hello world", "hello dashscope"]))