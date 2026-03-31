import os
from neo4j import GraphDatabase

# Neo4j 접속 정보 (본인의 환경에 맞게 수정하세요)
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"  # 설정한 비밀번호로 변경하세요.

# 로컬 파일 경로 (Windows 절대 경로로 변환)
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.abspath(os.path.join(BASE_PATH, "..", "data", "rdf", "library-schema.ttl")).replace("\\", "/")
OWL_PATH = os.path.abspath(os.path.join(BASE_PATH, "..", "data", "owl", "library.owl")).replace("\\", "/")
DATA_PATH = os.path.abspath(os.path.join(BASE_PATH, "..", "data", "rdf", "sample-data.ttl")).replace("\\", "/")

class Neo4jOntologyImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def run_query(self, query, message="Executing query..."):
        print(message)
        with self.driver.session() as session:
            try:
                result = session.run(query)
                return result
            except Exception as e:
                print(f"Error: {e}")
                return None

    def setup_n10s(self):
        # 1. n10s 초기 설정 (이미 되어있을 수 있으나 안전을 위해 실행)
        self.run_query("CREATE CONSTRAINT n10s_unique_uri IF NOT EXISTS FOR (r:Resource) REQUIRE r.uri IS UNIQUE", "Creating constraint...")
        self.run_query("CALL n10s.graphconfig.init()", "Initializing n10s graph config...")
        
    def import_data(self):
        # 2. 스키마 및 데이터 임포트
        # Neo4j Desktop/Server에서 'file:///' 프로토콜로 로컬 파일에 접근하려면 neo4j.conf의 
        # dbms.directories.import 설정을 확인해야 합니다.
        # 여기서는 절대 경로를 직접 사용하는 방식을 예제로 둡니다.
        
        print(f"Importing Schema from: {SCHEMA_PATH}")
        self.run_query(f"CALL n10s.rdf.import.fetch('file:///{SCHEMA_PATH}', 'Turtle')", "Importing library-schema.ttl...")
        
        print(f"Importing OWL from: {OWL_PATH}")
        self.run_query(f"CALL n10s.rdf.import.fetch('file:///{OWL_PATH}', 'Turtle')", "Importing library.owl...")
        
        print(f"Importing Sample Data from: {DATA_PATH}")
        self.run_query(f"CALL n10s.rdf.import.fetch('file:///{DATA_PATH}', 'Turtle')", "Importing sample-data.ttl...")

    def verify(self):
        print("\n--- Verification ---")
        query = "MATCH (n:Resource) RETURN count(n) as count"
        result = self.run_query(query, "Checking node count...")
        if result:
            for record in result:
                print(f"Total nodes (Resources): {record['count']}")

        query = "MATCH (n:lib__LibraryResource) RETURN n.lib__title as title"
        result = self.run_query(query, "Listing resources...")
        if result:
            print("Resources in database:")
            for record in result:
                print(f"- {record['title']}")

if __name__ == "__main__":
    importer = Neo4jOntologyImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    try:
        importer.setup_n10s()
        importer.import_data()
        importer.verify()
        print("\nImport Complete! Neo4j Browser에서 데이터를 확인하세요.")
    finally:
        importer.close()
