# %% 

import requests 
from bs4 import BeautifulSoup
from tqdm import tqdm

# req = requests.get('http://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&query=%EB%A9%98%ED%86%A0%EB%A7%81&queryText=&iStartCount=0&iGroupView=5&icate=all&colName=bib_t&exQuery=&exQueryText=&order=%2FDESC&onHanja=false&strSort=RANK&pageScale=10&orderBy=&fsearchMethod=&isFDetailSearch=&sflag=1&searchQuery=%EB%A9%98%ED%86%A0%EB%A7%81&fsearchSort=&fsearchOrder=&limiterList=&limiterListText=&facetList=&facetListText=&fsearchDB=&resultKeyword=&pageNumber=1&p_year1=&p_year2=&dorg_storage=&mat_type=&mat_subtype=&fulltext_kind=&t_gubun=&learning_type=&language_code=&ccl_code=&language=&inside_outside=&fric_yn=&image_yn=&regnm=&gubun=&kdc=&ttsUseYn=')


# http://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&queryText=&strQuery=%EB%A9%98%ED%86%A0%EB%A7%81&exQuery=&exQueryText=&order=%2FDESC&onHanja=false&strSort=RANK&p_year1=&p_year2=&iStartCount=0&orderBy=&fsearchMethod=search&sflag=1&isFDetailSearch=N&pageNumber=&resultKeyword=&fsearchSort=&fsearchOrder=&limiterList=&limiterListText=&facetList=&facetListText=&fsearchDB=&icate=bib_t&colName=bib_t&pageScale=10&isTab=Y&regnm=&dorg_storage=&language=&language_code=&query=%EB%A9%98%ED%86%A0%EB%A7%81
# http://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&queryText=&strQuery=%EB%A9%98%ED%86%A0%EB%A7%81&exQuery=&exQueryText=&order=%2FDESC&onHanja=false&strSort=RANK&p_year1=&p_year2=&iStartCount=10&orderBy=&fsearchMethod=search&sflag=1&isFDetailSearch=N&pageNumber=&resultKeyword=&fsearchSort=&fsearchOrder=&limiterList=&limiterListText=&facetList=&facetListText=&fsearchDB=&icate=bib_t&colName=bib_t&pageScale=10&isTab=Y&regnm=&dorg_storage=&language=&language_code=&query=%EB%A9%98%ED%86%A0%EB%A7%81
# http://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&queryText=&strQuery=%EB%A9%98%ED%86%A0%EB%A7%81&exQuery=&exQueryText=&order=%2FDESC&onHanja=false&strSort=RANK&p_year1=&p_year2=&iStartCount=20&orderBy=&fsearchMethod=search&sflag=1&isFDetailSearch=N&pageNumber=&resultKeyword=&fsearchSort=&fsearchOrder=&limiterList=&limiterListText=&facetList=&facetListText=&fsearchDB=&icate=bib_t&colName=bib_t&pageScale=10&isTab=Y&regnm=&dorg_storage=&language=&language_code=&query=%EB%A9%98%ED%86%A0%EB%A7%81

texts = '' 
# 1800
for i in tqdm(range(0, 1800, 10)):
    url = 'http://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&queryText=&strQuery=%EB%A9%98%ED%86%A0%EB%A7%81&exQuery=&exQueryText=&order=%2FDESC&onHanja=false&strSort=RANK&p_year1=&p_year2=&iStartCount=' + str(i) + '&orderBy=&fsearchMethod=search&sflag=1&isFDetailSearch=N&pageNumber=&resultKeyword=&fsearchSort=&fsearchOrder=&limiterList=&limiterListText=&facetList=&facetListText=&fsearchDB=&icate=bib_t&colName=bib_t&pageScale=10&isTab=Y&regnm=&dorg_storage=&language=&language_code=&query=%EB%A9%98%ED%86%A0%EB%A7%81'
    req = requests.get(url)
    html = req.text

    soup = BeautifulSoup(html, 'html.parser')
    titles = soup.select('p.title > a')

    for i in range(len(titles)):
        texts += ' ' + titles[i].get_text() + '\n'
# %%
print(texts)



# %% 
## 특수문자 처리
import re

parse_text = texts

clean_lines = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', parse_text)
p = re.compile('[^0-9]')
clean_lines = "".join(p.findall(clean_lines))
# %%

# print(parse_text)
print('------------------------')
print(clean_lines)


# %% stopwords 

f = open('D:/work/paper_ko/datasets/stopwords.txt', mode='r', encoding='utf-8')

lines = f.readlines()

stop_words = ''
for ll in lines:
    # print(ll)
    stop_words += ' ' + ll

# %%
from konlpy.tag import Okt


okt = Okt() 
# results = okt.nouns(clean_lines)

stopwords_results = []

for ll in clean_lines.split('\n'):
    # print(ll)
    stopwords_results.append(okt.nouns(ll))



# %%
print(stopwords_results)


# %%
from gensim.models import FastText

ft_model = FastText(stopwords_results, size=100, window=5, min_count=5, workers=4, sg=1)

# %%
print(ft_model.wv.most_similar('혁신', topn=10))
# print(ft_model.wv.similarity('멘토링', '창업'))
# %%
