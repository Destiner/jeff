"""Frozen pre-authoring scenario allocation; no external data access."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
PLANS = [
('guided cooking sessions', 'folding dumplings|allergen substitution|class timetable|bread fermentation|knife grip adaptation|burnt caramel instruction|ingredient station numbering|pasta pacing|sauce rescue|shared hob access'),
('stationery delivery', 'flat packed tracing sheets|ink bottle leakage|parcel dimensions|pencil substitution notice|rainproof wrapping|missing order component|delivery address update|paper texture and cutting|dispatch receipt|folder corners and parcel tracking'),
('podcast editing', 'remote guest level matching|deleted qualifying sentence|episode export settings|breath removal and clipped laughter|repairing a chair squeak|music drowning speech|speaker track inventory|chapter markers and names|quiet speaker clarity|unapproved outro replacement'),
('language dictionary apps', 'regional pronunciation search|wrong verb example|offline pack update|word history and sync|inflection lookup|search keyboard reset|entry count change|audio clarity and speed control|interface language switch|bookmark recovery and tagging'),
('garden fencing installation', 'sloping ground alignment|blocked access gate|panel delivery schedule|privacy and loose latch|root preservation|exposed nail ends|boundary length record|stain finish and debris|storm stability|unannounced hedge removal'),
('document scanning', 'faint pencil annotations|cropped margin notes|file delivery inventory|image sharpness and page order|fragile foldout handling|search text corrupting surnames|collection receipt|colour accuracy and file size|scan resolution instruction|receipts legibility and skew'),
('meal preparation kits', 'portioning for solo cook|split sauce pouch|weekly menu change|spice balance and chopping estimate|leftover ingredient use|undercooked bean directions|storage date labels|vegetable freshness and packaging|late supper assembly|unmarked nut garnish'),
('tailoring fittings', 'sleeve mobility adjustment|pin damage|appointment duration|jacket shoulders and lining|uneven posture allowance|trouser hem measurement|fitting location update|waist fit and pocket angle|garment collection time|collar correction and appointment delay'),
('car wash visits', 'salt removal beneath arches|wax streaks|service lane allocation|clean glass and wet seat|care around loose trim|scratched bonnet|receipt itemisation|wheel finish and queue|tree sap removal|unreturned floor mat'),
('local newspaper delivery', 'dry paper during storm|repeated wrong doorway|edition date change|timely arrival and bent supplements|temporary mobility accommodation|unreadable soaked copy|route start notification|correct issue and noisy gate|holiday pause record|sports insert and doorstep placement'),
('online art lessons', 'demonstrating brush pressure|invisible charcoal marks|video length update|perspective explanation and rushed exercise|feedback on colour values|unanswered glazing question|lesson file formats|camera detail and missing materials list|caption placement|critique specificity and interrupting timer'),
('skateboard repairs', 'bearing seizure repair|uneven wheel installation|parts collection record|smooth steering and loose hardware|saving original graphic|grip tape covering bolt holes|deck width record|axle alignment and rough edge|repair completion notice|truck stability and quoted cost'),
('charity shop purchases', 'tested secondhand radio|concealed cracked casserole|donation stock arrival|coat warmth and broken zip|staff locating matching volume|stained tablecloth folded inward|purchase receipt listing|toy completeness and sharp corner|record playback|incorrect marked shoe sizes'),
('public park seating', 'bench height for standing|splintered armrest|bench relocation notice|shade and uneven supports|space beside mobility aid|drainage onto seat|seat numbering map|back support and hot metal|new plaque installation|view and wobbling base'),
('food market stalls', 'explaining sour cherry uses|stale flatbread|stall trading hours|fresh herbs and crushed stems|custom grind for cafetiere|unmarked chilli addition|produce origin sign|cheese flavour and excess rind|bread slice thickness|incorrect change'),
('photobook binding', 'layflat panorama|detached endpaper|spine title record|stitching and cover alignment|thick paper accommodation|trimmed captions|binding material specification|colourful cloth and glue smell|order page count update|page opening and spine lettering'),
('rehearsal room acoustics', 'quiet flute audibility|persistent bass boom|room dimension record|vocal clarity and handclap flutter|string quartet separation|sound masking count in|panel placement record|dry percussion and boxy cello|spoken cues audibility|ringing overtone at piano'),
('indoor plant watering services', 'adjusting dormant orchid care|standing water in saucer|visit date log|healthy fern and dripped floor|separating succulent schedule|watering dormant bulbs|plant location list|soil checks and unlatched door|key return record|leaf recovery and mineral residue'),
('furniture restoration', 'repairing rocking chair joint|sanding through veneer|wood species record|table finish and stiff drawer|retaining original tool marks|staining over active split|collection time record|new cane and uneven colour|removable finish choice|wobbly repaired leg'),
('video caption editing', 'identifying offscreen speaker|missing safety word|caption file inventory|accurate names and crowded lines|preserving interrupted sentence|captions revealing punchline early|language track update|sound descriptions and blocked diagram|export frame rate record|readable line breaks and typo'),
('orienteering map printing', 'legible contour detail|smudged control circles|print run inventory|water resistance and folded legend|colour separation at dusk|wrong scale reproduction|paper dimensions record|clear symbols and clipped north arrow|fine vegetation marks|missing course overprint'),
('weaving loom rental', 'tension adjustment lesson|cracked heddle|rental duration record|smooth treadles and worn reed|narrow doorway assembly|missing tie up cords|loom serial record|even shed and awkward return slot|extension date record|working brake and rough beam'),
('falconry demonstrations', 'explaining bird choice|rushed welfare question|demonstration schedule|clear handling and blocked view|changing flight for wind|baiting without explanation|bird roster change|close observation and loud microphone|safe viewing distance|inaccurate habitat explanation'),
('community darkroom sessions', 'recovering dense negative print|contaminated developer tray|enlarger booking record|focus coaching and timer fault|guidance for contact sheets|unannounced light exposure|chemical batch record|clean prints and crowded drying rack|session duration update|contrast advice and dirty easel')
]
if __name__ == '__main__':
    groups = {}
    for d, (domain, plan) in enumerate(PLANS):
        for j, scenario in enumerate(plan.split('|')):
            n = d * 10 + j + 1
            groups[f'data:pilot-v2:sentiment-b:g{n:03d}'] = {
                'split': 'train' if d < 20 else 'validation',
                'domain': domain,
                'scenario_plan': scenario,
            }
    destination = ROOT / 'group_assignments.json'
    if destination.exists():
        raise SystemExit('Assignments already frozen; refusing overwrite')
    destination.write_text(json.dumps({'groups': groups}, indent=2) + '\n')
