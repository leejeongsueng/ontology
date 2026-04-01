# 온톨로지 설명 문서

이 프로젝트는 도서관 도메인을 RDF/RDFS/OWL로 정의하고,
그래프 DB(Neo4j)에서 데이터/관계를 검증하기 위한 학습용 모델입니다.

## 1. 파일 역할

- `data/rdf/library-schema.ttl`
  - RDFS 기반 클래스/속성 정의
  - `subClassOf`, `domain`, `range` 중심
- `data/owl/library.owl`
  - OWL 기반 제약/추론 규칙 추가
  - inverse/symmetric/transitive/property chain 등
- `data/rdf/sample-data.ttl`
  - 한글화된 인스턴스 데이터(저자, 도서, 이용자, 대출, 예약 등)

## 2. 모델 요약

클래스 구조:
- 사람: `Person` > `Author`, `LibraryUser` > `Student`, `Staff`
- 자료: `LibraryResource` > `Book`, `EBook`, `Multimedia`
- 운영: `Loan`, `Reservation`
- 위치: `Location` > `Floor`, `Shelf`
- 기타: `Genre`, `Publisher`

주요 관계:
- 저자/자료: `hasAuthor` <-> `wrote` (inverse)
- 자료/장르: `hasGenre`
- 자료/출판사: `publishedBy`
- 대출: `loanedResource`, `borrowedBy`
- 예약: `reservedResource`, `reservedBy`
- 위치: `locatedAt`, `within`
- 연관자료: `isRelatedTo` (symmetric)

## 3. OWL 규칙 포인트

- `LibraryResource`는 최소 1명의 저자 필요(`minCardinality 1`)
- `isRelatedTo`는 양방향 관계로 해석 가능(symmetric)
- `within`은 계층적 포함 관계 전파(transitive)
- `locatedAt` + `within`은 위치 추론 확장을 위한 chain으로 정의

## 4. 한글 데이터 네이밍

샘플 데이터의 개체 이름과 문자열 값을 한글로 정리했습니다.

예시 URI:
- `http://example.org/library#도서_1984`
- `http://example.org/library#저자_조지오웰`
- `http://example.org/library#출판사_세커앤워버그`
- `http://example.org/library#이용자_앨리스`

예시 literal:
- `"멋진 신세계"`, `"마음의 사회"`, `"앨리스 김"`

## 5. Neo4j import 시 해석 주의

`n10s` import 결과에서 클래스가 항상 라벨로 그대로 매핑된다고 가정하면
쿼리가 쉽게 깨집니다. 그래서 현재 스크립트는:

- 라벨 고정 조회 대신 URI prefix 기반 검증 사용
- 속성 키도 고정값 대신 동적 탐색(`keys(n)` + `title` 포함 키 탐색)

이 방식은 매핑 모드가 달라도 검증 로직이 유지된다는 장점이 있습니다.

## 6. 스크립트 검증 항목

`import_to_neo4j.py`의 `verify()`는 아래를 확인합니다.

1. 전체 `:Resource` 수
2. 한글 URI prefix별 개수 기대값 일치 여부
3. 도서/전자책/멀티미디어 title 조회
4. `hasAuthor` 대상이 `저자_` 개체인지 무결성 점검

이 검증은 단순 실행 성공 여부보다 데이터 품질까지 같이 점검하도록 설계되어 있습니다.
