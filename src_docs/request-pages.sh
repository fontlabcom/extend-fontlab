#!/bin/sh
# this_file: src_docs/request-pages.sh
# Pages builds latest default; guards expose source races without rewriting refs.
set -eu
expected=${1:?Expected qualified output commit is required}
: "${GITHUB_REPOSITORY:?Repository identity is required}"
test "$(git rev-parse HEAD)" = "$expected"
test "$(gh api "repos/$GITHUB_REPOSITORY" --jq .default_branch)" = main
gh api "repos/$GITHUB_REPOSITORY/pages" | python -c '
import json, sys
site = json.load(sys.stdin)
assert site["build_type"] == "legacy", "Pages must use branch source"
assert site["source"] == {"branch": "main", "path": "/docs"}, "Pages must publish main:/docs"
'
remote_sha=$(gh api "repos/$GITHUB_REPOSITORY/git/ref/heads/main" --jq .object.sha)
if test "$remote_sha" != "$expected"; then
  echo "Pages request superseded by current main: $remote_sha"
  exit 0
fi
gh api --include --method POST "repos/$GITHUB_REPOSITORY/pages/builds"
test "$(gh api "repos/$GITHUB_REPOSITORY/git/ref/heads/main" --jq .object.sha)" = "$expected"
