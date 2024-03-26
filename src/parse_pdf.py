import tempfile
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.utils.constants import PartitionStrategy
from unstructured.cleaners.core import clean, group_broken_paragraphs
from unstructured.chunking.title import chunk_by_title
from unstructured .documents.elements import(
    Header,
    Footer,
    Image,
    CompositeElement,
    Table
)

from tools.vision import vision_completion 


def parse_pdf(filename:str):
    """ 分割并获取元素 """
    elements = partition_pdf(
        filename="file/Aluminium-Sympathetic-Powerful-TSC-5 (3).pdf",
        strategy=PartitionStrategy.HI_RES,
        extract_images_in_pdf=True, 
        extract_image_block_types=["Image","Table"],
        extract_image_block_to_payload=False,
        extract_image_block_output_dir=tempfile.gettempdir()
    )


    """  清洗页头页脚 """
    filtered_elements = [
        element
        for element in elements
        if not (isinstance(element, Header) or isinstance(element, Footer))
    ]

    min_image_width = 250
    min_image_height = 270

    """ 对文本进行清洗，图像转换为描述性文本 """
    for element in filtered_elements:
        # print(element.text)
        if element.text != "":
            element.text = group_broken_paragraphs(element.text)
            element.text = clean(
                element.text,
                bullets=False,
                extra_whitespace=True,
                dashes=False,
                trailing_punctuation=False
            )
        if isinstance(element, Image):
            point1 = element.metadata.coordinates.points[0]
            point2 = element.metadata.coordinates.points[2]
            width = abs(point2[0]-point1[0])
            height = abs(point2[1]-point1[1])
            if width >= min_image_width and height >= min_image_height:
                element.text = vision_completion(element.metadata.image_path)

    """ 进行分块 """
    chunks = chunk_by_title(
        elements=filtered_elements,
        multipage_sections=True,
        combine_text_under_n_chars=0,
        new_after_n_chars=None,
        max_characters=4096,
    )

    text_list = []

    for chunk in chunks:
        if isinstance(chunk, CompositeElement):
            text = chunk.text
            text_list.append(text)
        elif isinstance(chunk, Table): ## 表格转换为html
            if text_list:
                text_list[-1] = text_list[-1] + "\n\n" + chunk.metadata.text_as_html

    ## 获取文本列表
    result_list = []

    for text in text_list:
        split_text = text.split("\n\n", 1)
        if len(split_text) == 2:
            title,body=split_text
            result_list.append({"title": title, "body": body})

    import pandas as pd
    df = pd.DataFrame(result_list)
    df.to_excel("output/result.xlsx", index=True, header=True)

parse_pdf("/")






