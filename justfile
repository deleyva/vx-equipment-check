# Comprobación de PC Vitalinux

# Bump version, commit, tag, and push — triggers GitHub Actions release
release version:
    #!/usr/bin/env bash
    set -euo pipefail
    CURRENT=$(node -pe "require('./package.json').version")
    echo "📦 Bump: v${CURRENT} → v{{version}}"
    npm version {{version}} --no-git-tag-version
    sed -i '' 's/"version": "'"${CURRENT}"'"/"version": "{{version}}"/' src-tauri/tauri.conf.json
    git add package.json package-lock.json src-tauri/tauri.conf.json
    git commit -m "Bump version to v{{version}}"
    git tag "v{{version}}"
    git push && git push origin "v{{version}}"
    echo "✅ v{{version}} pushed — GitHub Actions will build the release"
