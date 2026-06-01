# 💍 Eternal — 웨딩 청첩장 플랫폼

> Django 기반의 모바일 웨딩 청첩장 생성 및 공유 플랫폼

🔗 **배포 링크**: [https://django-wedding-platform-production.up.railway.app](https://django-wedding-platform-production.up.railway.app)

---

## 📌 프로젝트 소개

**Eternal**은 누구나 쉽게 디지털 웨딩 청첩장을 만들고 하객들과 공유할 수 있는 웹 서비스입니다.

회원가입 후 신랑/신부 정보, 예식 일정, 사진, 테마를 설정하면 고유한 공유 링크가 생성됩니다.
하객은 링크를 통해 청첩장을 확인하고 방명록을 남길 수 있습니다.

---

## 🛠 기술 스택

| 분류 | 기술 |
|------|------|
| **Backend** | Python 3.11, Django 5.2 |
| **Frontend** | Django Template, Tailwind CSS, Vanilla JS |
| **Database** | SQLite (로컬 개발), PostgreSQL (Railway 배포) |
| **정적 파일** | WhiteNoise |
| **배포** | Railway |
| **외부 API** | Kakao Maps API |
| **인증** | Django 내장 Auth (세션 기반) |

---

## ✨ 주요 기능

### 회원 관리
- 이메일 기반 회원가입 / 로그인 / 로그아웃
- 회원가입 후 자동 로그인
- 로그인 후 원래 페이지로 리다이렉트

### 청첩장 관리
- 청첩장 생성 / 수정 / 삭제
- 대표 사진 업로드 (가로형 / 세로형 선택)
- 갤러리 사진 최대 8장 업로드
- Classic / Modern / Romantic 3가지 테마 선택
- 실시간 미리보기

### 청첩장 공유 페이지
- UUID 기반 고유 공유 링크 자동 생성
- D-day 카운트다운
- 카카오맵 연동 (예식장 위치 자동 검색)
- 갤러리 캐러셀 (5초마다 자동 슬라이드 + 라이트박스)
- 계좌번호 클립보드 복사 기능
- BGM 재생 / 일시정지

### 방명록
- 로그인 없이 방명록 작성 가능
- 청첩장별 방명록 독립 관리

---

## 🏗 Django 활용 포인트

### 1. Django ORM
```python
# SQL 없이 Python 코드로 DB 조회
weddings = Wedding.objects.filter(user=request.user)
wedding = get_object_or_404(Wedding, pk=pk, user=request.user)
```

### 2. Django Form (유효성 검사 자동화)
```python
class WeddingForm(forms.ModelForm):
    def clean_wedding_date(self):
        wedding_date = self.cleaned_data.get('wedding_date')
        if wedding_date < date.today():
            raise forms.ValidationError('결혼식 날짜는 오늘 이후여야 해요!')
        return wedding_date
```

### 3. Django Auth (인증 / 권한 관리)
```python
@login_required  # 로그인한 사용자만 접근 가능
def dashboard(request):
    ...
```

### 4. Django Template 상속
```html
<!-- base.html을 상속받아 공통 레이아웃 재사용 -->
{% extends 'base.html' %}
{% block content %}
...
{% endblock %}
```

### 5. Model save() 오버라이드 — UUID 공유 링크 자동 생성
```python
def save(self, *args, **kwargs):
    if not self.share_code:
        self.share_code = uuid.uuid4().hex[:8].upper()
    super().save(*args, **kwargs)
```

### 6. ForeignKey 관계 (1:N)
```python
# 방명록 → 청첩장 1:N 관계
class Guestbook(models.Model):
    wedding = models.ForeignKey(Wedding, on_delete=models.CASCADE, related_name='guestbooks')
```

---

## 📁 프로젝트 구조

```
wedding-platform/
├── accounts/               # 회원 관련 앱
│   ├── views.py            # 로그인, 회원가입, 로그아웃
│   └── urls.py
├── config/                 # Django 설정
│   ├── settings.py
│   └── urls.py
├── weddings/               # 청첩장 앱
│   ├── models.py           # Wedding, Guestbook 모델
│   ├── views.py            # CRUD, 공유 페이지
│   ├── forms.py            # WeddingForm, GuestbookForm
│   └── urls.py
├── templates/              # HTML 템플릿
│   ├── base.html           # 공통 레이아웃
│   ├── accounts/           # login.html, register.html
│   └── weddings/           # dashboard.html, edit.html, wedding_page.html
├── static/
│   └── css/                # 스타일 파일
├── media/                  # 업로드 사진 저장 (자동 생성)
├── manage.py
├── Procfile                # Railway 배포 설정
└── requirements.txt
```

---

## 🗄 데이터베이스 모델

| 모델 | 주요 필드 |
|------|----------|
| **Wedding** | id, user(FK), groom_name, bride_name, wedding_date, venue, share_code(UUID), theme, photo, photo_orientation |
| **Guestbook** | id, wedding(FK), name, message, created_at |

---

## 📊 구현 흐름

```
회원가입 → 로그인
  → 대시보드 (청첩장 생성)
    → 신랑/신부 정보 입력 + 사진 업로드 + 테마 선택
      → 고유 공유 링크 자동 생성
        → 링크 복사 → 하객에게 공유
          → 하객: 청첩장 확인 + 방명록 작성
```

---

## 🚀 설치 방법

### 사전 요구사항

- Python 3.11 이상
- pip3

### 1. 레포지토리 클론

```bash
git clone https://github.com/yunniku/django-wedding-platform.git
cd django-wedding-platform
```

### 2. 가상환경 생성 및 활성화

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 패키지 설치

```bash
pip3 install -r requirements.txt
```

### 4. 환경변수 설정

프로젝트 루트(manage.py와 같은 위치)에 `.env` 파일을 생성하세요:

```
SECRET_KEY=your-secret-key-here
KAKAO_MAP_KEY=your-kakao-map-api-key
```

- `SECRET_KEY`: Django 비밀 키 (아무 랜덤 문자열이나 사용 가능, 예: `python3 -c "import secrets; print(secrets.token_hex(32))"` 로 생성)
- `KAKAO_MAP_KEY`: [Kakao Developers](https://developers.kakao.com)에서 앱 생성 후 발급받은 JavaScript 키

### 5. 미디어 폴더 생성

```bash
mkdir -p media
```

> 사진 업로드 기능에 필요한 폴더입니다. `.gitignore`에 포함되어 있으므로 직접 생성해야 합니다.

### 6. 마이그레이션 및 서버 실행

```bash
# DB 테이블 생성
python3 manage.py migrate

# 개발 서버 실행
python3 manage.py runserver
# → http://localhost:8000
```

---

## 📖 사용법

### 청첩장 만들기
1. **회원가입** 후 로그인
2. 대시보드에서 **새 청첩장 만들기** 클릭
3. 신랑 / 신부 이름, 예식 날짜, 예식장 입력
4. 대표 사진 업로드 (가로형 / 세로형 선택)
5. 갤러리 사진 최대 8장 업로드
6. **Classic / Modern / Romantic** 테마 선택
7. 계좌번호, 축가, BGM 등 선택 항목 입력
8. **저장** 클릭 → 청첩장 생성 완료

### 청첩장 공유하기
1. 대시보드에서 생성된 청첩장의 **공유 링크 복사**
2. 카카오톡, 문자 등으로 하객에게 링크 전송
3. 하객은 링크에서 D-day 카운트다운, 지도, 갤러리, 계좌번호 확인 가능

### 방명록
- 하객은 로그인 없이 청첩장 공유 페이지에서 방명록 작성 가능
- 작성된 방명록은 대시보드에서 청첩장별로 확인 가능

---

## 🎨 테마 미리보기

| 테마 | 분위기 | 색상 |
|------|--------|------|
| **Classic** | 전통적이고 우아한 스타일 | 크림 / 골드 |
| **Modern** | 심플하고 세련된 미니멀 스타일 | 화이트 / 블랙 |
| **Romantic** | 따뜻하고 감성적인 스타일 | 핑크 / 로즈 |

---

## 🚀 배포 구조

### Railway (서비스 운영)

```
git push → Railway 자동 배포
├── Django 앱 → gunicorn 실행
├── DB: PostgreSQL (Railway 내장)
├── 정적 파일: WhiteNoise
└── https://django-wedding-platform-production.up.railway.app
```

> 로컬 개발 시 SQLite를 사용하며, Railway 배포 시 자동으로 PostgreSQL로 전환됩니다.

---

## 🤝 기여 방법

1. 이 레포를 **Fork** 하세요
2. 새 브랜치를 생성하세요
   ```bash
   git checkout -b feature/새기능
   ```
3. 변경사항을 커밋하세요
   ```bash
   git commit -m "feat: 새 기능 추가"
   ```
4. 브랜치에 Push 하세요
   ```bash
   git push origin feature/새기능
   ```
5. **Pull Request**를 열어주세요

---

## 👨‍💻 개발자

| 항목 | 내용 |
|------|------|
| **개발 기간** | 2026 |
| **개발 인원** | 1인 개발 |
| **GitHub** | [yunniku](https://github.com/yunniku) |
