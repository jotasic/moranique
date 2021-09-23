# moranique
## 모라니크 백엔드 과제

### 아래 2가지의 API를 설계 및 구현

1. 블로그 게시물 조회
    - url: `api/blogs`
2. 블로그 게시물 작성
    - url: `api/blog/create`

### 필수 조건

1. Django Rest Framework 를 통한 API 설계 및 구현
2. AWS 를 통한 서버 배포

### 우대 사항

1. pythonic 한 코드
2. Django/DRF 표준에 맞는 코드
3. 테스트 코드
4. AWS 제품 선택 사유 및 다른 대안 제시
5. 실제 운영환경에서 겪을 수 있는 문제를 해결하기 위한 방안 제시
6. 협업을 고려한 코드

## File Structure
```bash
├── Docker-compose-dev.yml
├── Dockerfile-dev
├── Dockerfile-prod
├── README.md
├── api
│   ├── __init__.py
│   ├── blogs
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── urls.py
│   └── users
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── migrations
│       ├── models.py
│       ├── serializers.py
│       ├── tests.py
│       └── views.py
├── manage.py
├── moranique
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   └── wsgi.py
├── requirements.txt
└── utils
    ├── __init__.py
    ├── apps.py
    └── management
        ├── __init__.py
        └── commands
            ├── __init__.py
            └── wait_for_db.py
```

## Modeling
[모델링-erdcloud](https://www.erdcloud.com/d/esZSo9NXQ5cEagrws)

<img width="1428" alt="스크린샷 2021-09-18 오후 8 55 32" src="https://user-images.githubusercontent.com/8219812/134524640-a7760706-c6d1-4d22-b3b4-1c076be09acf.png">


## API

[Detail-PostMan](https://www.postman.com/wecode-21-1st-kaka0/workspace/moranique/collection/16042359-3e1f330b-46b0-436b-ad7e-a8dbfe0d54ab?ctx=documentation)

|Web API             |URL                      |method  | 비고|
|--------------------|-------------------------|--------|-----|
|토큰발행            |/api/user/token/         | post    |-    |
|토큰갱신            |/api/user/token/refresh/ | post    | -
|회원가입            |/api/user/registration/  | post    |-|
|Blog Post 조회      |/api/blogs               | get    | filter, pagination|
|Blog Post 상세정보  |/api/blogs/\<id>         | get    |-|
|Blog Post 생성      |/api/blog/create         | post   |-|




## 개발환경 구축 방법

1. Github Clone
```bash
git clone https://github.com/jotasic/moranique.git
```

2. manage.py 가 있는 폴더로 이동 후, docker-compose 설정 파일인 .dockerenv.dev 생성
```bash
DJANGO_SECRECT_KEY=[DJANGO SECRECT KEY 입력]
AWS_ACCESS_KEY_ID=[AWS ACCESS KEY ID 입력]
AWS_SECRET_ACCESS_KEY=[AWS SECRET ACCESS KEY 입력]
AWS_REGION=[S3가 있는 REGION 이름 입력]
AWS_STORAGE_BUCKET_NAME=[S3를 만들 시 입력한 BUCKET NAME 입력]
```
위에 기제된 입력란에 입력되는 값들은 외따음표를 붙여야 된다.

```
ex)
AWS_REGION='us-east-2' // Ok
AWS_REGION="us-east-2" // No
```

> AWS S3 관련 설정은 아래 블로그를 참조해서 생성 밎 입력한다. 
> https://nachwon.github.io/django-deploy-7-s3/


3.  docker-compose up 실행
```bash
$ docker-compose up -f ./Docker-compose-dev.yml up
```

## 배포 방법
1. Github Clone
```bash
git clone https://github.com/jotasic/moranique.git
```

2. docker image 생성
```bash
docker build --build-arg ARG_DJANGO_SECRECT_KEY=[DJANGO SECRECT KEY 입력]  --build-arg ARG_SQL_HOST=[Database 주소 입력] --build-arg ARG_SQL_PORT=[Database port 번호] --build-arg ARG_SQL_DATABASE=[database 이름] --build-arg ARG_SQL_USER=[database user 이름] --build-arg ARG_SQL_PASSWORD=[database 비밀번호] --build-arg ARG_AWS_ACCESS_KEY_ID=[AWS ACCESS KEY ID 입력] --build-arg ARG_AWS_SECRET_ACCESS_KEY=[AWS SECRET ACCESS KEY 입력] --build-arg ARG_AWS_REGION=[S3가 있는 REGION 이름 입력] --build-arg ARG_AWS_STORAGE_BUCKET_NAME=[S3를 만들 시 입력한 BUCKET NAME 입력] --no-cache -t [docker image명 입력] -f Dockerfile-prod .
```
위에 기제된 입력란에 입력되는 값들은 외따음표를 붙여야 된다.

```
ex)
ARG_AWS_REGION='us-east-2' // Ok
ARG_AWS_REGION="us-east-2" // No
```


3. docker hub에 생성한 image push
```bash
docker push  [docker image명 입력]
```

4. 서버로 이동 후 만든 docker 이미지 pull
```bash
docker pull  [docker image명 입력]
```

5. docker image를 이용해서 컨테이너 생성
```bash
docker run -d --rm -p 8000:8000 --name moranique [docker image명 입력]
```
