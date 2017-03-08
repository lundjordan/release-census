This document is the new version of https://wiki.mozilla.org/ReleaseEngineering/Merge_Duty/Steps. It's heavily inspired by https://gist.github.com/lundjordan/b66bff783b6853e024f6.

# MergeDuty Tasks

**Consists of roughly 4 individual days of work. Each day you must action several sequential tasks. The 4 days are spread out over about 18 days**

## Terminology

* Merge Prep Day: day we prepare for the upcoming 'Release Merge Day' and 'Stabilizing Branch Merge Day'
  * when: day 1 - usually a monday and 1 week before 'Release Merge Day'
* Release Merge Day: day we merge csets from 'm-b -> m-r'
  * when: day 7 usually a mon and 1 week before 'Stabilizing Branch Merge Day'
* Stabilizing Branches Merge Day: day we merge csets from 'm-a -> m-b' and 'm-c -> m-a'
  * when: day 14 usually a mon and 1 day before 'Release Day'
* Release Day: official day of release
  * when: day 15 usually a Tues
* Unthrottle Day: day we unthrottle m-a (usually)
  * when: day 18 usually Fri

## Pre-requirements

1. Edit `~/.hgrc` to include:
```ini
[extensions]
transplant=
mq=
rebase=
graphlog=
```
1. Have your computer wired to a stable Internet connection (several gecko clones and huge pushes are planned).
1. File a merge day bug, if it's not done already. [Example](https://bugzilla.mozilla.org/show_bug.cgi?id=1123369).

## Day 1 - Prep day #1

1. On the merge day bug, create 2 patches to bump [gecko_versions.json](https://dxr.mozilla.org/mozilla-central/source/mozilla/gecko_versions.json). Get them reviewed but **don't land them yet**
  1. patch 1: bump **only mozilla-release**. It will serve Firefox's release candidate. [Example](https://bug1123369.bugzilla.mozilla.org/attachment.cgi?id=8580307).
  1. patch 2: bump the remaining branches. This includes m-b, m-a, m-c and comm branches. [Example](https://bug1123369.bugzilla.mozilla.org/attachment.cgi?id=8580308).

1. do a no-op trial run of performing the mozilla-beta -> mozilla-release migration:
```sh
mkdir merge_day
cd merge_day
wget https://hg.mozilla.org/build/tools/raw-file/default/buildfarm/utils/archiver_client.py
python archiver_client.py mozharness --destination mozharness-central --repo mozilla-central --rev default --debug  # Central must be used against every branch
python mozharness-central/scripts/merge_day/gecko_migration.py -c merge_day/beta_to_release.py
```
1. The script should have created a diff:
```sh
hg -R build/mozilla-release diff
```

## Day 7 - Release Merge Day

### Reconfigs part 1

1. Look at the merge day bug and see if patches need to land at this stage.
1. Land "patch 1"
1. Wait 1 hour for the reconfig to happen (via cron job). If you can't wait, ask for a manual reconfig to buildduty folks.
1. Wait for the go-to-merge email in release-drivers

### Merge beta to release

1. [Close mozilla-beta](https://mozilla-releng.net/treestatus/show/mozilla-beta). Check "Remember this change to undo later".
1. Run the [no-op trial run](#day-1-merge-prep-day) one more time, and show the diff to your co-releaseduty.
1. Push your changes:
```sh
python mozharness-central/scripts/merge_day/gecko_migration.py \
  -c selfserve/production.py -c merge_day/beta_to_release.py \
  --create-virtualenv --commit-changes --push
```
:warning: If an issue comes up during this phase, you may not be able to ran this command (or the no-op one) correctly. You may need to publicly backout some tags/changesets to get back in a known state.
1. Verify changesets are visible on [hg pushlog](https://hg.mozilla.org/releases/mozilla-release/pushloghtml) and [Treeherder]( https://treeherder.mozilla.org/#/jobs?repo=mozilla-release). It may take a couple of minutes to appear.

### Bump ESR version

Note: you may have 1 or 2 ESRs to bump.

1. Steps are similar to a merge:
```sh
# go to merge_day directory, created on day 1
ESR_VERSION=45
python mozharness-central/scripts/merge_day/gecko_migration.py -c mozharness-esr$ESR_VERSION/configs/merge_day/bump_esr.py
hg -R build/mozilla-esr$ESR_VERSION diff
python mozharness-central/scripts/merge_day/gecko_migration.py -c mozharness-esr$ESR_VERSION/configs/merge_day/bump_esr.py \
  --commit-changes --push
```
1. Verify new changesets popped on https://hg.mozilla.org/releases/mozilla-esr`$ESR_VERSION`/pushloghtml

### Uplift locales

1. Get a copy of the key called `ffxbld_rsa` on a buildbot master (ctlbld).
1. There are several tens of repos to upgrade. Using an external machine saves time.
```sh
ssh cruncher-aws.srv.releng.usw2.mozilla.com
screen
mkdir l10n && cd l10n
wget https://hg.mozilla.org/build/braindump/raw-file/default/releases-related/beta2release_l10n.sh
chmod 755 beta2release_l10n.sh
# copy ffxbld_rsa in the current folder
chmod 600 ffxbld_rsa
./beta2release_l10n.sh # Can be rerun. Cloned locales are skipped. If a locale failed pushing, delete the repo.
```

### It's done!

1. Reply to the migration request with the template:

> This is now complete:
    * mozilla-beta is merged to mozilla-release, new version is XX.Y
    * l10n mozilla-beta repos are merged to mozilla-release
    * esr is now XX.Y.Z
    * beta will stay closed until next Monday

## Day 11 - Prep day #2
1. Similar to prep day #1 (you may need to redownload `mozharness-central`):
```sh
# go to merge_day directory, created on day 1
python mozharness-central/scripts/merge_day/gecko_migration.py -c merge_day/aurora_to_beta.py
python mozharness-central/scripts/merge_day/gecko_migration.py -c merge_day/central_to_aurora.py
```

## Day 14 - Stabilizing Branches Merge Day

### Reconfigs part 2

1. Do the same things as part 1, except you should land "patch 2" instead.

### Merge aurora to beta

It's almost identical to beta to release:

1. [Close mozilla-aurora](https://mozilla-releng.net/treestatus/show/mozilla-aurora). Check "Remember this change to undo later".
1. 
```sh
# go to merge_day directory, created on day 1
python mozharness-central/scripts/merge_day/gecko_migration.py -c merge_day/aurora_to_beta.py
hg -R build/mozilla-beta diff # Validate it with someone else
python mozharness-aurora/scripts/merge_day/gecko_migration.py \
  -c selfserve/production.py -c merge_day/aurora_to_beta.py \
  --create-virtualenv --commit-changes --push --trigger-builders
```
1. Verify changesets are visible on [hg pushlog](https://hg.mozilla.org/releases/mozilla-beta/pushloghtml) and [Treeherder]( https://treeherder.mozilla.org/#/jobs?repo=mozilla-beta). It may take a couple of minutes to appear.
1. Tell sheriffs this particular migration is done

### Merge central to aurora

1. No need to close central.
1. 
```sh
python mozharness-central/scripts/merge_day/gecko_migration.py -c merge_day/central_to_aurora.py
hg -R build/mozilla-aurora diff # Validate it with someone else
scp cltbld@buildbot-master81.bb.releng.scl3.mozilla.com:/builds/buildbot/build_scheduler/master/BuildSlaves.py oauth.txt
python mozharness-central/scripts/merge_day/gecko_migration.py \
  -c balrog/production.py -c selfserve/production.py \
  -c merge_day/central_to_aurora.py \
  --create-virtualenv --commit-changes \
  --push --trigger-builders
```
1. Verify changesets are visible on [hg pushlog](https://hg.mozilla.org/releases/mozilla-aurora/pushloghtml) and [Treeherder]( https://treeherder.mozilla.org/#/jobs?repo=mozilla-aurora). It may take a couple of minutes to appear.
