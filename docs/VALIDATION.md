# Validation report — 0.9.0 test build

Date: 2026-10-30. Artifact: `dist/Windows_11_PSP_Theme.ptf`. SHA-256: `0aa31c608d6906748d27343f516e42840da441e4717216d96c04da7002e67eb2` (rebuilds may differ with environment or source changes).

## Passed

- 445,952-byte PTF v1 container; correct magic, five groups, 74 records including the four-byte color metadata record. File is below PTF Studio's 768 KiB preflight limit.
- Project `scripts/validate.py`: record ranges, unique supported slots, compression decode, GIM signatures, wallpaper BMP 480 × 272 and metadata color record.
- Independent extraction and decoding with GeofrontTeam LibPSPThemes (commit can be checked against upstream): 73 PNG image resources were extracted successfully. Every generated category/body/focus resource had the expected decoded dimensions and transparent corner; decoded focus alpha was identical to source alpha. Wallpaper decoded to exact source pixels.
- Focus resources are 64-level white-alpha outer halos. Input SVGs and all raster resources are present. README references point to files in the repository. ZIP integrity was checked.

## Not tested / limitations

- **No PSP hardware, emulator, firmware version, or PTF Studio model profile was tested.** The software previews are custom drawings from source images, not PSP captures. Actual compatibility, appearance and installation behavior remain unverified on PSP Go, PSP-1000/2000/3000 and E1000.
- Slot 54 is a generic fallback; PTF Studio 1.0 documents Go-only System Storage, saved-data and resume entries as using that fallback. Their actual behavior still needs device testing. UMD and network entry availability varies by model.
- The two optional wallpaper variants are PNG only; they have not been embedded in or tested as separate PTFs. Icons are original Fluent-inspired interpretations, not official Windows icons.
- PTF has fixed XMB layout and cannot add Windows functionality. Images may appear different after firmware palette handling or text rendering.

Reference: https://github.com/S1implyBlue/PTF-Studio (commit `3b2c6407201bf02a22412725c9009a52bbdf1517`) and https://github.com/GeofrontTeam/LibPSPThemes .
