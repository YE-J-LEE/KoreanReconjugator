# Subject

입력받은 한국어 문장에 대해 여러 가지 옵션에 따라 다양한 문장으로 변환해주는 연구입니다.  
ex) 평서문 -> 의문문, 의문문 -> 평서문, 평서문 -> 제안문

# Members

- 2015104203 컴퓨터공학과 이예준
- 2015104174 컴퓨터공학과 박기홍

# Prerequiste

- [fastText for pretraining](https://radimrehurek.com/gensim/models/fasttext.html)
- [Korean Morpheme analyzer](https://github.com/kakao/khaiii)
- [Rule-based morpheme reconstructor](https://github.com/YE-J-LEE/KoreanReconjugator/blob/master/code/morphemeMerger.py)
- Corpus: [AI-hub](https://www.aihub.or.kr/aidata/87), [KAIST](http://semanticweb.kaist.ac.kr/home/index.php/KAIST_Corpus)
- Sequence to sequence model

# Keyword

- Preprocessing : Encoder와 Decoder에 들어갈 input, output corpus pair들은 본 프로젝트 연계 산업체인 미리내에서 지원을 받은 corpus를 가지치기로 재조합하여 만들었다. 일반적으로 (입력 문장) + (Tense or conjugation option) -> (출력 문장) 형태로 이루어져 있다.

- Training : 학습 모델은 원초적인 형태로 Sequence to sequence model을 채택했으며 아래 그림과 같이 Encoder와 Decoder에 넣어 학습을 진행했다. 이때 OOV(OutofVocabulary)에 대응하기 위해 각 형태소들은 gensim의 fastText로 pre-training시켰다.
  ![example](https://user-images.githubusercontent.com/51117133/130418474-48c38361-d21f-4531-a07e-37e8901e6b13.png)

- Clean output : 학습 이후 모델에 문장을 입력시키고 나오는 결과값은 Decoder를 보다시피 완성형이 아닌 형태소로만 이루어진 문장이 나온다. 또한 아래 그림처럼 형태소들을 그저 str+= 같은 연산으로 합하는 것이 아니고 중간 모음이 다른 모음으로 교체되고 받침은 탈락되어야 하는 경우가 있다. 이를 위해 Decoder로 나온 형태소들을 [다시 재조합하는 기능](https://github.com/YE-J-LEE/KoreanReconjugator/blob/master/code/morphemeMerger.py)을 추가적으로 개발했다.
  ![example](https://user-images.githubusercontent.com/51117133/130420509-468f14c0-0e86-4235-b645-43536677885e.png)

# Architecture

## Training

![training](https://user-images.githubusercontent.com/51117133/130421211-1556dd36-064c-4de0-b058-da3b40cfdc1f.png)

## Work flow

![flow](https://user-images.githubusercontent.com/51117133/130421453-4df2b8cc-3f57-4a6a-8cdb-c8c89a1b82da.png)

# Result

## Attention visulization

![visualize](https://user-images.githubusercontent.com/51117133/130421759-90d772b6-dba8-4060-92ae-1acbe91d0f03.png)

## Demo

![demo](https://user-images.githubusercontent.com/51117133/130421799-ca2a3925-e529-4550-afdc-8c6121de802e.png)
