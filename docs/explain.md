# 온톨로지 심화 학습 가이드: 도서관 시스템

이 문서는 구축된 '도서관 시스템' 온톨로지를 쉽게 이해할 수 있도록 핵심 개념과 설계를 설명합니다.

---

## 1. RDFS vs OWL: 무엇이 다른가요?

이 프로젝트는 두 가지 방식으로 온톨로지를 정의하고 있습니다.

### [RDFS (RDF Schema)](../data/rdf/library-schema.ttl)
*   **역할:** 데이터의 **기본 구조(Hierarchy)**를 잡는 역할을 합니다.
*   **핵심 요소:** `rdfs:subClassOf`, `rdfs:domain`, `rdfs:range`.
*   **설명:** "작가는 사람의 일종이다", "책은 작가를 가진다"와 같은 단순한 계층과 속성 관계를 정의합니다. 가볍고 빠르지만 복잡한 논리를 표현하기엔 부족합니다.

### [OWL (Web Ontology Language)](../data/owl/library.owl)
*   **역할:** 데이터 간의 **복잡한 논리와 제약 조건**을 정의합니다.
*   **핵심 요소:** `owl:inverseOf`, `owl:SymmetricProperty`, `owl:TransitiveProperty`, `owl:disjointWith`, **`owl:propertyChainAxiom`** 등.
*   **설명:** RDFS보다 훨씬 강력한 추론(Inference)을 가능하게 합니다. 예를 들어, 위치 정보의 연쇄 법칙을 정의하여 "책이 선반에 있고 선반이 1층에 있다면, 책은 1층에 있다"는 사실을 자동으로 도출합니다.

---

## 2. 주요 클래스(Class) 설계 (확장)

클래스는 실세계의 '개념'을 나타내며, 이번 확장에서는 자산의 종류와 사용자 유형을 구체화했습니다.

| 클래스 | 설명 | 특징 |
| :--- | :--- | :--- |
| `LibraryResource` | 도서관의 모든 자산 | `Book`, `EBook`, `Multimedia`의 상위 클래스 |
| `Book`, `EBook`, `Multimedia` | 자산의 세부 종류 | 각 자산은 매체 특성에 따라 분류됨 |
| `Student`, `Staff` | 사용자 유형 | `LibraryUser`를 상속받아 권한이나 정책 분리가 가능함 |
| `Location`, `Floor`, `Shelf` | 물리적 위치 | 자산이 어디에 있는지 계층적으로 표현 |
| `Reservation` | 예약 정보 | 대출 외에 예약 프로세스를 관리하기 위한 클래스 |

---

## 3. 속성(Property)의 마법: 추론 이해하기

OWL의 강력함은 속성의 특성에서 나옵니다.

### ① 역관계 (Inverse Property)
*   **정의:** `lib:wrote` ↔ `lib:hasAuthor`
*   **효과:** 작가가 책을 썼다는 사실만 알면, 책의 저자가 누구인지 자동으로 연결됩니다.

### ② 대칭적 속성 (Symmetric Property)
*   **정의:** `lib:isRelatedTo`
*   **효과:** A와 B가 관련 있다면, B와 A도 자동으로 관련 있는 것으로 처리됩니다.

### ③ 이행적 속성 (Transitive Property)
*   **정의:** `lib:partOfSeries`, **`lib:within`**
*   **효과:** "선반 A는 1층에 있다", "1층은 본관에 있다"면 "선반 A는 본관에 있다"는 논리가 성립합니다.

### ④ 속성 체인 (Property Chain Axiom)
*   **정의:** `lib:locatedAt` ∘ `lib:within` → `lib:locatedAt`
*   **효과:** **고급 추론**입니다. 자산이 `선반`에 있고, 선반이 `층` 안에 있다면, 자산이 해당 `층`에 있다는 관계를 자동으로 생성합니다.

---

## 4. 고급 제약 조건 (Restrictions)

### 서로소 관계 (Disjoint Classes)
`Author`와 `LibraryUser`는 서로소입니다. 또한, 이번 확장에서는 다양한 자산 종류들도 서로소로 설정하여 논리적 명확성을 높일 수 있습니다.

### 카디널리티 (Cardinality)
`LibraryResource` 클래스에는 `minCardinality 1` 제약이 걸려 있어, 모든 자산은 반드시 최소 한 명의 저자 정보를 가져야 합니다.

---

## 5. 샘플 데이터로 확인하기

`data/rdf/sample-data.ttl` 파일을 보면 실제 인스턴스들이 정의되어 있습니다.

1.  **조지 오웰(George Orwell)**은 `lib:Author`로 정의되었습니다.
2.  **1984**라는 책은 `lib:hasAuthor`로 조지 오웰과 연결되고, `lib:isbn`을 가집니다.
3.  **앨리스(Alice)**라는 이용자가 **1984**를 대출한 기록(`lib:Loan_001`)이 존재합니다.

이 데이터를 Protege의 추론기(Reasoner)로 돌리면, 명시적으로 적지 않은 수많은 관계들이 자동으로 생성되는 것을 볼 수 있습니다.

---

## 6. 다음 단계: 어떻게 활용하나요?

1.  **시각화:** Protege 프로그램에서 `library.owl`을 열어 클래스 계층도를 확인해 보세요.
2.  **질의:** SPARQL을 사용하여 "특정 장르의 책을 빌려간 사용자의 이름은?"과 같은 복잡한 질문을 던져보세요.
3.  **확장:** 반납 여부(`isReturned`), 연체료 계산 등 더 복잡한 비즈니스 로직을 속성으로 추가해 보세요.
