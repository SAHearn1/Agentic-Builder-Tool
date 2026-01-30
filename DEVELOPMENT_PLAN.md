# Agentic Builder Tool - Development Plan

> **Document Owner:** Shawn Hearn  
> **Last Updated:** January 30, 2026  
> **Status:** Active Development

---

## 📊 Project Overview

**Repository:** https://github.com/SAHearn1/Agentic-Builder-Tool  
**Live Demo:** https://agentic-builder-tool.vercel.app  
**Tech Stack:** Python 3.11+ | LangGraph | FastAPI | Claude 3.5 Sonnet

**Purpose:** Autonomous DevOps agent that writes code, manages GitHub repos, deploys to Vercel, and stores artifacts in GCS.

---

## 🎯 Current Status

### Recently Completed
| Item | Date | Notes |
|------|------|-------|
| ✅ Merged PR #9 | Jan 30, 2026 | Lazy-load optional dependencies |
| ✅ Merged PR #8 | Jan 30, 2026 | Setup guide & deployment improvements |
| ✅ Added DEVELOPMENT_PLAN.md | Jan 30, 2026 | This document |

### Blocking Issues
| Issue | Priority | Action Needed |
|-------|----------|---------------|
| Vercel deployment returning 500 | 🔴 Critical | Set env vars & redeploy |

---

## 🗺️ Development Roadmap

### Phase 1: Stabilization ⏳ IN PROGRESS
**Target:** February 2026  
**Goal:** Production-ready deployment

| Task | Status | Notes |
|------|--------|-------|
| Merge PR #9 (lazy-load dependencies) | ✅ Done | Jan 30, 2026 |
| Merge PR #8 (deployment fixes) | ✅ Done | Jan 30, 2026 |
| Set Vercel environment variables | ⬜ **ACTION REQUIRED** | See instructions below |
| Trigger Vercel redeploy | ⬜ **ACTION REQUIRED** | After env vars set |
| Verify /health endpoint | ⬜ Blocked | Waiting on deploy |
| Verify /agent/task endpoint | ⬜ Blocked | Waiting on deploy |
| Test end-to-end agent flow | ⬜ Blocked | Waiting on deploy |

#### 🔧 REQUIRED: Vercel Environment Variables

Go to: **Vercel Dashboard → agentic-builder-tool → Settings → Environment Variables**

Add these variables:

```
ANTHROPIC_API_KEY=sk-ant-api03-your-key
GITHUB_TOKEN=ghp_your-token
VERCEL_TOKEN=your-vercel-token
GCS_PROJECT_ID=your-gcp-project
GCS_BUCKET_NAME=your-bucket-name
GOOGLE_APPLICATION_CREDENTIALS_JSON={"type":"service_account",...}
APP_ENV=production
ALLOWED_ORIGINS=https://agentic-builder-tool.vercel.app
```

**Note:** For `GOOGLE_APPLICATION_CREDENTIALS_JSON`, paste the entire service account JSON as a single line.

After adding, click **Redeploy** on the latest deployment.

---

### Phase 2: Testing & Quality
**Target:** February 2026  
**Goal:** Reliable, testable codebase

| Task | Status | Owner |
|------|--------|-------|
| Add unit tests for all tools | ⬜ Todo | - |
| Add integration tests for GitHub tools | ⬜ Todo | - |
| Add integration tests for Vercel tools | ⬜ Todo | - |
| Set up GitHub Actions CI pipeline | ⬜ Todo | - |
| Add test coverage reporting | ⬜ Todo | - |
| Add pre-commit hooks (black, ruff, mypy) | ⬜ Todo | - |

### Phase 3: Feature Expansion
**Target:** March 2026  
**Goal:** Enhanced capabilities

| Task | Status | Owner |
|------|--------|-------|
| Add AWS deployment tools (S3, Lambda) | ⬜ Todo | - |
| Add Docker build/push tools | ⬜ Todo | - |
| Add Slack/Discord notification tools | ⬜ Todo | - |
| Add database migration tools | ⬜ Todo | - |
| Implement agent memory/persistence | ⬜ Todo | - |
| Add multi-file commit support | ⬜ Todo | - |

### Phase 4: User Experience
**Target:** March 2026  
**Goal:** Easy onboarding & usage

| Task | Status | Owner |
|------|--------|-------|
| Build web UI dashboard | ⬜ Todo | - |
| Add task history/logging UI | ⬜ Todo | - |
| Create example task library | ⬜ Todo | - |
| Add streaming response UI | ⬜ Todo | - |
| Write comprehensive tutorials | ⬜ Todo | - |

### Phase 5: Enterprise Features
**Target:** Q2 2026  
**Goal:** Production enterprise use

| Task | Status | Owner |
|------|--------|-------|
| Add authentication/API keys | ⬜ Todo | - |
| Add rate limiting | ⬜ Todo | - |
| Add audit logging | ⬜ Todo | - |
| Add multi-tenant support | ⬜ Todo | - |
| Add role-based access control | ⬜ Todo | - |

---

## 📋 Backlog (Unprioritized)

- [ ] Support for GitLab (in addition to GitHub)
- [ ] Support for Netlify (in addition to Vercel)
- [ ] Support for Azure DevOps
- [ ] Webhook triggers for automated workflows
- [ ] Template library for common project scaffolds
- [ ] Cost tracking for API usage
- [ ] Agent conversation branching
- [ ] Rollback/undo capabilities
- [ ] Integration with Notion/Linear for project management

---

## 🔧 Technical Debt

| Item | Severity | Notes |
|------|----------|-------|
| Hardcoded iteration limit | Low | Make configurable per-request |
| No request validation | Medium | Add Pydantic validators |
| Missing type hints in some functions | Low | Full mypy compliance |
| No retry logic for API calls | Medium | Add exponential backoff |
| Secrets in environment variables | Low | Consider secrets manager |

---

## 📈 Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Test Coverage | 0% | 80% |
| Open PRs | 0 | 0 |
| Deployment Status | ❌ Failing | ✅ Healthy |
| Avg Task Completion Time | Unknown | < 60s |
| Documentation Coverage | 80% | 100% |

---

## 🏷️ Labels for GitHub Issues

Create these labels for tracking:

| Label | Color | Description |
|-------|-------|-------------|
| `phase-1` | `#1D76DB` | Stabilization phase |
| `phase-2` | `#5319E7` | Testing & quality |
| `phase-3` | `#0E8A16` | Feature expansion |
| `phase-4` | `#FBCA04` | User experience |
| `phase-5` | `#D93F0B` | Enterprise features |
| `bug` | `#D73A4A` | Bug report |
| `enhancement` | `#A2EEEF` | New feature |
| `documentation` | `#0075CA` | Documentation |
| `good-first-issue` | `#7057FF` | Good for newcomers |

---

## 📅 Weekly Check-in Template

```markdown
## Week of [DATE]

### Completed
- [ ] Task 1
- [ ] Task 2

### In Progress
- [ ] Task 3 (50%)

### Blocked
- [ ] Task 4 - Reason: [explain]

### Next Week
- [ ] Task 5
- [ ] Task 6
```

---

## 📞 Resources

- **LangGraph Docs:** https://langchain-ai.github.io/langgraph/
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Anthropic API:** https://docs.anthropic.com/
- **Vercel API:** https://vercel.com/docs/rest-api
- **GitHub API:** https://docs.github.com/en/rest

---

*This document should be updated weekly during active development.*
