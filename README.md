# GitHub URL Validator

Este repositório contém um utilitário Python para validar e normalizar URLs do GitHub, garantindo compatibilidade com conectores que exigem formatos estritos.

## Funcionalidades

- Detecta URLs inválidas para abertura de repositórios/paths.
- Extrai `owner`, `repo`, `branch` e `path`.
- Sugere URLs canônicas no formato esperado por conectores estritos.

## Uso

```bash
python github_url_validator.py "https://github.com/openai/codex/tree/main/docs"
```

## Exemplo de Saída

```json
{
  "input_url": "https://github.com/openai/codex/tree/main/docs",
  "is_github": true,
  "classification": "repo_tree_url",
  "owner": "openai",
  "repo": "codex",
  "branch": "main",
  "path": "docs",
  "is_valid_for_strict_connector": true,
  "canonical_url": "https://github.com/openai/codex/tree/main/docs",
  "reason": "URL compatível com conector estrito",
  "search_query_hint": null
}
```
