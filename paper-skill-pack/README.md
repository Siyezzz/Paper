# Paper Skill Pack

A compact, evidence-first skill collection for academic paper discovery, reading, evaluation, and drafting.

Copy the folders under `skills/` to your Codex skills directory, or install selected folders into a project-local skill location supported by your agent.

The collection intentionally separates discovery from citable evidence: search results are candidates, while claims in a draft must trace to a paper PDF or an authoritative publication page.

## Included skills

### Upstream research skills

- `research-lr-ra`: literature mapping and reading prioritization.
- `research-literature-trace`: source screening and citation traceability.
- `paper-finder`: search a local paper-note collection.
- `paper-analyzer`: generate structured notes for a single paper; includes helper scripts in `scripts/`.

### Pack-specific companion skills

- `paper-note-search`: search a local paper-note collection.
- `paper-deep-reading`: make structured, source-grounded notes for one paper.
- `paper-evidence-writing`: draft only from an explicit evidence ledger.
- `paper-evaluation-design`: design reproducible empirical evaluations and ablations.

## Install

Copy any folder under `skills/` into your Codex skills directory:

```bash
cp -R paper-skill-pack/skills/research-lr-ra ~/.codex/skills/
cp -R paper-skill-pack/skills/research-literature-trace ~/.codex/skills/
cp -R paper-skill-pack/skills/paper-finder ~/.codex/skills/
cp -R paper-skill-pack/skills/paper-analyzer ~/.codex/skills/
```

On Windows PowerShell:

```powershell
Copy-Item -Recurse -Force paper-skill-pack\skills\research-lr-ra $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse -Force paper-skill-pack\skills\research-literature-trace $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse -Force paper-skill-pack\skills\paper-finder $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse -Force paper-skill-pack\skills\paper-analyzer $env:USERPROFILE\.codex\skills\
```

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for upstream attribution.
