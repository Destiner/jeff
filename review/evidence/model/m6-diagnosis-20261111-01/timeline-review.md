# Narrow online optimization timeline review

Fresh reviewer used only stdlib and actual online/progress/event/receipt fields, noinputtexts, DataD5scheduleanalysis, weights/model/tokenizerload, tests, Evaluation/finalfiles, writes or tuning. Presentationnumbers1-basedlogorder; changingweightonlineCE. Norms are sampledlast-updatepreclipnorms,notwindowmeans/maxima.

| presentations | meanCE | CErange | endupdate | preclipnorm | elapsedseconds |
|---|---:|---|---:|---:|---:|
|1–100|1.491697|.023462–13.505731|25|146.455|129.31|
|101–200|1.501557|.006389–4.565269|50|42.740|162.78|
|201–300|1.415126|.290963–3.797978|75|164.572|197.61|
|301–400|1.428162|.223039–4.326760|100|78.129|230.92|
|401–500|1.481832|.557804–3.381416|125|67.291|265.38|
|501–600|1.384111|.591573–2.241767|150|74.812|301.47|
|601–700|1.372271|.687465–2.060881|175|41.061|337.45|
|701–800|1.354450|.730454–3.198930|200|55.061|372.68|
|801–900|1.355907|.922994–1.970128|225|36.169|411.41|
|901–1000|1.348004|.949644–2.176619|250|14.349|450.78|
|1001–1100|1.386634|.801015–2.077949|275|41.286|491.44|
|1101–1200|1.391454|.782957–1.993841|300|22.010|531.18|
|1201–1300|1.386146|.678376–1.948571|325|31.361|569.36|
|1301–1400|1.366124|.888673–3.500868|350|29.391|607.45|
|1401–1500|1.341591|.648237–1.907686|375|20.131|646.30|

All1500CEfinite; mean1.400338,median1.355179,populationSD.596858,range.006389–13.505731. Largestloss presentation8/update2=13.505731; retaineduntrimmed. Next131=4.565269,396=4.326760,395=4.227581,109=4.076002. Counts>2:114;>2.5:42;>3:24;>4:5;>5:1. No outlier removedfromanyreportedresult.

Successive250-presentationmeans1.475757/1.451593/1.377753/1.348144/1.398505/1.350275; populationSD1.1259/.6619/.3906/.2872/.2992/.3051; >3counts13/9/1/0/0/1. Nonmonotonicmodestdecline andsubstantialdispersioncontraction,notfixedsnapshotlearningproof.

375clipphases/steps,1500presentations,zeroextra backwards; finalAdamstep375. All15recordedpreclipnorms>1(range14.349–164.572); clippingactiveonthosesamples. Other360normvalues/postclipnorms/directions/perparamnormsnotretained. Successfulcompletionmeanseveryclipcallpassedfinitepositivechecks,notrecoverablefulltrajectory/clippingfrequency.

Training elapsed94.471→646.297s(~551.83s).100-presentationintervals~33.3–40.7s; some laterslowdownwithoutlate loss explosion. Synchronizedphasetotals forward114.23s/backward292.12s/clip20.65s/step124.04s. Successive500 forward34.50/38.40/41.32s; backward90.88/98.43/102.82s. ObservedMPSdrivermax11.85GB/minrecommendedheadroom7.22GB; CPUlifetimeRSS3.37GB unchanged—notinstantaneousRSS orpeaks. No recordedthermal/swap/resource-stresscause.

Supported: finitevariableearlylossnarrows, sampledpreclipnormsdecline/fluctuate, optimizercontinues375. Unsupported: rootcause, exposureorderattribution, snapshotaccuracy/discrimination, resource-inducedfailure. OnlineCEuseschangingweightsbeforeupdates; cannotexplainallfinalargmax0oridentifyties. No baselinecomparison/newrecipe/fallbackrecommendedorauthorized.
