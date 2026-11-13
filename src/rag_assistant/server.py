from mcp.server.mcpserver import MCPServer
from rag_assistant.answer import load_rag, answer_question

# Création du serveur MCP
mcp = MCPServer("rag-assistant")

# Chargement des ressources du RAG
chunks, embeddings, model = load_rag()

# Déclaration d'un premier outil
@mcp.tool()
def addition(a: int, b: int) -> int:
    """Additionne deux nombres entiers."""
    return a + b

@mcp.tool()
def ask_rag(question: str) -> str:
    """Répond à une question en s'appuyant sur le corpus mathématique."""
    return answer_question(question, chunks, embeddings, model)

if __name__ == "__main__":
    mcp.run()