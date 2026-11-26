"""Create synthetic PRs via the sandbox's GitHub Actions identity."""

import json
import os
import subprocess

REPO = "yangbobo2021/anthropic-sdlc-codeowners-lab"
CASES = {"ci-override": "codeowners-ruleset"}


def main():
    assert os.environ["GITHUB_REPOSITORY"] == REPO
    assert os.environ["GITHUB_REF"] == "refs/heads/codex/owner-ruleset-driver"
    for case, base in CASES.items():
        head = f"codex/owner-case-{case}"
        payload = {"title": f"CODEOWNERS fixture {case}", "head": head, "base": base,
                   "body": "Synthetic test input for CODEOWNERS review requests.", "draft": False}
        args = ["gh", "api", f"repos/{REPO}/pulls", "--method", "POST", "--input", "-"]
        result = subprocess.run(args, input=json.dumps(payload), capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(f"{case}: {result.stderr.strip()}")
        pr = json.loads(result.stdout)
        assert pr["user"]["login"] == "github-actions[bot]" and pr["user"]["type"] == "Bot"
        assert pr["base"]["ref"] == base and pr["head"]["ref"] == head
        record = {"case":case,"pr":pr["number"],"url":pr["html_url"],"author":pr["user"]["login"],
                  "base":pr["base"]["sha"],"head":pr["head"]["sha"]}
        print("SDLC0057_PR="+json.dumps(record,sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
