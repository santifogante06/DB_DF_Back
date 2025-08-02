def load_queries(path):
    """Load SQL queries from a file."""
    queries = {}
    with open(path, "r") as file:
        key = ""
        buffer = ""
        for line in file:
            if line.startswith("--"):
                if key and buffer:
                    queries[key] = buffer.strip()
                key = line[2:].strip()
                buffer = ""
            else:
                buffer += line
        if key and buffer:
            queries[key] = buffer.strip()
    return queries
