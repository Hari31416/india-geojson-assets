"""Build a reproducible, versioned display/original boundary distribution."""

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mapshaper", type=Path, required=True)
    args = parser.parse_args()
    manifest = {"version": "v1", "builder": "mapshaper@0.7.86", "simplification": "5% weighted keep-shapes, precision=0.00001", "assets": {}}
    if (args.source / "manifest.json").exists():
        sources = [(args.source / entry["original"]["path"], Path(entry["legacy_path"]).relative_to("geojsons").with_suffix(".geojson.gz")) for entry in json.loads((args.source / "manifest.json").read_bytes())["assets"].values()]
    else:
        sources = [(path, path.relative_to(args.source)) for path in sorted(args.source.rglob("*.geojson.gz"))]
    for path, relative in sources:
        asset_id = relative.name.removesuffix(".geojson.gz").lower().replace("_", "-")
        original = gzip.decompress(path.read_bytes())
        source = json.loads(original)
        with tempfile.TemporaryDirectory() as temporary:
            input_path, output_path = Path(temporary) / "input.geojson", Path(temporary) / "display.geojson"
            input_path.write_bytes(original)
            subprocess.run([str(args.mapshaper), str(input_path), "-simplify", "5%", "keep-shapes", "-o", "format=geojson", "precision=0.00001", str(output_path)], check=True, capture_output=True)
            display = json.loads(output_path.read_bytes())
        assert len(display["features"]) == len(source["features"]), path
        for before, after in zip(source["features"], display["features"], strict=True):
            assert before["properties"] == after["properties"], path
            assert after.get("geometry") and after["geometry"].get("coordinates"), path
        source_key = next(key for key in ("STNAME_SH", "dtname", "district") if key in display["features"][0]["properties"])
        for feature in display["features"]:
            feature["properties"]["name"] = feature["properties"][source_key]
            if source_key == "district":
                feature["properties"]["dtname"] = feature["properties"][source_key]
        data = json.dumps(display, separators=(",", ":"), ensure_ascii=False).encode()
        if len(data) > 1024 * 1024:
            raise ValueError(f"Display geometry exceeds 1 MiB: {path}")
        entry = {"legacy_path": "geojsons/" + str(relative).removesuffix(".gz"), "feature_count": len(display["features"]), "feature_key": "name", "original_feature_key": source_key, "level": "states" if source_key == "STNAME_SH" else "districts"}
        for kind, payload in [("display", data), ("original", original)]:
            filename = f"{kind}/{asset_id}/{digest(payload)}.geojson.gz"
            compressed = gzip.compress(payload, mtime=0)
            target = args.output / filename
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(compressed)
            entry[kind] = {"path": filename, "sha256": digest(payload), "gzip_sha256": digest(compressed), "bytes": len(payload), "gzip_bytes": len(compressed)}
        manifest["assets"][asset_id] = entry
        print(asset_id, len(original), "->", len(data))
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (args.output / "manifests").mkdir(exist_ok=True)
    (args.output / "manifests/v1.json").write_bytes((args.output / "manifest.json").read_bytes())


if __name__ == "__main__":
    main()
