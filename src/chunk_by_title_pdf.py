import tempfile                                 # 用于创建临时文件和目录

from tools.vision import vision_completion               #自定义的图像描述函数

from unstructured.partition.auto import partition # 用于分割PDF元素

from unstructured.chunking.title import chunk_by_title
from unstructured.cleaners.core import clean, group_broken_paragraphs
from unstructured.documents.elements import (
    CompositeElement,
    Footer,
    Header,
    Image,
    Table,
)

"""1. 分区, 从PDF中提取元素"""
pdf_name = "file/Aluminium-Sympathetic-Powerful-TSC-5 (3).pdf"

# 从PDF中提取元素
elements = partition(
    filename=pdf_name,                        # 这是要处理的PDF文件的名称
    pdf_extract_images=True,                  # 表示是否从PDF文件中提取图像
    pdf_image_output_dir_path = tempfile.gettempdir(), # 系统临时文件夹 用于存储提取的图像的目录
    skip_infer_table_types=["jpg", "png", "xls", "xlsx"], # 指定了在推断表格类型时要跳过的文件类型
    strategy="hi_res",                        # 用于提取图像的策略,这里代表高分辨率策略 low_res 代表低分辨率策略
)


# 从PDF中提取的元素中删除页眉和页脚
filtered_elements = [
    element
    for element in elements
    if not (isinstance(element, Header) or isinstance(element, Footer))
]


"""2. 元素进行清洗与处理"""
# 设置图像的最小宽度和高度
min_image_width = 250
min_image_height = 270

for element in filtered_elements:
    if element.text != "":
        element.text = group_broken_paragraphs(element.text) # ？？？ 将元素中的文本分组
        element.text = clean(           # 如果元素中含有文本
            element.text,
            bullets=False,              # 表示是否移除文本中的列表符号
            extra_whitespace=True,      # 表示是否移除文本中的额外空格
            dashes=False,               # 表示是否移除文本中的破折号
            trailing_punctuation=False, # 表示是否移除文本中的尾部标点
        )
    elif isinstance(element, Image):    # 如果元素是图像
        # 获取图像的两个对角点的坐标
        point1 = element.metadata.coordinates.points[0]
        point2 = element.metadata.coordinates.points[2]
        # 计算图像的宽度和高度
        width = abs(point2[0] - point1[0])
        height = abs(point2[1] - point1[1])
        # 如果图像的宽度和高度大于最小宽度和高度
        if width >= min_image_width and height >= min_image_height:
            # 获取图像描述文本
            element.text = vision_completion(element.metadata.image_path)


"""3. 将PDF元素进行分块, 保证每块大小一致, 便于后续处理"""

chunks = chunk_by_title(
    elements=filtered_elements, # 这是要处理的PDF元素
    multipage_sections=True,    # 表示是否将多页的部分分成单独的部分
    combine_text_under_n_chars=0, # 表示是否将长度小于等于指定字符数的文本组合在一起
    new_after_n_chars=None,        # 表示是否在指定字符数后创建新的部分
    max_characters=4096,           # 表示每个部分的最大字符数
)


# ？？？
text_list = []
for chunk in chunks:
    if isinstance(chunk, CompositeElement):            # ??? 复合元素指代的是什么
        text = chunk.text
        text_list.append(text)
    elif isinstance(chunk, Table):
        if text_list:                                  # 如果text_list不为空
            text_list[-1] = text_list[-1] + "\n\n" + chunk.metadata.text_as_html #文本与表格联系起来，保证连贯性
        else:
            text_list.append(chunk.metadata.text_as_html)


result_list = []
for text in text_list:
    split_text = text.split("\n\n", 1)         #??? 表格元素进行分割
    if len(split_text) == 2:
        title, body = split_text
        result_list.append({"title": title, "body": body})


import pandas as pd
df = pd.DataFrame(result_list)
print(df)
df.to_excel("output.xlsx", index=True, header=True)
