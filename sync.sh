#!/usr/bin/env bash
# SFUSION (Smart Fusion) is an open-source visual data engineering platform for kinematic normalization and telemetry fusion.
# Copyright (C) 2026 Noxfort Systems
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# File: sync.sh
# Author: Gabriel Moraes
# Date: October 2026

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
