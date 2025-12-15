## Basic Setup

### Formatter Setup

- go download **Ruff** for your python formatter, and also the extension **Svelte for VS Code**
- Set the following in your user Setting for your VScode

```json
// settings.json
{
  "[python]": {
    "editor.tabSize": "2",
    "editor.defaultFormatter": "charliermarsh.ruff"
  },
  "[svelte]": {
    "editor.tabSize": 2,
    "editor.defaultFormatter": "svelte.svelte-vscode"
  }
  // your other settings ...
}
```

- Use tab size 2 for the entire project development
- format document when you need.
- For other IDE/text editor, please consult the documentation for the IDE/text editor

## Reusable Components

## External Library

- ### Frontend

  - localization [svelte-i18n](https://github.com/kaisermann/svelte-i18n/blob/main/docs/Getting%20Started.md)
  - UI component library [svelte-shadcn](https://shadcn-svelte.com/)
  - alert notification [Svelte Sonner](https://svelte-sonner.vercel.app/)

- ### Backend
  - Sql database [SqlAlchemy](https://docs.sqlalchemy.org/en/20/)
  - Server [fastapi](https://fastapi.tiangolo.com/)
  - encryption [bcybt](https://github.com/pyca/bcrypt)
  - jwt [PyJWT](https://pyjwt.readthedocs.io/en/stable/)
