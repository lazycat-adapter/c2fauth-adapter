from pathlib import Path

import yaml


root = Path(__file__).resolve().parents[1]
manifest = yaml.safe_load((root / "lzc-manifest.yml").read_text())
package = yaml.safe_load((root / "package.yml").read_text())
assert package["package"] == "cloud.lazycat.app.c2fauth"
assert manifest["services"]["2fauth"]["binds"] == ["/lzcapp/var/data:/2fauth"]
print("2FAuth adapter contract passed")
