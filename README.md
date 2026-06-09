# Eternal — 웨딩 청첩장 플랫폼

Django 기반 모바일 웨딩 청첩장 생성 및 공유 서비스

## 프로젝트 정보

- 개발 기간: 2026
- 개발 인원: 1인
- 주요 기술: Django, SQLite/PostgreSQL, Tailwind CSS, Kakao Maps API, WhiteNoise

- GitHub
  - https://github.com/yunniku/django-wedding-platform

- 배포
  - https://django-wedding-platform-production.up.railway.app

---

## 1. 프로젝트 개요
Flask로 REST API 구조를 먼저 학습한 이후, Django의 ORM / Auth / Form / Template 기능을 직접 사용해 보다 완성도 있는 서비스를 구현하기 위해 시작한 프로젝트입니다.

로그인, 청첩장 생성, 공유 링크, 방명록, 이미지 업로드, 지도 연동처럼 기능이 여러 개 필요한 서비스를 빠르게 만들어보고 싶었고, 인증 / ORM / Form / Template이 모두 내장된 Django가 적합하다고 판단했습니다.

Django Template 기반 SSR 구조로 전체 서비스를 구현하여 하나의 프레임워크로 완결된 웹 서비스를 만드는 경험을 쌓았습니다. 이후 Excel FreeThrow 프로젝트에서 DRF + React 구조로 전환하면서 SSR과 SPA 방식의 차이를 직접 비교하는 기반이 되었습니다.

## 2. 기술 스택
| 분류 | 기술 | 선택 이유 |
|------|------|-----------|
| Backend | Django 5.2 | 인증, ORM, Form, Admin이 내장되어 별도 라이브러리 없이 풀스택 구현 가능 |
| Frontend | Django Template, Tailwind CSS | SSR 기반 빠른 UI 구현. Template 상속으로 레이아웃 재사용 |
| Database | SQLite / PostgreSQL | 개발 환경은 SQLite, 배포 환경은 Railway PostgreSQL로 전환 |
| Auth | Django 내장 Auth | 회원가입 / 로그인 / 세션 관리 / 비밀번호 해싱 자동 처리 |
| External API | Kakao Maps API | 예식장 이름 키워드 검색 후 지도 마커 자동 표시 |
| Static | WhiteNoise | 별도 웹 서버 없이 Django에서 직접 정적 파일 서빙 |
| Deploy | Railway | git push 시 자동 배포. PostgreSQL 내장 |

---

## 3. 주요 기능

### 3-1. 청첩장 관리
- 청첩장 생성 / 수정 / 삭제
- 대표 사진 업로드 (가로형 / 세로형 선택)
- 갤러리 사진 최대 8장 업로드
- Classic / Modern / Romantic 3가지 테마 선택
- 실시간 미리보기

### 3-2. 공유 페이지 (하객 뷰)
- UUID 기반 고유 공유 링크 자동 생성 — 로그인 없이 누구나 접근 가능
- D-day 카운트다운 (서버에서 계산 후 템플릿에 전달)
- 카카오맵 연동 (예식장 이름 키워드 검색 → 지도 마커 표시)
- 갤러리 캐러셀 (5초 자동 슬라이드 + 라이트박스)
- 계좌번호 클립보드 복사
- BGM 재생 / 일시정지

### 3-3. 방명록
- 로그인 없이 방명록 작성 가능
- 청첩장별 방명록 독립 관리 (Wedding : Guestbook = 1 : N)

### 3-4. 회원 관리
- 이메일 기반 회원가입 / 로그인
- 회원가입 후 자동 로그인
- 로그인 후 원래 페이지로 리다이렉트

## 4. 시스템 구조
Django MTV 기반 SSR 구조로 구현되어 있으며, 인증 / 청첩장 / 방명록 기능을 하나의 서버에서 통합 처리합니다.

사용자의 요청은 Django View에서 처리되며, ORM을 통해 DB를 조회한 뒤 Template에 context를 전달하여 HTML을 렌더링합니다.

```
Frontend (Django Template SSR)
├── accounts/
│   ├── login.html       로그인 페이지
│   └── register.html    회원가입 페이지
│
└── weddings/
    ├── dashboard.html    내 청첩장 목록
    ├── edit.html         청첩장 생성/수정
    └── wedding_page.html 공유 청첩장 페이지 (하객 뷰)

        │  HTTP Request
        ↓

Backend (Django Views)
├── accounts/views.py
│   ├── login()           로그인 처리
│   └── register()        회원가입 + 자동 로그인
│
└── weddings/views.py
    ├── dashboard()       내 청첩장 조회
    ├── create_wedding()  청첩장 생성
    ├── edit_wedding()    청첩장 수정
    ├── delete_wedding()  삭제 처리
    ├── wedding_page()    공유 페이지 (public access)
    └── write_guestbook() 방명록 작성

        │  DB Query
        ↓

Database
└── SQLite (local) / PostgreSQL (production)
```

### 4-1. 데이터 흐름
사용자 → URL 접속
  → Django View 실행
    → ORM을 통해 DB 조회 / 저장
      → Template에 context 전달
        → HTML 렌더링
          → 사용자에게 페이지 반환

### 4-2. 구조 설계 핵심 포인트
- Django MTV 기반 SSR 구조로 프론트엔드와 백엔드 통합 설계
- 별도 API 서버 없이 View에서 모든 비즈니스 로직 처리
- accounts / weddings 앱 분리를 통한 도메인 책임 분리
- ORM 기반 데이터 처리로 SQL 직접 작성 없이 CRUD 구현
- share_code 기반 공개 URL 구조로 로그인 없이 접근 가능한 페이지 제공

---

## 5. 핵심 구현 포인트

### 5-1. UUID 공유 링크 자동 생성
청첩장마다 고유한 공유 링크를 생성하기 위해 `save()` 메서드를 오버라이드했습니다. 최초 저장 시에만 `share_code`를 생성하고 이후 수정 시에는 유지되도록 설계했습니다.

```python
def save(self, *args, **kwargs):
    if not self.share_code:
        self.share_code = uuid.uuid4().hex[:8].upper()
    super().save(*args, **kwargs)
```

공유 URL 구조: `/w/{share_code}/` (예: `/w/A3F2BC91/`)
로그인 없이 누구나 접근 가능하도록 구성했습니다.

---

### 5-2. Django Form으로 유효성 검사 자동화
초기에는 `request.POST`로 데이터를 직접 처리했으나, 유효성 검사가 없어 잘못된 날짜가 저장되는 문제가 발생했습니다. Django Form의 `clean_*` 메서드를 활용해 검증 로직을 분리했습니다.

```python
class WeddingForm(forms.ModelForm):
    def clean_wedding_date(self):
        wedding_date = self.cleaned_data.get('wedding_date')
        if wedding_date < date.today():
            raise forms.ValidationError('결혼식 날짜는 오늘 이후여야 해요!')
        return wedding_date
```

이를 통해 `form.is_valid()` 한 줄로 전체 검증이 가능하도록 구조를 단순화했습니다.

---

### 5-3. 권한 관리 — 본인 청첩장만 조회
`get_object_or_404`에 `user=request.user` 조건을 추가하여, URL을 통한 직접 접근 시에도 본인 데이터만 조회되도록 제한했습니다.

```python
# 본인 청첩장만 조회 — 다른 사람 pk 입력 시 404
wedding = get_object_or_404(Wedding, pk=pk, user=request.user)
```

---

### 5-4. 카카오맵 API 키 보안 처리
API 키를 코드에 직접 노출하지 않고 `.env` → `os.getenv()` → 템플릿 전달 구조로 관리했습니다.

```python
return render(request, 'weddings/wedding_page.html', {
    'wedding': wedding,
    'kakao_map_key': os.getenv('KAKAO_MAP_KEY'),
    'days_left': (wedding.wedding_date - date.today()).days,
})
```

---

### 5-5. Tailwind CSS 도입 과정에서 겪은 문제
기존에는 CSS 파일을 분리하여 관리했으나 유지보수 문제가 발생해 Tailwind CSS로 전환했습니다. 이 과정에서 preflight 기능이 기존 스타일을 초기화하면서 UI가 깨지는 문제가 발생했습니다.

`tailwind.config`에서 아래 설정으로 해결했습니다.

```javascript
// tailwind.config.js
module.exports = {
  corePlugins: {
    preflight: false
  }
}
```

---

## 6. 배포 구조
git push → Railway 자동 배포
├── Django 앱 → gunicorn 실행
├── DB: PostgreSQL (Railway 내장)
├── 정적 파일: WhiteNoise
└── 환경변수: SECRET_KEY, KAKAO_MAP_KEY Railway에서 관리

로컬 환경 - SQLite 사용
배포 환경 - PostgreSQL로 자동 전환되도록 구성

Django ORM을 사용하여 데이터베이스가 변경되어도 코드 수정 없이 동일한 로직이 동작하도록 설계했습니다.

---

## 7. AI 활용 내역
본 프로젝트는 AI(Claude, ChatGPT)를 개발 보조 도구로 사용했습니다.
문제 원인 분석, 코드 리뷰, 학습 보조 용도로 AI를 활용했으며 최종 설계, 구현, 디버깅은 직접 수행했습니다.

### 직접 설계 및 구현
- Django MTV 패턴 기반 전체 아키텍처 설계 (Model / Template / View)
- UUID 기반 save() 메서드 오버라이드로 공유 링크 자동 생성 로직 구현
- Django Form clean_wedding_date()를 통한 입력 유효성 검증 로직 설계
- get_object_or_404(Wedding, pk=pk, user=request.user) 기반 권한 제어 구현
- Kakao Maps API 키 .env 분리 및 템플릿 context 전달 구조 설계
- Django Template 상속 구조 설계 (base.html 기반 레이아웃 구성)
- Tailwind CSS preflight 충돌 문제 분석 및 해결
- Railway 배포 환경 구성 (Procfile, PostgreSQL 연동 포함)

### AI 보조 활용
- Tailwind CSS와 기존 커스텀 CSS 충돌 원인 파악
- 이메일 기반 로그인 시 `authenticate()` 호환 방식 검토
- Django `LOGIN_REDIRECT_URL` / `next` 파라미터 처리 방식 확인
- README 초안 작성 및 문서 구조 개선

---
