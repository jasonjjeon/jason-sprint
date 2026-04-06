#!/usr/bin/env node

/**
 * BIND AI Pack 자동 업데이트 체크
 * Claude Code SessionStart hook에서 실행됨
 *
 * 동작: ~/.bind-ai-pack/ 에서 git pull → 버전 비교 → 변경 시 재배포
 */

import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { execSync } from 'node:child_process';
import { homedir } from 'node:os';

const cwd = process.cwd();
const versionFile = join(cwd, '.bind-version');
const packDir = join(homedir(), '.bind-ai-pack');

// 1. bind-ai-pack 워크스페이스가 아니면 무시
if (!existsSync(versionFile)) {
  process.exit(0);
}

let localVersion;
try {
  localVersion = readFileSync(versionFile, 'utf-8').trim();
} catch {
  process.exit(0);
}

// 2. ~/.bind-ai-pack/ 에서 git pull
if (existsSync(join(packDir, '.git'))) {
  try {
    const pullResult = execSync('git pull --ff-only', {
      cwd: packDir, stdio: 'pipe', shell: true, timeout: 15000,
    }).toString().trim();

    // 변경이 있었으면 버전 비교
    if (pullResult !== 'Already up to date.') {
      const pkgPath = join(packDir, 'package.json');
      if (existsSync(pkgPath)) {
        const pkg = JSON.parse(readFileSync(pkgPath, 'utf-8'));
        const latestVersion = pkg.version;
        if (latestVersion && latestVersion !== localVersion) {
          console.log(`[BIND AI Pack update] v${localVersion} → v${latestVersion}. Say "update" to apply.`);
        }
      }
    }
  } catch {
    // 네트워크 없으면 무시
  }
}

// 3. Anthropic 공식 스킬 자동 업데이트 (git pull)
const skillsRepoDir = join(homedir(), '.claude', 'anthropic-skills');
if (existsSync(join(skillsRepoDir, '.git'))) {
  try {
    execSync('git pull --ff-only', { cwd: skillsRepoDir, stdio: 'pipe', shell: true, timeout: 10000 });
  } catch { /* 실패해도 무시 */ }
}
