# Agro: working notes for Claude

This repository (FARADTechnologies/Agro) is the deployed full system: the backend copied
from FARADTechnologies/agro-invest-portal (private, where the backend team works) plus the
redesigned web UI in `web/`. It must always run the newest backend with a UI that fits it.

## Standing order: keep everything current, without asking

At the start of every session, and before finishing any task:

1. `git remote add upstream https://github.com/FARADTechnologies/agro-invest-portal.git` if
   missing, then `sh scripts/sync-upstream.sh`. Exit 0 = up to date; exit 10 = the backend was
   copied and the script lists upstream web/ changes.
2. Port every listed upstream web change into the redesign: same behaviour, our look
   (sage/lime theme, rounded-2xl panels, motion). New upstream pages may be copied as-is and
   restyled; never overwrite our redesigned files with upstream's.
3. If an open pull request `sync/upstream` exists (made by the Upstream sync workflow), finish
   it the same way and merge it.
4. `cd web && npx tsc --noEmit && npm run build` (build with a separate `NEXT_DIST_DIR` or stop
   the dev server first: the build overwrites `.next`).
5. Commit, push to `origin main`. CI tests and deploys to Render. If the Render deploy hook
   secrets are missing, deploy by hand in the Render dashboard (Manual Deploy → Deploy latest
   commit, API first). If neither works, end the reply with a line in CAPITALS asking the user
   to push or deploy.

UI text is Azerbaijani only for now.

## Waiting to merge

- Branch `ui/citizenship-admin-listings` (citizenship at registration, no sahibkar role, listing
  desk in /admin) needs backend PR FARADTechnologies/agro-invest-portal#1. As soon as that PR is
  merged upstream: run the sync, then merge this branch into main (resolve
  `web/src/lib/api/schema.d.ts` by taking upstream's), typecheck, build, push.

## Rules

- `api/`, `seed/`, `ektis-mock/`, `geo/`, `docs/`, `deploy/nginx/`, `docker-compose.yml`,
  `.env.example` and `web/src/lib/api/schema.d.ts` are exact upstream copies. Do not edit
  them here; change them upstream. Render glue lives in `deploy/render/`.
- Never `git merge` upstream into this repository: the histories are unrelated and upstream
  is private. `.upstream-sync` records the upstream commit this repository matches.
- Local UI work: `cd web && npm run dev:live` uses the deployed API; `npm run mock-api` plus
  `npm run dev` works offline with the mock.
