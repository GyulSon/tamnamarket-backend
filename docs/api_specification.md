# 🍊 탐라장터(TamnaMarket) API 명세서

본 문서는 탐라장터 백엔드 시스템에서 제공하는 모든 API에 대한 명세서입니다.

## 📌 공통 정보
- **Base URL**: `http://localhost:8000` (또는 실제 배포 서버 도메인)
- **Response Format**: 모든 응답은 아래와 같은 공통 형식을 따릅니다.
  ```json
  {
    "isSuccess": true,
    "message": "성공 메시지 (필요 시)",
    "content": { ... } // 실제 데이터 결과
  }
  ```

---

## 🛠 1. 판매 프로세스 (Sale Domain)

### [POST] 품종 분석 및 초기 생성 (Step 1)
이미지를 분석하여 품종을 분류하고, 상품 데이터를 초기 생성합니다.
- **URL**: `/api/sale/classification`
- **Request Body (Multipart/form-data)**:
  - `file`: `UploadFile` (분석할 이미지 1장)
- **Response**:
  - `content`:
    ```json
    {
      "product_id": 123,
      "category": "한라봉"
    }
    ```

### [POST] 상품 이미지 추가 등록 (Step 2)
1단계 이후 추가로 상품 사진 3장을 등록합니다.
- **URL**: `/api/sale/image`
- **Request Body (Multipart/form-data)**:
  - `product_id`: `int` (Body)
  - `images`: `List[UploadFile]` (최대 3장)
- **Response**:
  - `content`:
    ```json
    {
      "message": "추가 이미지 3장 업로드 완료"
    }
    ```

### [POST] AI 판매글 생성 (Step 3)
농부의 음성을 분석하여 판매글 제목과 설명을 생성합니다.
- **URL**: `/api/sale/text`
- **Request Body (Multipart/form-data)**:
  - `product_id`: `int` (Body)
  - `voices`: `List[UploadFile]` (최대 4개 - 3개는 분석용, 마지막은 저장용)
- **Response**:
  - `content`:
    ```json
    {
      "title": "제주 애월에서 갓 수확한 한라봉",
      "final_description": "당도가 높고 과육이 풍부한 최고급 한라봉입니다."
    }
    ```

### [POST] 적정가 추천 (Step 4)
시장 데이터를 기반으로 적정 판매가를 추천합니다.
- **URL**: `/api/sale/price`
- **Request Body (JSON)**:
  ```json
  {
    "product_id": 123
  }
  ```
- **Response**:
  - `content`:
    ```json
    {
      "product_id": 123,
      "recommended_price": 23000
    }
    ```

### [GET] 판매글 상세 조회 (Step 5)
최종 완성된 판매 정보를 조회합니다.
- **URL**: `/api/sale/salead?product_id={product_id}`
- **Response**:
  - `content`:
    ```json
    {
      "product_id": 123,
      "title": "제주 애월에서 갓 수확한 한라봉",
      "price": 23000,
      "images": ["/static/images/img1.jpg", "..."],
      "voice_url": "/static/audio/voice.mp3",
      "final_description": "..."
    }
    ```

---

## 📺 2. 메인 화면 (MainScreen Domain)

### [GET] 메인 콘텐츠 조회
전체 판매글 목록을 랜덤 또는 순차적으로 조회합니다.
- **URL**: `/api/mainscreen/content?buyer_id={buyer_id}`
- **Response**:
  - `content`: `List[MainContentItem]`
    ```json
    [
      {
        "product_id": 1,
        "title": "맛있는 감귤",
        "price": 15000,
        "thumbnail": "/static/images/thumb.jpg",
        "seller_name": "김농부",
        "category": "감귤"
      }
    ]
    ```

### [GET] 콘텐츠 필터링
품종별로 판매글을 필터링하여 조회합니다.
- **URL**: `/api/mainscreen/filter?buyer_id={buyer_id}&category={category}`
- **Response**: 위와 동일 (필터링된 결과)

---

## 👨‍🌾 3. 농부 및 구독 (Farmer/Subscription Domain)

### [GET] 구독 중인 농부 목록
구매자가 구독 중인 농부들의 요약 정보를 조회합니다.
- **URL**: `/api/subscription/farmer?buyer_id={buyer_id}`
- **Response**:
  - `content`: `List[FarmerSummary]`
    ```json
    [
      {
        "seller_id": 1,
        "name": "귀농달인",
        "profile_img": "/static/images/profile.jpg",
        "residence": "제주시 애월읍"
      }
    ]
    ```

### [GET] 농부 프로필 상세
특정 농부의 프로필 정보 및 인증 이력을 조회합니다.
- **URL**: `/api/farmer/profile?seller_id={seller_id}`
- **Response**:
  - `content`:
    ```json
    {
      "seller_id": 1,
      "name": "김농부",
      "experience": "감귤 재배 20년",
      "repurchase_rate": 85.5,
      "total_sales": 1200,
      "images": ["/static/images/p1.jpg"]
    }
    ```

---

## 🛒 4. 주문 (Order Domain)

### [POST] 상품 구매 (Step 6)
상품을 구매하고 주문 정보를 기록하며, 농부에게 알림을 보냅니다.
- **URL**: `/api/order/product`
- **Request Body (JSON)**:
  ```json
  {
    "product_id": 123,
    "buyer_id": 1
  }
  ```
- **Response**:
  - `content`:
    ```json
    {
      "order_id": 456,
      "status": "결제 및 주문 기록 완료"
    }
    ```

---

## 🏥 5. 공통 (Health Check)

### [GET] 서버 헬스 체크
서버 상태를 확인합니다.
- **URL**: `/`
- **Response**:
  ```json
  {
    "status": "ok",
    "message": "탐라장터 API가 정상 작동 중입니다."
  }
  ```
