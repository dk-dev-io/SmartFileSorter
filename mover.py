from pathlib import Path
import shutil

class Mover:
    def move(self, src: Path, target_paths: list, file_name: str):
        for dest in target_paths:
            dest_path = Path(dest) / file_name
            counter = 1

            while dest_path.exists():
                dest_path = Path(dest) / f"{dest_path.stem}_{counter}{dest_path.suffix}"
                counter += 1

            try:
                shutil.copy2(src, dest_path)
            except Exception:
                pass 

        if src.exists():
            try:
                src.unlink()
            except Exception:
                pass