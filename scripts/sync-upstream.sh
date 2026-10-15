#!/bin/sh
# Brings the backend from the upstream repository (FARADTechnologies/agro-invest-portal)
# into this one and lists what changed in the upstream web UI.
#
# The backend paths below are exact copies of upstream: this script replaces them
# wholesale, including files upstream deleted. The web UI here is a redesign, so
# upstream web/ changes are not copied; they are listed to port by hand.
# .upstream-sync records the upstream commit this repository is in step with.
#
#   git remote add upstream https://github.com/FARADTechnologies/agro-invest-portal.git
#   sh scripts/sync-upstream.sh            # exit 0: up to date, 10: synced (commit it)
set -eu
cd "$(dirname "$0")/.."

REMOTE=${UPSTREAM_REMOTE:-upstream}
PATHS="api seed ektis-mock geo docs deploy/nginx docker-compose.yml .env.example web/src/lib/api/schema.d.ts"

git fetch -q "$REMOTE" main
last=$(cat .upstream-sync)
head=$(git rev-parse "$REMOTE/main")
if [ "$last" = "$head" ]; then
  echo "Up to date with $REMOTE/main ($(git rev-parse --short "$head"))."
  exit 0
fi

echo "New upstream commits:"
git log --oneline "$last..$head"

for p in $PATHS; do
  git rm -rqf --ignore-unmatch -- "$p"
  if git cat-file -e "$head:$p" 2>/dev/null; then
    git checkout "$head" -- "$p"
  fi
done
echo "$head" > .upstream-sync
git add .upstream-sync

echo
echo "Upstream web UI changes to port into the redesign by hand:"
git diff --stat "$last" "$head" -- web ':(exclude)web/src/lib/api/schema.d.ts'
echo
echo "Other upstream changes to review (README, scripts, CI):"
exclude=""
for p in $PATHS web; do exclude="$exclude :(exclude)$p"; done
# shellcheck disable=SC2086
git diff --stat "$last" "$head" -- . $exclude
exit 10
