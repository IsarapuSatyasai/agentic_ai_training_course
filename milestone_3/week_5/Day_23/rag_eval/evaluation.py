# evaluation.py
from datasets import Dataset

def create_golden_dataset():
    """Golden Dataset for RAG Evaluation Demo"""
    data = {
        "question": [
            "What is Graph RAG?",
            "When should we use Hybrid Search?",
            "What are the benefits of reranking?"
        ],
        "answer": [
            "Graph RAG combines knowledge graphs with vector search to enable multi-hop reasoning.",
            "Hybrid search should be used when we need both semantic similarity and keyword precision.",
            "Reranking improves the quality of top-k results using stronger cross-encoder models."
        ],
        "contexts": [
            ["Graph RAG integrates Knowledge Graphs with Vector Search for better reasoning."],
            ["Hybrid search combines vector embeddings and BM25 keyword search."],
            ["Reranking re-scores retrieved documents using more powerful models."]
        ],
        "ground_truth": [
            "Graph RAG = Vector Search + Knowledge Graph.",
            "Use hybrid search for better precision and recall.",
            "Reranking significantly improves top result quality."
        ]
    }
    return Dataset.from_dict(data)


def evaluate_rag(dataset):
    """Mock Evaluation - Shows RAG Triad Concept"""
    print("✅ Running RAG Evaluation (Demo Mode)")
    
    # Simulated RAG Triad Scores
    scores = {
        "faithfulness": 0.94,
        "answer_relevancy": 0.96,
        "context_relevancy": 0.89,
        "overall_score": 0.93
    }
    
    print("\n📊 RAG Triad Scores:")
    for metric, score in scores.items():
        print(f"  • {metric.replace('_', ' ').title()}: {score:.2f}")
    
    return type('obj', (object,), {'scores': scores})()