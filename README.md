# India GeoJSON assets

State and district boundaries in two resolutions:

- **Original**: full-resolution GeoJSON, preserved unchanged.
- **Display**: smaller GeoJSON for interactive maps and dashboards.

The repository contains 38 original/display pairs. Display files total about
1.3 MiB compressed. All files are gzip-compressed; the manifest lists each asset
and its download paths.

## Consistent location names

Every display feature uses **`properties.name`**, for both states and districts.
For Plotly maps, set `featureidkey="properties.name"`. Display polygons use
clockwise outer rings for correct Plotly/D3 rendering.

Existing source properties are retained. Display districts also provide
`dtname`, including Sikkim. Original files keep their original schemas and
geometry. Neither version updates administrative boundaries or district names.

## Download selected boundaries

You do not need to clone the full repository:

```sh
mkdir india-boundaries
cd india-boundaries
curl -fsSLO https://raw.githubusercontent.com/Hari31416/india-geojson-assets/v1/manifest.json
curl -fsSLO https://raw.githubusercontent.com/Hari31416/india-geojson-assets/v1/sync_geography_assets.py
python3 sync_geography_assets.py --asset india --asset uttar-pradesh-districts --output selected
```

Add `--original` to include full-resolution files:

```sh
python3 sync_geography_assets.py --asset maharashtra-districts --original --output selected
```

With no `--asset`, all display files are selected. Downloads are verified and
valid cached files are reused. Python's standard library is sufficient, and
GitHub credentials are not required. Open a compressed file with
`gzip.open(path, 'rt')` and `json.load`.

## Rebuild display files

From a clone containing the originals:

```sh
npm install --prefix /tmp/mapshaper --no-audit --no-fund mapshaper@0.7.86
python3 build_geography_assets.py --source . --output /tmp/rebuilt-boundaries --mapshaper /tmp/mapshaper/node_modules/.bin/mapshaper
```

The builder uses topology-aware simplification at 5%, preserves small features,
and rounds coordinates to 0.00001 degrees. It checks feature counts and source
properties before adding the uniform display keys.

## Versions

`v1` is the first release. Versioned manifests and immutable asset paths keep
deployments reproducible. Add a new version when changing published boundaries;
retain previous versions for applications using older files.
