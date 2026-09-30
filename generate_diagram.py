from agent import graph

def save_mermaid_diagram():
    # Retrieve the Mermaid string from the compiled graph
    mermaid_code = graph.get_graph().draw_mermaid()
    
    print("--- MERMAID GRAPH DIAGRAM ---")
    print(mermaid_code)
    
    # Save it to a markdown file for your README
    with open("diagram.md", "w") as f:
        f.write("# Graph Architecture Diagram\n\n")
        f.write("```mermaid\n")
        f.write(mermaid_code)
        f.write("\n```\n")
        
    print("\n[SUCCESS] Mermaid diagram saved to 'diagram.md'!")

if __name__ == "__main__":
    save_mermaid_diagram()