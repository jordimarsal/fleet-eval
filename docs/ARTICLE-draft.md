# Our benchmark crowned a "best reviewer" this morning. By afternoon, the data had taken it back.

This morning our evaluation battery told us who the best code reviewer was in our local LLM fleet: MiniCPM-V 4.7, recall 0.56 on real code defects, two full defects ahead of the next model. The plan was to route all review work to it.

By this afternoon we had run the same grading against 24 more defects. MiniCPM found 4 of the 24: recall 0.167 on fresh material, 0.27 overall, in a tie with the pack and behind one model it had beaten hours earlier.

Nothing changed except the number of questions. That gap between 0.56 and 0.167 is the winner's curse, and we watched it happen in our own data. This post is the postmortem: what the battery was, why the ranking looked solid, the calculation that should have stopped us from crowning anyone, and the habit we're keeping.

## Why we were ranking reviewers at all

We run a fleet of ten local models on two RTX 5080s. Nine are served by llama.cpp from a single script; the tenth is Strata, a 125B model on its own engine. The goal behind the fleet is role routing: if one model is measurably better at planning, implementing, or reviewing code, it should get that role instead of every session defaulting to the same daily model.

For the reviewer role we needed a ranking, so we built a battery for it. The design matters later, so here it is briefly.

Defects come from our own git history. For every `fix` commit in our repositories, the pre-state of the changed code is a real defect, and the fix itself defines what a competent review must catch. We harvested several hundred candidate commits across twenty-odd repositories, filtered to small reviewable diffs, and curated the survivors by hand.

Each model sees the defective code as a proposed pull request and answers with a numbered list of defects: correctness bugs, security issues, resource leaks. Style opinions are excluded by the prompt. Grading is mechanical, with no judge model in the loop: for each defect we derived regex patterns from the remedy, meaning tokens that the fix adds which do not exist in the buggy code. The models never saw the answer key, and the answer key came from our own production history rather than a synthetic list of classic bugs.

The first wave covered 9 defects. The results:

| Model | Found | Recall |
|---|---|---|
| minicpm | 5/9 | **0.56** |
| Strata | 3/9 | 0.33 |
| inkling2 | 3/9 | 0.33 |
| Huihui | 2/9 | 0.22 |
| SC117 | 2/9 | 0.22 |
| qwen38 | 2/9 | 0.22 |
| gemma4 | 1/9 | 0.11 |
| qwen36 | 0/9 | 0.00 |
| qwen4b | 0/9 | 0.00 |

A clear leader, two models at zero, a plausible middle. The obvious move was to write "reviewer: minicpm" into the routing config and move on.

## Why we paused instead

The first reason is sample size, and it is the boring one. At a true recall near 0.3, a Wilson 95% confidence interval on 9 samples spans about ±32 points. Our "clear lead" was two defects. The whole spread in that table, from 0.00 to 0.56, fits inside a single confidence interval of any cell in it.

The second reason is the one this post is about. The question we answered was not "is minicpm a good reviewer?" It was "which of ten models scored highest today?" When you take the maximum of ten noisy measurements, the max is dominated by whichever draw happened to be lucky. The winner of a small contest is selected partly for its luck, so its observed score overstates its true skill. Statisticians call it the winner's curse. It shows up in auctions and clinical trials, and leaderboards run on the same mechanism.

Neither reason required new data to see. But we wanted to know how bad the trap was for our exact numbers, so we ran one calculation before spending hours harvesting more defects.

## The calculation that should have stopped us

The question: if all ten models in the fleet were exactly identical, same true recall, differing only in sampling luck across 9 defects, what would the observed results look like?

This needs no simulation software. Each model's score is a binomial draw, and the max and min of ten independent draws have closed-form distributions. Set the true recall to 0.27, close to what the fleet later showed it had:

| 10 identical models, n=9 defects | Value |
|---|---|
| Expected score of the observed "leader" | 0.51 |
| P(some model posts 5/9 = 0.56 or better) | 50% |
| P(some model posts 0/9) | 45% |

If every model in the fleet had identical skill, the expected top score would be 0.51. We observed 0.56. Half the times you run this experiment, some model walks away with a headline of 0.56 or better; 45% of the time, some model walks away with a zero. Both things we saw in our real table, the champion at the top and the two zeros at the bottom, are exactly what an all-equal fleet produces. The wave-one ranking was indistinguishable from noise, and the part we found most convincing, the clear leader and the clear losers, was the part selection noise manufactures most reliably.

## The check we could actually run

A calculation is only an argument, so we wanted the data to say it too. We expanded the corpus with 24 more defects from the same pipeline, 33 in total, and re-ran all ten models. Same prompt format, same grading key, same models. Since every model answered every defect, the right test between two models is paired (McNemar), which is far more sensitive than comparing two loose percentages.

Everything collapsed into one band:

| Model | Wave 1 (n=9) | Final (n=33) |
|---|---|---|
| minicpm | 0.56 | 0.27 |
| inkling2 | 0.33 | 0.33 |
| Strata | 0.33 | 0.27 |
| Huihui | 0.22 | 0.24 |
| SC117 | 0.22 | 0.24 |
| inkling2unc | — | 0.24 |
| qwen38 | 0.22 | 0.21 |
| gemma4 | 0.11 | 0.18 |
| qwen36 | 0.00 | 0.18 |
| qwen4b | 0.00 | 0.12 |

No model finds more than a third of real defects. No model is below 0.12. McNemar found no significant difference between any pair; the smallest p-value, 0.18, belongs to the gap between the leader and the third model from the bottom.

And the number that closes the case: MiniCPM kept 5 of its 9 finds on the original defects. Those were real skill and they stay in the data. On the 24 new defects it found 4. Fresh material, same grading: 0.167, below the fleet average it was supposed to be leading.

## What we do instead of crowning

No routing for reviewers, for now. The top band is interchangeable, so the config names Strata as the reference (it is also the strongest on a synthetic review battery, where these same models score far higher, which is its own post) and the rest of the top band stays available. Routing survives only where the signal survived: implementation quality, where one model is measurably ahead, and per-language worker selection.

The battery stays open. The corpus grows as our repositories grow, and every new defect tightens the band around whatever true differences exist. If a real difference of useful size appears, McNemar will catch it.

## Lessons, stated so we can reuse them

1. Expand before you crown. A battery that cannot tell the top from the bottom cannot crown anyone. If expanding is cheap, do it first; if it is expensive, that is a sign the ranking was never actionable.
2. The max of N draws measures luck. Any selection over many noisy candidates (models, prompts, agents, hyperparameters) inherits the curse. The check is cheap: compute E[max] under the equal-skill hypothesis. If your observed winner sits at or below it, you have no winner.
3. Paired beats loose. Comparing two scores with confidence intervals wastes information. When every candidate answers the same items, McNemar on the discordant pairs is the test.
4. Publish the null. This post documents a ranking that died. The cost was an afternoon of harvesting and an evening of compute. The alternative was a routing decision that quietly sent review work to a mediocre reviewer for months.

## Reproduce it

Everything is public at github.com/jordimarsal/fleet-eval: the harvesting and curation scripts, the 33-defect corpus with its grading patterns (defects from private repositories are excluded), every model's raw answers, the grading script, and `docs/winner_curse_sim.py`, which prints the max/min statistics used above. The fleet runs on llama.cpp on two RTX 5080s. No cloud APIs were involved at any point.
