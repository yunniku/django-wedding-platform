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
| **Database** | SQLite (개발), PostgreSQL (배포) |
| **배포** | Railway |
| **외부 API** | Kakao Maps API |
| **인증** | Django 내장 Auth |

---

## ✨ 주요 기능

### 회원 관리
- 이메일 기반 회원가입 / 로그인
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
- 카카오맵 연동 (예식장 위치)
- 갤러리 캐러셀 (자동 슬라이드)
- 계좌번호 복사 기능
- BGM 재생

### 방명록
- 로그인 없이 방명록 작성 가능
- 청첩장별 방명록 관리

---

## 🏗 Django 활용 포인트

### 1. Django ORM
```python
# SQL 없이 파이썬 코드로 DB 조회
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

### 3. Django Auth (인증/권한 관리)
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

### 5. Model save() 오버라이드
```python
def save(self, *args, **kwargs):
    # 공유 코드 자동 생성 (UUID)
    if not self.share_code:
        self.share_code = uuid.uuid4().hex[:8].upper()
    super().save(*args, **kwargs)
```

### 6. ForeignKey 관계
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
│   ├── accounts/
│   └── weddings/
├── static/css/             # 스타일 파일
├── manage.py
├── Procfile                # Railway 배포 설정
└── requirements.txt
```

---

## 🚀 로컬 실행 방법

```bash
# 1. 레포지토리 클론
git clone https://github.com/your-username/wedding-platform.git
cd wedding-platform

# 2. 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 3. 패키지 설치
pip3 install -r requirements.txt

# 4. 환경변수 설정 (.env 파일 생성)
SECRET_KEY=your-secret-key
KAKAO_MAP_KEY=your-kakao-map-key

# 5. 마이그레이션
python3 manage.py migrate

# 6. 서버 실행
python3 manage.py runserver
```

---

## 🎨 테마 미리보기

| Classic | Modern | Romantic |
|---------|--------|----------|
| 크림 / 골드 | 화이트 / 블랙 | 핑크 / 로즈 |

---

## 📝 구현 흐름

```
회원가입 → 로그인 → 청첩장 생성 → 공유 링크 복사 → 하객이 청첩장 확인 + 방명록 작성
```

---

## 👨‍💻 개발자

| 항목 | 내용 |
|------|------|
| **개발 기간** | 2026 |
| **개발 인원** | 1인 개발 |
| **GitHub** | [링크] |
