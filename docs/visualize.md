# 온톨로지 시각화 및 확인 가이드 (Protege & Neo4j)

이 가이드는 구축된 `library.owl` 및 `sample-data.ttl` 파일을 **Protege**와 **Neo4j**에서 확인하고 활용하는 방법을 설명합니다.

---

## 1. Protege에서 확인하기 (추론 및 구조 확인)

Protege는 온톨로지 설계 및 추론을 위한 가장 표준적인 도구입니다.

### ① 파일 열기
1. [Protege 공식 웹사이트](https://protege.stanford.edu/)에서 프로그램을 다운로드하여 실행합니다.
2. `File` -> `Open` 메뉴를 통해 `data/rdf/sample-data.ttl` 파일을 엽니다.
   * **중요:** `sample-data.ttl` 파일은 내부적으로 `library.owl`과 `library-schema.ttl`을 임포트하도록 설정되어 있어, 이 파일 하나만 열면 모든 구조와 데이터를 한꺼번에 불러올 수 있습니다.
   * 만약 파일을 찾지 못한다는 팝업이 뜨면, 같은 폴더 내의 해당 파일들을 수동으로 지정해 주세요.

### ② 클래스 및 데이터 확인
1. **클래스 계층:** `Entities` -> `Classes` 탭에서 전체 구조를 확인합니다.
2. **데이터(Individuals):** `Entities` -> `Individuals` 탭을 클릭하면 `George Orwell`, `1984` 등의 샘플 데이터를 볼 수 있습니다.

### ③ 추론(Reasoner) 실행 및 결과 확인
1. 상단 메뉴 `Reasoner` -> `HermiT`을 선택합니다.
2. `Reasoner` -> `Start reasoner`를 클릭합니다.
3. **추론 결과 확인:**
   * `1984` 책을 클릭했을 때 `hasAuthor` 관계뿐만 아니라 역관계인 `wrote`가 자동으로 추론되는지 확인합니다.
   * `SymmetricProperty` 설정에 의해 `1984`와 `Brave New World`가 양방향으로 연결되는지 확인합니다.
   * **`locatedAt` 추론 확인:** `1984` 책이 `Shelf_A1`에 있고, `Shelf_A1`이 `Floor_1` 내부에 있을 때, `1984`가 `Floor_1`에 `locatedAt` 되어 있는지(Property Chain) 확인합니다.
   * `Inferred Hierarchy`를 통해 논리적으로 모순이 없는지(Inconsistent 클래스가 없는지) 확인합니다.

---

## 2. Neo4j에서 확인하기 (그래프 시각화)

Neo4j는 데이터를 그래프 형태로 시각화하고 쿼리(Cypher)를 던지기에 최적화되어 있습니다. RDF 데이터를 다루기 위해 **neosemantics (n10s)** 플러그인이 필요합니다.

### ① 사전 준비 (자동화 스크립트 사용 시)
제공된 Python 스크립트를 사용하여 Neo4j에 데이터를 자동으로 임포트할 수 있습니다.

1.  **준비 사항:**
    *   Neo4j Desktop이 설치되어 있고 데이터베이스가 실행 중이어야 합니다.
    *   `n10s (neosemantics)` 플러그인이 설치되어 있어야 합니다.
    *   Python 라이브러리 설치: `pip install neo4j`
2.  **스크립트 실행:**
    *   [`scripts/import_to_neo4j.py`](../scripts/import_to_neo4j.py) 파일을 열어 `NEO4J_PASSWORD`를 본인의 설정에 맞게 수정합니다.
    *   터미널에서 실행: `python scripts/import_to_neo4j.py`
3.  **결과 확인:**
    *   Neo4j Browser에서 다음 쿼리를 실행하여 시각화된 그래프를 확인합니다.
    ```cypher
    MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 50
    ```

### ② 수동 임포트 방법
Neo4j Desktop을 설치하고 다음 단계를 따릅니다.

### ② n10s 초기화 (Cypher 실행)
Neo4j Browser에서 다음 명령어를 실행하여 그래프 구성을 초기화합니다.
```cypher
CREATE CONSTRAINT n10s_unique_uri FOR (r:Resource) REQUIRE r.uri IS UNIQUE;
CALL n10s.graphconfig.init();
```

### ③ RDF 데이터 임포트
로컬 파일 경로를 사용하여 데이터를 불러옵니다. (Windows 경로 주의: `file:///D:/...` 형식)
```cypher
// 1. 온톨로지(OWL) 임포트
CALL n10s.onto.import.fetch("file:///D:/수업자료/ontology/data/owl/library.owl", "Turtle");

// 2. 샘플 데이터(RDF) 임포트
CALL n10s.rdf.import.fetch("file:///D:/수업자료/ontology/data/rdf/sample-data.ttl", "Turtle");
```

### ④ 데이터 확인 및 쿼리
모든 노드와 관계를 시각적으로 확인합니다.
```cypher
MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 100;
```

**특정 작가가 쓴 책 찾기 예시:**
```cypher
MATCH (a:Author {name: "George Orwell"})-[:wrote]->(b:Book)
RETURN b.title;
```

---

## 3. 요약: 어떤 도구가 더 좋을까요?

*   **논리 검증 및 추론**이 목적이라면? → **Protege**를 추천합니다.
    *   "이 설계에 모순이 없는가?", "추론을 통해 숨겨진 관계가 잘 나오는가?"를 확인하기 좋습니다.
*   **대규모 데이터 시각화 및 검색**이 목적이라면? → **Neo4j**를 추천합니다.
    *   "데이터가 어떻게 얽혀 있는가?", "복잡한 경로를 따라 데이터를 검색하고 싶은가?"를 확인하기 좋습니다.
