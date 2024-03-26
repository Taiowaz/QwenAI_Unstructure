import http
import dashscope

response = dashscope.Generation.call(
    model = dashscope.Generation.Models.qwen_max,
    messages=[
        {
            "role" : "user",
            "content" : "韩德斌是谁？"
        }
    ]
)
if response.status_code == http.HTTPStatus.OK:
    print(response.output["text"])