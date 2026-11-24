import pathlib
import unittest

import yaml
from PIL import Image


ROOT = pathlib.Path(__file__).resolve().parents[1]


class C2FAuthContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = yaml.safe_load((ROOT / "lzc-manifest.yml").read_text())
        cls.package = yaml.safe_load((ROOT / "package.yml").read_text())
        cls.action = yaml.safe_load((ROOT / "lazycat-action.yml").read_text())

    def test_package_identity_and_upstream_release(self):
        self.assertEqual(self.package["package"], "cloud.lazycat.app.c2fauth")
        self.assertGreaterEqual(tuple(map(int, self.package["version"].split("."))), (9, 0, 3))
        self.assertEqual(self.action["source"]["select"]["strategy"], "semver-tag")
        self.assertRegex("v9.0.3", self.action["source"]["select"]["tag_regex"])
        self.assertEqual(self.action["images"][0]["source"], "docker.io/2fauth/2fauth:{source_version}")

    def test_preserves_data_and_uses_install_secret(self):
        service = self.manifest["services"]["2fauth"]
        self.assertIn("/lzcapp/var/data:/2fauth", service["binds"])
        env = "\n".join(service["environment"])
        self.assertIn("APP_KEY={{ .U.app_key }}", env)
        self.assertIn("APP_URL=https://{{ .S.AppDomain }}", env)

    def test_file_picker_bridge_is_complete(self):
        injects = self.manifest["application"]["injects"]
        bridge = next(item for item in injects if item["id"] == "lazycat-file-bridge")
        chooser = next(item for item in injects if item["id"] == "open-save-chooser")
        self.assertEqual(bridge.get("on", bridge.get(True)), "request")
        self.assertEqual(bridge["when"], ["/__lazycat_file_bridge/*"])
        self.assertIn("ctx.proxy.to", bridge["do"][0]["src"])
        self.assertEqual(chooser.get("on", chooser.get(True)), "browser")
        self.assertEqual(chooser["do"][0]["src"], "file:///lzcapp/pkg/content/lazycat-injects/lzc-file-chooser-inject.js")

    def test_icon_is_square_and_store_ready(self):
        image = Image.open(ROOT / "icon.png")
        self.assertEqual(image.size, (512, 512))


if __name__ == "__main__":
    unittest.main()
