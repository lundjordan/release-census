# Setting up a specific branch to test staging releases

## Intro
Being releaseduty creates a certain advantage in time as it requires both squirrels to touch lots of the infrastructure and
components that form our release automation pipeline. It's expected that from time to time, whenever we need
to make significant changes to our release automation, staging releases need to be performed before we flip the changes to
production. This is where the releaseduty knowledge comes to rescue!

Historically, we have been using staging releases mostly to test beta1 of a new cycle. That is because a beta release is our most
common type of release and it is the one we usually start any transformation process with. We used it when we switched to `release
promotion` but also for `tcmigration` projects. This how-to page assumes the same but a different type of release should behave somewhat
similar. So mainly rather larger changes to the code base, changes that actually impose a staging release beforehand.

## Simulation project branch

Project branch `jamun` has traditionally been our culprit to simulate `beta`. We used `date` for simulating nightlies from `central`.

Use cases:
- for `central` -> `beta` staging release we would use `from_repo_url` = `central`  and `to_repo_url` = jamun
- for `date` -> `central -> `beta` (stuff that lands in `central` and right after that goes in `beta`) staging release we would use `from_repo_url` = `date`  and `to_repo_url` = jamun

## Merge scripts

1.
```sh
mkdir staging_release_merge
cd staging_release_merge
wget https://hg.mozilla.org/build/tools/raw-file/default/buildfarm/utils/archiver_client.py
python archiver_client.py mozharness --destination mozharness-central --repo mozilla-central --rev default --debug  # Central must be used against every branch
```

2. Modify the `mozharness-central/configs/merge_day/central_to_beta.py` file to look like this
```diff
--- mozharness-central.orig/configs/merge_day/central_to_beta.py2017-07-10 06:26:15.000000000 -0400
+++ mozharness-central/configs/merge_day/central_to_beta.py20172017-07-10 09:53:01.838515927 -0400
@@ -67,8 +67,8 @@
     # "hg_share_base": None,
     "tools_repo_url": "https://hg.mozilla.org/build/tools",
     "tools_repo_branch": "default",
-    "from_repo_url": "ssh://hg.mozilla.org/mozilla-central",
-    "to_repo_url": "ssh://hg.mozilla.org/releases/mozilla-beta",
+    "from_repo_url": "ssh://hg.mozilla.org/projects/date",
+    "to_repo_url": "ssh://hg.mozilla.org/projects/jamun",

     "base_tag": "FIREFOX_BETA_%(major_version)s_BASE",
     "end_tag": "FIREFOX_BETA_%(major_version)s_END",
```

3. Run the actual script to get the "diff" between the two branches:
```sh
python mozharness-central/scripts/merge_day/gecko_migration.py -c merge_day/central_to_beta.py
```

4. The script should have created a diff. Check that everything is okay and push to jamun
```sh
hg -R build/jamun diff
hg out -r . jamun
hg push
```

## Staging tools

- [staging Ship-it](https://ship-it-dev.allizom.org/)
- [release runner dev](https://hg.mozilla.org/build/puppet/file/default/manifests/moco-nodes.pp#l633)
- release automation notificats [group](https://groups.google.com/a/mozilla.com/forum/?hl=en#!forum/release-automation-notifications-dev) and #release-notifications-dev IRC channel
- [balrog staging](https://balrog-admin.stage.mozaws.net/)

A note on Balrog staging. Historically, we've had issues with plugging the staging instance to
the staging releases, so we used another workaround:
- from aws console, create a new ubuntu AWS instance
- login to it and clone Balrog [codebase](https://github.com/mozilla/balrog)
- follow the [installation](https://github.com/mozilla/balrog#installation) process
- point that instance in all configs [mozharnss configs](https://dxr.mozilla.org/mozilla-central/source/testing/mozharness/configs/releases/) that need it. Sample [here](https://dxr.mozilla.org/mozilla-central/source/testing/mozharness/configs/releases/dev_updates_firefox_beta.py#23)

## Staging configs

- release runner will consume [project branch configs](https://dxr.mozilla.org/build-central/source/buildbot-configs/mozilla/project_branches.py#114)
- mozharness [configs](https://dxr.mozilla.org/mozilla-central/source/testing/mozharness/configs/releases/) - all configs with `dev` prefix
- in order to avoid pushing patcher configs changes/tags to *real* [tools](http://hg.mozilla.org/build/tools/) repo, please point to a user fork. You can reuse rail's [tools repo](https://hg.mozilla.org/users/raliiev_mozilla.com/tools)

## Misc

TODO - Release runner is smart. It only takes into account the Tier1 stuff.
