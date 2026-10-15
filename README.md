# India GeoJSON assets

Versioned state and district boundaries for map charts. Every asset has both:

- `original/`: full-resolution, unchanged original GeoJSON content, gzip-compressed.
- `display/`: smaller, topology-aware simplified GeoJSON for interactive maps.

`manifest.json` lists all 38 assets, legacy filenames, feature counts, original
location keys, and SHA-256 checksums for compressed and decompressed files.
`manifests/v1.json` freezes the first release. Filenames contain the content hash;
do not overwrite published files or tags when adding a new version.

All display features expose **`properties.name`**, whether they are states or
districts. Existing properties remain available, including `STNAME_SH` for states
and `dtname` for districts. Sikkim's source `district` field also has a `dtname`
compatibility alias in display files. Original files retain their source schemas.

## Download selected assets

From a GenBI checkout:

```sh
python3 scripts/sync_geography_assets.py --asset india --asset uttar-pradesh-districts
python3 scripts/sync_geography_assets.py --asset maharashtra-districts --original
```

Without cloning the full data repository, download the manifest and helper:

```sh
mkdir india-boundaries
cd india-boundaries
curl -fsSLO https://raw.githubusercontent.com/Hari31416/india-geojson-assets/v1/manifest.json
curl -fsSLO https://raw.githubusercontent.com/Hari31416/india-geojson-assets/v1/sync_geography_assets.py
python3 sync_geography_assets.py --asset bihar-districts --original --output selected
```

With no `--asset`, the helper downloads all display versions. `--original` adds
the corresponding full-resolution versions. Checksums are verified before an
atomic replacement; valid cached files are reused. The helper uses Python's
standard library and requires no GitHub credentials. Gzip files can be opened
with `gzip.open(path, 'rt')` followed by `json.load`.

The release's display files total roughly 1.3 MiB compressed. Uttar Pradesh's
display JSON is under 0.5 MiB, compared with roughly 16 MiB in its source file.
Display simplification preserves feature counts and original properties; a
canonical `name` key is added for plotting. It does not update administrative
boundaries or district names.

## Rebuild

Install Mapshaper 0.7.86 in a build-only directory, then use:

```sh
npm install --prefix /tmp/mapshaper --no-audit --no-fund mapshaper@0.7.86
python3 build_geography_assets.py --source . --output /tmp/rebuilt-boundaries --mapshaper /tmp/mapshaper/node_modules/.bin/mapshaper
```

The build uses weighted simplification at 5%, `keep-shapes`, and output precision
of 0.00001 degrees. It verifies feature counts/properties before adding uniform
display keys, and rejects display files exceeding 1 MiB. Originals are retained
byte-for-byte after decompression. See `DATA_PROVENANCE.md` for source details.
