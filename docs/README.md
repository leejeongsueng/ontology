# 온톨로지 예제 프로젝트: 도서관 시스템

이 프로젝트는 온톨로지 학습을 위한 간단한 도서관 시스템 예제입니다.

## 1. 프로젝트 구조
- `data/rdf/`: RDF 스키마(RDFS) 및 샘플 데이터 파일
- `data/owl/`: OWL 온톨로지 정의 파일
- `docs/`: 프로젝트 문서

## 2. 온톨로지 설계 (도서관)

### 클래스 (Classes)
- `Person`: 사람을 나타내는 기본 클래스
- `Author`: 작가 (`Person`의 하위 클래스). `wrote` 속성을 통해 `Book`과 연결됩니다.
- `LibraryUser`: 도서관 이용자 (`Person`의 하위 클래스). `Author`와는 서로소(Disjoint) 관계입니다.
- `Book`: 도서 클래스. 최소 1명 이상의 작가를 가져야 한다는 제약 조건이 있습니다.
- `Genre`: 도서의 장르 (예: Dystopian, Fiction)
- `Publisher`: 출판사
- `Loan`: 대출 기록. 특정 사용자가 특정 책을 대출한 정보를 담습니다.

### 속성 (Properties)
- `hasAuthor` / `wrote`: 도서와 작가 간의 역관계(Inverse)
- `publishedBy` / `hasPublisher`: 도서와 출판사 간의 역관계
- `hasGenre`: 도서의 장르 지정
- `borrowedBy` / `loanedBook`: 대출 기록과 사용자/도서 간의 연결
- `isRelatedTo`: 도서 간의 연관 관계 (SymmetricProperty: A가 B와 관련 있으면 B도 A와 관련 있음)
- `partOfSeries`: 시리즈물 관계 (TransitiveProperty: A가 B의 후속작이고 B가 C의 후속작이면 A는 C의 시리즈 일부)
- `isbn`: 도서의 고유 번호 (FunctionalProperty: 하나의 책은 하나의 ISBN만 가짐)
- `loanDate` / `returnDate`: 대출 및 반납 일시 (xsd:dateTime)

## 3. 주요 파일 설명
- `data/rdf/library-schema.ttl`: RDFS를 이용한 기본 계층 구조 및 속성 정의
- `data/owl/library.owl`: OWL을 이용한 고급 제약 조건(역관계, Functional Property 등) 정의
- `data/rdf/sample-data.ttl`: 실제 인스턴스 데이터 (George Orwell, 1984 등)

## 4. 활용 및 시각화 가이드
- **[시각화 및 확인 가이드 (Protege & Neo4j)](./visualize.md)**: 이 문서를 통해 온톨로지를 시각화하고 쿼리하는 방법을 확인할 수 있습니다.
- 이 파일들은 RDF/OWL 편집기(예: Protege)에서 불러와 시각화하거나 추론 기능을 테스트해 볼 수 있습니다.
- SPARQL 엔진 또는 Neo4j Cypher를 사용하여 데이터를 질의할 수 있습니다.
