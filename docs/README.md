# Library Ontology 프로젝트 문서

이 프로젝트는 도서관 도메인을 RDF/RDFS/OWL로 모델링하고,
Neo4j(`n10s`)로 적재해 그래프 형태로 검증하는 예제입니다.

## 디렉터리 구조

- `data/rdf/library-schema.ttl`: RDFS 스키마
- `data/owl/library.owl`: OWL 온톨로지(제약/추론 규칙)
- `data/rdf/sample-data.ttl`: 한글화된 샘플 인스턴스 데이터
- `scripts/import_to_neo4j.py`: Neo4j import + 검증 스크립트
- `docs/`: 사용/검증/쿼리 문서

## 핵심 모델

클래스:
- `LibraryResource`, `Book`, `EBook`, `Multimedia`
- `Person`, `Author`, `LibraryUser`, `Student`, `Staff`
- `Genre`, `Publisher`, `Loan`, `Reservation`, `Location`, `Floor`, `Shelf`

주요 속성:
- 객체 속성: `hasAuthor`, `wrote`, `hasGenre`, `publishedBy`, `loanedResource`, `borrowedBy`, `reservedResource`, `reservedBy`, `locatedAt`, `within`, `isRelatedTo`
- 데이터 속성: `title`, `name`, `isbn`, `loanDate`, `returnDate`

## 데이터 네이밍 규칙 (한글)

샘플 개체 URI prefix:
- `도서_`, `전자책_`, `멀티미디어_`
- `저자_`, `출판사_`, `장르_`
- `이용자_`, `대출_`, `예약_`
- `층_`, `서가_`

## 현재 import/검증 동작

`import_to_neo4j.py` 기준:
- 결과 소비 오류(`ResultConsumedError`) 방지를 위해 세션 내부에서 결과를 리스트로 변환
- 라벨(`LibraryResource`) 존재를 가정하지 않음
- URI prefix(한글) 기준으로 샘플 데이터 정합성 검증
- `hasAuthor` 링크 대상이 `저자_` prefix인지 무결성 점검

## 실행

```bash
python scripts/import_to_neo4j.py
```

실행 후 verify 출력에서:
- prefix별 count가 expected와 일치하는지
- 자료 title 조회가 정상인지
- `hasAuthor` 무결성 경고가 없는지
를 확인하세요.

## 관련 문서

- [시각화/검증 가이드](./visualize.md)
- [Cypher 쿼리 모음](./cypers.md)
- [모델 설명](./explain.md)
