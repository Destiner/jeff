import json,hashlib,datetime
from pathlib import Path
p=Path(__file__).parent
rows=[json.loads(x) for x in (p/'blind-sample.jsonl').read_text().splitlines()]
# Human/assistant decisions derived solely from displayed natural-language sample; indices are one-based.
choices=[
(3,'Visitor is ineligible: zero distinct eligible signers, below one.'),
(3,'Two distinct eligible signers; duplicate legal signature ignored.'),
(3,'Urgency 3 ties A/C; C has smaller minutes 8.'),
(2,'Iris/Noor tie at 4 shifts; Iris travels 15 rather than 20 minutes.'),
(1,'FIFO exhausts Q=3,R=5 then S=1, totaling nine.'),
(2,'Quarantined P skipped; M=7,N=2 leaves demand three.'),
(2,'5 times 9 times 60 =2700 seconds.'),
(4,'(4 times 3 +2) times 10 =140.'),
(3,'(120-20) times .70=70.'),
(1,'150 qualifies; (150-15) times .90=121.5.'),
(3,'Daily capped credits 2+0+10=12.'),
(3,'4+6+6=16 before final cap of 15.'),
(4,'-3.1 is .9 from -4 and 1.1 from -2.'),
(4,'4.12 is .12 from 4 and .13 from 4.25.'),
(1,'Adjacent runs XX,Y,XXX encode 2X-1Y-3X.'),
(3,'Runs GG,AA,G encode G(2) A(2) G(1).'),
(1,'Deadline order Y,Z,X completes at 2,5,9, all on time.'),
(2,'Starting 5, setup-inclusive finishes 10,14,17 all permitted.'),
(1,'Export veto overrides custodian grant.'),
(1,'Engineer grants record; producer grants schedule; no veto.'),
(3,'ABD is common contiguous length three; cannot extend to four.'),
(1,'BABA occurs in both and is length four, maximal.'),
(4,'After {[( the closing ] mismatches top (.'),
(4,'After x{y[z](q), top opener is { but next closer is ].'),
(2,'Numeric merge puts A1,B1 then A2,A3 before tied B2.'),
(2,'South wins equal keys at 1 and 4: S1 N1 S2 S3 N2.'),
(2,'First set has one 1 (odd), second zero (even).'),
(3,'Constraint 1 odd passes; constraint 2 zero fails odd; constraint 3 one fails even.'),
(2,'M and K medians are 9, L is 8; latest name M wins.'),
(1,'Medians Yew 6.5, Oak 7, Pine 8.'),
(4,'Next active days after Fri are Sat then Sun.'),
(4,'Active starting Sun counts immediately as day one.'),
(2,'Seven usable per pack; fourteen demand needs two and meets minimum.'),
(3,'45+5=50 usable, two 25-unit packs.'),
(2,'Floors 2,4,1 leave one for last Sport: 2,4,2.'),
(1,'Exact .6,1.2,1.2; floor 0,1,1 leaves one awarded Dance by largest remainder.'),
(2,'Integers 5..9 intersect 9..12 only at 9.'),
(3,'10..25 intersects 5..10 only at 10.'),
(2,'30/2=45/3=15; explicit Tie.'),
(3,'7/4=14/8; explicit equality rule selects A.'),
(2,'Reflect (2,-1) to (2,1); add (1,4) gives (3,5).'),
(4,'Negate to (1,-3), swap to (-3,1), translate to (-3,4).'),
(2,'One batch remains; 9-2=7.'),
(2,'Discard the sole batch; subsequent removal clamped to zero.'),
(1,'21 is only one minute after 20, insufficient; 22 is two.'),
(2,'65 ends90 leaving10;70 ends95 leaving5;80 overlaps100..120. None has >20 gap before later appointment.'),
(2,'Ignoring underscore leaves B,A,a, matching case-sensitive aAB.'),
(3,'Ignoring dots and case leaves tsr, matching rst.'),
(3,'Score80 meets outer >=80; income26 fails <=25, yielding Half.'),
(3,'Vibration6 fails >6; hours100 meets >=100, yielding Service.'),
(3,'X adds10, I subtracts1 before V, V adds5:14.'),
(1,'C subtracts100 before D500; I subtracts1 before X10:409.'),
(1,'3-2=1;12/1=12.'),
(2,'(2+3)*5-1=24.'),
(1,'A before B by ready tie; then C after both, then D.'),
(3,'Initially Proof and Layout ready; alphabetical last Proof, then Layout,Edit,Ship.'),
(4,'All four codewords distance two from0011; listed last S wins.'),
(2,'Distances Red4,Blue1,Gold5,Teal2; Blue unique minimum.'),
(3,'All two-reading means4; earliest start1.'),
(1,'Four-reading sums8,7,8; earliest maximum start1.')]
assert len(rows)==len(choices)==60
out=[]
for r,(idx,reason) in zip(rows,choices):
 o=r['options'][idx-1]
 out.append({'row_id':r['id'],'chosen_option_id':o['id'],'chosen_option_text':o['text'],'reason':reason,'ambiguity':'None material identified; exactly one supplied option follows the stated rule.','must_fix':[]})
f=p/'decisions-frozen.jsonl'; f.write_text(''.join(json.dumps(x)+'\n' for x in out))
(p/'freeze-record.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'labels_revealed':False},indent=2)+'\n')
print('60 decisions frozen; no targets read by this script.')
