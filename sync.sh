#!/usr/bin/env bash
# ==============================================================================
# SFUSION - Automated Synchronization and Push Script
# Usage:
#   ./sync.sh "commit message"
#   ./sync.sh                     (uses automated timestamped message)
# ==============================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

BRANCH=$(git branch --show-current 2>/dev/null || echo "main")
COMMIT_MSG="$1"

if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="chore: update SFUSION modules ($(date '+%Y-%m-%d %H:%M:%S'))"
fi

echo -e "${BLUE}=== [SFUSION] Synchronizing with GitHub ===${NC}"
echo -e "${BLUE}Current branch:${NC} ${BRANCH}"

echo -e "${BLUE}1/3 Staging files...${NC}"
git add -A

if git diff --cached --quiet; then
    echo -e "${YELLOW}No new changes to commit.${NC}"
else
    echo -e "${BLUE}2/3 Committing: \"${COMMIT_MSG}\"...${NC}"
    git commit -m "$COMMIT_MSG"
fi

echo -e "${BLUE}3/3 Pushing to GitHub (origin ${BRANCH})...${NC}"
git push origin "$BRANCH"

echo -e "${GREEN}✔ SFUSION successfully updated on GitHub!${NC}"
