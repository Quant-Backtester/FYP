# Basic Setup

## Formatter Setup

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
  },
  // your other settings ...
}
```
- Use tab size 2 for the entire project development
- format document when you need.



# External Library
- read [svelte-i18n](https://github.com/kaisermann/svelte-i18n/blob/main/docs/Getting%20Started.md) for localization
- read [svelte-shadcn](https://shadcn-svelte.com/) for UI component library