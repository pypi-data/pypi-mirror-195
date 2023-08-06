This project is an attempt to re-define certain architectures to be optimised to run on the ANE. More specifically, it aims to adopt this Apple's [`ml-ane-transformers`](https://github.com/apple/ml-ane-transformers) codebase to the [Whisper](https://github.com/openai/whisper) architecture. I've been working with the commit hash `d18e9ea` (there have been some changes to return signatures of internal functions -- that may not impact us, but I haven't tested that yet)

---

## Install

```bash
pip install git+https://github.com/openai/whisper/.git@d18e9ea5dd2ca57c697e8e55f9e654f06ede25d0
pip install git+https://github.com/apple/ml-ane-transformers
pip install whisper_ane
```
