# How to set up a new ESR branch

## Intro

This manual describes how to set up a new ESR branch. The same process can be
applied for any branch set up, with slight modifications.

Example tracking bug: [Bug 1334535 - tracking bug for build and release of
Firefox 52.0esr](https://bugzilla.mozilla.org/show_bug.cgi?id=1334535)

## Internal changes

This section covers changes to buildbot-configs and tools.

See [Bug 1339832](https://bugzilla.mozilla.org/show_bug.cgi?id=1339832)  for
the details and example changes.

Some highlights:

* Explicitly list the platforms (and use lock_platforms) since we don't ship
  ESR to all mozilla-central/release platforms (android, for example)
* Copy mozilla-beta configs, compare them to the previous ESR release and check
  if you understand what they stand for

### tools changes

* copy the old patcher config, so we can generate partial updates against the
  previous ESR release.
* since the config patch introduces new configuration file(s) which are needed
  to be symlinked on the build/scheduler masters there is a need for a fabric
  methods to create the links

It's important that the buildbot-configs changes are landed and in production
prior to adding the symlinks and adjusting production-masters.json. When you
land these two changes you must immediately run the fabric method to put the
symlinks in place to ensure the masters will continue to function correctly.

## External systems

CI relies on multiple systems, supported by different teams. File bugs in
advance to make sure other teams have enough time to address the issue.
Usually starting the whole process 2 weeks in advance of release builds (3
weeks before the release), gives enough time to everybody.

## Tasks

Below is the list of bugs filed as a part of the ESR52 cycle. Go through the
list and verify that they are still valid for this ESR cycle and clone them if
needed.

Bug | Title
----|------
[1333745](https://bugzilla.mozilla.org/show_bug.cgi?id=1333745) | Please add tracking-thunderbird_esr52 and status-thunderbird_esr52 to the tracking flags
[1335870](https://bugzilla.mozilla.org/show_bug.cgi?id=1335870) | please create tracking-firefox-esr52 and status-firefox-esr52 flags
[1337061](https://bugzilla.mozilla.org/show_bug.cgi?id=1337061) | Add mozilla-esr52 and comm-esr52 to release_repositories
[1337066](https://bugzilla.mozilla.org/show_bug.cgi?id=1337066) | Please clone releases/mozilla-beta to releases/mozilla-esr52
[1337087](https://bugzilla.mozilla.org/show_bug.cgi?id=1337087) | update tree closure hooks for mozilla-esr52
[1337090](https://bugzilla.mozilla.org/show_bug.cgi?id=1337090) | Add mozilla-esr52 and comm-esr52 to treeherder
[1337091](https://bugzilla.mozilla.org/show_bug.cgi?id=1337091) | Add mozilla-esr52 and comm-esr52 to treestatus
[1337093](https://bugzilla.mozilla.org/show_bug.cgi?id=1337093) | Add mozilla-esr52 and comm-esr52 to orange factor
[1337366](https://bugzilla.mozilla.org/show_bug.cgi?id=1337366) | Gecko-specific changes to support mozilla-esr52
[1337489](https://bugzilla.mozilla.org/show_bug.cgi?id=1337489) | HTTP 500 for all trees view due to missing comm-esr52 repo
[1339057](https://bugzilla.mozilla.org/show_bug.cgi?id=1339057) | Please add the approval-esr52 flag
[1339074](https://bugzilla.mozilla.org/show_bug.cgi?id=1339074) | Add mozilla-esr52 to the various lists in repository.py
[1339076](https://bugzilla.mozilla.org/show_bug.cgi?id=1339076) | Make sure the right hooks are running on mozilla-esr52
[1339832](https://bugzilla.mozilla.org/show_bug.cgi?id=1339832) | Buildbot specific changes to enable mozilla-esr52
[1340669](https://bugzilla.mozilla.org/show_bug.cgi?id=1340669) | Update merge day and esr docs
[1341330](https://bugzilla.mozilla.org/show_bug.cgi?id=1341330) | Please add mozilla-esr52 to DXR
[1341491](https://bugzilla.mozilla.org/show_bug.cgi?id=1341491) | Set ESR_NEXT in ship-it config
[1342117](https://bugzilla.mozilla.org/show_bug.cgi?id=1342117) | Set watch_all_branches to True for ESR52
[1342204](https://bugzilla.mozilla.org/show_bug.cgi?id=1342204) | Enable TC on mozilla-esr52
[1342431](https://bugzilla.mozilla.org/show_bug.cgi?id=1342431) | Turn off TC-based Android jobs on ESR52
[1343097](https://bugzilla.mozilla.org/show_bug.cgi?id=1343097) | Add mozilla-esr52 and comm-esr52 to release-notifications heroku app
[1343366](https://bugzilla.mozilla.org/show_bug.cgi?id=1343366) | browser_parsable_css.js fails on ESR52 ASAN builds due to the ESR branding changes

## Merge

Once mozilla-release is merged from mozilla-beta you can run the script which
pulls last changes from mozilla-release, updates some configs and replaces some
branding bits.

### Running gecko_migration.py for mozilla-esr

The script will tag mozilla-release. It will continue by pulling
mozilla-release to mozilla-esrNN, adjusting branding and changing some configs.
Once the script finishes, run an hg diff to see the uncommitted changes that
the script generated:

    ESR_VERSION=51
    # checkout mozharness from the gecko tree using archiver
    wget https://hg.mozilla.org/build/tools/raw-file/default/buildfarm/utils/archiver_client.py
    python archiver_client.py mozharness --destination mozharness-esr$ESR_VERSION \
      --repo releases/mozilla-esr$ESR_VERSION --rev default --debug
    # run the script
    python mozharness-esr$ESR_VERSION/scripts/merge_day/gecko_migration.py \
      -c merge_day/release_to_esr.py
    hg -R build/mozilla-esr$ESR_VERSION diff
    python mozharness-esr$ESR_VERSION/scripts/merge_day/gecko_migration.py -c \
      merge_day/release_to_esr.py --commit-changes --push

The push should be available at Treeherder.

In case of failure, you can start again from the top; no need to clobber (the
on-by-default clean-repos action will be sufficient). It should be faster the
second time, since you won't be pulling in as many changesets from hg.m.o.

## Release builds

Make sure to run a staging release.

## Update this documentation

Keep this documentation up to date.

## Ship it!

Close the bug and have some tea. :)
