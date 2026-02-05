import json
from datetime import datetime
from pathlib import Path
from safe_client import run_prompt, Prompt
        
def main():
    suite = json.load(open("suites/suite-001-dummy.json"))
    run_id = f"RUN-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    run_path = Path(f"logs/{run_id}")
    run_path.mkdir(parents=True)

    results = []
    for prompt_file in suite["prompts"]:
        case = json.load(open(prompt_file))
        prompt = Prompt(**case)
        response = run_prompt(prompt)
        print(case['text'])
        print(response)
        result = {"id": case["id"], "status": "ok", "response": response}
        results.append(result)
        json.dump(result, open(run_path / f"{case['id']}.json", "w"))
    
    summary = {"run_id": run_id, "total": len(results)}
    json.dump(summary, open(run_path / "summary.json", "w"))
    print(f"\n✅ Done: {run_path}")

if __name__ == "__main__":
    main()