import re
import math


# corpus_library:用于分词的语料
# corpus_dictionary:语料库词频
# 格式：[词语：频率]
corpus_dictionary = {}
corpus_library = ''

# 对待分词的文章预处理,按标点符号进行分割，且分词时保留标点符号
def pre_process(sentences):

    _sentences = sentences.split()
    return _sentences


def init_corpus_library(_path):

    global corpus_library
    with open(_path, 'r', encoding='gbk', errors='ignore') as file:
        corpus_library = str(file.readlines())

# 初始化语料库
def init_corpus_dictionary(path):

    global corpus_dictionary
    split_corpus = []
    with open(path, 'r', encoding='gbk') as corpus_file:
        for corpus_line in corpus_file.readlines():
            corpus_line = corpus_line.strip('\n')
            split_line = corpus_line.split(',')
            split_corpus.append(split_line)

        for each_line in split_corpus:
            corpus_dictionary[each_line[0]] = each_line[1]
    print('show the corpus:' )
    print(corpus_dictionary )

# 获得句子中的所有候选词
def get_candidate_words(sentence):

    global corpus_dictionary
    candidate_words = []

    for begin in range(len(sentence)):
        word = sentence[begin]
        candidate_words.append([word, begin, begin])
        for end in range(1, 4):
            if begin + end < len(sentence):
                word += sentence[begin + end]
                if word in corpus_dictionary:
                    candidate_words.append([word, begin, begin + end])

    return candidate_words


# 获得所有分词结果
def split_sentence(sentence):

    global corpus_dictionary
    candidate_words = get_candidate_words(sentence)

    print(candidate_words)
    count = 0

    for word in candidate_words:
        if count > 1000:
            break
        if word[1] == 0 and word[2] != len(sentence) - 1:
            for word in candidate_words:
                if word[1] == 0 and word[2] != len(sentence) - 1:
                    end = word[2]
                    for later_word in candidate_words:
                        if later_word[1] == end + 1:
                            word_seq = [word[0] + ' ' + later_word[0], word[1], later_word[2]]
                            candidate_words.append(word_seq)
                            count += 1
                    candidate_words.remove(word)


    split_sen = []  # 存储分词结果序列
    for s in candidate_words:
        if s[1] == 0 and s[2] == len(sentence) - 1:
            split_sen.append(s[0])

    return split_sen


'''
# 用于对每种分词的结果计算其句子的概率
# P(w1,w2,...,wn) = P(w1/start)P(w2/w1)P(w3/w2).....P(Wn/Wn-1)
# 加1平滑
def get_probability(sequence):

    global corpus_dictionary

    word_list = sequence.split(' ')
    dic_sum = len(corpus_dictionary)

    probability = 1.0

    # 计算第一个词出现的概率P(start)
    if word_list[0] not in corpus_dictionary:
        count = 0.001
    else:
        count = float(corpus_dictionary.get(word_list[0])) + 0.001
    probability *= count

    # 计算P(w2)P(w3).....P(Wn)
    for i in range(1, len(word_list) - 1):
        if word_list[i] not in corpus_dictionary:
            count = 0.001
        else:
            count = float(corpus_dictionary.get(word_list[i])) + 0.001
        probability  *= count

    return probability

'''



# 用于对每种分词的结果计算其句子的概率
# P(w1,w2,...,wn) = P(w1/start)P(w2/w1)P(w3/w2).....P(Wn/Wn-1)
# 加1平滑
def get_probability(sequence):

    global corpus_dictionary
    global corpus_library

    word_list = sequence.split(' ')
    dic_sum = len(corpus_dictionary)

    probability = 0.0

    # 计算第一个词出现的概率P(start)
    if word_list[0] not in corpus_dictionary:
        count = 1
    else:
        count = float(corpus_dictionary.get(word_list[0])) + 1

    probability += math.log(count / dic_sum)

    # 计算P(w2)P(w3).....P(Wn)
    for i in range(1, len(word_list) - 1):
        if word_list[i] not in corpus_dictionary:
            count = 1
        else:
            count = len(re.findall(r'\s' + word_list[i] + r'\s' + word_list[i+1] + r'\s', corpus_library)) + 1
        probability  += math.log(count / dic_sum)

    return probability



# 求得最大概率分词结果
def get_max_probability(split_sen):
    max_probability = - 9999.99
    max_probability_sentence = ''

    for i in range(len(split_sen)):

        probability = get_probability(split_sen[i])
        print(i)
        print(probability)
        if probability > max_probability:
            max_probability = probability
            max_probability_sentence = split_sen[i]

    return max_probability_sentence


if __name__ == '__main__':

    path = 'corpus.txt'
    init_corpus_dictionary(path)
    _path = 'corpus_lib.txt'
    init_corpus_library(_path)

    sentences = ''
    result = 'result.txt'
    path2 = 'test.txt'


    with open(path2, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            sentences += str(line)

    pattern = r'(,|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）)'
    _sentences = re.split(pattern, sentences)
    result_text = ''

    for sentences1 in _sentences:
        if len(sentences1) == 1:
            result_text += (' '+ sentences1)

        elif len(sentences1) > 10:
             for i in range(0, len(sentences1), 10):

                 each_sentence = sentences1[i:i + 10]

                 split_sen = split_sentence(each_sentence)
                 print(split_sen)
                 print(len(split_sen))
                 max_pro_sen =  get_max_probability((split_sen))
                 print(max_pro_sen)
                 result_text += max_pro_sen

        else:
            split_sen = split_sentence(sentences1)
            print(split_sen)
            print(len(split_sen))
            max_pro_sen = get_max_probability((split_sen))
            print(max_pro_sen)
            result_text += max_pro_sen


    with open(result, 'r+', encoding='gbk') as fileout:
        fileout.write(result_text)

    fileout.close()
    print('finished')



    

