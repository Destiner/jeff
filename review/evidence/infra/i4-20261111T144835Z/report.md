# Infra I4 — delivered; observation stopped

## Coverage and result

Active window **2026-11-11 14:48:35–15:48:44.204149 UTC: 60m09.204s**. The closing snapshot finished9.204s after the planned15:48:35 cutoff; no further board-wide/resource observation follows. The window included implementation/review and foreground waiting, not continuous process tracing. Subsequent owner availability is separate and does not extend these results.

One small owned usability improvement shipped; no runtime fix, model run, scheduler intervention, or new monitoring product. Main merge **`2f00734e3375758bbb6852490e3ad03731e7d175`**, implementation `3d885d1cc2d356f92b6d8fd8e4485dd63184bacd`.

## Concrete findings and interventions

1. **Receipt explanation access:** the canonical `read` command displayed only a message, preventing the bounded reviewer from inspecting its recipient explanation without raw-path discovery. Added read-only `receipt MESSAGE_ID`, reusing existing validation, returning the stored status/times/note or explicit unread. No state, authority, task-accounting, or format change. Actual scratch before/after preserved every board hash; actual canonical main reads then exposed E4's completed explanation. Evaluation acknowledged availability and said no scoring/workflow change was needed. Benefit demonstrated: explanation accessible via one canonical command. No measured time-saving or model-quality benefit claimed.
2. **Historical blocked label:** E4's original blocked note still cited unpublished Data while its later delivery receipt said scoring had completed. A single precise peer question elicited Evaluation's clarification: no current blocker, only self-integration remained. Evaluation closed E4 after its own merge at14:59:26. No duplicate scoring, new approval gate, or receipt-transition redesign. Infra did not cause or accelerate that completion.
3. **Crossing schema proposals:** Model/Runtime flat/nested manifest proposals crossed; Runtime explicitly accepted Model's flat schema before implementing its older example, and Model later completed the related receipts. Concrete friction was resolved by the actual owners, without Infra interference. This is not proof that a failure or delay was averted.
4. **Correct rejection of an operator mistake:** Infra tried `--reply-to` against a message between different owners. Endpoint validation correctly rejected it, publishing nothing. Reissued the question with evidence IDs in the body and clarified this distinction in owned docs; no relaxed routing or new reference field.

## Actual communication statistics

[Final metadata/statistics](final-stats.json) count only owner↔owner messages **created inside the window**, excluding lead routes and pre-existing traffic: **31 messages /16 distinct directed routes**. At cutoff:26 completed,2 acknowledged-outstanding,3 unread/right-censored.

For28 messages with recorded acknowledgements: minimum19.577s, median265.689s (4m26s), nearest-rank p90=1657.613s (27m38s), maximum2050.932s (34m11s). Unread ages remain separate in the JSON. This is creation-to-acknowledgement elapsed, not transport latency; active/idle time, task purpose, and comprehension are not established by receipts. Completing a delivery receipt is not completing every underlying task. The requested [interim](interim.md) used its own15:40:45.671969 cutoff and was sent as `fe710818-db33-4e40-ad7d-8155c2683be2`.

## Resources and throughput: what is actually known

- P3 failure/correction/regrant/completion all predated this window. [Targeted historical reconstruction](p3-review.md) records the corrected process's38.271s busy interval and207.993s reported-ready-request→grant interval; those are not current utilization or evidence of contention. Runtime's correction was not duplicated.
- At14:55:22, a selected-counter `ps` query found only the four historically known P3 PIDs absent. No global process/command/environment dump, repeated weight scan, or inference of systemwide idleness.
- Model explicitly reported queue idle/no reservation at15:29:27 and no ML grant yet at15:31:19 while preparing M6. A new M6 full-run-starting notice appeared in the closing metadata snapshot. No M6 PID/counter/busy interval was established during the window. Later utilization/critical path remains unknown; the start notice is not a measured execution trace.
- Therefore **compute/experimentation is not established as the bottleneck**. Preparation, schema negotiation and attention were visible; ready execution, dependency waiting and all idle time must not be conflated. No training, scheduling, or resource-limit changes were made by Infra.

## Overhead and no-benefit findings

- **48 instrumented canonical inbox checks**, including18 full metadata rounds; **0 failed inbox calls**. Their measured work totalled **3.166s wall /2.779s CPU**, excluding interpreter startup/final log append, foreground waits, other CLI/build work, subagent inference/tokens and owner attention. This is a scoped subtotal, not total experiment cost.
- **3 completed subagents**: two independent bounded evidence reviews and one patch review. The first two reported103s/92s evidence-reading intervals (overlapped, not total session time),12 canonical reads,27 explicit file reads and15 shell calls. The patch reviewer read4 files in6 tool calls including2 shell commands; elapsed time unmeasured. Two harmless source-path lookup mistakes occurred during reviews.
- **2 successful Infra peer updates +1 rejected send**, with one useful peer clarification received; one requested interim to lead. Routine observations were not broadcast. One targeted PID query. Three package builds (two isolated, one integrated) succeeded; no tests/lint. Shared merge lock acquired on first attempt, released after successful integration; no contention demonstrated in that attempt.
- Local observation CPU cost was tiny, but retaining an active owner through quiet rounds has attention/tool/model-token cost not captured here. After the visibility fix, no further useful Infra patch was demonstrated. There is no causal time-saved figure or evidence of improved ML throughput.

## Evidence and stopping state

[Append-only events](events.md), `checks.jsonl`, uniquely named `round-*.json`, [consumer review](consumer-review.md), [scratch workflow](receipt-demo/cli.log), and [canonical main workflow](receipt-demo/canonical-main.log) are retained here. No protected final content, raw evaluation cases, or weight payloads were inspected.

All three subagents and all one-shot capture commands have finished. No observer/job remains, no ML slot is held by Infra, and actual/pending additional spend is **£0**. Keep the existing bounded manual check-ins and explicit READY/grant/start/exit handoffs; no watcher or new telemetry framework is justified. Lead's continuation policy is a separate bounded availability trial, not an extension of I4. Its newly committed shared wording will be reflected in the owned mailbox docs as a small follow-on, without further observation or a tool feature.
