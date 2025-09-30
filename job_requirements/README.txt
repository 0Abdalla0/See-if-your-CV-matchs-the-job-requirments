Job Requirements package
Generated: 2025-09-30 07:41:57 UTC

Contents:
- 10 job requirement files (JSON) and corresponding human-readable Markdown files.
- matching_rules.json: a suggested scoring algorithm and notes to help you build an automated tester.

Usage ideas:
- Use the JSON files to build a script that parses CV text, looks for keywords, compares years of experience and degree, and computes a match score using matching_rules.json.
- The 'keywords' field provides many tokens you can search the CVs for. Use case-insensitive matching and allow simple stemming (e.g., 'docker' matches 'Docker').

Notes:
- These are templates for testing only. Adjust weights and rules to match your hiring policy.
