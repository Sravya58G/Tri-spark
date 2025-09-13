from typing import List, Dict
import datetime
class SessionStore:
    def __init__(self):
        self.history = []  # list of dicts with keys: question, answer, sources, timestamp

    def add(self, question: str, answer: str, sources: List[str]):
        entry = {'question': question, 'answer': answer, 'sources': sources, 'timestamp': datetime.datetime.utcnow().isoformat()}
        self.history.append(entry)

    def export_txt(self):
        lines = []
        for i, e in enumerate(self.history, 1):
            lines.append(f"Q{i}: {e['question']}")
            lines.append(f"A{i}: {e['answer']}")
            lines.append(f"Sources: {', '.join(e['sources'])}")
            lines.append("---")
        return "\n".join(lines)
