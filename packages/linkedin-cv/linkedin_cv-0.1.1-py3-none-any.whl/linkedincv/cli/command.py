import subprocess
from pathlib import Path


def build(tex_script_path: Path, out_folder: Path) -> None:
    COMMAND = f"""
        xelatex -synctex=1 -interaction=nonstopmode {tex_script_path}
        mv main.pdf {out_folder}/
    """
    Path(out_folder).mkdir(parents=True, exist_ok=True)
    subprocess.run(COMMAND, shell=True, check=True)
