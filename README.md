# 2023 대구를 빛내는 해커톤

* 팀명
    * 죄잇나

* 제출 타입 및 주제
    * S타입 - 사용자 맞춤형 법률 자문 챗봇 서비스

* 프로젝트 한 줄 설명
    * 취약 계층을 위해 LLM 기술과 판례 데이터를 활용한 법률 도우미 챗봇
      
* 프로젝트 활용된 기술
    * Generative AI Studio에서 제공하는 프롬프트 설계를 활용 - 질문에 대한 답변을 해주는 챗봇 역할
  <img src="https://miro.medium.com/v2/resize:fit:1400/1*6GkpsfFHSnlA_S8uGdQLxg.png">
    * PG Vector를 활용 - 데이터를 벡터로 저장 및 쿼리 가능
  <img src="https://supabase.com/images/blog/embeddings/og_pgvector.png">
    * 배포 때 사용한 기술
      
      
* 시연 영상
    * 유튜브 링크
    * 유튜브 영상 설명란에 다음과 같은 규칙을 사용하여 타임스탬프를 작성할 것
          00:00
          00:00
          00:00

# 배포

* front
   * Google Cloud Platform의 Computer Engine에서 VM instance 추가 
   * pip, nginx 및 react 관련 module 다운로드 
   * lawItNa repo의 Front 부분을 build
   * 빌드한 부분을 nginx와의 symbolic link 연결을 통해 배포 
   * instance의 외부 ip를 통한 접속 가능
     
* back

# 로컬 실행 방법

# 참고
## PG Vector Access info
    # 성한
        PROJECT_ID = "valiant-imagery-399603"
        LOCATION = "asia-northeast3"
        instance_connection_name = "valiant-imagery-399603:asia-northeast3:lecturetest"
        db_user = "postgres"
        db_pass = "porsche911gt3"
        db_name = "postgres"

    # 정래
        PROJECT_ID = "esoteric-stream-399606"
        LOCATION = "us-central1"
        instance_connection_name = "esoteric-stream-399606:asia-northeast3:wjdfoek3"
        db_user = "postgres"
        db_pass = "pgvectorwjdfo"
        db_name = "pgvector"
