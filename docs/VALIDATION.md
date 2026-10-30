# Validation and completion status

Date: 2026-10-30

## Verified
- Wallpaper conversion: PNG, RGB, 480 × 272 pixels. Source artwork generated specifically for this project.
- Seven category SVG files generated from `scripts/make_icons.py`.
- PTF Studio 1.0's published source describes Go-only storage and resume items as aliases for first-level fallback, and warns that adding record IDs 60–65 can cause rejection.

## Not verified / incomplete
- No PTF has been built. PTF format, resource encoding, transparency, compressed size and installability have not been tested.
- No PSP model, firmware, emulator, or XMB profile has been tested; no hardware was available.
- The icons are preliminary; subcategories and focus states remain to be designed and mapped.
- Native XMB previews, installation guide, release archive and reproducible PTF build pipeline are outstanding.

## Next steps
1. Finish icon and focus artwork, accurately mapping supported PTF records and Go fallback.
2. Use a reputable PTF builder and verify independently, including GIM decode and visual comparison.
3. Inspect model profiles in PTF Studio and clearly label screenshots as simulated.
4. Test on PSP Go and other hardware where available; document firmware versions and outcomes.
5. Only publish a release once artifact and documentation checks pass.

Reference: https://github.com/S1implyBlue/PTF-Studio (version 1.0, commit 3b2c6407201bf02a22412725c9009a52bbdf1517). Its live viewer is a simulation, not a PSP emulator.
