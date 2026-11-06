#!/bin/sh
# this_file: src_docs/publish.sh
# Commit only generated output; ordinary push rejects concurrent writers.
set -eu
source_sha=${1:?Expected source commit is required}
: "${GITHUB_OUTPUT:?GitHub output file is required}"
test "$(git rev-parse HEAD)" = "$source_sha"
test -z "$(git diff --cached --name-only)"
remote_ref=$(git ls-remote --exit-code origin refs/heads/main)
remote_sha=$(printf '%s\n' "$remote_ref" | cut -f1)
if test "$remote_sha" != "$source_sha"; then
  echo "Publication superseded by current main: $remote_sha"
  exit 0
fi
git add -- docs
if ! git diff --cached --quiet; then
  git -c user.name='github-actions[bot]' \
      -c user.email='41898282+github-actions[bot]@users.noreply.github.com' \
      commit -m 'docs: rebuild generated site'
  git push origin HEAD:refs/heads/main
fi
printf 'sha=%s\n' "$(git rev-parse HEAD)" >> "$GITHUB_OUTPUT"
