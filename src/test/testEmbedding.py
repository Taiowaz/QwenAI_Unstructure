import dashscope

from http import HTTPStatus

def test_embed(input:str):
    resp = dashscope.TextEmbedding.call(
        model=dashscope.TextEmbedding.Models.text_embedding_v1,
        input=input,
    )
    if resp.status_code == HTTPStatus.OK:
        return resp.output["embeddings"][0]["embedding"];
    else:
        print(resp)

if __name__ == "__main__":
    print(test_embed());