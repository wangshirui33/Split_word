# Split_word
split words with 2-gram 

算法说明：

1_	语料库：
人民日报语料库199801(corpus_lib.txt)，并统计出其中出现的单词与词频(corpus.txt)。

2_	测试文件：
计算语言学课程发布的test.txt。

3_	算法流程：

1_	按行读入测试文件，利用标点符号分割，按句子长度10为标准进行分词训练。分词过程如下。
1_	从每个句子中找出所有的候选词。每次取4个字，判断它们每个是否在语料库(corpus.txt)中，如果是的话则存为候选词。并存储下这个词的位置，最后得到此句子中所有的候选词
1_	计算出一个句子所有的切分结果。在候选词集合中，遍历所有开始位置为0但结结束位不为0的候选词，按照词的开始位置和结束位置进行拼凑，长度等于句子长度即为一个切分结果。当遍历结束后，这些元素就是一个句子所有的切分结果。 
使用2-gram模型计算出每种切分结果的概率，选出最大概率的句子切分结果。计算概率时使用条件概率和加一平滑。P(wn/wn-1)利用语料库(corpus_lib.txt)查询计算。
条件概率的公式为：
P(w1,w2,…,wn) = P(w1/start)P(w2/w1)P(w3/w2)…..P(Wn/Wn-1) 
1_)	将每一个切分句子的最大概率切分结果存入结果文件中(result.txt)
