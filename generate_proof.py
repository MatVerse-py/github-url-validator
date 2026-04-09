import subprocess
import hashlib
import json
import sys
import os
from datetime import datetime

def run_script(script_path, test_input):
    try:
        result = subprocess.run(
            [sys.executable, script_path, test_input],
            capture_output=True,
            text=True,
            timeout=10
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except Exception as e:
        return {"error": str(e)}

def hash_file(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def get_git_info():
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        remote = subprocess.check_output(["git", "remote", "get-url", "origin"], text=True).strip()
        return {"commit": commit, "remote": remote}
    except:
        return None

def generate_proof(script_path, test_input):
    execution = run_script(script_path, test_input)
    git_info = get_git_info()
    
    proof = {
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "environment": {
            "python_version": sys.version,
            "os": sys.platform
        },
        "git": git_info,
        "artifacts": {
            "script": {
                "path": script_path,
                "sha256": hash_file(script_path)
            }
        },
        "input": test_input,
        "execution": execution,
    }

    # Canonical JSON for hashing
    canonical_json = json.dumps(proof, sort_keys=True).encode()
    proof["proof_hash"] = hashlib.sha256(canonical_json).hexdigest()

    return proof

if __name__ == "__main__":
    script = "github_url_validator.py"
    test_url = "https://github.com/repos?q=admin%3A%40me"

    if not os.path.exists(script):
        print(f"Error: {script} not found")
        sys.exit(1)

    proof = generate_proof(script, test_url)

    with open("execution_proof.json", "w") as f:
        json.dump(proof, f, indent=2)

    print(f"Proof generated successfully. Hash: {proof['proof_hash']}")
