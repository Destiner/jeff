"""Materialize agent-authored synthetic intent examples; CPU serialization only.
Correct choices are authored first here, then deterministically repositioned.
This script does not query a model or independently verify semantic labels.
"""
import collections
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
JOB = 'data:pilot-v1:intent:agent-authoring-r1'
TEACHER = {'provider': os.environ.get('PI_PROVIDER') or 'unknown', 'model_alias': os.environ.get('PI_MODEL') or 'unknown', 'immutable_revision': None}
# Each group contains four different requests, not four paraphrases.
DATA = [
    [
        ("My library book is due tomorrow. I haven't finished it; can I keep it for another week?", ["Extend the loan on the current book.", "Reserve a different book.", "Pay an overdue charge."]),
        ("The catalogue says the gardening guide is out on loan. Please put me in the queue for when it comes back; I don't need recommendations.", ["Place a reservation for the borrowed gardening guide.", "Recommend other gardening books.", "Renew the user's existing loans.", "Check the library's closing time."]),
        ("I still have my library card, but I can't remember the PIN for the online account. How do I get back in?", ["Help reset the library account PIN.", "Replace a lost library card.", "Explain how to borrow an ebook.", "Change the account's postal address.", "Cancel a book reservation."]),
        ("I've moved to 8 Rowan Lane. My loans are fine; please update where you send library notices.", ["Update the member's mailing address.", "Renew all current library loans.", "Stop all library notifications.", "Register a second library membership."]),
    ],
    [
        ("My parcel is already on its way. Can you send it to the staffed pickup shop rather than my house?", ["Redirect the parcel to a pickup shop.", "Cancel the order before dispatch.", "Arrange collection of a return.", "Report missing parcel contents."]),
        ("The tracking page says delivered, but nothing is at my door or with either neighbour. I need you to investigate where it went.", ["Investigate a parcel marked delivered but not received.", "Change the delivery address for a future parcel.", "Request a faster shipping service."]),
        ("I won't be home on Tuesday. Don't change the address; could the courier come on Thursday instead?", ["Reschedule the delivery day.", "Redirect delivery to another address.", "Provide proof of an earlier delivery.", "Cancel the shipment.", "Add insurance to a future shipment."]),
        ("The item is fine, but I no longer want it. Please arrange for a courier to collect this return from my home.", ["Book a home collection for a return.", "Report damage to an incoming parcel.", "Ask the courier to leave a parcel outside.", "Track a replacement shipment."]),
    ],
    [
        ("I'm outside the theatre and need to get to the hospital by bus. Which route should I take?", ["Plan a bus route from the theatre to the hospital.", "Request a refund for a bus ticket.", "Report a bus arriving late."]),
        ("I got off the number 12 without my blue bag. It has no valuables, but I'd like help getting it back.", ["Report and recover an item left on a bus.", "Find the next departure of route 12.", "Complain about the bus fare.", "Apply for a concession pass."]),
        ("The bus was clean and on time. The driver refused the valid pass on my phone, though. Please log a complaint about that refusal, not a refund request.", ["Record a complaint about a driver rejecting a valid pass.", "Request reimbursement for a cancelled service.", "Compliment the bus cleaning staff.", "Replace a phone-based travel pass.", "Check whether a route serves the station."]),
        ("I'm visiting for one afternoon. What's the price of a single bus journey? I'm not asking for directions.", ["Provide the single-journey bus fare.", "Plan an afternoon sightseeing route.", "Sell an annual commuter pass.", "Explain how to recover lost property."]),
    ],
    [
        ("I'd like a little space to grow beans this year. Is there a way to join the waiting list for a garden plot?", ["Add the resident to the garden plot waiting list.", "Reserve a communal watering can.", "Report damage to an existing plot.", "Cancel a garden membership."]),
        ("The tap by plot 6 keeps running even when shut. My seedlings are doing well; please get the tap fixed.", ["Report a faulty communal tap for repair.", "Request advice about watering seedlings.", "Apply to move to plot 6."]),
        ("I borrowed the garden's fork, not a spade. I can't bring it back by tonight; may I return it on Saturday instead?", ["Extend the borrowed garden fork's return deadline.", "Reserve a spade for Saturday.", "Buy a replacement garden fork.", "Report that a tool has been stolen.", "Book a garden orientation session."]),
        ("I am giving up my plot at the end of this month. Please close my plot agreement rather than moving me to a different bed.", ["End the member's garden plot agreement.", "Transfer the member to another plot.", "Renew the plot agreement for another year.", "Join the next communal planting day."]),
    ],
    [
        ("The evening Spanish class clashes with my new shift. Could you move my enrolment to the Saturday class?", ["Transfer the student to the Saturday Spanish class.", "Withdraw the student from all courses.", "Issue a certificate for a completed course."]),
        ("I know a little Italian from my grandparents. Before I enrol, how can I find out which level to choose?", ["Arrange guidance or assessment to choose an Italian course level.", "Enrol the student in the most advanced class.", "Change the language of an existing enrolment.", "Request a tuition refund."]),
        ("I completed the German course last spring. My employer now needs proof; could you send a completion certificate?", ["Provide proof of completion of the German course.", "Send the syllabus for a future German course.", "Book a German placement assessment.", "Change a course payment method.", "Request extra conversation practice."]),
        ("I can attend next week's lesson, but the worksheet link no longer works. Please send me a working copy of the worksheet.", ["Provide an accessible copy of the lesson worksheet.", "Excuse an absence from next week's lesson.", "Move the student to another course.", "Explain the course cancellation policy."]),
    ],
    [
        ("My bike's rear brake barely slows it down. Can I book a repair slot? I can bring it in myself.", ["Schedule a bicycle brake repair.", "Arrange collection of a bicycle.", "Order a new bicycle helmet.", "Cancel an existing workshop booking."]),
        ("You've already repaired my bike. Is it ready for me to collect today?", ["Check whether the repaired bicycle is ready for collection.", "Book the bicycle's first repair appointment.", "Request a quote for a new repair."]),
        ("Before you replace the wheel, please tell me the full cost. Don't start the work until I've agreed to the price.", ["Provide a wheel replacement quote before doing the work.", "Authorise immediate wheel replacement.", "Arrange a test ride of a new bike.", "Request a receipt for a finished repair.", "Book a puncture repair lesson."]),
        ("The chain adjustment you did yesterday is slipping again. I'd like you to inspect that same problem under the repair guarantee.", ["Arrange a follow-up inspection of the unsuccessful chain repair.", "Purchase a second-hand bicycle.", "Book an unrelated annual service.", "Ask for cycling route advice."]),
    ],
    [
        ("Water is coming up through the pavement outside my gate. It's not a billing question; please report the leak.", ["Report a suspected water main leak.", "Dispute the household water bill.", "Change the billing address."]),
        ("The meter reading on my bill is 840, but today's actual reading is 604. Please correct the bill using the reading I supplied.", ["Request a bill correction using the actual meter reading.", "Arrange installation of a new water meter.", "Report low water pressure.", "Set up a new water account."]),
        ("I'm moving out next Friday. I need the water account at this flat closed from that date, not transferred to another property.", ["Close the water account on the move-out date.", "Transfer the account to a new address.", "Arrange a repair at the current address.", "Increase the monthly payment.", "Request advice on saving water."]),
        ("My bill amount is right. Can I spread payment across monthly instalments instead of paying it all now?", ["Arrange monthly instalment payments.", "Challenge the meter reading.", "Close the water account.", "Book a water quality inspection."]),
    ],
    [
        ("I bought museum tickets for Sunday but can now only come on Monday. Please change the visit date, if there is space.", ["Reschedule the museum tickets to Monday.", "Cancel the tickets without replacement.", "Reserve a museum café table.", "Purchase an exhibition catalogue."]),
        ("My father uses a wheelchair. Before we buy tickets, could you tell me whether the sculpture gallery has step-free access?", ["Provide step-free access information for the sculpture gallery.", "Book a wheelchair repair.", "Reserve tickets for a guided tour."]),
        ("The headphones on audio guide 17 only play in one ear. I'm still in the museum; may I swap this unit for a working one?", ["Replace a faulty museum audio guide during the visit.", "Refund all admission tickets.", "Change the language of an exhibition label.", "Report a lost pair of personal headphones.", "Book an audio-described tour for another date."]),
        ("We enjoyed the exhibition. I'd like a receipt showing the tickets and total paid for my expenses claim.", ["Provide a receipt for the ticket purchase.", "Collect feedback about the exhibition.", "Reserve more tickets for the same exhibition.", "Request a refund because the visit was disappointing."]),
    ],
    [
        ("My dog's boarding stay is booked for three nights. Our trip is longer now; can you add Sunday night?", ["Extend the dog's boarding reservation by one night.", "Cancel the entire boarding reservation.", "Book a dog grooming appointment."]),
        ("Please add to Pippin's care notes that he eats only the food I'm bringing. I'm not asking to buy a different food from you.", ["Record the dog's feeding instructions for the stay.", "Order dog food from the boarding facility.", "Request a refund for unused meals.", "Arrange a veterinary appointment."]),
        ("We arrive tomorrow. What vaccination paperwork do you need to see before accepting our cat?", ["Explain the vaccination documentation required for cat boarding.", "Schedule a vaccination at the boarding facility.", "Change the cat's pickup time.", "Request photos of the cat during its stay.", "Cancel tomorrow's boarding booking."]),
        ("Our flight lands late. Could my sister collect the rabbit instead of me? I'd like to authorise her for pickup.", ["Add the sister as an authorised person to collect the rabbit.", "Extend the rabbit's stay automatically.", "Change the rabbit's feeding plan.", "Book transport from the airport."]),
    ],
    [
        ("I don't want to perform on stage. Is there a way I can volunteer to build scenery for the next production?", ["Enquire about joining the scenery-building team.", "Register for an acting audition.", "Buy tickets for the next production.", "Request a rehearsal recording."]),
        ("I already have a part in the play, but can't find the rehearsal timetable. Please send the current schedule.", ["Provide the current rehearsal timetable.", "Apply for a part in the play.", "Withdraw from the production."]),
        ("My seat for Friday is right behind a pillar. Could you move my ticket to an unobstructed seat for the same performance?", ["Exchange the ticket for an unobstructed seat at Friday's performance.", "Change the ticket to a different performance date.", "Apply to join the backstage crew.", "Request a refund for a cancelled show.", "Reserve a place in an acting workshop."]),
        ("I left a red scarf in the dressing room after last night's show. Could someone check the lost-property box for it?", ["Locate a scarf left at the theatre.", "Order a red scarf for a costume.", "Reserve a dressing room for a future show.", "Complain about the dressing room temperature."]),
    ],
    [
        ("I've got a broken microwave, not general rubbish. Does the recycling centre accept it?", ["Explain whether the centre accepts a broken microwave.", "Book a household rubbish collection.", "Report fly-tipping near the centre."]),
        ("I already know you take mattresses. I just need a slot to bring mine in this Saturday.", ["Book a Saturday recycling-centre visit to drop off a mattress.", "Check whether mattresses are accepted.", "Arrange a mattress collection from home.", "Purchase a replacement mattress."]),
        ("Someone dumped tyres outside the centre's gate last night. Please log that so the council can remove them; they aren't mine.", ["Report dumped tyres outside the recycling centre.", "Request permission to dispose of the user's tyres.", "Appeal a personal dumping fine.", "Renew a vehicle entry permit.", "Ask for the price of recycled tyres."]),
        ("My old van permit has the wrong registration after I changed vehicles. Please update the permit with the new registration.", ["Update the vehicle registration on the recycling-centre permit.", "Apply for a driving licence.", "Book a vehicle repair.", "Cancel a recycling-centre appointment."]),
    ],
    [
        ("I can still take my piano lesson this week, but not at four. Could we move it to six?", ["Reschedule this week's piano lesson to six.", "Cancel all future piano lessons.", "Book a piano tuning.", "Change from piano to guitar lessons."]),
        ("I'm learning clarinet at home. Before booking regular lessons, could I try a single introductory session?", ["Arrange a trial clarinet lesson.", "Buy a clarinet from the teacher.", "Enrol in a full term immediately."]),
        ("The piece you assigned has a missing second page in my copy. Could you send that page? I don't need a different piece.", ["Provide the missing page of the assigned music.", "Assign a different piece of music.", "Explain how to replace a broken instrument.", "Reschedule the next lesson.", "Register the student for an examination."]),
        ("Please stop my automatic lesson payments after the current term. I'll finish the lessons already paid for.", ["End automatic lesson payments after the current term.", "Refund every lesson in the current term.", "Cancel the remaining paid lessons immediately.", "Add another weekly lesson."]),
    ],
    [
        ("Our tent pitch is booked already. We will arrive after the office closes; how should we check in?", ["Explain the procedure for checking in after reception closes.", "Create a new tent pitch reservation.", "Cancel the existing campsite reservation."]),
        ("The power socket on pitch 14 has stopped working. The tent lights work on our battery, so this is about the hookup. Please send someone to repair it.", ["Arrange repair of the pitch's electrical hookup.", "Rent a battery-powered camping lamp.", "Change the guest's arrival date.", "Request directions to pitch 14."]),
        ("We don't need another night. We do need an extra parking space for a second car during our booked stay. Can you reserve one?", ["Reserve parking for a second car during the existing stay.", "Extend the campsite stay by one night.", "Reserve an additional tent pitch.", "Arrange bicycle hire.", "Ask about vehicle breakdown assistance."]),
        ("Could you tell me the quiet hours? We want to know when to turn our music off, not complain about another camper.", ["Provide the campsite's quiet-hour rules.", "File a noise complaint against another camper.", "Book a campsite music event.", "Cancel a pitch because of noise."]),
    ],
    [
        ("The kitchen ceiling drips whenever the upstairs shower runs. Please arrange a repair visit; my rent payment is not the issue.", ["Arrange a maintenance visit for the ceiling leak.", "Dispute a rent payment.", "Request permission to repaint the kitchen.", "Apply to transfer to another property."]),
        ("Your contractor is booked for Tuesday morning. I can't be home then; please move that visit to an afternoon.", ["Reschedule the existing contractor visit to an afternoon.", "Report a new repair problem.", "Cancel the tenancy."]),
        ("The loose stair rail has been fixed, but the repair ticket still says open. Please mark that ticket as completed; no further visit is needed.", ["Close the completed stair-rail repair ticket.", "Book another stair-rail repair visit.", "Report a new staircase defect.", "Request reimbursement for repair materials.", "Ask permission to install a stair lift."]),
        ("I would like to put up a shelf, but I haven't drilled anything. Can you tell me whether I need the landlord's permission?", ["Explain whether permission is needed to install a shelf.", "Report damage caused by drilling.", "Arrange emergency shelf removal.", "Ask the landlord to buy furniture."]),
    ],
    [
        ("I want to join the food co-op. How do I become a member?", ["Explain how to join the food cooperative.", "Cancel an existing membership.", "Track a grocery delivery."]),
        ("My vegetable box arrived without the potatoes listed on the invoice. Please credit me for the missing potatoes rather than send another box.", ["Issue a credit for the potatoes missing from the delivered box.", "Send a full replacement vegetable box.", "Change the next box's delivery address.", "Provide a recipe using potatoes."]),
        ("I'll be away for two weeks. Keep my membership active, but pause my weekly box until I return.", ["Temporarily pause the weekly box deliveries.", "Permanently cancel cooperative membership.", "Increase the weekly box size.", "Refund all past deliveries.", "Apply to volunteer at the shop."]),
        ("The newsletter mentions a member vote. Could you send me the date and joining details for that meeting?", ["Provide the member voting meeting's date and access details.", "Submit a vote on the member's behalf.", "Change the member's food order.", "Unsubscribe the member from the newsletter."]),
    ],
    [
        ("I'm not ready for deep water yet. Can you enrol me in the adult beginners' swimming class?", ["Enrol the user in an adult beginner swimming class.", "Book an advanced diving lesson.", "Reserve a lane for competitive training.", "Cancel a pool membership."]),
        ("I know the pool opens at seven. When is there a session without children?", ["Provide the timetable for adults-only swimming sessions.", "Provide the general pool opening time.", "Book a child's swimming lesson."]),
        ("Locker 28 won't unlock, and my clothes are inside. I'm standing beside it; could a staff member help open it?", ["Send staff to help open the stuck locker.", "Rent a locker for next month.", "Report stolen clothes.", "Ask for longer swimming time.", "Replace a lost membership card."]),
        ("I was charged twice for yesterday's swim. Please reverse the duplicate charge, not cancel my membership.", ["Refund the duplicate swim admission charge.", "Cancel the user's pool membership.", "Reserve two places in a swim session.", "Explain the price of an annual pass."]),
    ],
    [
        ("I don't own a telescope. May I borrow a club one for the public observing night?", ["Arrange borrowing a club telescope for the observing night.", "Buy a telescope from another member.", "Book a private planetarium show."]),
        ("The forecast says cloud all evening. Has tonight's club observing session been called off?", ["Check whether tonight's observing session is cancelled.", "Request an explanation of cloud formation.", "Cancel a telescope purchase.", "Register for next year's club meeting."]),
        ("I can get to the dark-sky site myself. What I need is help aligning my telescope's mount when I arrive. Can someone show me?", ["Arrange guidance on aligning the telescope mount.", "Arrange transport to the dark-sky site.", "Replace the telescope with club equipment.", "Provide membership payment details.", "Request a map of local bus routes."]),
        ("My email address changed, and I missed the last two club notices. Please replace the old address on the mailing list.", ["Update the email address on the club mailing list.", "Unsubscribe the user from all club notices.", "Book two observing sessions.", "Report a broken club telescope."]),
    ],
    [
        ("The meal account shows no balance, although I topped it up yesterday. Please trace the payment.", ["Investigate the missing school meal account top-up.", "Order a second lunch for today.", "Apply for a kitchen job.", "Cancel all school meals."]),
        ("My child is going on a trip on Friday. Please cancel just Friday's booked lunch; keep the rest of the week as it is.", ["Cancel only the child's Friday lunch booking.", "Cancel every lunch for the week.", "Change the child's school trip booking."]),
        ("We've been advised that my child must avoid sesame. Please update the meal service's allergy record before next week's lunches.", ["Record the child's sesame allergy for school meals.", "Request a diagnosis of the child's symptoms.", "Ask for a copy of last month's menu.", "Transfer the meal account to another school.", "Increase the daily meal spending limit."]),
        ("I'm not asking to change the menu. Where can I see the ingredients in Tuesday's curry before I choose a lunch?", ["Provide ingredient information for Tuesday's curry.", "Replace Tuesday's curry on the menu.", "Cancel an already booked Tuesday lunch.", "Refund a meal eaten last week."]),
    ],
    [
        ("I haven't placed an order yet. How much would twelve matte prints at 20 by 30 centimetres cost?", ["Quote a price for twelve matte prints at the specified size.", "Track a previously placed print order.", "Repair a camera lens."]),
        ("Order 461 hasn't been printed yet. I selected glossy by mistake; please switch it to matte without changing the size.", ["Change the existing order's paper finish to matte.", "Resize the prints in the existing order.", "Cancel the entire print order.", "Add framing to the order."]),
        ("All six prints came with the same green streak. The image files don't have it. Can you reprint the faulty batch?", ["Arrange replacement prints for the defective batch.", "Edit a green object out of the original photographs.", "Buy a new camera.", "Change the delivery address on a future order.", "Request a quote for scanning negatives."]),
        ("My order is marked ready. Is Saturday collection possible, and what hours is the counter open?", ["Provide Saturday collection availability and counter hours for the ready order.", "Book a photography class on Saturday.", "Ask the lab to reprint the order.", "Request shipping instead of collection."]),
    ],
    [
        ("I can spare two hours on Sunday and would like to help with the street cleanup. Please sign me up.", ["Register the user as a volunteer for Sunday's cleanup.", "Report a missed council bin collection.", "Request a paid street-cleaning job.", "Donate money to the volunteer group."]),
        ("I signed up for the food parcel round, but my bicycle broke. Can someone else take over my delivery shift tomorrow?", ["Find replacement cover for the user's volunteer delivery shift.", "Arrange a bicycle repair for the user.", "Sign the user up for an extra shift."]),
        ("The event is still on, and I can still attend. Could you tell me the meeting point? The old map link is blank.", ["Provide the volunteer event's meeting location.", "Cancel the volunteer event.", "Remove the user from the volunteer rota.", "Request reimbursement for travel.", "Arrange volunteer safeguarding training."]),
        ("I spent twelve pounds on bags for the approved cleanup. How do I claim that expense back?", ["Explain how to claim reimbursement for approved cleanup supplies.", "Ask for donations to fund a future cleanup.", "Order more bags for the next event.", "Register a complaint about litter."]),
    ],
    [
        ("I'm not travelling yet, just planning. Does this station have a lift from the entrance to platform 3?", ["Provide lift access information for platform 3.", "Sell a ticket to platform 3.", "Report a lift that has broken during the user's trip."]),
        ("I left my suitcase in the station waiting room, not on the train. Could you check station lost property?", ["Look for a suitcase left in the station waiting room.", "Search a train for the suitcase.", "Reserve luggage storage for a future trip.", "Book assistance with carrying luggage."]),
        ("My train is still running. I need a staff member to help me board with my wheelchair at 14:10; please book that assistance.", ["Book wheelchair boarding assistance for the 14:10 train.", "Claim compensation for a cancelled train.", "Arrange wheelchair repairs.", "Change the ticket to a later train.", "Request a seat in the station café."]),
        ("I bought the ticket already. Which platform is the 09:35 service to Norchester leaving from?", ["Find the departure platform for the 09:35 service.", "Purchase a ticket to Norchester.", "Refund the existing ticket.", "Reserve station parking for the day."]),
    ],
    [
        ("My pot is dry and ready. Can I reserve space in the next bisque firing?", ["Book the pot into the next bisque kiln firing.", "Enrol in a wheel-throwing lesson.", "Buy a finished ceramic pot.", "Cancel studio membership."]),
        ("I'm new to glazes. Before I coat this bowl, could someone show me how to use the dipping bucket safely?", ["Arrange guidance on safely dip-glazing the bowl.", "Book a bisque firing for an unmade pot.", "Request a refund for a finished bowl."]),
        ("My fired mug is on the collection shelf, but I can't get there this week. Could you hold it until next Friday rather than dispose of it?", ["Extend the storage period for the finished mug.", "Fire the mug a second time.", "Ship the mug to another studio.", "Sell the mug to a visitor.", "Book a new mug-making class."]),
        ("The wheel pedal at station 4 keeps sticking. I have stopped using it; please arrange maintenance.", ["Report the sticking pottery wheel pedal for maintenance.", "Reserve station 4 for an extra session.", "Request advice on centring clay.", "Order a personal pottery wheel."]),
    ],
    [
        ("Our team can play this season. Where do I submit the roster to register us for the recreational volleyball league?", ["Explain how to register the team roster for the league.", "Withdraw the team from the season.", "Book an individual coaching lesson."]),
        ("The fixtures list has us down for two games at the same time. Please correct the clash; we're not forfeiting either game.", ["Resolve the team's conflicting fixture times.", "Record the team as forfeiting both games.", "Change the team's uniform colour.", "Request a copy of the scoring rules."]),
        ("Our result was 3–1, but the website lists a 1–3 loss. Could you fix the recorded result? The referee's sheet has the right score.", ["Correct the reversed match result on the website.", "Appeal the referee's decisions during the match.", "Schedule a replay of the match.", "Register a new player.", "Ask for a refund of league fees."]),
        ("I lost the link to the league's conduct policy. Please send it; I don't want to file a complaint about anyone.", ["Provide the league's conduct policy.", "File a conduct complaint against another player.", "Report a match score.", "Cancel an upcoming fixture."]),
    ],
    [
        ("I'd like to inspect the old market ledgers next Thursday. Could you reserve a reading-room appointment?", ["Book a reading-room visit to consult the market ledgers.", "Order a published history book.", "Donate personal records to the archive.", "Request a tour of the archive building."]),
        ("The catalogue entry is clear, but I cannot visit. Can I order a digital scan of the single map listed as M-42?", ["Request a digital reproduction of the specified archive map.", "Reserve an in-person reading-room seat.", "Correct the map's catalogue description."]),
        ("I made a scan request last month and paid the invoice. It hasn't arrived; could you check its progress rather than create a new order?", ["Check the status of the existing paid scan request.", "Place a second scan order.", "Request general advice on digitising family photographs.", "Donate scanning equipment.", "Cancel the user's reading-room membership."]),
        ("I want to print an archive photograph in a local history booklet. What permission do I need? I'm not asking for a new scan.", ["Explain permission requirements for reproducing an archive photograph in a booklet.", "Create a fresh scan of the photograph.", "Register for a research appointment.", "Ask the archive to publish the booklet."]),
    ],
    [
        ("My phone was stolen. Please block the SIM now; I haven't bought a replacement handset yet.", ["Suspend the stolen phone's SIM service.", "Sell the user a new handset.", "Increase the monthly data allowance."]),
        ("The monthly price is fine, but I use more data now. What plans have a larger allowance without changing my number?", ["Compare plans with more data while retaining the phone number.", "Request a different phone number.", "Report the phone as stolen.", "Cancel the mobile service entirely."]),
        ("I paid this month's bill yesterday. The account still says overdue, so please trace the payment before charging me again.", ["Investigate why the recent bill payment has not been credited.", "Set up a second bill payment immediately.", "Request a new data plan.", "Order a replacement charger.", "Ask for international roaming rates."]),
        ("I'm going abroad next week. I don't want to activate anything yet; how much would calls cost there?", ["Provide call roaming prices for the destination without activating a service.", "Activate an international roaming package.", "Cancel the domestic mobile plan.", "Change the user's billing address."]),
    ],
    [
        ("I haven't handled bees before. Could I book the beginner hive-handling session at the community apiary?", ["Register for the beginner hive-handling session.", "Order a colony of bees immediately.", "Report a swarm on public land.", "Cancel an apiary membership."]),
        ("I'm already on Saturday's course, but don't own a veil. Could you reserve a loan veil in my size? I don't need another course place.", ["Reserve a protective veil to borrow for the existing course booking.", "Book a second place on Saturday's course.", "Buy a new hive."]),
        ("My labelled honey jar is ready at the apiary shed. I can't collect it this week; please keep it there until the next open day.", ["Hold the user's honey jar until the next open day.", "Arrange a new honey extraction session.", "Donate the honey jar to another member.", "Request delivery of a bee colony.", "Register for a honey tasting event."]),
        ("I noticed the latch on the shared hive stand gate won't close. This isn't a bee-health report; please arrange to fix the latch.", ["Report the shared apiary gate latch for repair.", "Request an inspection for bee disease.", "Apply for a personal hive stand.", "Ask for advice on feeding bees."]),
    ],
    [
        ("We've booked a canal boat for the weekend. Is it possible to add bedding hire to that reservation?", ["Add hired bedding to the existing boat booking.", "Extend the hire by an extra weekend.", "Buy a canal boat."]),
        ("Before I book, can you confirm whether your boats permit dogs? I'm not trying to reserve a kennel.", ["Provide the boat hire company's policy on dogs aboard.", "Reserve a kennel for a dog.", "Cancel an existing boat reservation.", "Arrange a dog-walking service."]),
        ("We are moored safely, but the boat's freshwater pump has stopped. Please send technical help; we don't need a route change.", ["Arrange technical assistance for the hired boat's failed freshwater pump.", "Replan the canal route.", "Order bottled water for home delivery.", "Request a refund for a future hire.", "Book an extra night at the marina."]),
        ("Our return time is nine tomorrow. Could we pay for a noon return instead? The return marina would stay the same.", ["Request a later boat return time.", "Change the return marina.", "Cancel tomorrow's boat collection.", "Request directions to the nearest lock."]),
    ],
    [
        ("I'd like to borrow runner bean seeds. Could you tell me which varieties the seed library currently has?", ["List the available runner bean seed varieties.", "Reserve a garden plot.", "Request a refund for seeds bought elsewhere.", "Report a problem with the library building."]),
        ("I borrowed tomato seeds and have saved some from my crop. How should I label them when I return seeds to the library?", ["Explain how to label saved seeds being returned to the seed library.", "Renew a borrowed gardening book.", "Ask the library to identify a tomato disease."]),
        ("The envelope says dwarf peas, but I took it home thinking it was broad beans. I haven't opened it; can I exchange it for broad bean seeds?", ["Exchange the unopened pea seed packet for broad bean seeds.", "Diagnose why the peas failed to grow.", "Order an extra copy of a gardening book.", "Donate the user's harvest to a food bank.", "Extend the seed library's opening hours."]),
        ("I volunteer at the seed desk. I can't cover my shift on the 18th; please remove me from that day's rota only.", ["Remove the volunteer from the seed-desk shift on the 18th.", "End the user's seed library membership.", "Cancel all future seed-desk sessions.", "Reserve seeds for collection on the 18th."]),
    ],
    [
        ("I've joined the makerspace but haven't used its laser cutter. Can I book the required safety induction?", ["Book the laser cutter safety induction.", "Reserve unrestricted machine time immediately.", "Buy a laser cutter for home use."]),
        ("I'm certified and have a file ready. Please reserve the laser cutter for an hour on Thursday afternoon.", ["Reserve an hour of laser cutter use on Thursday afternoon.", "Register for a first-time safety induction.", "Ask a technician to design the file.", "Cancel the makerspace membership."]),
        ("The cutter stopped halfway through my paid slot because its extractor failed. Please credit the unused machine time; I'm not seeking help with the design.", ["Request credit for machine time lost to the equipment failure.", "Request design assistance for the cutting file.", "Reserve another slot without a credit.", "Buy a replacement extraction unit.", "Book a general woodworking course."]),
        ("I have some sheet material but no packaging label. Before using the machine, where can I find the list of materials you're allowed to cut?", ["Provide the approved-materials guidance for the laser cutter.", "Authorise cutting unidentified material immediately.", "Order new packaging labels.", "Report an equipment fault."]),
    ],
    [
        ("Our choir has been accepted for the festival. Could you send the upload link for our stage layout? We're not applying again.", ["Provide the submission link for the accepted choir's stage layout.", "Submit a new festival application.", "Buy audience tickets for the choir.", "Request a recording of last year's festival."]),
        ("We have a singer who cannot climb stairs. Before choosing accommodation, which festival lodging options have step-free rooms?", ["Provide accessibility information about festival lodging options.", "Change the choir's performance repertoire.", "Book a medical appointment for the singer."]),
        ("Our pianist is travelling separately, but that isn't the problem. The programme misspells our choir's name; please correct it before printing.", ["Correct the choir's name in the festival programme.", "Arrange transport for the pianist.", "Change the choir's performance time.", "Register an additional singer.", "Book rehearsal accommodation."]),
        ("We have returned all the borrowed music stands. Could you release the equipment deposit? We don't need to borrow them again.", ["Arrange return of the deposit for the returned equipment.", "Reserve music stands for another performance.", "Pay a new equipment hire deposit.", "Report missing music stands."]),
    ],
]

QUESTIONS = [
    'Which action best matches the user\'s main request?',
    'What is the user asking the recipient to do?',
    'Choose the action that addresses the explicit request.',
    'Which response action would fulfil the user\'s intent?',
]


def materialize():
    plan = json.loads((ROOT / 'group_assignments.json').read_text())
    assert len(DATA) == len(plan) == 30
    rows = {'train': [], 'validation': []}
    counters = collections.Counter()
    for group_index, examples in enumerate(DATA, 1):
        group_id = f'data:pilot-v1:intent:g{group_index:02d}'
        assignment = plan[group_id]
        assert len(examples) == assignment['planned_rows'] == 4
        split = assignment['split']
        for local_index, (state, descriptions) in enumerate(examples, 1):
            row_id = f'data:pilot-v1:intent:g{group_index:02d}:r{local_index:02d}'
            n = len(descriptions)
            # Cycle across every available position independently per split/arity.
            target_position = counters[(split, n)] % n
            counters[(split, n)] += 1
            distractors = descriptions[1:]
            # Rotate distractors independently rather than keeping their source order.
            offset = (group_index + local_index) % len(distractors)
            distractors = distractors[offset:] + distractors[:offset]
            ordered = distractors[:]
            ordered.insert(target_position, descriptions[0])
            options = [{'id': hashlib.sha256(f'{row_id}:choice:{j}'.encode()).hexdigest()[:14], 'text': text} for j, text in enumerate(ordered)]
            rows[split].append({
                'schema_version': '0.1', 'id': row_id, 'state': state,
                'question': QUESTIONS[(group_index + local_index) % len(QUESTIONS)],
                'options': options, 'target_id': options[target_position]['id'],
                'group_id': group_id, 'task_family': 'intent', 'split': split,
                'provenance': {'kind': 'teacher', 'source': JOB, 'label_basis': 'teacher',
                               'teacher_model': f"{TEACHER['provider']}/{TEACHER['model_alias']}"},
            })
    for split, examples in rows.items():
        (ROOT / f'{split}.jsonl').write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in examples))
    metadata = {
        'schema_version': '0.1', 'shard_id': 'data-pilot-v1-intent-r1', 'generation_job': JOB,
        'task_family': 'intent', 'teacher': TEACHER,
        'source_identity': 'Original synthetic requests and competing action descriptions authored by the existing agent session; no external dataset or private real data.',
        'generation_settings': {'method': 'Existing agent text generation, followed by local Python CPU serialization and deterministic option placement.', 'temperature': None, 'top_p': None, 'generation_seed': None, 'settings_unknown_reason': 'Not exposed to this agent session.', 'separate_model_calls': 0, 'network_generation': False, 'option_order': 'Per-split per-option-count target position cycle starting at zero; distractor rotation by group and local row index.', 'source_content_revision': '1', 'generator_revision': 'generate.py r1', 'group_assignment_revision': 'group_assignments.json r1'},
        'groups': plan,
        'row_counts': {split: len(examples) for split, examples in rows.items()},
        'group_counts': {'train': 25, 'validation': 5},
        'label_strategy': 'All labels are teacher-authored primary-request interpretations. Structural validation and teacher self-review do not independently verify semantic correctness.',
        'usage_constraints': {'origin': 'Original synthetic agent-generated content.', 'terms': 'Subject to existing provider/access terms; no separately asserted redistribution license. No external source license was imported or claimed.', 'external_datasets': False, 'private_real_data': False},
        'cost': {'currency': 'GBP', 'additional_spend': 0, 'pending_spend': 0, 'basis': 'Existing approved agent access only; local lightweight CPU processing. Existing access/subscription cost not separately attributed.'},
        'limitations': ['Only 120 examples across 30 small scenario clusters.', 'English-only synthetic requests, not representative user traffic.', 'Teacher labels and teacher self-review are not independent correctness evidence.', 'Validation holds out complete source scenarios, not all abstract action types; generic actions such as booking and repair appear in both splits.', 'All options describe actions; broader intent taxonomies and ambiguous multi-intent requests are excluded.', 'Immutable teacher revision and sampling settings are unknown.', 'Option counts are 3, 4, and 5; no binary or six-choice examples in this shard.'],
    }
    (ROOT / 'metadata.json').write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'row_counts': metadata['row_counts'], 'teacher': TEACHER}, indent=2))


if __name__ == '__main__':
    materialize()
