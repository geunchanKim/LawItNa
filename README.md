# 2023 대구를 빛내는 해커톤

* 팀명
    * 죄잇나

* 제출 타입 및 주제
    * S타입 - 사용자 맞춤형 법률 자문 챗봇 서비스

* 프로젝트 한 줄 설명
    * 취약 계층을 위해 LLM 기술과 판례 데이터를 활용한 법률 도우미 챗봇

* 프로젝트 활용된 기술
    <!-- * Generative AI Studio에서 제공하는 프롬프트 설계를 활용 - 질문에 대한 답변을 해주는 챗봇 역할 -->
    * Google Cloud Vertexai에서 제공하는 Chatmodel을 가져와 사용했다.
    Chat model을 사용할 땐, prompt engineering 기법을 이용해 우리가 제공하려는 서비스의 취지에 맞게 context를 설정했다.
    context를 설정할 땐, Chat model의 답변의 다양성을 위해 hyper parameter 중 temperature는 0.3으로 설정했고, top-k는 10개로 한정했다.
    Chat model에 history 기능을 추가해서, chatbot이 사용자의 이전 질문들과 그에 대한 자신의 답변을 기억할 수 있도록 했다.
  <img src="https://miro.medium.com/v2/resize:fit:1400/1*6GkpsfFHSnlA_S8uGdQLxg.png"><br>
    * PG Vector를 활용 - 데이터를 벡터로 저장 및 쿼리 가능
    Google Cloud SQL에서 제공하는 PostgreSQL의 pgvector를 이용해 VectorDB를 구현했다.
    VectorDB의 경우, 일반 DB와 같은 형태인데 vector 값도 저장할 수 있는 DB로 벡터끼리의 유사도를 계산할 수 있는 기능을 제공한다.
    데이터셋은 81년도부터 현재까지 민사소송과 관련된 판례들을 담았고, 원고의 주장과 피고의 주장을 합쳐서 벡터화 시켜 저장했다.
    해당 데이터셋의 출처는 [AI Hub의 법률/규정 (판결서, 약관 등) 텍스트 분석 데이터셋](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=580)이다.
    DB에 질의를 할 땐, 사용자의 질문을 벡터화해서 원고의 주장, 피고의 주장과 Cosine Distance가 가장 짧은 3개의 데이터들만을 가져왔는데,
    3개의 데이터만 가져온 이유는 Chat model의 input token 범위 제한때문에 그렇다.
    데이터들은 판례명, 원고, 피고의 주장, 판례와 관련된 법률명, 판례 내용, 판례 결과로 이루어져 있다.
    이 데이터들은 Chat model의 context에 입력되어 Chat model이 이 데이터들을 사용자의 질문에 답변할 때 활용한다.
  <img src="https://supabase.com/images/blog/embeddings/og_pgvector.png"><br>
    * [배포 때 사용한 기술](#배포) 참조

* 시연 영상
    * [유튜브 링크](https://youtu.be/zst59_EFqmA)

# 배포

* front
   * Google Cloud Platform의 Computer Engine에서 VM instance 추가
   * pip, nginx 및 react 관련 module 다운로드 
   * lawItNa repo의 Front 부분을 build
   * 빌드한 부분을 nginx와의 symbolic link 연결을 통해 배포 
   * instance의 외부 ip를 통한 접속 가능
     
* back
   * Google Cloud Platform의 Computer Engine에서 VM instance 추가
   * VM instance
        * name: lawitna-instance
        * id: 4954201756402566821
        * region: asia-northeast3 (seoul)
        * external ip: 34.22.68.208
        * web browser ssh 콘솔로 제어
   * pip, flask, flask_cors 등 기본 환경 및 flask 실행에 필요한 module 다운로드
   * google-ai-platform, pg8000 등 google generatiive ai, pg vector api 사용을 위한 module 다운로드
   * instance내에 backend repository git-clone
   * VM instance내에서 run.py 실행
   * instance의 외부 ip를 통한 접속 가능

* [배포 링크](http://www.lawitna.kro.kr/) 

# 로컬 실행 방법

0. 사전 준비
* 로컬에 가져오기
~~~
git clone https://github.com/mouse4432/LawItNa.git
~~~

* version
~~~
python --version #python 3.10.12 이상
pip --version #pip 22.0.2 이상
npm -v #npm 10.1.0 이상
node -v #node 20.8.1 이상
~~~

* requirements.txt 다운로드
~~~
pip install -r requirements.txt
~~~

* pytorch 다운로드
~~~
https://pytorch.org/get-started/locally
본인 환경에 맞게 설정 후 다운로드 코드 사용해서 pytorch 다운
~~~

1. Back 실행
* 터미널을 Back으로 설정
~~~
python run.py | python3 run.py #본인 환경에 맞는 python 명령어 실행
~~~

2. Front 실행
* 터미널을 Front으로 설정
~~~
npm update
npm start run
~~~
