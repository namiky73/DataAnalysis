import sys
import MeCab
import TermExtract.MeCab
import TermExtract.Core
import sqlite3

# MeCabの実行とその結果のパース
# 参考: http://qiita.com/Salinger/items/529a77f2ceeb39998665
def mecab_parse(text):
    tagger = MeCab.Tagger("-Ochasen")
    node = tagger.parseToNode(text)
    words = {}
    nouns = {}
    verbs = {}
    adjs = {}
    while node:
        pos = node.feature.split(",")[0]
        word = node.surface
        if pos == "名詞":
            if word in nouns:
                nouns[word] = nouns[word] + 1
            else:
                nouns[word] = 1
        elif pos == "動詞":
            if word in verbs:
                verbs[word] = verbs[word] + 1
            else:
                verbs[word] = 1
        elif pos == "形容詞":
            if word in adjs:
                adjs[word] = adjs[word] + 1
            else:
                adjs[word] = 1

        if word in words:
            words[word] = words[word] + 1
        else:
            words[word] = 1

        node = node.next

    parsed_words_dict = {
        "all": words,
        "nouns": nouns,
        "verbs": verbs,
        "adjs": adjs
    }
    return parsed_words_dict


def term_extract(text):
    tagger = MeCab.Tagger('')
    mecab_result = tagger.parse(all_sentence)

    # 参考: http://gensen.dl.itc.u-tokyo.ac.jp/pytermextract/mecab.html
    cmp_nouns = TermExtract.MeCab.cmp_noun_dict(mecab_result)
    return cmp_nouns



if __name__ == '__main__':
    con = sqlite3.connect("./data_db/textream.sqlite3",timeout=30.0)
    rows = con.execute('select content from comments')

    all_sentence = ""
    for row in rows:
        all_sentence += row[0]

    parsed_words_dict = mecab_parse(all_sentence)
    words = parsed_words_dict["all"]
    for k, v in sorted(words.items(), key=lambda x:x[1]):
        print(k, v)

    # 複合語の語間に空白文字があることに注意
    cmp_nouns = term_extract(all_sentence)
    for k, v in sorted(cmp_nouns.items(), key=lambda x:x[1]):
        print(k, v)
