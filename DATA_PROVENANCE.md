# Data provenance

The original files were copied from the bundled GeoJSON assets in
https://github.com/Hari31416/genbi-v2 at commit
`cfe5fe73bc75d779c329eeaed07ffae65b3d0b1d`.

`source-sha256.json` preserves that application's original checksums. Each
decompressed file in `original/` matches its corresponding source checksum.
`manifest.json` maps the legacy filename to the new content-addressed file and
records compressed and decompressed checksums for both resolutions.

The imported application files did not document an upstream publisher or data
license. This repository records that limitation and does not assign a new
license to the underlying boundaries. Geometry attributes, names, and vintage
are inherited from those source files; simplification makes no claim that they
represent the latest administrative boundaries.

Display files were produced with Mapshaper 0.7.86. Geometry is simplified and
coordinates rounded for screen display. Original properties are retained, a
uniform `name` property is added, and Sikkim's `district` property is also copied
to `dtname` for compatibility. Source files are not altered.
