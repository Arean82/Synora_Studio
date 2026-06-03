# server/logic/graph_rag.py
import re
import networkx as nx

class GraphManager:
    """
    Lightweight, ultra-fast Knowledge Graph engine powered by NetworkX.
    Extracts structural relations (AST-style heuristics) from raw text/code
    to provide multi-hop GraphRAG context.
    """
    def __init__(self):
        self.graph = nx.DiGraph()
        
    def clear(self):
        """Wipes the knowledge graph."""
        self.graph.clear()
        
    def ingest_document(self, text: str):
        """
        Parses textual document to build nodes and edges.
        Uses fast heuristic Regex for Option A implementation.
        """
        if not text:
            return
            
        # Parse Classes and Inheritance
        class_matches = re.finditer(r'class\s+([A-Za-z0-9_]+)(?:\((.*?)\))?:', text)
        for match in class_matches:
            class_name = match.group(1)
            self.graph.add_node(class_name, type="Class")
            
            # Inheritance mapping
            bases = match.group(2)
            if bases:
                for base in bases.split(','):
                    base = base.strip()
                    if base:
                        self.graph.add_node(base, type="Class")
                        self.graph.add_edge(class_name, base, relation="inherits_from")
        
        # Parse Functions
        func_matches = re.finditer(r'def\s+([A-Za-z0-9_]+)\s*\(', text)
        for match in func_matches:
            func_name = match.group(1)
            self.graph.add_node(func_name, type="Function")
            
        # Parse Imports/Dependencies
        import_matches = re.finditer(r'^(?:from\s+([A-Za-z0-9_\.]+)\s+)?import\s+([A-Za-z0-9_\.\,\s]+)', text, re.MULTILINE)
        for match in import_matches:
            module = match.group(1)
            items = match.group(2)
            if items:
                for item in items.split(','):
                    item = item.strip()
                    if item:
                        self.graph.add_node(item, type="Dependency")
                        if module:
                            self.graph.add_node(module, type="Module")
                            self.graph.add_edge(item, module, relation="imported_from")

    def query_subgraph(self, query: str, depth: int = 1) -> str:
        """
        Extracts a localized sub-graph neighborhood based on semantic 
        keyword overlap with the query.
        """
        if self.graph.number_of_nodes() == 0 or not query:
            return ""
            
        # 1. Find seed nodes that match query tokens
        query_tokens = set(re.findall(r'\w+', query.lower()))
        seed_nodes = []
        for node in self.graph.nodes():
            if str(node).lower() in query_tokens:
                seed_nodes.append(node)
                
        # 2. Fallback: if no exact match, just grab the most central/connected nodes
        if not seed_nodes:
            degrees = sorted(self.graph.degree, key=lambda x: x[1], reverse=True)
            seed_nodes = [n for n, d in degrees[:5] if d > 0]
            if not seed_nodes:
                return ""
                
        # 3. Extract neighborhood up to depth limits
        subgraph_nodes = set(seed_nodes)
        for _ in range(depth):
            current_layer = set(subgraph_nodes)
            for node in current_layer:
                subgraph_nodes.update(self.graph.predecessors(node))
                subgraph_nodes.update(self.graph.successors(node))
                
        sub_g = self.graph.subgraph(subgraph_nodes)
        
        # 4. Format structured data for LLM Context Prompt Injection
        results = ["--- LOCAL KNOWLEDGE GRAPH (GraphRAG) ---"]
        results.append(f"Found {sub_g.number_of_nodes()} related entities and {sub_g.number_of_edges()} relationships mapped to your query:")
        
        for u, v, data in sub_g.edges(data=True):
            relation = data.get('relation', 'is_related_to')
            results.append(f" - [{u}] --({relation})--> [{v}]")
            
        # Add isolated standalone nodes that matched but had no edges
        isolated = list(nx.isolates(sub_g))
        if isolated:
            results.append("\nStandalone Entities Found:")
            for iso in isolated[:10]:
                n_type = self.graph.nodes[iso].get("type", "Entity")
                results.append(f" - [{iso}] (Type: {n_type})")
                
        return "\n".join(results) + "\n----------------------------------------\n"
