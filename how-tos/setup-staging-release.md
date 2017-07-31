# Setting up a specific branch to test staging releases

## Intro
Being releaseduty creates a certain advantage in time as it requires both squirrels to touch lots of the infrastructure and
components that form our release automation pipeline. It's expected that from time to time, whenever we need
to make significant changes to our release automation, staging releases need to be performed before we flip the changes to
production. This is where the releaseduty knowledge comes to rescue!

Historically, we have been using staging releases mostly to test `beta 1` of a new cycle. That is because a `beta` release is our most
common type of release and it is the one we usually start any transformation process with. We used it when we switched to `release
promotion` but also for `tcmigration` projects. This how-to page assumes the same, but a different type of release should behave somewhat
similar. So mainly rather larger changes to the code base, changes that actually impose a staging release beforehand.

## Simulation project branch

Project branch `jamun` has traditionally been our culprit to simulate `beta`. We used `date` for simulating nightlies from `central`.

Use cases:
- for `central` -> `beta` staging release we would use `from_repo_url` = `central`  and `to_repo_url` = `jamun`
- for `date` -> `central` -> `beta` (stuff that lands in `central` and right after that goes in `beta`) staging release we would use `from_repo_url` = `date`  and `to_repo_url` = `jamun`

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
hg -R build/jamun commit -m "Uplift from central to jamun"
hg -R build/jamun out -r . jamun
hg -R build/jamun push
```

## Staging tools

- dev [Ship-it](https://ship-it-dev.allizom.org/)
- staging [release runner](https://dxr.mozilla.org/build-central/rev/5f83e0516fc449586bbce4db4eb759f6cede8781/puppet/manifests/moco-nodes.pp#633)
- release automation notifications [group](https://groups.google.com/a/mozilla.com/forum/?hl=en#!forum/release-automation-notifications-dev) and `#release-notifications-dev` IRC channel
- ~~staging [balrog](https://balrog-admin.stage.mozaws.net/)~~ Spawn your own balrog instance. See dedicated appendix below.
- point that instance in all configs [mozharnss configs](https://dxr.mozilla.org/mozilla-central/source/testing/mozharness/configs/releases/) that need it. Sample [here](https://dxr.mozilla.org/mozilla-central/rev/7d2e89fb92331d7e4296391213c1e63db628e046/testing/mozharness/configs/releases/dev_updates_firefox_beta.py#23)

## Staging configs

- release runner will consume [project branch configs](https://dxr.mozilla.org/build-central/rev/92614acc90330edf360d97d8575b7e917ddc43b2/buildbot-configs/mozilla/project_branches.py#114)
- mozharness [configs](https://dxr.mozilla.org/mozilla-central/source/testing/mozharness/configs/releases/) - all configs with `dev` prefix
- in order to avoid pushing patcher configs changes/tags to *real* [tools](http://hg.mozilla.org/build/tools/) repo, please point to a user fork. You can reuse rail's [tools repo](https://hg.mozilla.org/users/raliiev_mozilla.com/tools-fake/)

A note on creating custom `tools` repo.
Rather than reusing an existing fellow RelEnger `tools` repo, you should clone your own to avoid missing permissions sort-of-issues.
That can be done in the following way (more on this [here](https://wiki.mozilla.org/Release:Release_Automation_on_Mercurial:Staging_Specific_Notes#Setup_staging_repos)):

```sh
ssh hg.mozilla.org clone tools-fake build/tools
# Will show: Please wait.  Cloning /build/tools to /users/jlorenzo_mozilla.com/tools-fake
```

## Misc

- TODO Release runner is smart. It only takes into account the Tier1 stuff.
- Update verify tests are flaky and we need to invest some time to make them work. Our assumption is that we need to better flip variables [here](https://dxr.mozilla.org/mozilla-central/rev/7d2e89fb92331d7e4296391213c1e63db628e046/testing/mozharness/configs/releases/dev_updates_firefox_beta.py)

## Appendix: Start up your own Balrog instance

A note on Balrog. Historically, we've had issues with plugging the staging instance to
the staging release pipeline, so we used another workaround:
- From aws console, create a new ubuntu AWS instance
  - Select the datacenter "us-east-1"
  - Pick the latest Ubuntu provided by AWS
  - Instance Type: Choose m3.medium. You can't choose a t2 because of the network (see next point).
  - Network: Pick "Launch into EC2-Classic". If you run it under a VPC, you won't be able to reach the machine outside of the internal VPN. Moreover, it won't allocate a DNS entry. t2 instances only allow VPC networks.
  - Security group: Choose an existing security group named "balrog-dev". It will open the ports needed for you and release promotion to access Balrog
- login to it and clone Balrog [codebase](https://github.com/mozilla/balrog)
- before starting the balrog process, we need to set `STAGING=1` to make balrog accept `http://ftp.stage.mozaws.net` in the blobs, something like
```diff
diff --git a/docker-compose.yml b/docker-compose.yml
index a0dee5a1..9c712750 100644
--- a/docker-compose.yml
+++ b/docker-compose.yml
@@ -29,17 +29,17 @@ services:
       # Grab mail information from the local environment
       - SMTP_HOST
       - SMTP_PORT
       - SMTP_USERNAME
       - SMTP_PASSWORD
       - SMTP_TLS
       - NOTIFY_TO_ADDR
       - NOTIFY_FROM_ADDR
-      - STAGING
+      - STAGING=1
     healthcheck:
         test: nc -z -v balrogadmin 7070
         interval: 5s
         timeout: 30s
         retries: 10


   balrogpub:
```
- Installer the latest versions of docker and docker-compose. During July 2017, the docker version present in the repo weren't compatible with docker-compose.yml in balrog.
  - [Docker installation](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/). Don't forget the [post installation steps](https://docs.docker.com/engine/installation/linux/linux-postinstall/) which require you to log out and log back in.
  - [Docker-compose installation](https://docs.docker.com/compose/install/).
- follow the [installation](https://github.com/mozilla/balrog#installation) process.
