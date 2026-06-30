# graph_utils.py
from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

class GraphDB:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            NEO4J_URI, 
            auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
        )

    def close(self):
        self.driver.close()

    def run_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return result.data()

    def build_sample_graph(self):
        """Create sample graph for demo"""
        queries = [
            # Create nodes
            "MERGE (p:Person {name: 'Satyasai Esarapu', role: 'Senior AI Engineer'})",
            "MERGE (c:Company {name: 'xAI Solutions', location: 'Hyderabad'})",
            "MERGE (proj:Project {name: 'Advanced RAG System'})",
            "MERGE (tech:Technology {name: 'Graph RAG'})",
            
            # Create relationships
            "MATCH (p:Person), (c:Company) WHERE p.name = 'Satyasai Esarapu' AND c.name = 'xAI Solutions' MERGE (p)-[:WORKS_AT]->(c)",
            "MATCH (p:Person), (proj:Project) WHERE p.name = 'Satyasai Esarapu' MERGE (p)-[:WORKED_ON]->(proj)",
            "MATCH (proj:Project), (tech:Technology) WHERE proj.name = 'Advanced RAG System' MERGE (proj)-[:USES]->(tech)"
        ]
        
        for q in queries:
            self.run_query(q)
        
        return "Sample graph created successfully!"