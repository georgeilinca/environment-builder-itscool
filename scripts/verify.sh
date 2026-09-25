#!/bin/bash

set -u

GENERATED_FILE="generated.yml"

echo "=================================================================="
echo " Environment Builder - Verificarea instalarii tehnologiilor cerute"
echo "=================================================================="
echo

if [ ! -f "$GENERATED_FILE" ]; then
    echo "ERROR: Fisierul cu variabile generate nu a fost gasit: $GENERATED_FILE"
    echo "Ruleaza validarea configurarii mai intai (scriptul Python)."
    exit 1
fi

if ! command -v yq >/dev/null 2>&1; then
    echo "ERROR: Comanda 'yq' nu este instalata."
    echo "Instaleaza yq pentru a putea analiza fisierul YAML."
    exit 1
fi

echo "Citesc tehnologiile cerute..."
echo

FAILED=0

check_technology() {
    local technology="$1"
    local version="$2"
    local command="$3"

    if ! command -v "$command" >/dev/null 2>&1; then
        echo "[FAIL] $technology"
        echo "       Comanda '$command' nu a fost gasita."
        echo "       Versiune ceruta: $version"
        echo
        FAILED=1
        return
    fi

    local installed_version

    installed_version=$("$command" --version 2>&1 | head -n 1)

    echo "[INFO] $technology"
    echo "       Versiune ceruta:   $version"
    echo "       Versiune instalata: $installed_version"

    if [[ "$installed_version" == *"$version"* ]]; then
        echo "       Rezultat: [OK]"
    else
        echo "       Rezultat: [FAIL]"
        FAILED=1
    fi

    echo
}

TECHNOLOGIES=$(yq -r '.technologies | keys | .[]' "$GENERATED_FILE")

for technology in $TECHNOLOGIES; do

    enabled=$(yq -r ".technologies.$technology.enabled" "$GENERATED_FILE")

    if [ "$enabled" != "true" ]; then
        continue
    fi

    version=$(yq -r ".technologies.$technology.version" "$GENERATED_FILE")
    command=$(yq -r ".technologies.$technology.command" "$GENERATED_FILE")

    check_technology "$technology" "$version" "$command"
done

echo "=================================================================="

if [ "$FAILED" -eq 0 ]; then
    echo "Verificarea s-a incheiat cu succes - PASSED."
    exit 0
else
    echo "Verificarea a esuat - FAILED."
    exit 1
fi