"""Deterministic pack validation; no model calls or random draws."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("reader", ROOT / "card_meanings.py")
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)


class PackTests(unittest.TestCase):
    def setUp(self):
        self.pack = reader.MeaningPack(ROOT)

    def test_complete_pack_and_distinct_identities(self):
        self.assertEqual(len(self.pack.cards), 22)
        self.assertTrue(self.pack.cards["atu_11_fortitude"]["title"].startswith("力量"))
        self.assertTrue(self.pack.cards["atu_08_justice"]["title"].startswith("正义"))

    def test_selection_is_deduplicated_and_token_sum_exact(self):
        ids = ["atu_00_fool", "atu_08_justice", "atu_00_fool"]
        selected = self.pack.select(ids)
        self.assertEqual(list(selected["cards"]), ids[:2])
        for encoding, tokens in selected["receipt"]["text_tokens"].items():
            self.assertEqual(tokens, sum(c["tokens"][encoding] for c in selected["cards"].values()))
        self.assertNotIn("text", selected["receipt"])

    def test_empty_enabled_pack_is_not_disabled(self):
        self.assertTrue(self.pack.select([])["receipt"]["enabled"])
        self.assertEqual(self.pack.select([])["cards"], {})
        self.assertFalse(reader.disabled_receipt()["enabled"])

    def test_unknown_identity_is_not_numeric_fallback(self):
        with self.assertRaises(reader.MeaningPackError):
            self.pack.select(["08"])

    def test_missing_pack_fails(self):
        with self.assertRaises(reader.MeaningPackError):
            reader.MeaningPack(ROOT / "missing")

    def with_copy(self, change):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "pack"
            shutil.copytree(ROOT / "cards", target / "cards")
            shutil.copy2(ROOT / "manifest.json", target)
            change(target)
            with self.assertRaises(reader.MeaningPackError):
                reader.MeaningPack(target)

    def test_modified_body_fails_checksum(self):
        self.with_copy(lambda p: (p / "cards/atu_00_fool.md").write_text("changed", encoding="utf-8"))

    def test_missing_card_fails(self):
        def change(path):
            data = json.loads((path / "manifest.json").read_text(encoding="utf-8"))
            del data["cards"]["atu_00_fool"]
            (path / "manifest.json").write_text(json.dumps(data), encoding="utf-8")
        self.with_copy(change)

    def test_file_escape_fails(self):
        def change(path):
            data = json.loads((path / "manifest.json").read_text(encoding="utf-8"))
            data["cards"]["atu_00_fool"]["file"] = "../outside.md"
            (path / "manifest.json").write_text(json.dumps(data), encoding="utf-8")
        self.with_copy(change)

    def test_local_defaults_and_explicit_off(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            self.assertIsNone(reader.resolve_pack(config_dir=target))
            (target / "meanings.local.json").write_text(
                json.dumps({"enabled": True, "pack": "pack"}), encoding="utf-8")
            self.assertEqual(reader.resolve_pack(config_dir=target), target / "pack")
            self.assertIsNone(reader.resolve_pack(disabled=True, config_dir=target))
            self.assertEqual(reader.resolve_pack(ROOT, config_dir=target), ROOT)
            (target / "meanings.local.json").write_text('{"enabled": true}', encoding="utf-8")
            with self.assertRaises(reader.MeaningPackError):
                reader.resolve_pack(config_dir=target)

    def test_export_has_no_private_editorial_links(self):
        for entry in self.pack.cards.values():
            for forbidden in ("../review/", "状态：", "E:\\", "E:/", "<!--"):
                self.assertNotIn(forbidden, entry["text"])


if __name__ == "__main__":
    unittest.main()
