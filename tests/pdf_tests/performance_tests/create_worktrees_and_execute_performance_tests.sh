#!/usr/bin/env bash

set -euo pipefail

#
# CONFIGURATION
#

NUMBER_OF_COMMITS=20

#
# DETERMINE REPOSITORY ROOT
#

REPO_ROOT="$(git rev-parse --show-toplevel)"
WORKTREE_ROOT="${1:-"$(dirname "$REPO_ROOT")/borb-worktrees"}"
BENCHMARK_SCRIPT="$REPO_ROOT/tests/pdf_tests/performance_tests/benchmark.py"
RESULTS_DIR="$REPO_ROOT/tests/pdf_tests/performance_tests/assets"

#
# CLEANUP
#

git -C "$REPO_ROOT" worktree prune

mkdir -p "$WORKTREE_ROOT"
mkdir -p "$RESULTS_DIR"

echo "Repository: $REPO_ROOT"
echo "Worktrees:  $WORKTREE_ROOT"
echo "Results:    $RESULTS_DIR"
echo

#
# CREATE WORKTREES AND RUN BENCHMARKS
#

git -C "$REPO_ROOT" log -"${NUMBER_OF_COMMITS}" --format="%H" | while read -r commit; do

    short_hash="${commit:0:12}"
    worktree_path="$WORKTREE_ROOT/$short_hash"
    worktree_benchmark="$worktree_path/tests/pdf_tests/performance_tests/benchmark.py"
    result_file="$RESULTS_DIR/$short_hash.json"

    echo "========================================"
    echo "Commit: $short_hash"
    echo "========================================"

    #
    # CREATE OR REUSE WORKTREE
    #

    if [[ ! -e "$worktree_path" ]]; then
        echo "Creating worktree..."
        git -C "$REPO_ROOT" worktree add --detach "$worktree_path" "$commit"
    else
        echo "Reusing existing worktree..."
    fi

    #
    # COPY BENCHMARK SCRIPT
    #

    echo "Copying benchmark script..."
    mkdir -p "$(dirname "$worktree_benchmark")"
    cp "$BENCHMARK_SCRIPT" "$worktree_benchmark"

    #
    # RUN BENCHMARK
    #

    echo "Benchmarking $short_hash..."
    (
      cd "$worktree_path"
      export PYTHONPATH="$worktree_path${PYTHONPATH:+:$PYTHONPATH}"
      python tests/pdf_tests/performance_tests/benchmark.py --output "$result_file"
    )
    echo "Results:"
    cat "$result_file"
    echo
done

#
# SUMMARY
#

echo "========================================"
echo "All benchmarks completed!"
echo "========================================"

echo
echo "Results:"
ls -lh "$RESULTS_DIR"

echo
echo "Worktrees:"
git -C "$REPO_ROOT" worktree list