# When a RAG answer is wrong, did retrieval or generation fail?

Research note for the loopnotes.dev article on telling RAG retrieval failures from generation failures. Gathered 2026-11-18.

## Conclusions

1. The widely repeated claim that about 70% of RAG failures are retrieval failures has no primary source; one of the top results says so itself. Count the stage in your own wrong answers before deciding to start with retrieval.
2. None of the top three results measures which failure stage moves when chunk settings change on the same question set. In our run (Evidence 4), prefixing the heading path halved retrieval misses while accuracy stayed at 21 of 30, because other questions then failed with the right chunk in the prompt. Log the stage of each wrong question; accuracy alone hides what a chunk change did.
3. Retrieval and generation need different checks. Ragas Context Recall measures what was retrieved and needs a reference answer, while Faithfulness checks the answer against the retrieved context. Build a small set of questions with reference answers to measure retrieval. Faithfulness alone won't show it.
4. A reranker only reorders the list it receives (Amazon Bedrock's definition of reranker input). If the right chunk is missing from the candidate list, a reranker cannot fix that failure. Check the candidates before you add one.
5. "Not in Context" is a separate failure point (Barnett et al. 2024): the chunk was retrieved but dropped while the prompt was assembled. Log the final context the model received separately from the top-k list. Otherwise this failure looks like a generation failure.

## The question

Someone's RAG app gives wrong answers to some questions. They have probably changed chunk size or overlap once or twice already. They want to know whether the wrong answers come from retrieval (the right passage was never found), from context assembly (it was found but did not reach the prompt) or from generation (it reached the prompt and the model still answered wrong). That tells them whether to keep tuning chunks or to change the prompt or model.

## Evidence 1: what the top results say and leave out

Checked 2026-11-18 for the natural-language query "how to tell if RAG wrong answer is retrieval failure or generation failure" and the keyword "rag retrieval failure vs generation failure".

| Result | One-line summary | Measures failure stages on a question set? |
|---|---|---|
| latitude.so: "How to debug a RAG pipeline that returns wrong answers" (vendor blog, 2026-07-22, about 1,800 words, 7 H2s) | Stage-by-stage debugging and a known-good-context test. Calls "70% of RAG failures are retrieval" a widely repeated heuristic with no primary source. Recommends larger or overlapping chunks without numbers. | No |
| zilliz AI FAQ: "if a RAG system's answers are poor…" (short Q&A) | Measure retrieval (recall@k) separately from generation. | No |
| dev.to wonderlab: "RAG series 9: root cause diagnosis with Ragas" (about 1,500 words with code) | Three failures created on purpose and diagnosed with Ragas (faithfulness 0.829 to 0.320). Compares 64- and 512-token chunks while also changing k, so the two effects can't be told apart. | No (3 constructed cases) |

Other results on the page: hackernoon, datanorth, memx, a Redis blog, and LlamaIndex's "RAG failure mode checklist" documentation. All of them explain the method. None reports a measured split of failure stages.

What every top result already covers: the rule (gold evidence not in top-k means retrieval; in top-k but not in the final context means assembly; in the final context but answered wrong means generation), the need to log the top-k list and the final context, and the known-good-context test. What none covers: on one fixed question set, which stage's failures move when chunk settings change, and whether bigger chunks under a fixed context budget fix retrieval failures while creating assembly failures.

## Evidence 2: official definitions (read 2026-11-18)

| Source | What it says | Which stage it points to |
|---|---|---|
| [Ragas: Context Recall](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_recall/) | "measures how many of the relevant documents (or pieces of information) were successfully retrieved"; needs a reference. The page also says the legacy metrics API is deprecated in 0.4 and will be removed in 1.0. | Retrieval |
| [Ragas: Faithfulness](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/) | "how factually consistent a response is with the retrieved context", scored 0 to 1, higher scores mean better consistency. | Generation |
| [Amazon Bedrock: rerank](https://docs.aws.amazon.com/bedrock/latest/userguide/rerank.html) | Minimum input: a reranker model, the query, and "A list of documents that the reranker must reorder according to their relevance to the query." | Retrieval (only within the candidate list) |
| [Barnett et al., Seven Failure Points When Engineering a RAG System (arXiv 2401.05856, CAIN 2024)](https://arxiv.org/abs/2401.05856) | Seven failure points, FP1 Missing Content to FP7 Incomplete. "Not in Context" means the document was retrieved but did not make it into the context used for generation. | Assembly |
| [Lewis et al., Retrieval-Augmented Generation (arXiv 2005.11401)](https://arxiv.org/abs/2005.11401) | The original design: retrieved passages are passed to a generator. | Background |

## Evidence 3: how people phrase the search

Google autocomplete, checked 2026-11-18 with hl=en:

- Returned: "rag retrieval failure", "rag not working well", "anythingllm rag not working", "openwebui rag not working", "lm studio rag not working", "rag debugging", "how to evaluate retrieval quality in rag (pipelines)", "rag failure modes", "why rag is used (in llm)", "rag retrieval and generation", "rag retrieval augmented generation vs fine tuning".
- Empty: "rag wrong answer", "rag chunk size vs", "rag hallucination even with", "rag context recall vs". Demand for these is spread across full-sentence queries, not one short phrase.

No Naver data was collected because the topic has no Korea angle.

## Evidence 4: E1, 30 questions over the Kubernetes docs under four chunk settings (run 2026-11-18)

Setup, fixed before any answer was generated:

- Corpus: kubernetes/website `content/en/docs`, commit `1fad96080d1f9d8221813823b27b78f0299265dd` (2026-11-17), CC BY 4.0. Front matter, Hugo shortcodes and link targets stripped (`e1/scripts/build.py`). Tokens counted with tiktoken cl100k_base.
- 30 questions written before the run (`e1/questions.jsonl`, created 2026-11-18T08:05Z): 10 short facts (S), 10 with a condition (C), 10 procedures (P). Each has a gold sentence from one docs page and the expected answer terms.
- Settings: A = 500-token windows, overlap 100 (1,195 chunks); B = 1,000-token windows, overlap 200 (628); C = split at Markdown headings, large sections in 500/100 windows, page title and heading path prefixed to each chunk (2,671); D = the same split as C without the prefix (2,671).
- Retrieval: nomic-embed-text v1.5 (Q8_0), cosine, top-50 kept, top-k 5. Assembly: top-5 chunks added in rank order until a 3,000-token budget is full; lower-ranked chunks are cut. Generation: Qwen2.5-3B-Instruct (Q4_K_M) through llama.cpp, temperature 0, seed 42, a two-line "Answer / Quote" prompt that allows "not in context". To save CPU time, an answer was generated only when the gold sentence reached the prompt.
- Labels: gold sentence not in top-5 = retrieval; in top-5 but cut by the budget = assembly; in the prompt but the Answer line is wrong = generation. The Answer line decides, because that is what an app shows: a reply that states the right value and then ends with "Answer: not in context" is a generation failure. Four replies the string grader marked wrong were right in meaning and were overridden (`e1/grading-overrides.json`, each with its reason). The per-question table is `e1/e1-classified.csv`; its last column also says whether the right terms appear anywhere in the reply.

Results (correct / retrieval / assembly / generation, out of 30):

| Setting | Correct | Retrieval | Assembly | Generation |
|---|---|---|---|---|
| A 500/100 | 18 | 6 | 0 | 6 |
| B 1,000/200 | 5 of 22 generated, 8 not generated | 7 | 4 | 6 of 22 |
| C headings + path prefix | 21 | 4 | 0 | 5 |
| D headings, no prefix | 21 | 8 | 0 | 1 |

What the per-question rows show:

1. **The heading path moved failures between stages without moving accuracy.** C and D cut the documents at the same places; only the prefix differs. The prefix halved retrieval misses (D 8, C 4) and accuracy stayed at 21 of 30 in both. Of the four questions the prefix rescued from retrieval (S08, P09, C09, P10), two were then answered correctly and two failed with the gold sentence in the prompt; two questions D answered correctly (C06, P06) failed at generation under C. An accuracy number alone would say the prefix did nothing.
2. **No question failed at generation in all three fully generated settings (A, C, D).** C06 failed at generation in A and C, C05 in C and D; every other generation failure appeared in one setting only. The questions that failed at the same stage in all three were retrieval misses (S10, C03, P04); C05 was wrong in all three but moved from retrieval (A) to generation (C, D). With this small model, whether the right chunk in the prompt led to a right answer depended on what else sat in the prompt, so a generation failure here was not a fixed property of the question.
3. **Bigger chunks under a fixed budget created assembly failures.** In B, only three or four 1,000-token chunks fit in 3,000 tokens, and four questions had the gold chunk at rank 4 or 5 and lost it (S02, S06, S07, S10). A answered three of those (S02, S06, S07) correctly.
4. Content-only view: if a reply counts as right whenever it states the right value anywhere, A goes to 21 correct and 3 generation failures; C and D do not change. Point 1 holds under both views.

Not run, because the machine ran out of memory while B was generating and local model servers are no longer started on it: generation for 8 B questions (P03 to P10, all with the gold sentence in the prompt), the B-control run without a budget, and the known-good rerun (gold chunk alone for each generation failure). The numbers above come from one run of one 3B model on one corpus and say nothing general about how RAG failures split.

## Limits

- Result URLs other than official pages were not kept in the brief; the titles above find them. The top-result comparison covers the results seen on one day for two queries. Rankings change.
- The Barnett failure-point names and the "Not in Context" definition were checked against the arXiv PDF on November 18, 2026 (FP3: "Documents with the answer were retrieved from the database but did not make it into the context for generating an answer.").
- Evidence 4 is one run of a 3B model on 30 questions; it shows that stages move under a chunk change, not how your own wrong answers will split.

## Added for the reader (2026-11-18)

Two "how" steps the article now gives, with where they come from.

- **Logging the prompt the model actually received.** In our run (`e1/scripts/gen.py`) each question's record holds the top-k IDs (`topk`), the IDs that went into the prompt (`final_ids`), the prompt's token count (`final_tokens`) and the prompt text (`final_context`), written right before the model call. For frameworks, checked 2026-11-18:
  - [LlamaIndex observability](https://developers.llamaindex.ai/python/framework/module_guides/observability/): `llama_index.core.set_global_handler("simple")` "prints every LLM input/output pair to the terminal".
  - [LangSmith: trace with LangChain](https://docs.langchain.com/langsmith/trace-with-langchain): set `LANGSMITH_TRACING` (plus an API key) and run the code as usual; each LLM invocation becomes a nested run in the trace.
- **What a heading-path prefix looks like.** Setting C in `e1/scripts/build.py` joins the section word, the page title and the headings above the chunk with " > " and puts that line before the chunk text. The rank-2 chunk for P09 ("After draining a node for maintenance…", rank 9 without the prefix) is `C:tasks/administer-cluster/safely-drain-node.md#4` and starts with `Tasks > Safely Drain a Node > Use \`kubectl drain\` to remove a node from service`; its text contains `kubectl uncordon <node name>`.
- Moved out of the article body (reader r1): Barnett et al. FP3 "Not in Context" (Conclusion 5 above); the Ragas Context Recall / Faithfulness contrast (Conclusion 3 above); the generation model name (Qwen2.5-3B-Instruct, temperature 0) and the 17-of-18 count of retrieval misses ranked 7 to 37 under A, C and D (6 + 4 + 8 misses; one ranked outside the top 50).
- Moved out of the article body (reader r2, 2026-11-18): how the 30 questions were made (10 short facts, 10 with a condition, 10 procedures, written before the run; Evidence 4 Setup) and the rank range of the remaining retrieval misses (ranks 7 to 37, see above). The article now shows the assembly loop from `e1/scripts/gen.py` in shortened form as an example of logging kept and dropped chunk IDs. Setting B has no score out of 30 because 8 of its questions were not generated (Evidence 4).
- **Splitters that keep headings as metadata (reader r3, checked 2026-11-18).** [LlamaIndex MarkdownNodeParser API reference](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/markdown/): with `include_metadata` (default True) each node gets `metadata["header_path"]`, joined by `header_path_separator` (default "/"). [LangChain MarkdownHeaderTextSplitter reference](https://reference.langchain.com/python/langchain-text-splitters/markdown/MarkdownHeaderTextSplitter): `headers_to_split_on` = "Headers we want to track"; `strip_headers` defaults to True (headers removed from chunk text).
- Moved out of the article body (reader r3, 2026-11-18): in the Q-28 scene, the prompt's token count sat just under the 3,000-token limit when ranks 4 and 5 were cut.

Article: [RAG Retrieval vs Generation Failure: How I Tell Them Apart](https://loopnotes.dev/rag-retrieval-vs-generation-failure/)
