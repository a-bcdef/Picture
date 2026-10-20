
import json
from pathlib import Path
from urllib.parse import quote
import os

REPOSITORY = os.environ.get(
    "GITHUB_REPOSITORY", "a-bcdef/Picture"
)
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "ligeicon.json"

IMAGE_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".webp",
    ".gif", ".ico", ".svg", ".bmp"
}

def main():
    owner, repo = REPOSITORY.split("/", 1)
    icons = []

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        if path == OUTPUT or path.name == "generate_icons.py":
            continue
        if ".git" in path.parts or ".github" in path.parts:
            continue
        if path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        relative = path.relative_to(ROOT).as_posix()
        url = (
            f"https://raw.githubusercontent.com/{owner}/{repo}/"
            f"{quote(BRANCH, safe='')}/{quote(relative, safe='/')}"
        )

        icons.append({
            "name": path.stem,
            "url": url
        })

    data = {
        "name": "Picture",
        "description": "我的图片图标库",
        "icons": icons
    }

    OUTPUT.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )

    print(f"共生成 {len(icons)} 个图标索引")

if __name__ == "__main__":
    main()
