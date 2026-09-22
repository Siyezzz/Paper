---
name: paper-note-search
description: Search a local collection of paper notes by title, author, keyword, method, dataset, or research domain.
---

# Paper Note Search

Use this skill only for an existing local paper-note collection. It does not search the web or establish new literature evidence.

## Workflow

1. Parse the request into title, author, domain, method, dataset, or keyword terms; retain exclusions.
2. Search note filenames, frontmatter, and body text. Report the source note path and the matching passage.
3. Rank exact title and author matches above method/domain mentions. Explain ties or ambiguous author names.
4. Return a compact result table: paper, score, why it matched, and local note path.

Do not invent metadata absent from the local notes. If no results exist, suggest a search query for the literature-mapping workflow instead.
