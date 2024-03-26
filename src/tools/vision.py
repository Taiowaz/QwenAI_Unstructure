import dashscope
dashscope.api_key="sk-f14f6af73bb24bbebb5b1525cc93027b"

# 导入通义千问VL模型，用于图像识别
from dashscope import MultiModalConversation



def vision_completion(image_path: str) -> str:     # image_path: str这种语法被称为类型注解（Type Annotation）。
    messages = [                                   # image_path是变量名，str是该变量的预期类型，即字符串。                            
        {
            "role": "user",
            "content": [
                {
                    "image": "file://"+image_path
                    },
                {
                    "text":"What is in this image? Only return neat facts in English."
                }
            ]
        }
    ]
    response = MultiModalConversation.call(model="qwen-vl-plus",
                                           messages=messages,
                                           max_tokens=1024) 
    print(response)
    return response.output.choices[0].message.content[0]["text"]; # 返回识别结果


