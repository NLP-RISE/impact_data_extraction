# impact_data_extraction

### Motivation
- Lighter version of Wikipmacts database
- Allows creating a package release for our normalizers
- Evaluation set that we are able to modify without affecting work on the main Wikimpacts repo

### Goals
- Implement JSON output using LangChain
- Experiment with CoT and MAD for impact data extraction
- Advanced prompting to handle multi-event articles in the same way as single-event articles

### TODOs
- [x] move relevant code
- [x] get clean annotations
- [ ] plot stats on clean annotations
- [ ] benchmark some open source models on the exact same datasets before the double annotations and corrections + gpt4 + gpt5
- [ ] implement simple CoT with open source models; proposed qwen and deepseek (maybe deepseek R)
- [ ] implement MAD CoT with open source models; compare results