#!/usr/bin/env bash
set -euo pipefail

tag="${1:?tag is required}"
notes="${2:?notes file is required}"
prerelease="${3:?prerelease flag is required}"
repo="${GH_MIRROR_REPO:?GH_MIRROR_REPO is required}"
case "$prerelease" in
  true|false) ;;
  *) echo "prerelease must be true or false" >&2; exit 2 ;;
esac

token="$(tools/gh_app_token.sh)"
auth="Authorization: Bearer ${token}"
response="$(mktemp)"
request="$(mktemp)"
trap 'rm -f "$response" "$request"' EXIT
for delay in 0 5 15 30 60; do
  [ "$delay" = 0 ] || sleep "$delay"
  code=$(curl -sS -o /dev/null -w '%{http_code}' --max-time 30 -H "$auth" \
           "https://api.github.com/repos/${repo}/git/ref/tags/${tag}")
  [ "$code" = "200" ] && break
done
if [ "$code" != "200" ]; then
  echo "tag ${tag} never reached the GitHub mirror (HTTP $code)." >&2
  echo "Refusing to POST: GitHub would create the tag at main instead." >&2
  exit 1
fi
jq -n --arg t "$tag" --rawfile b "$notes" --argjson p "$prerelease" \
   '{tag_name:$t,name:$t,body:$b,draft:false,prerelease:$p} + (if $p then {} else {make_latest:"true"} end)' \
   > "$request"
for delay in 0 5 15 30 60; do
  [ "$delay" = 0 ] || sleep "$delay"
  code=$(curl -sS -o "$response" -w '%{http_code}' --max-time 30 \
           -X POST -H "$auth" -H 'Accept: application/vnd.github+json' \
           --data @"$request" \
           "https://api.github.com/repos/${repo}/releases")
  case "$code" in
    201) echo "mirrored release ${tag} to ${repo}"; exit 0 ;;
    422) echo "release ${tag} already exists on the mirror"; exit 0 ;;
  esac
  echo "HTTP $code: $(cat "$response")" >&2
done
echo "GitHub refused the Release object for ${tag} on every attempt." >&2
echo "The tag is mirrored; only the GitHub Release is missing." >&2
exit 1
