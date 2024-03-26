from click import prompt
import dashscope
from http import HTTPStatus

from testEmbedding import test_embed

query = "韩德斌是谁?"
""" 对问题向量化 """
resp = dashscope.TextEmbedding.call(
        model=dashscope.TextEmbedding.Models.text_embedding_v1,
        input=query,
    )
if resp.status_code == HTTPStatus.OK:
        query_embedding = resp.output["embeddings"][0]["embedding"];

""" 在向量知识库中找最相关的文本 """
from pinecone import Pinecone
pc = Pinecone()
# 连接远端数据库
index = pc.Index("example-index")
# 获取最相关的文本
resp = index.query(
        vector=query_embedding,
        top_k=5,
        include_metadata=True,
)


relative_texts = []

relative_texts =  [match["metadata"]["text"] for match in resp.matches]


prompt = "请基于此文本：" + "；".join(relative_texts) + "\n回答问题：" + query


""" 结合相关文本生成回答 """

resp = dashscope.Generation.call(
        model = dashscope.Generation.Models.qwen_max,
        prompt = prompt
)
if resp.status_code == HTTPStatus.OK:
    print(resp.output["text"])






