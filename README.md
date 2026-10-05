# BYOK Store

A public catalog of bring‑your‑own‑key AI Android apps: the static site in `docs/` (GitHub Pages) plus `catalog.json`, which the **BYOK Store** Android app (`app/`) reads.

- Site: https://mohithash.github.io/byok-store/
- Catalog JSON: https://mohithash.github.io/byok-store/catalog.json

## Regenerate

```sh
FACTORY=/path/to/byok-factory python3 store_site.py   # writes site/ (git-ignored)
rm -rf docs/* && cp -r site/* docs/                   # what publish.sh does before it commits and pushes
```

- `FACTORY` is optional. Without it the script uses the first of `../byok-factory` (next to this repo) and `/root/claude/Factory` that exists. The store directory is wherever `store_site.py` lives, and the output always goes to `site/` beside it.
- `./publish.sh "message"` regenerates, copies `site/` into `docs/`, commits and **pushes to `main`**. It can be run from any directory.
- Release links use the factory's `RELEASED_VERSION` file (e.g. `1.0`; it defaults to `1.0` when the file is missing): `releases/download/{id}-v{ver}/{id}-v{ver}.apk`.
- An app is `released` when `dist/{id}-v{ver}.aab` exists in the factory **or** the current `docs/catalog.json` already marks it released. So regenerating on a machine without `dist/` never turns a released app back into "soon".
- The site is `template.html` with `__COUNT__`/`__CATS__` filled in. It is a single self-contained file with no external scripts.

## catalog.json

Top level: `generated` / `updated` (ISO date of the build), `count`, `categories`, `engine_features`, `apps`.

`engine_features` comes from `FEATURES_BY_VERSION` in `store_site.py`: the list for the newest engine version ≤ the Factory's `RELEASED_VERSION`, so the store only promises what the downloadable APKs actually do. Add the next version's list there before bumping `RELEASED_VERSION`.

Each app has `id`, `name`, `tagline`, `category`, `about`, `colors`, `icon`, `icon_url`, `package`, `tools[]` (`emoji`, `title`, `subtitle`), `apk`, `aab`, `source`, `listing`, `kind` (`factory` | `bespoke`), `released`, and:

| field | factory apps | hand-built (`bespoke`) apps |
|---|---|---|
| `version` | the factory `RELEASED_VERSION` | that app's own release (e.g. `1.2`) |
| `features` | what the app includes at its released `version`: the `engine_features` list, except that from v1.1 the share-into-the-app line is per app (photos only for apps with a photo tool) | `[]` (their abilities are described in `about`) |

Fields are only ever **added**, never renamed or removed, so older StoreApp builds keep working.

## Site features

- Search, category chips plus a **Hand‑built** chip, and a sort menu (Featured · A–Z · Category).
- The state lives in the URL, so a link restores the same view: `?q=`, `?cat=`, `?sort=`, and `#app-id` to open an app.
- <kbd>/</kbd> focuses search. <kbd>Esc</kbd> clears the search or closes the app dialog.
- The app dialog shows the version, the tools, a collapsed "What's inside every app" list for factory apps, and a **Copy link** button.
- An "Every app includes" panel under the header lists `engine_features`. It is collapsed on phones.
