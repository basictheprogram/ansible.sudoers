# TODO

Flagged during the `ansible-sync-role` sync (2026-07-03) but not resolved
in that session.

* **No `LICENSE` file exists.** `meta/main.yml` and `README.md` both claim
  MIT, but there is no actual `LICENSE` file in the repo to back that up.
  Add one (Step 5b of the sync skill will stack a Real Time Enterprises
  copyright line onto it once it exists).

* **`.gitlab-ci.yml` is stale relative to this sync** and was intentionally
  left untouched (out of scope for `ansible-sync-role`):
  * `BRANCH_NAME: "ansible-core-2.19"` — the role now targets ansible-core
    >= 2.20.
  * The `molecule` job's matrix still includes `debian11`, which this sync
    just dropped from the supported-platform list (EOL, LTS ends
    2026-08-31). The matrix should be updated to match `molecule.yml`'s new
    platform list (ubuntu jammy/noble/resolute, debian bookworm/trixie,
    el-9).

* **RedHat/EL gets no packages installed by this role** — there's no
  `vars/RedHat.yml`, so `sudoers_packages` falls back to
  `defaults/main.yml`'s empty `[]` for EL hosts. This is pre-existing
  behavior, not something this sync changed, but it's worth confirming
  whether EL hosts are actually expected to have `sudo` pre-installed by
  some other role/base image, or whether this is a real gap.

* **The legacy monolithic sudoers path (`monolithic_sudoers.yml`) has no
  molecule coverage.** All six fixture platforms in the current
  `molecule.yml` (ubuntu jammy/noble/resolute, debian bookworm/trixie,
  el-9) are new enough to hit the modern drop-in path
  (`sudoers.yml`/`ubuntu26.yml`). If the monolithic path still needs to
  work for some out-of-band old host, it isn't exercised by `molecule
  test` today.

* **`management_user` and `group_support_users` are now required inputs**,
  enforced by the new `tasks/preflight.yml` (added this sync). Previously
  these variables only failed with a confusing Jinja "undefined variable"
  error deep inside `sudoers.yml`/`ubuntu26.yml`, and only on hosts that
  actually reached that path (legacy-OS-only hosts never touched them at
  all). Now every consumer must define both, even ones that currently only
  hit the legacy monolithic path. Flagging per the sync's decision to make
  this check unconditional rather than OS-version-conditional.

* **`tasks/veeam12.yml` has a pre-existing uncommitted local change** that
  predates this sync session (removes several `rm -rf /tmp/*`-style
  commands from `VEEAM12_COMMANDS` and loosens `visudo` validation from
  `-csf` to `-cf`). This sync did not touch that file or that change —
  it's still sitting in the working tree and will be included in whatever
  commit follows. Worth a deliberate look before committing, since it's a
  security-relevant sudoers command list.
