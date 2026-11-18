import os
import shutil
from pathlib import Path


def main() -> None:
    image = Path(__file__).with_name("entry.png")
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(image, output_dir / image.name)


if __name__ == "__main__":
    main()
