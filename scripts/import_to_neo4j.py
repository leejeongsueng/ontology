import os
from neo4j import GraphDatabase

NEO4J_URI = "neo4j://127.0.0.1:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "qwerty12!@"

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
                return list(result)
            except Exception as e:
                print(f"Error: {e}")
                return None

    def setup_n10s(self):
        self.run_query(
            """
            CREATE CONSTRAINT n10s_unique_uri IF NOT EXISTS
            FOR (r:Resource) REQUIRE r.uri IS UNIQUE
            """,
            "Ensuring n10s URI uniqueness constraint..."
        )

        self.run_query(
            """CALL n10s.graphconfig.init({ handleVocabUris: "MAP" })""",
            "Initializing n10s config (MAP mode)..."
        )

    def clear_database(self):
        self.run_query(
            "MATCH (n) DETACH DELETE n",
            "Clearing existing nodes and relationships..."
        )

    def import_data(self):
        print(f"Importing Schema from: {SCHEMA_PATH}")
        self.run_query(
            f"CALL n10s.rdf.import.fetch('file:///{SCHEMA_PATH}', 'Turtle')",
            "Importing library-schema.ttl..."
        )

        print(f"Importing OWL from: {OWL_PATH}")
        self.run_query(
            f"CALL n10s.rdf.import.fetch('file:///{OWL_PATH}', 'RDF/XML')",
            "Importing library.owl (RDF/XML)..."
        )

        print(f"Importing Sample Data from: {DATA_PATH}")
        self.run_query(
            f"CALL n10s.rdf.import.fetch('file:///{DATA_PATH}', 'Turtle')",
            "Importing sample-data.ttl..."
        )

    def verify(self):
        print("\n--- Verification ---")

        result = self.run_query(
            "MATCH (n:Resource) RETURN count(n) AS count",
            "Counting Resource nodes..."
        )
        if result is not None and len(result) > 0:
            print(f"Total Resource nodes: {result[0]['count']}")

        # Sample-data individual counts by URI prefix (Koreanized dataset).
        expected_prefix_counts = {
            "도서_": 2,
            "전자책_": 1,
            "멀티미디어_": 1,
            "저자_": 3,
            "출판사_": 3,
            "장르_": 3,
            "이용자_": 2,
            "대출_": 1,
            "예약_": 1,
            "층_": 2,
            "서가_": 2,
        }
        print("\nSample-data node counts (by URI prefix):")
        for prefix, expected in expected_prefix_counts.items():
            count_result = self.run_query(
                f"""
                MATCH (n:Resource)
                WHERE n.uri STARTS WITH 'http://example.org/library#{prefix}'
                RETURN count(n) AS count
                """,
                f"- Counting `{prefix}` nodes..."
            )
            actual = count_result[0]["count"] if count_result else 0
            status = "OK" if actual == expected else f"MISMATCH (expected {expected})"
            print(f"  {prefix:12} -> {actual} [{status}]")

        # Titles for concrete library resources from sample-data.
        resources_result = self.run_query(
            """
            MATCH (n:Resource)
            WHERE n.uri STARTS WITH 'http://example.org/library#도서_'
               OR n.uri STARTS WITH 'http://example.org/library#전자책_'
               OR n.uri STARTS WITH 'http://example.org/library#멀티미디어_'
            WITH n, [k IN keys(n) WHERE toLower(k) CONTAINS 'title'] AS title_keys
            RETURN n.uri AS uri,
                   CASE WHEN size(title_keys) > 0 THEN n[title_keys[0]] ELSE null END AS title,
                   CASE WHEN size(title_keys) > 0 THEN title_keys[0] ELSE null END AS title_key
            ORDER BY uri
            """,
            "\nListing resource titles from sample-data..."
        )
        if resources_result is not None and len(resources_result) > 0:
            print("Library resources:")
            for record in resources_result:
                print(f"- {record['uri']} | title={record['title']} (key={record['title_key']})")
        else:
            print("No sample library resources found by URI prefix.")

        # Validate hasAuthor targets in a schema-agnostic way.
        bad_author_links = self.run_query(
            """
            MATCH (r:Resource)-[rel]->(a:Resource)
            WHERE toLower(type(rel)) CONTAINS 'hasauthor'
              AND (a.uri IS NULL OR NOT a.uri STARTS WITH 'http://example.org/library#저자_')
            RETURN r.uri AS resource_uri, type(rel) AS rel_type, a.uri AS author_uri
            """,
            "\nChecking hasAuthor link integrity..."
        )
        if bad_author_links:
            print("Warning: invalid hasAuthor target(s) found:")
            for record in bad_author_links:
                print(f"- {record['resource_uri']} -[{record['rel_type']}]-> {record['author_uri']}")


if __name__ == "__main__":
    importer = Neo4jOntologyImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    try:
        importer.clear_database()
        importer.setup_n10s()
        importer.import_data()
        importer.verify()
        print("\nImport Complete! Check Neo4j Browser.")
    finally:
        importer.close()
