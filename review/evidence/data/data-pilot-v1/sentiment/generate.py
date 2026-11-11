"""Render original agent-authored sentiment cases; no model calls or label audit."""
import collections
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
JOB = 'jeff-data-pilot-v1-sentiment-agent-r1'
# P/N/U/M are authoring annotations, not independently derived labels.
CASES = [
    [
        ("The oat cappuccino was creamy without being too sweet. I enjoyed every sip and would order it again.", "the oat cappuccino", "P"),
        ("I do not mind waiting for coffee, but being ignored at the counter after my order was ready was unacceptable. The counter service disappointed me.", "the counter service", "N"),
        ("The cafe receipt lists one tea and one roll. Payment was made at the counter at 10:15.", "the cafe visit as described", "U"),
        ("The cafe visit had a lovely breakfast and an uncomfortably cramped table. Neither cancels out the other for me; my reaction to the visit is mixed.", "the cafe visit overall", "M"),
    ],
    [
        ("The replacement bus driver explained the diversion clearly and helped me find my stop. I appreciated that care.", "the driver's assistance", "P"),
        ("The evening bus never arrived, and no cancellation notice appeared. I am unhappy with the service on that journey.", "the evening bus service", "N"),
        ("I boarded the number 14 at the station and left it at Market Street, three stops later.", "the bus journey", "U"),
        ("The new bus seats are comfortable, but their narrow spacing leaves my knees pressed against the seat ahead. I like one aspect and dislike the other.", "the new seating arrangement", "M"),
    ],
    [
        ("The librarian found the out-of-print atlas I needed and arranged a loan. That was genuinely helpful.", "the librarian's help", "P"),
        ("The study room was not quiet at all: staff left a radio playing throughout my booking. I would not book that room again.", "the study room experience", "N"),
        ("My library card currently has two novels checked out. Both have the same return date.", "the borrowing arrangement", "U"),
        ("Online renewal saves me a trip, which I love, but the renewal page repeatedly loses my selections, which frustrates me. My view of that page has both sides.", "the online renewal page", "M"),
    ],
    [
        ("These walking shoes did not give me the blisters I feared. After a full day on my feet, I am delighted with their comfort.", "the shoes' comfort", "P"),
        ("The shoes look smart, but the question for me is grip: the soles slide even on a dry floor. Their grip is terrible.", "the shoes' grip", "N"),
        ("The pair is size 8, has black laces, and arrived in a cardboard shoe box.", "the shoes", "U"),
        ("I value how light these trainers are and dislike how quickly their fabric stains. Taken together, those features leave me with a mixed opinion.", "the trainers overall", "M"),
    ],
    [
        ("The recipe app's scaling tool adjusted every ingredient correctly for six people. I love not having to do those calculations myself.", "the recipe scaling tool", "P"),
        ("The search keeps returning meat dishes after I select the vegetarian filter. That filter is not useful to me.", "the vegetarian search filter", "N"),
        ("There are twelve recipes in my saved folder. I added a soup recipe to it this morning.", "the saved-recipe feature", "U"),
        ("The cooking timer is easy to set, which pleases me, but its alarm is too faint, which annoys me. I have both praise and criticism for the timer.", "the cooking timer", "M"),
    ],
    [
        ("The laundrette attendant removed a stain I had given up on. I am very pleased with that help.", "the attendant's help", "P"),
        ("My clothes came out of the dryer still soaked after the full paid cycle. I am dissatisfied with that dryer.", "the dryer", "N"),
        ("I used machine 6 for a forty-minute wash and paid with a card.", "the laundry visit", "U"),
        ("The laundry pickup was punctual, which I appreciated, but the clothes returned with a strong fragrance I disliked. My opinion of the pickup service is mixed.", "the pickup service overall", "M"),
    ],
    [
        ("The pruning shears cut cleanly with little pressure. My hands no longer ache after trimming, and I am happy with them.", "the pruning shears", "P"),
        ("The trowel handle snapped while I was digging soft compost. It is not sturdy enough, and I regret buying it.", "the trowel", "N"),
        ("The rake has a wooden handle and twelve metal teeth. It hangs beside the shed door.", "the rake", "U"),
        ("The watering can's narrow spout gives excellent control, but its handle digs painfully into my palm. I see real merits and drawbacks in this can.", "the watering can", "M"),
    ],
    [
        ("I asked for a trim without losing the shape, and the stylist did exactly that. I am thrilled with the haircut.", "the haircut", "P"),
        ("The receptionist was friendly, but my comment is about booking: my confirmed slot was given away. I am unhappy with the booking process.", "the booking process", "N"),
        ("My appointment is recorded as a wash and cut. The salon sent the reminder yesterday.", "the appointment arrangement", "U"),
        ("The colour consultation gave me useful advice, yet I felt rushed when asking follow-up questions. I appreciated the advice and disliked the pace.", "the colour consultation", "M"),
    ],
    [
        ("Every piece of fruit arrived fresh and unbruised. I am pleased with the quality of the delivered fruit.", "the fruit quality", "P"),
        ("I did not approve substitutions, yet the order replaced my rice with an item I cannot use. I am frustrated by that substitution.", "the grocery substitution", "N"),
        ("The order contains milk, oats, and four apples. The delivery window is listed as 6 to 7 pm.", "the grocery order", "U"),
        ("The delivery arrived early enough to help with dinner, which was great, but two frozen items had thawed, which was disappointing. My view of the delivery overall is mixed.", "the delivery overall", "M"),
    ],
    [
        ("The audio guide made the unfamiliar sculptures understandable without talking down to me. I really enjoyed it.", "the audio guide", "P"),
        ("The gallery lighting left the captions unreadable. That made viewing the exhibit frustrating.", "the exhibit lighting", "N"),
        ("The museum has moved the ceramics collection to the second floor. Its entrance is beside the lift.", "the collection's location", "U"),
        ("The family trail had engaging puzzles, but its map sent us down a closed corridor. I liked the activities and disliked the navigation.", "the family trail", "M"),
    ],
    [
        ("The headphones block the train rumble without squeezing my head. I am delighted with their noise cancellation.", "the headphones' noise cancellation", "P"),
        ("Music sounds fine, but callers cannot hear me through the microphone. I am disappointed specifically with the microphone.", "the microphone", "N"),
        ("The headphones connect through Bluetooth and have a charging socket on the left side.", "the headphones", "U"),
        ("The earbuds have rich sound that I enjoy, but their touch controls trigger accidentally and annoy me. Overall, I have both praise and complaints.", "the earbuds overall", "M"),
    ],
    [
        ("The instructor offered seated alternatives without making anyone feel singled out. I valued that inclusive teaching.", "the instructor's teaching", "P"),
        ("The class was advertised for beginners, but no basic moves were explained. I felt let down by the instruction.", "the class instruction", "N"),
        ("The stretching class lasts forty-five minutes. Mats are stored along the back wall.", "the stretching class", "U"),
        ("The circuit class has an encouraging coach, which I like, and music loud enough to hurt my ears, which I dislike. My feelings about the class are mixed.", "the circuit class overall", "M"),
    ],
    [
        ("The locker code worked on the first try, and collecting my parcel took seconds. I am pleased with the collection process.", "the parcel collection process", "P"),
        ("The screen froze before opening my compartment, and support could not release it. That collection attempt was a frustrating waste of time.", "the attempted collection", "N"),
        ("The collection message names locker bank C and gives a deadline of Thursday evening.", "the collection instructions", "U"),
        ("Having access late at night is convenient, but the locker bays are so low that retrieving a heavy box is painful. I like the access hours and dislike the layout.", "the locker service overall", "M"),
    ],
    [
        ("The chair's lumbar support keeps my back comfortable through long editing sessions. It has been a great purchase for support.", "the lumbar support", "P"),
        ("The armrests will not stay at the selected height. I am fed up with having to reset them.", "the adjustable armrests", "N"),
        ("The chair has five wheels and a grey fabric seat. I assembled it on Tuesday.", "the desk chair", "U"),
        ("I enjoy the chair's reclining movement, but I dislike the loud creak every time it reclines. I cannot describe the reclining feature as wholly good or wholly bad.", "the reclining feature", "M"),
    ],
    [
        ("The cinema staff found a captioned screening that suited us. Their help made the outing possible, and I appreciated it.", "the staff's assistance", "P"),
        ("The film was excellent, but the broken seat tipped sideways throughout it. I was unhappy with the seat, not the film.", "the cinema seat", "N"),
        ("Our tickets were for screen 3, row F. The feature began after three trailers.", "the cinema outing", "U"),
        ("The screen's picture was beautifully sharp, while the sound was painfully loud. I enjoyed the visuals and disliked the audio, so my presentation review has both sides.", "the audiovisual presentation", "M"),
    ],
    [
        ("The mechanic explained why the brake cable needed replacing and showed me the worn part. I appreciated the clear explanation.", "the mechanic's explanation", "P"),
        ("The wheel still rubs the frame after the repair. I am not satisfied with the repair result.", "the wheel repair", "N"),
        ("The workshop invoice lists a new chain and an adjustment to the rear gears.", "the listed maintenance work", "U"),
        ("The puncture repair itself was excellent, but the workshop returned the bike two days after the promised time. My review of the service is mixed: good work, poor timing.", "the repair service overall", "M"),
    ],
    [
        ("The fern arrived with healthy roots and fresh fronds. I am delighted with the plant's condition.", "the fern's condition", "P"),
        ("The plant pot arrived cracked, and water leaks straight out. I am disappointed with the pot.", "the plant pot", "N"),
        ("The plant label says to use indirect light. The pot measures fifteen centimetres across.", "the plant purchase", "U"),
        ("The plant subscription introduced me to varieties I love, but several were poorly suited to the low-light preference I supplied. I enjoy the discoveries and dislike the matching.", "the plant subscription", "M"),
    ],
    [
        ("My tutor corrected pronunciation patiently and gave examples I could actually repeat. I found the lesson extremely helpful.", "the pronunciation lesson", "P"),
        ("The tutor spent most of my paid conversation lesson taking personal calls. I did not get useful practice and am unhappy about it.", "the conversation lesson", "N"),
        ("The next lesson covers past-tense verbs. It is booked for half an hour on Wednesday.", "the next language lesson", "U"),
        ("The online lesson's exercises were stimulating, but the tutor's shared audio kept cutting out. I appreciated the learning material and was frustrated by its delivery.", "the online lesson overall", "M"),
    ],
    [
        ("The lunch container stayed sealed in my bag with soup inside. I am very happy with its leak protection.", "the container's leak protection", "P"),
        ("The lid warped after one dishwasher cycle despite being marked dishwasher-safe. I regret buying this lid.", "the storage lid", "N"),
        ("The set includes three rectangular containers. The smallest holds half a litre.", "the storage set", "U"),
        ("The glass containers let me see leftovers easily, which I like, but their weight makes carrying lunch awkward, which I dislike. My overall opinion has both positives and negatives.", "the glass containers", "M"),
    ],
    [
        ("The lifeguard calmly helped me find a lane matching my pace. I appreciated the guidance.", "the lifeguard's guidance", "P"),
        ("The changing-room lockers would not lock, so I could not secure my belongings. I was unhappy with those lockers.", "the changing-room lockers", "N"),
        ("Lane swimming runs from 7 to 9 in the morning. The pool is twenty-five metres long.", "the lane-swimming setup", "U"),
        ("The family swim has plenty of floating toys, which my children enjoy, but the session is too crowded for comfortable movement. I like the activities and dislike the crowding.", "the family swim session", "M"),
    ],
    [
        ("The discussion host invited quieter members to speak without putting them on the spot. I thought the hosting was excellent.", "the discussion hosting", "P"),
        ("The group announced spoilers for next month's book after I asked them not to. I found that disregard upsetting.", "the group's handling of spoilers", "N"),
        ("The book club meets on the first Monday of each month. This month's selection is a short-story collection.", "the book club arrangement", "U"),
        ("The new discussion format gives everyone a turn, which I value, but its strict timer cuts off useful exchanges, which I dislike. I have a mixed view of the format.", "the new discussion format", "M"),
    ],
    [
        ("The weather app's rain alert gave me enough time to bring the washing in. I am pleased with that alert.", "the rain alert", "P"),
        ("The widget keeps showing yesterday's temperature after refresh. I no longer find that widget dependable and am frustrated with it.", "the temperature widget", "N"),
        ("The app displays wind speed in kilometres per hour. I have selected two towns in its location list.", "the weather app", "U"),
        ("I like the forecast chart's clear hourly detail, but I dislike its tiny labels that I have to zoom to read. My reaction to the chart is mixed.", "the forecast chart", "M"),
    ],
    [
        ("The tent stayed dry through a night of heavy rain. Its waterproofing exceeded my expectations, and I am pleased.", "the tent's waterproofing", "P"),
        ("The pole joint split during the first careful assembly. I am disappointed with the poles' durability.", "the tent poles", "N"),
        ("The tent has two entrances and a separate groundsheet. We pitched it facing east.", "the tent", "U"),
        ("The compact tent is wonderfully light to carry, but its roof is too low for me to sit upright. I like its portability and dislike its headroom.", "the compact tent overall", "M"),
    ],
    [
        ("The tailor shortened the sleeves without disturbing the lining. I am delighted with the workmanship.", "the sleeve alteration", "P"),
        ("I asked for the original hem to be preserved, but it was cut off. I am unhappy with how that request was handled.", "the handling of the hem request", "N"),
        ("The alteration slip records a two-centimetre adjustment at the waist. Collection is scheduled for Friday.", "the alteration arrangement", "U"),
        ("The jacket now fits beautifully, but the alteration cost was much higher than the quote. I am happy with the fit and unhappy with the price change.", "the tailoring service overall", "M"),
    ],
    [
        ("The pottery tutor helped me centre the clay without taking over. I loved learning the technique that way.", "the tutor's instruction", "P"),
        ("My finished bowl was given to someone else, and the workshop could not trace it. I am very disappointed with the collection system.", "the finished-work collection system", "N"),
        ("The workshop uses stoneware clay. Each participant has a numbered shelf for drying pieces.", "the pottery workshop setup", "U"),
        ("The glazing session offered colours I loved, but the rushed cleanup left no time to finish my pattern. I enjoyed the materials and disliked the pacing.", "the glazing session overall", "M"),
    ],
    [
        ("The boarding staff sent a thoughtful update about my nervous cat and followed her feeding routine. I felt reassured and am very pleased with their care.", "the boarding staff's care", "P"),
        ("My dog's labelled blanket was lost during boarding, and nobody tried to find it. I am upset with their handling of his belongings.", "the handling of the dog's belongings", "N"),
        ("The boarding form lists two meals per day and a collection time of noon on Sunday.", "the boarding arrangement", "U"),
        ("The boarding kennels had spacious runs that I liked, but their constant loud speaker announcements worried my dog. I see both a benefit and a drawback in the environment.", "the boarding environment", "M"),
    ],
    [
        ("The observatory guide explained Saturn's rings in language my child could follow. We loved that explanation.", "the guide's explanation", "P"),
        ("The telescope queue was unmanaged, and repeated pushing meant we never reached the eyepiece. I was disappointed with the queue management.", "the telescope queue management", "N"),
        ("The public observing session begins at 8 pm. Two telescopes are set up on the terrace.", "the observing session", "U"),
        ("The observatory's talk had fascinating images, but the room was so cold that I struggled to stay comfortable. I enjoyed the content and disliked the room conditions.", "the observatory talk experience", "M"),
    ],
    [
        ("The luggage attendant carefully matched my claim ticket before returning my bag. I appreciated that attention to security.", "the bag-return procedure", "P"),
        ("The luggage desk closed before its posted time, leaving me unable to collect my suitcase. I am unhappy with its reliability.", "the luggage desk's reliability", "N"),
        ("I stored one suitcase for four hours. The claim ticket shows bay 12 and a collection deadline of 6 pm.", "the luggage storage transaction", "U"),
        ("The storage site's position beside the station is excellent, but hauling my bag up its stairs was unpleasant. I like the location and dislike the access route.", "the luggage storage site overall", "M"),
    ],
    [
        ("The hearing loop made the speaker's words clear through my hearing aid without background buzz. I am delighted with its clarity.", "the hearing loop's audio clarity", "P"),
        ("The loop sign was displayed, but staff left the system switched off throughout the talk despite my request. I am disappointed with how it was operated.", "the operation of the hearing loop", "N"),
        ("The venue lists a hearing loop in rows A to D. Its information desk has a printed seating map.", "the hearing-loop provision as described", "U"),
        ("The loop signal was clear in the front seats, which I appreciated, but dropped out at the back, which frustrated me. My assessment of its coverage has both positives and negatives.", "the hearing loop's coverage", "M"),
    ],
    [
        ("The seed-swap organiser helped me find varieties suitable for my small balcony. I was grateful for that useful advice.", "the organiser's advice", "P"),
        ("Several seed packets had no plant names, and the desk refused to help identify them. I was disappointed with that labelling support.", "the seed labelling support", "N"),
        ("I exchanged two packets of bean seeds for one packet of marigolds. The event was held in the village hall.", "the seed exchange", "U"),
        ("The swap offered a wonderful variety of seeds, but the crowded table layout made browsing stressful. I liked the selection and disliked the arrangement.", "the seed-swap event overall", "M"),
    ],
]

OPTION_SETS = [
    {"P": "Positive only: the writer expresses approval or satisfaction, with no stated criticism of the specified subject.", "N": "Negative only: the writer expresses criticism or dissatisfaction, with no stated praise of the specified subject.", "U": "Neutral: the writer gives facts without expressing approval or disapproval of the specified subject.", "M": "Mixed: the writer explicitly expresses both favorable and unfavorable views of the specified subject."},
    {"P": "Favorable toward the named subject, with no stated criticism of that subject.", "N": "Unfavorable toward the named subject, with no stated praise of that subject.", "U": "Descriptive only: no evaluative attitude toward the named subject is stated.", "M": "Both praise and criticism of the named subject are stated; neither side should be discarded."},
    {"P": "The stated attitude toward this subject is favorable only, not a combination of praise and criticism.", "N": "The stated attitude toward this subject is unfavorable only, not a combination of praise and criticism.", "U": "No positive or negative attitude toward this subject is expressed.", "M": "The stated attitude combines satisfaction and dissatisfaction with this subject."},
]
QUESTIONS = [
    "What sentiment does the writer express toward {subject}?",
    "Considering only {subject}, which description matches the writer's attitude?",
    "Which description matches the expressed attitude toward {subject}?", 
    "Which option best captures the writer's sentiment about {subject}, rather than other things mentioned?",
]

def dump(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def main():
    assignments = json.loads((ROOT / 'group_assignments.json').read_text())
    teacher = os.environ.get('PI_MODEL') or 'unknown'
    provider = os.environ.get('PI_PROVIDER') or 'unknown'
    rows = []
    annotations = {}
    for group_index, cases in enumerate(CASES):
        group_id = f'data:pilot-v1:sentiment:g{group_index + 1:02d}'
        group = assignments['groups'][group_id]
        # Vary class order within groups, independently of choice position.
        shift = group_index % 4
        ordered = cases[shift:] + cases[:shift]
        for local_index, (state, subject, label) in enumerate(ordered):
            n = len(rows)
            four = n % 10 == 0
            pool = ['P', 'N', 'U', 'M'] if four else (['P', 'N', 'M'] if label == 'M' else ['P', 'N', 'U'])
            position = (n // 10) % 4 if four else n % 3
            distractors = [key for key in pool if key != label]
            if n % 2:
                distractors.reverse()
            distractors.insert(position, label)
            option_ids = [hashlib.sha256(f'{JOB}/{n}/{k}'.encode()).hexdigest()[:12] for k in range(len(pool))]
            row_id = f'data:pilot-v1:sentiment:g{group_index + 1:02d}:r{local_index + 1:02d}'
            options = [{'id': oid, 'text': OPTION_SETS[n % 3][key]} for oid, key in zip(option_ids, distractors)]
            row = {
                'schema_version': '0.1', 'id': row_id, 'state': state,
                'question': QUESTIONS[(group_index + local_index) % 4].format(subject=subject),
                'options': options, 'target_id': option_ids[position],
                'group_id': group_id, 'task_family': 'sentiment', 'split': group['split'],
                'provenance': {'kind': 'teacher', 'source': JOB, 'label_basis': 'teacher', 'teacher_model': teacher},
            }
            rows.append(row)
            annotations[row_id] = label
    for split in ['train', 'validation']:
        selected = [row for row in rows if row['split'] == split]
        (ROOT / f'{split}.jsonl').write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in selected))
    metadata = {
        'schema_version': '0.1', 'shard_id': JOB, 'task_family': 'sentiment',
        'teacher': {'provider': provider, 'model_alias': teacher, 'immutable_revision': None, 'revision_status': 'Not exposed by the agent environment'},
        'source': {'generation_job': JOB, 'kind': 'original synthetic agent-authored reviews and teacher labels', 'source_group_revision': 'sentiment-domains-r1', 'mechanism_revision': 'agent-review-situations-r1', 'group_assignments': 'group_assignments.json', 'generator': 'generate.py'},
        'generation_settings': {'method': 'Existing agent text generation; Python renders fixed authored cases and deterministic option rotation', 'temperature': None, 'top_p': None, 'sampling_seed': None, 'unknown_settings': 'Teacher sampling parameters and immutable model revision were not exposed', 'option_order': 'For 3 options global row index modulo 3; for every tenth row 4 options with four-way rotation; other option order alternates', 'external_datasets': False, 'network_generation': False, 'model_execution': False},
        'usage_constraints': {'origin': 'Original synthetic situations, no external datasets or private real records', 'terms': 'Generated through existing provider access and subject to existing provider terms; no separately asserted redistribution license', 'provider_terms_independently_reviewed': False},
        'cost': {'currency': 'GBP', 'additional_spend': 0, 'pending_spend': 0, 'existing_access': 'Existing agent access only; no additional billed calls or compute'},
        'row_counts': dict(collections.Counter(row['split'] for row in rows)),
        'group_counts': dict(collections.Counter(value['split'] for value in assignments['groups'].values())),
        'class_counts': {split: dict(collections.Counter(annotations[row['id']] for row in rows if row['split'] == split)) for split in ['train', 'validation']},
        'option_count_distribution': dict(collections.Counter(len(row['options']) for row in rows)),
        'label_strategy': 'Teacher-authored target labels; no executable semantic rule audit and no independent correctness verification',
        'limitations': ['Small synthetic English-only pilot; not representative of natural review frequency or writing styles', 'Explicit evaluative language and explicit mixed conclusions make some cases easier than ordinary reviews', 'Same teacher authored and reviewed the labels; self-review is not independent verification', 'Distinct validation domains do not eliminate shared phrasing or sentiment vocabulary across splits', 'Each group deliberately covers favorable, unfavorable, factual-neutral, and mixed situations; balanced authoring is not a real-world class prior', 'Mixed cases receive a mixed option; most other 3-option cases use positive, negative, neutral. This candidate-set pattern is an authoring shortcut, not proof of generalization', 'No sarcasm, implicit emotion, cultural variation, or genuinely unresolved ambiguity is represented'],
    }
    dump(ROOT / 'metadata.json', metadata)

if __name__ == '__main__':
    main()
