import json, pathlib, hashlib, datetime
B=pathlib.Path(__file__).parent
spec={
'fifo': [('o1','Amber 12 then Chalk 11; Indigo 0.'),('o2','Amber 12 then Chalk 16 exactly.'),('o3','North 30 then East 45 exactly.'),('o2','North 30, East 45, West 7.'),('o1','Moss 8 then Rust 11; Ink 0.'),('o1','Moss alone supplies 7.'),('o1','Glow 6, Halo 10, Spark 1.'),('o2','Glow 6 then Halo 4.'),('o3','Brass 9 then Steel 9.'),('o3','Brass 9, Steel 9, Iron 2.'),('o3','Polar 5 then Frost 9.'),('o2','Polar alone supplies 4.')],
'discount':[('o3','(90−12)×0.8 = £62.40.'),('o1','(140−12)×0.8 = £102.40.'),('o3','120×0.85−9 = £93.00.'),('o4','200×0.85−9 = £161.00.'),('o2','(260−40)×0.75−5 = £160.00.'),('o2','(340−40)×0.75−5 = £220.00.'),('o4','(80×0.9−6)×0.8 = £52.80.'),('o1','(130×0.9−6)×0.8 = £88.80.'),('o3','(115−15)×0.9×0.8 = £72.00.'),('o3','(165−15)×0.9×0.8 = £108.00.'),('o3','(96×0.75−8)×0.9 = £57.60.'),('o4','(176×0.75−8)×0.9 = £111.60.')],
'rounding':[('o4','2.35 halfway between 2.3 and 2.4; choose 2.4 g.'),('o1','2.349 below midpoint 2.35; 2.3 g.'),('o3','42.5 halfway between 40 and 45; choose 45 kPa.'),('o3','47.4 below midpoint 47.5; 45 kPa.'),('o4','1.205 halfway; higher 1.21 ppt.'),('o3','1.2149 below midpoint 1.215; 1.21 ppt.'),('o2','125 halfway; higher 130 kg.'),('o4','134.9 below midpoint 135; 130 kg.'),('o4','7.25 halfway; higher 7.5 mm.'),('o1','7.76 above midpoint 7.75; 8.0 mm.'),('o2','19 halfway; higher 20 cm.'),('o1','20.99 below midpoint 21; 20 cm.')],
'packs':[('o1','Deficit 19+5−8=16; ceil(16/8)=2, minimum 3.'),('o3','Deficit 37+6−(20−2)=25; ceil(25/12)=3.'),('o3','Deficit 94+16−(40−5)=75; ceil(75/25)=3, minimum 4.'),('o2','Final reserve explicitly 10; deficit 42+10−(25−5)=32; 2 packs.')],
'rates':[('o3','Aster and Bracken both 9, Clover 8; alphabetically earliest Aster.'),('o1','Dara and Ivo both 4.5, Nuri 40/9 lower; alphabetically latest Ivo.'),('o2','Birch 19/11 < 7/4 = Cedar = Ash.'),('o4','Blue and Copper both 6.75, Amber 20/3 and Dove 6.5 lower; earliest Blue.')],
'coordinates':[('o2','(2,5) → (5,3) → (−5,3).'),('o1','(−2,6) → (6,−2) → (4,2).'),('o3','(5,4) → (2,6) → (−6,2).'),('o4','(1,−3) → (−1,−3) → (3,−4) → (−3,4).')],
'cooldown':[('o3','09:20 follows cooldown; session+cooldown ends 09:40, touching next booking.'),('o1','13:44 too early; 14:10 ends 14:30 and final reset may overrun.'),('o1','10:30 follows ventilation and ends 10:48, leaving 12 min to 11:00.'),('o2','18:53 too early; 19:00 ends 19:10 with final reset allowed later.')],
'lexicographic':[('o2','Survival 92, hours 6 tie Shoal/Cove; lower cost 49 selects Cove.'),('o3','Damage 4, consent_age 19 tie Yew/Ash; 72 < 75 selects Yew.'),('o1','Deadline 12, shelf_use 85 tie Willow/Ochre; request 28 < 31 selects Ochre.'),('o1','Native species 16; gap 49 tie Brook/Verge; grant 940 < 950 selects Verge.')]
}
rows=[json.loads(l) for l in (B/'blind-inputs.jsonl').read_text().splitlines()]
counts={}; decisions=[]
for r in rows:
 m=r['id'].split(':')[2]; i=counts.get(m,0); counts[m]=i+1
 a,why=spec[m][i]; text=next(o['text'] for o in r['options'] if o['id']==a)
 decisions.append(dict(id=r['id'],answer_id=a,answer_text=text,rationale=why,ambiguity=False,multiple_supported=False,missing_rule=False))
assert len(decisions)==56
obj=dict(frozen_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),method='Direct semantic reasoning from id/state/question/options only; no target/source/generator/solver inspected before this freeze. Initial broad emission also exposed nonselected inputs only, not labels.',input_sha256=hashlib.sha256((B/'blind-inputs.jsonl').read_bytes()).hexdigest(),decisions=decisions)
p=B/'frozen-decisions.json'; p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n'); print(hashlib.sha256(p.read_bytes()).hexdigest())
