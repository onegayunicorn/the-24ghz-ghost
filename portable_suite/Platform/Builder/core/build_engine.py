"""PAF directory structure & metadata writer — the build engine."""
import configparser
from pathlib import Path
from Platform.Builder.core.launcher_generator import LauncherGenerator

class BuildEngine:
    def __init__(self, output_base, metadata: dict):
        self.meta = metadata
        self.build_name = f"{metadata['name']}_{metadata['version']}"
        self.build_path = Path(output_base) / self.build_name

    def create_structure(self) -> Path:
        for folder in ["App", "Data", "AppInfo", "Other/help"]:
            (self.build_path / folder).mkdir(parents=True, exist_ok=True)
        (self.build_path / ".nomedia").write_text(
            "Excludes icons/assets from Android photo galleries.\n", encoding="utf-8")
        self._write_appinfo()
        LauncherGenerator(self.meta["name"], self.meta["executable"]).write_all(self.build_path)
        return self.build_path

    def _write_appinfo(self):
        cfg = configparser.ConfigParser()
        cfg["Details"] = {
            "Name": self.meta["name"],
            "Version": self.meta["version"],
            "Publisher": self.meta.get("publisher", ""),
            "Category": self.meta.get("category", "Utilities"),
            "Description": self.meta.get("description", ""),
            "Executable": self.meta["executable"],
        }
        with open(self.build_path / "AppInfo" / "appinfo.ini", "w", encoding="utf-8") as f:
            cfg.write(f)
