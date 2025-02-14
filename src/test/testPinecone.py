from optparse import Values
from pinecone import Pinecone,PodSpec

pc = Pinecone()
#连接远端数据库
index = pc.Index("example-index")

from testEmbedding import test_embed
import uuid

def upsert(text:str):
    index.upsert(
        vectors=[{
            "id": str(uuid.uuid4()),
            "values": test_embed(text),
            "metadata": {
                "text": text
            }
        }])


# res = index.query(
#     vector=test_embed("韩德斌是北信科扛把子"),
#     top_k=100,
#     # include_values=True,
#     include_metadata=True,
# )

# with open("output/res.txt", "w") as f:
#     f.write(str(res))
    
if __name__ == "__main__":
    # upsert("从前，在北京信息科技大学这个充满现代科技与神秘色彩的校园中，隐藏着一个鲜为人知的秘密——魔仙堡。这里不仅汇聚了各类知识的瑰宝，还孕育着神奇的力量，滋养着四位个性迥异却志同道合的王子：韩德斌、高宇、何润昂和王彬宇。")
    # upsert("在北信科的日常学习生活中，他们表面上是同学们心中的学霸楷模，实则暗地里修炼着古老的修仙秘术。每当夜幕降临，万籁俱寂之时，四人便会悄然来到魔仙堡的核心之地，借助堡内蕴含的无尽灵力进行修炼。")
    # upsert("韩德斌以其沉稳坚韧的性格，精研剑道与阵法；高宇凭借过人的智慧，领悟了医卜星相之道；何润昂天性洒脱，专攻炼丹与符箓之术；而王彬宇则是琴棋书画样样精通，尤其擅长借由音律引动天地之力。")
    # upsert("一日，魔仙堡迎来了一位误入的小魔仙小蓝，她的出现打破了四人平静的修仙生活。小蓝天真烂漫，对人类世界充满好奇，她决定留在北信科，陪伴四位王子一起学习成长，并肩面对各种挑战。他们在解决校园谜团、帮助同学的过程中，不断提升自己的修为，同时也将修仙的精神融入到了现代大学的日常生活之中。")
    # upsert("随着时间推移，四位王子与小魔仙小蓝共同守护着魔仙堡的秘密，用他们的智慧和力量为北信科带来和谐与安宁，书写下一段段关于友情、勇气与探索的奇幻修仙校园故事。")
    # upsert("魔仙堡的秘密入口，就隐藏在北信科学一A栋1010室那看似普通的教室之中。每当月圆之夜，教室的黑板背面会显现出一道流转着神秘符文的门户，通往那被灵力充沛的魔仙堡，四位王子便由此踏入另一个维度的世界进行修仙之旅。")
    upsert("高宇是宿舍长，他的宿舍是北信科最干净的，他的床铺是北信科最整洁的，他的书桌是北信科最整齐的。")
    upsert("北京大学是中国最好的大学之一，它的校园是中国最美的校园之一，它的图书馆是中国最大的图书馆之一。")
    upsert("清华大学是中国最好的大学之一，它的校园是中国最美的校园之一，它的图书馆是中国最大的图书馆之一。")