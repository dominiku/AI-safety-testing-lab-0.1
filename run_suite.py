# run_suite.py (minimal version)
import json
from datetime import datetime
from pathlib import Path
# from safe_client import run_prompt

def main():
    # 1. SETUP
    suite = json.load(open("suites/suite-001-dummy.json"))
    run_id = f"RUN-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    print("\n",run_id)
    run_path = Path(f"logs/{run_id}")
    print(run_path)
    run_path.mkdir(parents=True)
    
    # 2. EXECUTE
    results = []
    for prompt_file in suite["prompts"]:
        case = json.load(open(prompt_file))
        
        try:
            response = run_prompt(case["text"])
            result = {"id": case["id"], "status": "ok", "response": response}
        except Exception as e:
            result = {"id": case["id"], "status": "error", "error": str(e)}
        
        results.append(result)
        json.dump(result, open(run_path / f"{case['id']}.json", "w"))
        print(f"✓ {case['id']}")

        print(result)
    
    # 3. TEARDOWN
    summary = {"run_id": run_id, "total": len(results)}
    json.dump(summary, open(run_path / "summary.json", "w"))
    print(f"\n✅ Done: {run_path}")

if __name__ == "__main__":
    main()