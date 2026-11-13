from mcp.server.mcpserver import MCPServer
from .answer import load_rag, answer_question

# Création du serveur MCP
mcp = MCPServer("rag-assistant")

# Chargement des ressources du RAG
chunks, embeddings, model = load_rag()

@mcp.tool()
def ask_rag(question: str) -> str:
    """Répond à une question en s'appuyant sur le corpus mathématique."""
    return answer_question(question, chunks, embeddings, model)

if __name__ == "__main__":
    mcp.run()