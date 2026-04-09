import hashlib
import json
import os
from datetime import datetime

class MatVerseLedger:
    def __init__(self, ledger_path="ledger.jsonl"):
        self.ledger_path = ledger_path
        self.entries = []
        self._load_ledger()

    def _load_ledger(self):
        if os.path.exists(self.ledger_path):
            with open(self.ledger_path, "r") as f:
                for line in f:
                    self.entries.append(json.loads(line))

    def append(self, proof_artifact):
        """Append a proof to the ledger with a link to the previous entry."""
        prev_hash = self.entries[-1]["entry_hash"] if self.entries else "0" * 64
        
        entry = {
            "index": len(self.entries),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "prev_hash": prev_hash,
            "proof_hash": proof_artifact["proof_hash"],
            "artifact_summary": {
                "input": proof_artifact.get("input"),
                "classification": proof_artifact.get("execution", {}).get("stdout", "").strip()
            }
        }
        
        # Compute entry hash (linking)
        entry_json = json.dumps(entry, sort_keys=True).encode()
        entry["entry_hash"] = hashlib.sha256(entry_json).hexdigest()
        
        self.entries.append(entry)
        with open(self.ledger_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
        
        return entry

    def get_merkle_root(self):
        """Compute Merkle Root of all entry hashes in the ledger."""
        if not self.entries:
            return None
        
        hashes = [e["entry_hash"] for e in self.entries]
        return self._compute_merkle_root(hashes)

    def _compute_merkle_root(self, hashes):
        if len(hashes) == 1:
            return hashes[0]
        
        new_hashes = []
        for i in range(0, len(hashes), 2):
            h1 = hashes[i]
            h2 = hashes[i+1] if i+1 < len(hashes) else h1
            combined = (h1 + h2).encode()
            new_hashes.append(hashlib.sha256(combined).hexdigest())
        
        return self._compute_merkle_root(new_hashes)

if __name__ == "__main__":
    # Test Ledger
    ledger = MatVerseLedger()
    print(f"Ledger initialized with {len(ledger.entries)} entries.")
    if ledger.entries:
        print(f"Current Merkle Root: {ledger.get_merkle_root()}")
