# 온톨로지 시각화 및 검증 가이드 (Protege & Neo4j)

이 문서는 `library.owl`, `library-schema.ttl`, `sample-data.ttl`을
Protege와 Neo4j에서 확인하는 방법을 설명합니다.

## 1. Protege에서 확인

1. Protege를 실행합니다.
2. `data/rdf/sample-data.ttl`을 엽니다.
3. import가 자동으로 해결되지 않으면 아래 파일을 수동으로 지정합니다.
- `data/owl/library.owl`
- `data/rdf/library-schema.ttl`

확인 포인트:
- 클래스 계층: `LibraryResource`, `Book`, `EBook`, `Multimedia`, `Author`, `LibraryUser`, `Loan`, `Reservation`
- 주요 속성: `hasAuthor`, `wrote`, `locatedAt`, `within`, `isRelatedTo`
- 개체 URI prefix: `도서_`, `전자책_`, `멀티미디어_`, `저자_`, `출판사_`, `장르_`, `이용자_`, `대출_`, `예약_`, `층_`, `서가_`

## 2. Neo4j 재적재 순서 (clear -> import)

프로젝트 스크립트:
- `scripts/import_to_neo4j.py`

실행:
```bash
python scripts/import_to_neo4j.py
```

현재 스크립트 실행 순서:
1. `MATCH (n) DETACH DELETE n`으로 기존 그래프 삭제
2. `n10s` 제약/설정 초기화
3. `library-schema.ttl` -> `library.owl` -> `sample-data.ttl` 순서로 import
4. 검증(`verify`) 실행

현재 스크립트 특징:
- 쿼리 결과는 세션 안에서 `list(result)`로 소비해 `ResultConsumedError`를 방지합니다.
- 검증은 `LibraryResource` 라벨을 고정 가정하지 않고 URI prefix 기반으로 수행합니다.
- `hasAuthor` 관계가 `저자_` 개체를 가리키는지 무결성 체크를 수행합니다.

## 3. verify()가 검사하는 항목

1. 전체 `:Resource` 노드 수
2. 한글 prefix별 개수 일치 여부
- `도서_`(2), `전자책_`(1), `멀티미디어_`(1)
- `저자_`(3), `출판사_`(3), `장르_`(3)
- `이용자_`(2), `대출_`(1), `예약_`(1)
- `층_`(2), `서가_`(2)
3. 자료 리소스(`도서_`, `전자책_`, `멀티미디어_`)의 `title` 조회
4. `hasAuthor` 관계 대상 무결성 점검

## 4. 빠른 시각화 쿼리

```cypher
MATCH (n)-[r]->(m)
RETURN n, r, m
LIMIT 100;
```

```cypher
MATCH (n:Resource)
RETURN count(n) AS total_resources;
```
