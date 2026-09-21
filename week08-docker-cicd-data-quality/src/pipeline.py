# The actual "pipeline" logic. Kept tiny on purpose — this project is about
# practicing the tooling (Docker/CI/tests) around code, not complex logic.

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

# This block only runs when the file is executed directly (e.g. `python src/pipeline.py`),
# NOT when it's imported elsewhere (like in the test file below) — that's what lets
# tests import add/subtract without this print statement firing every time.
if __name__ == "__main__":
    print("Pipeline ran:", add(2, 3))