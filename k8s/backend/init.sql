-- ==========================================
-- 탐나마켓 DB 초기화 스크립트 (DDL + DML)
-- Python 모델 기준으로 작성 (app/domains/*/models.py)
-- ==========================================

USE tamnamarket;

-- ==========================================
-- DDL: 테이블 생성
-- ==========================================

CREATE TABLE IF NOT EXISTS sellers (
    seller_id     INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(50)    NOT NULL,
    residence     VARCHAR(100),
    experience    TEXT,
    repurchase_rate DECIMAL(5,2),
    total_sales   INT            DEFAULT 0,
    created_at    DATETIME       DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS seller_images (
    image_id   INT AUTO_INCREMENT PRIMARY KEY,
    seller_id  INT NOT NULL,
    img1       VARCHAR(255),
    img2       VARCHAR(255),
    img3       VARCHAR(255),
    img4       VARCHAR(255),
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS buyers (
    buyer_id   INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(50) NOT NULL,
    created_at DATETIME    DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    product_id        INT AUTO_INCREMENT PRIMARY KEY,
    seller_id         INT NOT NULL,
    title             VARCHAR(100),
    category          VARCHAR(50),
    weight            VARCHAR(50),
    harvest_date      DATE,
    taste_feature     TEXT,
    farmer_comment    TEXT,
    price             INT,
    voice_path        VARCHAR(255),
    final_description TEXT,
    is_selling        BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS product_images (
    image_id   INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    img1       VARCHAR(255),
    img2       VARCHAR(255),
    img3       VARCHAR(255),
    img4       VARCHAR(255),
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS subscriptions (
    subscription_id INT AUTO_INCREMENT PRIMARY KEY,
    seller_id       INT NOT NULL,
    buyer_id        INT NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id) ON DELETE CASCADE,
    FOREIGN KEY (buyer_id)  REFERENCES buyers(buyer_id)  ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS wishlists (
    wishlist_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id  INT NOT NULL,
    buyer_id    INT NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    FOREIGN KEY (buyer_id)   REFERENCES buyers(buyer_id)    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS orders (
    order_id   INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    buyer_id   INT NOT NULL,
    order_date DATETIME    DEFAULT CURRENT_TIMESTAMP,
    status     VARCHAR(50) DEFAULT '결제 완료',
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    FOREIGN KEY (buyer_id)   REFERENCES buyers(buyer_id)    ON DELETE CASCADE
);

-- ==========================================
-- DML: 더미 데이터
-- ==========================================

-- 1. 판매자
INSERT INTO sellers (name, residence, experience, repurchase_rate, total_sales) VALUES
('김만복', '제주특별자치도 제주시 애월읍', '30년 전통의 서귀포 감귤 농장을 운영하고 있습니다. 정직과 신용을 최우선으로 합니다.', 68.50, 120),
('이옥자', '제주특별자치도 서귀포시 남원읍', '해녀 출신으로 직접 채취한 미역과 톳, 그리고 남편이 기른 한라봉을 판매합니다.', 55.20, 85),
('박성철', '제주특별자치도 제주시 구좌읍', '구좌 당근의 달인입니다. 흙 묻은 그대로의 싱싱함을 전해드립니다.', 62.00, 210),
('최경숙', '제주특별자치도 제주시 한경면', '바람 잘 날 없는 한경면에서 꿋꿋하게 자란 브로콜리와 양배추를 재배합니다.', 45.80, 45),
('강석호', '제주특별자치도 서귀포시 성산읍', '성산 일출봉 아래에서 자란 성산 무와 감자를 키우고 있습니다.', 59.40, 60);

-- 2. 판매자 이미지
INSERT INTO seller_images (seller_id, img1, img2, img3, img4) VALUES
(1, 'https://images.unsplash.com/photo-1595152772835-219674b2a8a6?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1523741543316-95f74577bf61?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&q=80'),
(2, 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&q=80'),
(3, 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&q=80'),
(4, 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1501196354995-cbb51c65aaea?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80'),
(5, 'https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1552058544-f2b08422138a?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1544723345-cbb4ff6a9b5f?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1488426862026-3ee34a7d66df?auto=format&fit=crop&q=80');

-- 3. 구매자
INSERT INTO buyers (name) VALUES
('이지은'), ('강하늘'), ('박서준'), ('김수현'), ('최지우'),
('정우성'), ('손예진'), ('현빈'), ('송혜교'), ('이동욱');

-- 4. 상품
INSERT INTO products (seller_id, title, category, weight, harvest_date, taste_feature, farmer_comment, price, voice_path, final_description, is_selling) VALUES
(1, '고산지대 타이벡 감귤 5kg',   '감귤',   '5kg',      '2026-03-25', '당도가 높고 산도가 적당하여 남녀노소 누구나 좋아합니다.',  '정성껏 키웠습니다. 맛있게 드세요!',     25000, '/audio/seller1_product1.mp3', '제주 애월의 따뜻한 햇살을 받고 자란 명품 감귤입니다.', TRUE),
(1, '산지직송 청귤(영귤) 2kg',    '감귤',   '2kg',      '2026-03-20', '새콤한 맛이 일품이며 청으로 담가 드시기 좋습니다.',       '여름의 싱그러움을 담았습니다.',          18000, '/audio/seller1_product2.mp3', '수제 청 제작에 최적화된 무농약 청귤입니다.', TRUE),
(2, '남원 한라봉 특과 3kg',       '만감류', '3kg',      '2026-03-28', '아삭한 식감과 풍부한 과즙이 특징입니다.',                 '선물용으로 아주 좋습니다.',              45000, '/audio/seller2_product1.mp3', '명절 선물 1순위, 귀한 분께 선물하세요.', TRUE),
(2, '자연산 건미역 500g',         '해조류', '500g',     '2026-03-10', '바다 향이 진하고 국물이 잘 우러납니다.',                  '해녀가 직접 채취했습니다.',              12000, '/audio/seller2_product2.mp3', '제주 바다의 영양을 그대로 담은 태양 건조 미역입니다.', TRUE),
(3, '구좌 흙당근 10kg',           '채소',   '10kg',     '2026-04-01', '단맛이 강하고 육질이 단단합니다.',                        '주스로 갈아 마시기 최고입니다.',         30000, '/audio/seller3_product1.mp3', '당근의 성지 구좌에서 갓 수확한 싱싱한 당근입니다.', TRUE),
(3, '당근 즙(파우치형) 30포',     '가공식품','30포',    '2026-03-15', '첨가물 없는 순수 당근 100%입니다.',                       '바쁜 아침 건강 한 잔 하세요.',           35000, '/audio/seller3_product2.mp3', '착즙 후 저온 살균하여 영양을 살렸습니다.', TRUE),
(4, '제주 브로콜리 2kg',          '채소',   '2kg',      '2026-03-30', '속이 꽉 차고 아삭한 식감이 좋습니다.',                    '세척 후 가볍게 데쳐 드세요.',            15000, '/audio/seller4_product1.mp3', '청정 제주 바람을 맞고 자란 브로콜리입니다.', TRUE),
(4, '무농약 양배추 1통',           '채소',   '1.5kg 내외','2026-03-22', '달큰하고 부드러운 맛이 특징입니다.',                    '건강을 위해 드셔보세요.',                 5000, '/audio/seller4_product2.mp3', '위 건강에 도움을 주는 신선한 양배추입니다.', TRUE),
(5, '성산 꿀감자 5kg',            '채소',   '5kg',      '2026-03-18', '포슬포슬한 분이 많이 나는 감자입니다.',                   '쪄서 드시면 정말 맛있습니다.',           22000, '/audio/seller5_product1.mp3', '철분이 풍부한 성산 토양에서 자랐습니다.', TRUE),
(5, '제주산 볶은 참깨 200g',      '양념',   '200g',     '2026-02-10', '고소한 풍미가 일품입니다.',                               '고향의 맛을 담았습니다.',                10000, '/audio/seller5_product2.mp3', '우리 땅에서 자란 국산 참깨 100%입니다.', TRUE);

-- 5. 상품 이미지
INSERT INTO product_images (product_id, img1, img2, img3, img4) VALUES
(1,  'https://images.unsplash.com/photo-1611080626919-7cf5a9caab53?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1557800636-894a64c1696f?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1591244391183-9bf05371322a?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1523472721958-978152f4d69b?auto=format&fit=crop&q=80'),
(2,  'https://images.unsplash.com/photo-1611080541599-8c6dbde6ed28?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1501746739263-4e830fabe61b?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1611080630327-023a1fb4d7c2?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1582231201995-17bd2761858c?auto=format&fit=crop&q=80'),
(3,  'https://images.unsplash.com/photo-1601004890684-d8cbf643f5f2?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1588636400827-046649a2a912?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1523438885200-e63329233fe2?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1559181567-c3190ca9959b?auto=format&fit=crop&q=80'),
(4,  'https://images.unsplash.com/photo-1604495941541-118f6735e8f4?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1534002133490-99729d47936d?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1534002133604-03a1fc6c547a?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1534002134234-93e15093557e?auto=format&fit=crop&q=80'),
(5,  'https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1590865101275-23677bb0b217?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1601493700631-2b16ec4b4b24?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1550081699-79c1c2e48a77?auto=format&fit=crop&q=80'),
(6,  'https://images.unsplash.com/photo-1502741126161-bca57833075c?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1511130541193-45564882e46b?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1563729784400-f97df88f118c?auto=format&fit=crop&q=80'),
(7,  'https://images.unsplash.com/photo-1584270354949-c26b0d5b4a0c?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1583663848850-4c441c49048a?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1592663527453-33e387c9f6a7?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1609142807703-c3400b467ec6?auto=format&fit=crop&q=80'),
(8,  'https://images.unsplash.com/photo-1594282486552-05b4d80fbb9f?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1155353592471-ef281d662f43?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1550989460-0adf9ea622e2?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1508313880080-c4bef0730395?auto=format&fit=crop&q=80'),
(9,  'https://images.unsplash.com/photo-1518977676601-b53f82aba655?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1552554746-880c10f81a7d?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1550147760-44c9966d6bc7?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1526470608268-f674ce90ebd4?auto=format&fit=crop&q=80'),
(10, 'https://images.unsplash.com/photo-1591195853225-bb10901e1da6?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1590682680695-43b964a3ae17?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1498579687545-d5a4fffb0a9e?auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1508170754724-6cd40962fc16?auto=format&fit=crop&q=80');

-- 6. 구독
INSERT INTO subscriptions (buyer_id, seller_id) VALUES
(1, 1), (1, 3),
(2, 2), (2, 5),
(3, 1), (4, 4), (5, 5);

-- 7. 찜
INSERT INTO wishlists (buyer_id, product_id) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5);

-- 8. 주문
INSERT INTO orders (buyer_id, product_id, status) VALUES
(1, 1,  '결제 완료'), (2, 3,  '결제 완료'), (3, 5,  '결제 완료'),
(4, 7,  '결제 완료'), (5, 9,  '결제 완료'), (6, 2,  '결제 완료'),
(7, 4,  '결제 완료'), (8, 6,  '결제 완료'), (9, 8,  '결제 완료'),
(10, 10,'결제 완료');
