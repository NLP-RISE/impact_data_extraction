# impact_data_extraction

### Motivation
- Lighter version of Wikipmacts database
- Allows creating a package release for our normalizers
- Evaluation set that we are able to modify without affecting work on the main Wikimpacts repo

### Goals
- Implement JSON output using ~~LangChain~~ outformer
- Experiment with CoT and MAD for impact data extraction
- Advanced prompting to handle multi-event articles in the same way as single-event articles

### TODOs
- [x] move relevant code
- [x] get clean annotations
- [x] plot stats on clean annotations
- [ ] benchmark some open source models on the exact same datasets before the double annotations and corrections + gpt4 + gpt5
- [x] solve the problem of clean json output
- [ ] implement simple CoT with open source models; proposed qwen and deepseek (maybe deepseek R)
- [ ] implement MAD CoT with open source models; compare results
- [ ] implement RAG for GADM to enable GID prediction by an LLM (preferably one that has also seen a lot of wikipedia or country data)
- [ ] consolidate double annotations with previous ones


### Candidate models

| Model | Notes |
|-------|-------|
| mistralai/Mixtral-8x7B-Instruct-v0.1 | works well out of the box |
| google/gemma-7b-it | ??? |