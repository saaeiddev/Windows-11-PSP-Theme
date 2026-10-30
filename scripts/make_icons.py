from pathlib import Path
out=Path(__file__).resolve().parents[1]/'icons'
icons={
'settings':'<path d="M32 10l3 5 6 1 5-2 4 5-2 5 2 6-2 5-5 1-3 5h-7l-3-5-6-1-5 2-4-5 2-5-2-6 2-5 5-1 3-5z"/><circle cx="32" cy="27" r="7" fill="#eaf7ff" stroke="#1166c4" stroke-width="3"/>',
'photo':'<rect x="10" y="13" width="44" height="31" rx="6"/><circle cx="24" cy="23" r="4" fill="#fff"/><path d="M14 40l11-11 6 6 7-8 12 13z" fill="#bdeaff" stroke="none"/>',
'music':'<circle cx="32" cy="28" r="19"/><circle cx="32" cy="28" r="13" fill="#d8efff" stroke="none"/><path d="M28 20l13 8-13 8z" fill="#0067ca" stroke="none"/>',
'video':'<rect x="10" y="15" width="44" height="28" rx="6"/><path d="M28 21l12 8-12 8z" fill="#fff" stroke="none"/>',
'game':'<path d="M22 19h20c8 0 12 8 13 17 1 7-4 9-8 5l-7-6H24l-7 6c-4 4-9 2-8-5 1-9 5-17 13-17z"/><path d="M20 23v10m-5-5h10" stroke="#fff" stroke-width="3"/><circle cx="43" cy="25" r="2" fill="#fff" stroke="none"/><circle cx="48" cy="30" r="2" fill="#fff" stroke="none"/>',
'network':'<circle cx="32" cy="28" r="19"/><path d="M14 31c2-10 14-17 26-13-9-1-15 4-15 11 0 7 9 11 20 6-7 10-25 11-31-4z" fill="#58d6d4" stroke="none"/><path d="M18 27c5-7 17-10 26-3" fill="none" stroke="#d8fbff" stroke-width="3"/>',
'extras':'<rect x="12" y="12" width="40" height="33" rx="8"/><path d="M21 22h9v9h-9zm13 0h9v9h-9zM21 34h9v6h-9zm13 0h9v6h-9z" fill="#e9f7ff" stroke="none"/>'}
for name, shape in icons.items():
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="64" height="48" viewBox="0 4 64 48"><defs><linearGradient id="g" x2="0" y2="1"><stop stop-color="#6bc7ff"/><stop offset="1" stop-color="#0063c7"/></linearGradient></defs><g fill="url(#g)" stroke="#1a73ce" stroke-width="2" stroke-linejoin="round">{shape}</g></svg>'''
 (out/f'{name}.svg').write_text(svg)
