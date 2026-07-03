Ansible Role: sudoers
======================

[![pipeline status](https://gitlab.real-time.com/ansible-roles/sudoers/badges/ansible-core-2.19/pipeline.svg)](https://gitlab.real-time.com/ansible-roles/sudoers/-/commits/ansible-core-2.19)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> **Fork notice** — This is a fork of
> [arillso/ansible.sudoers](https://github.com/arillso/ansible.sudoers) by
> Arillso. The role originally depended on `arillso.sudoers` as a Galaxy
> dependency; that dependency was later removed and reimplemented
> natively, so almost none of the original task/template code remains —
> but the fork lineage and copyright carry forward (see `LICENSE`).
> Bugs, feature requests, and pull requests for this fork should be
> submitted to
> **[basictheprogram/ansible.sudoers](https://github.com/basictheprogram/ansible.sudoers/issues)**.

Manages sudo access on Debian, Ubuntu, and RedHat/EL systems by dropping
files into `/etc/sudoers.d/`: SSH-agent passthrough, passwordless
(`NOPASSWD`) sudo for a list of management users, sudo command logging,
a restricted `Cmnd_Alias` for the `veeam12` backup service account, and
enforced `0440` permissions across every file in `/etc/sudoers.d/`.
Older OS releases use a legacy monolithic drop-in path instead; Ubuntu
26+ uses a dedicated path for the sudo-rs toolchain.

Requirements
------------

Ansible core >= 2.20. The `community.general` collection (for the
`sudoers` module), declared in `requirements.yml`; install with
`ansible-galaxy collection install -r requirements.yml`.

Supported Platforms
--------------------

| OS Family | Versions                       |
|-----------|---------------------------------|
| Debian    | 12 Bookworm, 13 Trixie          |
| Ubuntu    | 22.04 Jammy, 24.04 Noble, 26.04 Resolute |
| EL        | 9                                |

Role Variables
---------------

Available variables are listed below, along with default values (see
`defaults/main.yml`):

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `sudoers_packages` | `[]` | Packages to install before configuring sudoers. Overridden per OS family — see below. |

Two additional variables have no default and must be set by the
consumer (documented in `meta/argument_specs.yml`, enforced in
`tasks/preflight.yml`):

| Variable | Required | Description |
|----------|----------|-------------|
| `management_user` | yes | List of dicts, each with a `username` key. Every listed user is granted passwordless (`NOPASSWD`) sudo for all commands. |
| `group_support_users` | yes | List of dicts, each with a `username` key. Consulted by the `veeam12` sudoers drop-in, which checks this list for a user named `veeam12`. |

### OS-specific variables (vars/)

The following variables are loaded from `vars/<OsFamily>.yml` via
`include_vars` and are **not** user-overridable in the normal sense —
they reflect package names that differ per distribution.

| Variable | Debian / Ubuntu | RedHat |
|----------|-----------------|--------|
| `sudoers_packages` | `sudo`, `lsb-release` | not set (falls back to `defaults/main.yml`'s `[]`) |

Task Flow
---------

1. **Preflight assertions** — validates Ansible version (>= 2.20),
   that the target distribution is Debian, Ubuntu, or RedHat,
   and that `management_user`/`group_support_users` are defined
   with a `username` on every entry.
2. **Include OS-specific variables** — loads `vars/<OsFamily>.yml`
   for `sudoers_packages`.
3. **Dispatch by distribution** — `debian.yml`, `ubuntu.yml`, or
   `redhat.yml`, each choosing between the legacy monolithic path
   (older releases) and the modern drop-in path based on OS version.
   Ubuntu 26+ uses a dedicated `ubuntu26.yml` path for the sudo-rs
   toolchain.
4. **Modern drop-in path** (`sudoers.yml` / `ubuntu26.yml`) — SSH-agent
   passthrough, `NOPASSWD` sudo for `management_user`, sudo command
   logging (not on Ubuntu 26+, which instead removes any pre-existing
   logfile drop-in), the `veeam12` restricted command alias, and a
   final pass enforcing `0440` on every file under `/etc/sudoers.d/`.
5. **Legacy monolithic path** (`monolithic_sudoers.yml`) — SSH-agent
   passthrough, disables `requiretty`, and grants the `ansible` user
   NOPASSWD sudo. Does not configure `veeam12`.

Dependencies
------------

None.

Example Playbook
-----------------

```yaml
- hosts: servers
  roles:
    - role: realtime.sudoers
      management_user:
        - username: alice
        - username: bob
      group_support_users:
        - username: veeam12
```

License
-------

MIT

Author Information
--------------------

Originally created by Arillso ([arillso/ansible.sudoers](https://github.com/arillso/ansible.sudoers)).

This fork is maintained by Bob Tanner, Real Time Enterprises, Inc., at
[basictheprogram/ansible.sudoers](https://github.com/basictheprogram/ansible.sudoers).
Please open issues and pull requests there.
