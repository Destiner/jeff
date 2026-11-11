import json,hashlib
from pathlib import Path
from datetime import datetime,timezone
O=Path('/Users/destiner/Code/jeff/artifacts/data/data-pilot-v2/review-revisions')
rows=json.loads((O/'blind-inputs.json').read_text())
slots=[0,1,3,2,4,0,1,0,1,2,1,3,2,2,0,3,0,3,1,2,0,2,3,1,0,1,1,2,2,3,2,2,0,0,4,3,2,1,2,0]
reasons=[
'Overdue activation is the requested outcome; delivery, hardware replacement and moving an already-passed date do not express it.',
'Permanent mailing-list removal, not a pause or reduced frequency.',
'Asks about step-free vessel boarding, not booking assistance, fares, or shore access.',
'Requests pedestrian diversion directions, not a blockage report or vehicle route.',
'Transfer the purchased session to the partner, not refund, extension, new purchase or different trainer.',
'Move the existing booking rather than add another or cancel without replacement.',
'Transfer stored value; explicitly neither cash refund nor replacement of a failed card.',
'Compare tariffs before choosing; not applying a tariff or asking about exit fees.',
'Contest and remove a contradicted late fee; neither receipt replacement nor extension nor damage.',
'Availability enquiry before deciding, expressly not a reservation or collection-list signup.',
'Replace the subscribed area while retaining the subscription, not add an area or change timing.',
'Stale forecast timestamp requires investigation. Resending after delivery failure is adjacent but delivery failure is not asserted.',
'Add alerts alongside daily issues; neither replace nor merely increase routine frequency.',
'Obtain a formal written report of an existing appraisal; neither new verbal appraisal nor receipt nor revaluation.',
'Correct ownership attribution, explicitly retaining value; neither ownership transfer nor payer correction.',
'Authenticate the referenced certificate, not replace it, disclose full records or grant sharing permission.',
'Change pending postal destination only; not delay, digital format, or printed name.',
'Technical climbing difficulty is requested, not descent, restrictions or guided booking.',
'Recent reported anchor condition is requested; neither a new incident report nor a guided inspection. Wording appropriately avoids certification.',
'Offline guide access is requested, not failure reporting or weather alerts.',
'Repair the jam is the primary outcome. Belt service and motor replacement are possible interventions, not established requested intents; tension is not supported.',
'Temporary suspension with a specified resumption date, not reduced walks or termination.',
'Compliance certificate specifically requested; invoice explicitly inadequate, guarantee and new inspection are different.',
'Book advanced workshop; neither repeat basics nor seek entry assessment.',
'Recipient name changes, with address and billing explicitly unchanged.',
'Wants instruction in night-mode operation, not delegated configuration, a completion report, or fault investigation.',
'Explanation of the surcharge, not removal, overall comparison or site survey.',
'Report repeated abuse to conduct team; not result review, rule clarification or reassignment.',
'Disable future renewal while preserving current validity, not immediate cancellation or pause.',
'Smaller reusable box next delivery, not disposable, quantity reduction or immediate exchange.',
'First operator registration, not renewal or adding hardware to an existing record.',
'Withdraw later duplicate only, not both or merge.',
'Guidance for completing operator details; user retains submission/payment. Other options alter stage or agency.',
'Total walking duration enquiry, not distance, private alternative or reservation.',
'Private Tuesday tour for twelve, not public places, another date, training or self-guidance.',
'Readiness status of tagged sharpening job, not specification, appointment or price.',
'Change drop-off time only, not collection or service date.',
'Physical embossing of correct transcription, not large print or editing.',
'Cancel pending transcription before work, not hold, cancel completed delivery or change format.',
'Quote for braille with production awaiting approval, not large print, immediate work or input requirements.'
]
out={'frozen_at_utc':datetime.now(timezone.utc).isoformat(),'label_hidden':True,'parent_targets_or_generators_inspected':False,'input_sha256':hashlib.sha256((O/'blind-inputs.json').read_bytes()).hexdigest(),'judgments':[]}
for r,i,why in zip(rows,slots,reasons): out['judgments'].append({'id':r['id'],'chosen_option_id':r['options'][i]['id'],'chosen_slot_zero_based':i,'reason':why,'ambiguity':None,'mustfix':False,'rivals_review':'Plausible neighboring tasks; distinguishable as primary requested intents, not a claim that every downstream action is incompatible.'})
assert len(out['judgments'])==40
with (O/'blind-judgments-frozen.json').open('x') as f: json.dump(out,f,indent=2); f.write('\n')
print('Frozen 40 judgments before target/parent/generator inspection:',hashlib.sha256((O/'blind-judgments-frozen.json').read_bytes()).hexdigest())
