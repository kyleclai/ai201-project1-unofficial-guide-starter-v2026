# RAG

## How to increase confidence in RAG systems

Citations (however they can be right)

## How RAG Fails

1. Retrieval misses: the right chunk exists, but it wasn't fetched
2. The docs are wrong: retrieval can work perfectly and still deliver garbage (not an engineering prob - its a project mngmnt/communication one)
3. The model ignores it: it falls back on its training data and answer from memory anyway (stochastic parrot - if the words we used aren't similar enough to get a high confidence match fromm the chunk. the size of the chunk is the best way to make changes (size is one of the determining factors in determing the size of the vector) so it will fall on whatever data it has, usually the foudnational model).

Bad examples: ablucinaciones.com/cases
Hallucinations often look correct and have the right shape... but won't be right

token = a bit of data abt the size of a word (the size isn't determined, it can be a part of a word or in rare cases a phrase e.g. "and honestly" if it's super overuse). something that makes sense to itself. 
- Word, sub-word or group of words that occur together.

token: number representation of a token

embedding: entire chunks

