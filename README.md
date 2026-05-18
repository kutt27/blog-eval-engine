# Blog Evaluation Engine

A straightforward blog evaluator engine build using semantic rag. 

## Initial Architecture

![Architecture](/architecture.png)

## Data Flow

```text
POST /evaluate
   │
   ▼
_retrieve_context(req, k=6)
   ├── rag.build_query(audience, style, purpose, blog_type, platform, custom)
   └── rag.retrieve(query, k=6)
            ├── lazy load MiniLM model + chunks (cached in .rag_cache.npz)
            └── cosine top-k over normalized embeddings
   │
   ▼
build_prompt(req, snippets)  →  config + retrieved excerpts + content
   │
   ▼
llm.evaluate(prompt)   ──  Groq llama-3.3-70b-versatile, response_format=json_object
   │                       │
   │                       └── on any error → _mock_result(req) with mode="mock"
   ▼
EvaluationResult.model_validate(raw)  →  pydantic-enforced contract
```

The engine only handles few rules (focus is on technical blog now). Therefore, using torch is a overkill. Therefore, we are switching to a small model called `fastembed`. Reasons:
- ~40× smaller install
- No torch, no transformers — fewer moving parts
- Same retrieval quality for our use case (6 short markdown files)
- Same API surface (embed(list_of_texts) → iterator of numpy arrays)
- Cold-start is faster too (no torch import)

### Verify after install

```sh
pip install -r requirements.txt
python -c "import rag; r = rag.retrieve('how to evaluate beginner audience tutorials', k=3); [print(x['source'], '→', round(x['score'],3)) for x in r]"
```

First model will be downloaded on the first run.

Run the server:
```sh
python server.py
```

## API

```text
POST /evaluate HTTP/1.1
Content-Type: application/json

{
  "blog_type": "technical",
  "audience": "beginners",
  "style": "educational",
  "platform": "blog",
  "purpose": "teaching",
  "content": "..."
}
```
