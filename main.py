from typing import TypedDict, Literal

from langgraph.graph import END, START, StateGraph


class GraphState(TypedDict):
    user_input: str
    category: str
    output: str


def classify(state: GraphState) -> dict:
    """Classifie le texte selon sa longueur."""
    text = state["user_input"].strip()

    if not text:
        category = "empty"
    elif len(text) < 40:
        category = "short"
    else:
        category = "long"


def route_by_category(state: GraphState) -> Literal["handle_short", "handle_long"]:
    """Choisit le prochain node sans modifier le State."""
    if state["category"] == "short":
        return "handle_short"

    print("[ROUTER]", state["category"])

    return "handle_long"


def handle_empty(state: GraphState) -> dict:
    print("[NODE] classify")
    return {
        "output": (
            "Empty message."
        )
    }

def handle_short(state: GraphState) -> dict:
    print("[NODE] classify")
    return {
        "output": (
            f"Message court détecté : {state['user_input']}"
        )
    }


def handle_long(state: GraphState) -> dict:
    print("[NODE] classify")
    return {
        "output": (
            f"Message long détecté "
           f"({len(state['user_input'])} caractères)."
        )
    }


builder = StateGraph(GraphState)

# Nodes
builder.add_node("classify", classify)
builder.add_node("handle_short", handle_short)
builder.add_node("handle_long", handle_long)

# Edge fixe
builder.add_edge(START, "classify")

# Route conditionnelle
builder.add_conditional_edges(
    "classify",
    route_by_category,
    {
        "handle_short": "handle_short",
        "handle_long": "handle_long"
    },
)

# Sorties
builder.add_edge("handle_short", END)
builder.add_edge("handle_long", END)

# Compilation
app = builder.compile()

if __name__ == "__main__":
    examples = [
        "Bonjour LangGraph",
        (
            "Je souhaite comprendre précisément comment fonctionne "
            "le routage conditionnel dans LangGraph."
        ),
    ]

    for user_input in examples:
        result = app.invoke(
            {
                "user_input": user_input,
                "category": "",
                "output": "",
            }
        )

        print("\nInput:", result["user_input"])
        print("Category:", result["category"])
        print("Output:", result["output"])