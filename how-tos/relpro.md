# Pre-requirements

## understanding release promotion
* this task is optional and refers to understanding how release promotion works
* the original release workflow diagram before Buildbot -> Taskcluster migration, as to November 2015, can be found [here](https://www.lucidchart.com/documents/view/b733c8be-e607-445f-824a-f3353c287294)
* the up-to-date version of it, as to September 2016, is itteratively divided in two. First graph depicts the logic pieces and all tasks in Taskcluster, but lacks the dependencies between the tasks within the graph, and can be found [here](https://www.lucidchart.com/documents/view/1b59f91d-1dfa-4d1e-8a50-d2d2759a3fff)
* the follow-up version of it, with all the tasks and graph dependencies can be found [here](https://www.lucidchart.com/documents/view/29588c49-c18c-4800-be84-cca359d89ffc)
  * A "higher level" diagram of the release process is also available in the [Releng docs](http://moz-releng-docs.readthedocs.io/en/latest/release_workflows/index.html).

## taskcluster related
* **You need 2 bookmarklets in your browser to enhance the work with taskcluster**
  * Create a new bookmark, name it `Stop`, add `javascript:stop();` to Location
  * click and drag the [sort table](https://www.squarefree.com/bookmarklets/pagedata.html#sort_table) link to your Bookmarks Toolbar. [Rail](https://github.com/rail) found a fancier sort table [here](https://gist.githubusercontent.com/rail/11314a9e04cdabb33ccabc5419ef90d0/raw/21e095893a743df2a4a735cbcc751e165f2f6d98/table%2520sorter)
* Find the email with subject: "[desktop] Build of Firefox-46.0b4-build2" - it contains a link to the task graph
* After the task graph is loaded click on the "stop" bookmarklet
* Click the "sort table" bookmarklet - you'll get "a/d" table headers
* Sort the table by "State" ascending, so you get unscheduled and  scheduled tasks first

## tctalker setup

(Note: you can also use the new [taskcluster cli](https://github.com/taskcluster/taskcluster-cli) for many/most/all of the tctalker requirements.)

* **You need tctalker to play nicely with taskcluster jobs**
* navigate to [Taskcluster tools](https://tools.taskcluster.net) and make sure you're logged-in
* make sure the following scopes are listed under your [Taskcluster credentials](https://tools.taskcluster.net/credentials/):
```
auth:create-client:mozilla-ldap/<ldap_username>/*
auth:create-client:project/releng/*
```
* navigate to [Taskcluster clients](https://tools.taskcluster.net/auth/clients/) and create a new clientId - dedicated for playing with tctalker.
* it should already be pre-formatted to `mozilla-ldap/<ldap_username>/` at which you can concatenate any string. You can simply add *tctalker*.
* use *queue:** for **Client Scopes**
* hit the **Create Client** button and make sure you save the *Access token* that is generated
* create a json config file (e.g. "config.json") on disk that looks like this:

```
{
    "credentials": {
        "clientId": "you-will-never-guess",
        "accessToken": "nor here!"
    }
}
```

* clone yourself a copy of [tctalker](https://github.com/mozilla/tctalker) and change directory to the clone repo
* run the following:
```
python src/tctalker/tctalker.py --conf config.json <action> <task-id>
```
# Actions for Desktop related releases

## 1. email release-signoff re: release live on test channel

### why
* cdntest and localtest channels serve releases from the releases dir (mirrors/cdn) or candidates dir depending on the release and channel. They are testing channels used before we serve from the _real_ update channel
* we should notify release-signoff once updates are available on the ${branch}-{cdntest,localtest} channel because we don't have taskcluster email notifications yet

### when
* Desktop Firefox Betas
    * look in taskgraph for task with name `mozilla-beta beta final verification`
        * once this task has run successfully, that means we have 1) pushed to releases dir 2) and verified beta-cdntest is serving the release from there
* Desktop Firefox Release-Candidates
    * context: RCs are m-r releases that are served to beta uses prior to release channel users. RCs use `beta-cdntest` and `release-cdntest` for QA.
    * `beta-cdntest` serves updates from the candidates/ dir. We should notify release-signoff once all artifacts are available there. we don't worry about `release-cdntest` because that is not automatic in automation
        * look in taskgraph graph 1 for task with name `mozilla-release beta final verification`
        * once this task has run successfully, that means 1) the release has finished uploading all artifacts to candidates dir 2) and verified beta-cdntest is serving the release from there
* Desktop Firefox Releases (dot releases)
    * `release-localtest` serves updates from the candidates/ dir. We should notify release-signoff once all artifacts are available there. Again, release-cdntest depends on a human decision (not automatic) in automation so no email required.
        * look in taskgraph graph for task with name `firefox mozilla-release push to releases human decision task`.
        * this task should be the only task left that is blocking the graph (aside from the post release human task)
        * all other en-us, l10n, partial, and partner artifact generating tasks should be finished. However, in emergency situations, the partner artifacts should not block sending out the email should the `firefox mozilla-release checksums builder` ran succcessfully.
* Desktop Firefox ESRs
    * `esr-localtest` serves updates from the candidates/ dir. We should notify release-signoff once all artifacts are available there. Again, esr-cdntest depends on a human decision (not automatic) in automation so no email required.
        * look in taskgraph graph for task with name `firefox mozilla-esr push to releases human decision task`.
        * this task should be the only task left that is blocking the graph (aside from the post release human task)
        * all other en-us, l10n, partial, and partner artifact generating tasks should be finished.

### how
* Desktop Firefox Betas
    * email release-signoff@mozilla.org with subject only email `[desktop] Firefox Beta $version updates are available on the beta-cdntest channel now <EOM>`
* Desktop Firefox Release-Candidates
    * email release-signoff@mozilla.org with subject only email `[desktop] Firefox RC Release $version updates are available on the beta-cdntest channel now <EOM>`
* Desktop Firefox Releases (dot releases)
    * email release-signoff@mozilla.org with subject only email `[desktop] Firefox Release $version updates are available on the release-localtest channel now <EOM>`
* Desktop Firefox ESRs
    * email release-signoff@mozilla.org with subject only email `[desktop] Firefox ESR $version updates are available on the esr-localtest channel now <EOM>`


## 2. push to releases dir (mirrors)

### why
* some releases don't automatically push releases to the releases dir automatically. They instead wait on a human decision (sign off) to dictate when candidates dir looks good and we are ready to copy/push to releases dir

### when
* Desktop Firefox Release-Candidate Releases
    * release-cdntest channel serves updates from releases dir so it depends on this step unlike RC beta-cdntest channel
    * wait for sign off from release-signoff with email like: `[desktop] Please push ${version} to ${channel}` where version is like `46.0 build 3` and channel is like `release-cdntest` or `cdntest` or `mirrors` or `releases`
        * note: if they do not explicitly ask for `release-cdntest` it is okay to assume if you are confident but please reply with something like `pushed and please use explicit name when requesting next time: release-cdntest channel :)`
* Desktop Firefox Releases (dot releases)
    * wait for sign off from release-signoff with email like: `[desktop] Please push ${version} to {cdntest,releases,mirrors}` where version is like: `46.0.1 build 5`, and channel is like: `release-cdntest` or `cdntest` or `mirrors` or `releases`
        * note: if they do not explicitly ask for `release-cdntest` it is okay to assume if you are confident but please reply with something like `pushed and please use explicit name when requesting next time: release-cdntest channel :)`
* Desktop Firefox ESRs
    * wait for sign off from release-signoff with email like: `[desktop] Please push ${version} to {cdntest,releases,mirrors}` where version is like: `38.0esr` or `38.2.0esr`, and channel is like: `esr-cdntest` or `cdntest` or `mirrors` or `releases`
        * note: if they do not explicitly ask for `release-cdntest` it is okay to assume if you are confident but please reply with something like `pushed and please use explicit name when requesting next time: esr-cdntest channel :)`

### how
* Desktop Firefox Release-Candidate Releases
    * RC releases depend on two taskcluster graphs. pushing to releases happens in graph 2 and will start once graph 2 is submitted.
    * to generate and submit graph 2 of the release:
        * step 1) get a taskid from a any task in graph 1. this is used by graph 2 for obtaining release version, branch, etc.
        * step 2) call releasetasks_graph_gen.py and pass, among other things, the taskid obtained in step 1:
```bash
$ ssh `whoami`@buildbot-master85.bb.releng.scl3.mozilla.com  # host we release-runner and you generate/submit new release promotion graphs
$ sudo su - cltbld
$ TASK_TASKID_FROM_GRAPH1={insert a taskid from any task in graph 1}
$ cd /home/cltbld/releasetasks/
$ git pull origin master  # make sure we are up to date. note: make sure this is on master and clean first
$ cd /builds/releaserunner/tools/buildfarm/release/
$ hg pull -u # make sure we are up to date. note: make sure this is on default and clean first
$ source /builds/releaserunner/bin/activate
# call releasetasks_graph_gen.py with --dry-run and sanity check the graph output that would be submitted
$ python releasetasks_graph_gen.py --release-runner-config=../../../release-runner.yml --branch-and-product-config=/home/cltbld/releasetasks/releasetasks/release_configs/prod_mozilla-release_firefox_rc_graph_2.yml --common-task-id=$TASK_TASKID_FROM_GRAPH1 --dry-run
# call releasetasks_graph_gen.py for reals which will submit the graph to Taskcluster
$ python releasetasks_graph_gen.py --release-runner-config=../../../release-runner.yml --branch-and-product-config=/home/cltbld/releasetasks/releasetasks/release_configs/prod_mozilla-release_firefox_rc_graph_2.yml --common-task-id=$TASK_TASKID_FROM_GRAPH1
```

* Desktop Firefox Releases (dot releases)
    * wait for sign off from release-signoff with email like: `[desktop] Please push ${version} to {cdntest,releases,mirrors}` where version is like: `46.0.1 build 5`, and channel is like: `release-cdntest` or `cdntest` or `mirrors` or `releases`
        * note: if they do not explicitly ask for `release-cdntest` it is okay to assume if you are confident but please reply with something like `pushed and please use explicit name when requesting next time: release-cdntest channel :)`
    * get taskid from task with name `firefox mozilla-release push to releases human decision task` in task graph
    * This task is blocking `[beetmover] firefox mozilla-release push to releases`
    * To resolve the human decision task run the following:
```bash
 tctalker --conf ~/.taskcluster/relpro.json report_completed $TASK_ID
```

* Desktop Firefox ESRs
    * wait for sign off from release-signoff with email like: `[desktop] Please push ${version} to {cdntest,releases,mirrors}` where version is like: `38.0esr` or `38.2.0esr`, and channel is like: `esr-cdntest` or `cdntest` or `mirrors` or `releases`
        * note: if they do not explicitly ask for `esr-cdntest` it is okay to assume if you are confident but please reply with something like `pushed and please use explicit name when requesting next time: esr-cdntest channel :)`
* ESR releases depend on two taskcluster graphs. pushing to releases happens in graph 2 and will start once graph 2 is submitted.
    * to generate and submit graph 2 of the release:
        * step 1) get a taskid from a any task in graph 1. this is used by graph 2 for obtaining release version, branch, etc.
        * step 2) call releasetasks_graph_gen.py and pass, among other things, the taskid obtained in step 1:
```bash
$ ssh `whoami`@buildbot-master85.bb.releng.scl3.mozilla.com  # host we release-runner and you generate/submit new release promotion graphs
$ sudo su - cltbld
$ TASK_TASKID_FROM_GRAPH1={insert a taskid from any task in graph 1}
$ cd /home/cltbld/releasetasks/
$ git pull origin master  # make sure we are up to date. note: make sure this is on master and clean first
$ cd /builds/releaserunner/tools/buildfarm/release/
$ hg pull -u # make sure we are up to date. note: make sure this is on default and clean first
$ source /builds/releaserunner/bin/activate
# call releasetasks_graph_gen.py with --dry-run and sanity check the graph output that would be submitted
$ python releasetasks_graph_gen.py --release-runner-config=../../../release-runner.yml --branch-and-product-config=/home/cltbld/releasetasks/releasetasks/release_configs/prod_mozilla-esr52_firefox_rc_graph_2.yml --common-task-id=$TASK_TASKID_FROM_GRAPH1 --dry-run
# call releasetasks_graph_gen.py for reals which will submit the graph to Taskcluster
$ python releasetasks_graph_gen.py --release-runner-config=../../../release-runner.yml --branch-and-product-config=/home/cltbld/releasetasks/releasetasks/release_configs/prod_mozilla-esr52_firefox_rc_graph_2.yml --common-task-id=$TASK_TASKID_FROM_GRAPH1
```

## 3. signoffs

### why
* to guard against bad actors and compromised credentials we require that any changes to primary release channels (aurora, beta, release, esr) in balrog are signed off on by at least two people.

### when

* after the scheduled change has been created by the "updates" task, and prior to the desired publish time

### how

* through the Balrog Scheduled Changes UI (https://aus4-admin.mozilla.org/rules/scheduled_changes)

* RelEng
    * RelEng is responsible for reviewing the scheduled change to ensure that the mechanics are correct. Most notably, the mapping, fallbackMapping, and backgroundRate need to be verified.

* QE
    * QE is responsible for verifying updates on the cdntest channel. There were recent changes implemented to remove the Balrog signoff requirement for QE for all Firefox channels.  The change to remove this from ESR channels is still pending but should be implemented as soon as someone from QE signs off on this change request.

* RelMan
    * RelMan is responsible for reviewing the scheduled change to ensure that the shipping time is correct and to authorize that the release may be shipped. If circumstances change (eg, we discover a bug we're not willing to ship) after they sign off, they must revoke their signoff in Balrog.

### example

After the Scheduled Change has been created, the Balrog UI will look something like:
![scheduled change without signoffs](/how-tos/only_scheduled.png?raw=true)

When RelEng reviews it they will look at the Mapping, Fallback Mapping, and Backgound Rate (circled above). If everything looks good to them, they will click on the "Signoff as..." button and be presented with a dialog like:
![signoff modal dialog](/how-tos/signoff_dialog.png?raw=true)

After they make their Signoff, the primary UI will reflect that:
![scheduled change with one signoff](/how-tos/one_signoff.png?raw=true)

RelMan and QE will go through a similar process. Once they make their Signoffs the primary UI will reflect that as well:
![scheduled change with two signoffs](/how-tos/all_signoffs.png?raw=true)

Now that the Signoff requirements have been met, the Scheduled Change will be enacted at the prescribed time.


## 4. publish release

### why
* updates are automatically published by Balrog when the scheduled change created by
  release promotion hits its scheduled time and all required signoffs have been
  completed.

    * It is expected that RelEng and RelMan will sign off on the scheduled changes ahead
      of the ship date.
    * If the ship time, throttle rate, or anything else about the release changes between
      the change being scheduled and the expected ship time, the scheduled change should
      be updated (or deleted) to reflect the change. After doing so, Signoff will be
      required again.

* the publish release human decision task should be triggered after the release
  has been published in Balrog. It triggers the update bouncer aliases, mark as shipped,
  and bump version tasks.

### when
* All Desktop Firefox releases
    * Wait for email on the balrog-db-changes list that shows the mapping on the live channel
      being changed to the Release being shipped.

### how
* Desktop Firefox Betas, Desktop Firefox Release-Candidate (beta release prior to release release) and Desktop Firefox dot Releases
    * go to the task graph (there is only one) and find taskId of `publish release human decision task`
    * Resolve the "publish release human decision" task using the command below
    * Announce to release-signoff that the release is live
* Desktop Firefox Release and Release-Candidate (RC releases push to release channel)
    * go to the task graph #2 and find taskId of `publish release human decision task`
    * Resolve the "publish release human decision" task using the command below
    * Announce to release-signoff that the release is live
    * Schedule an update to change the background rate of the rule to 0% the next day.
        * Go to Balrog and "Schedule an Update" for the "firefox-release" rule that changes
          "backgroundRate" to 0 at 9am Pacific the following day. All other fields should remain the same.
* Desktop Firefox ESRs
    * depending on timing you may have 1 or 2 graphs. Go to the latest one and
      find taskId of `publish release human decision task`
    * Resolve the "publish release human decision" task using the command below
    * Announce to release-signoff that the release is live
```bash
 tctalker --conf ~/.taskcluster/relpro.json report_completed $TASK_ID
```

## 5. post release step

### why
* releases are needed to be marked as "shipped" in Ship-it to make the partial
  guessing algorithm work and make sure the product-details site has correct information
  about releases.

### when
* immediately after running `publish release` human decision step

### how
* Desktop Firefox Betas, Desktop Firefox Release, Desktop Firefox dot Releases, Desktop Firefox ESRs and Fennec Beta/Releases
    * it is done automatically so just sanity check that the `<product> <channel> mark release as shipped` has completed successfully in the graph
* Other *not* release-promotion based releases (Thunderbird) are needed to be marked as shipped on Ship It. To do so, visit
  https://ship-it.mozilla.org/releases.html, find the release in question, and
  click the "Shipped!" button.


# Actions for Mobile related releases

## 1. email release-signoff re: Fennec builds are available in the candidates directory

### why
* We don't serve updates to Fennec via Balrog; however, we upload the updates to candidates dir from where they are being used by QE for testing before we upload them to the Google Play Store
* we should notify release-signoff once updates are available in candidates directory because we don't have taskcluster email notifications yet

### when
* Mobile Firefox Betas, Releases and dot releases
    * look in taskgraph for tasks that are not yet green, `android-push-apk-breakpoint/opt`(pending) and `push-apk/opt`(unscheduled)
        * once these two tasks are the only leftovers which are not green yet, it means all builds are now uploaded to the candidates dir and you can send the email

### how
* Mobile Firefox Betas, Releases and dot releases
    * email release-signoff@mozilla.org with subject only email `[mobile] Fennec $version $build_no builds are available in the candidates directory <EOM>`

## 2. push to Google Play Store

### why
* pushing the APK to the Play store happens automatically but the task that's doing that is guarded by a human breakpoint, because we need to wait for QE signoff beforehand

### when
* Mobile Firefox Betas, Releases and dot releases
    * wait for sign off from release-signoff with email like: `[mobile] Please push ${version} to the GP`. For betas 2-N we usually send this email right after QE sends the signoff, without an explicit call from RelMan

### how
* Mobile Firefox Betas and dot releases
    * Resolve the aforementioned human task `android-push-apk-breakpoint/opt` from the Chain Of Trust graph (graphid2). Doing so should quickly enable the scheduling of the real `push-apk/opt` task that is pushing the apk to the Google Play store automatically.

```bash
Tip: If the have the graph1 id but not the graph2 id (COT graph) you can determine it by
1. Click on task group 1
2. Click on mozilla-beta candidates_fennec
3. The taskgroup id is the same as the candidates_fennec task id
```
* Mobile Firefox Release
    * Resolve the aforementioned human task `android-push-apk-breakpoint/opt` from the Chain Of Trust graph (graphid2). Doing so should quickly enable the scheduling of the real `push-apk/opt` task that is pushing the apk to the Google Play store automatically.
    * if pushapk's task expires in graph 1, do the following:

```bash
- select the task definition and copy it
- edit it:
    - update the timestamps
    - remove the breakpoint dependency from `task.dependencies`
- resubmit it
```

## 3. push to releases dir (mirrors)

### why
* Fennec releases don't automatically push to mirrors. They instead wait on a human decision (due to the need of QE sign off) to dictate when candidates dir looks good and we are ready to copy/push to releases dir

### when
* Mobile Firefox Betas, dot releases
    * after the successful pushing of the apk, you can perform this as well

### how
* Mobile Firefox Betas, Releases and dot releases
    * look for `fennec $branch push to releases human decision task` and mark it as resolved

* Mobile Firefox Releases
    * look for `fennec $branch push to releases human decision task` and mark it as resolved
    * if task is expired you'll need to resubmit this subset of tasks in a third graph! However, this should not include `candidates_fennec` job again (the one that is generating the Chain Of Trust graph)
    * to generate and submit graph 3 of the release:
        * step 1) get release information from Ship-it, such as branch, version, build_number and revision
        * step 2) call `releasetasks_graph_gen.py` and pass, among other things, the information from Ship-ut from step 1:
        * step 3) The resulted graphid should be tracked in releasewarrior (under issues for now, until we add support for graphN in releasewarrior)
```bash
ssh `whoami`@buildbot-master85.bb.releng.scl3.mozilla.com  # host we release-runner and you generate/submit new release promotion graphs
sudo su - cltbld
BRANCH=release
VERSION=TODO
BUILD_NUMBER=1
REVISION=TODO
cd /home/cltbld/releasetasks/
git status  # make sure we're clean
git branch  # make sure we're on master
git pull origin master  # make sure we are up to date.
cd /builds/releaserunner/tools/buildfarm/release/
hg status  # make sure this is clean
hg branch  # make sure this is on default
hg pull -u # make sure we are up to date.
source /builds/releaserunner/bin/activate
# call releasetasks_graph_gen.py with --dry-run and sanity check the graph output that would be submitted
python releasetasks_graph_gen.py --release-runner-config=../../../release-runner.yml --branch-and-product-config=/home/cltbld/releasetasks/releasetasks/release_configs/prod_mozilla-${BRANCH}_fennec_push_to_releases_graph.yml  --version $VERSION --build-number $BUILD_NUMBER --mozilla-revision $REVISION --dry-run
# call releasetasks_graph_gen.py for reals which will submit the graph to Taskcluster
python releasetasks_graph_gen.py --release-runner-config=../../../release-runner.yml --branch-and-product-config=/home/cltbld/releasetasks/releasetasks/release_configs/prod_mozilla-${BRANCH}_fennec_push_to_releases_graph.yml  --version $VERSION --build-number $BUILD_NUMBER --mozilla-revision $REVISION
```

# Troubleshooting

## Intermittent failures

If a task failed because of an intermittent failure (e.g.: network error, timeout), `rerun` it manually via [tctalker](https://github.com/mozilla/tctalker). Some tasks don't have automatic reruns set, but they do have 5 retries left. Thanks to reruns, you don't need to retrigger a task (which would have meant to reschedule the remaining subgraph).

## Flushing caches

If more than one build ran on a beta we need to flush the caches to remove the older builds from the CDN caches.  For instance in Firefox beta 46.0b5 we built builds 1 through 5 but we only ship build5.  See [Bug 1391843](https://bugzil.la/1391843) - Please purge CDN caches for firefox and devedition 56.0b4 as an example. After filing the bug as P1, it's highly recommended you follow up with the [mana docs](https://mana.mozilla.org/wiki/display/SVCOPS/Contacting+Cloud+Operations) to contact CloudOps by email as well as they don't always pay attention to P1 bugs.

## Working around Signoffs in Balrog

The Required Signoffs we have implemented in Balrog are there for a reason. In general, you should not try to workaround them. On occasion, extreme circumstances may warrant doing so, however. The most likely reason for this would be no members of a particular group being around, and needing to make an urgent change (eg: shutting off updates).

Note that even if you are a full fledged administrator, you yourself cannot make more than one Signoff on any given Scheduled Change. This is by design - we do not want a single account to be able make changes to protected Products or Channels. If you are certain you need to workaround the Signoffs, here's how:
* Find another person with some permissions in Balrog, and who is up to speed on the change you intend to make.
* Grant them the Role that you need to complete the Required Signoffs (through https://aus4-admin.mozilla.org/permissions).
* Have them make a Signoff with that Role.

As a concrete example, let's say we required 1 relman, 1 releng, and 1 qe signoff for Firefox release channel changes. Late on a Saturday night we discover a massive crash that requires us to shut off updates. Liz gets in contact with Kim to ask that this happen. Kim Schedules the necessary change in Balrog (which implicitly satisfies the releng signoff), and Liz signs off for relman. Because it is the weekend, and there was no planned work, QE is unavailable. Kim gets in contact with Aki, grants him the "qe" role, and Aki makes a Signoff under the "qe" Role, which fulfills the Signoff requirements. Kim then removes Aki's "qe" Role.

## Balrog channels

Firefox beta updates are served on the beta channel, Devedition Beta updates are served on the aurora channel.

## Creating a clone of a task using a different revision

This works with tasks where the task is on the edge of the graph, and has no dependencies.  Example: create https://tools.taskcluster.net/groups/Co8iBgS1RnKVNOWMZm0TUg/tasks/Co8iBgS1RnKVNOWMZm0TUg/details by cloning the failed task (Actions -> Edit Task) and replaced all revision entries with the new one

## PushApk: Fallback steps

If pushapk's task expires in graph 1, do the following:

- open the `push-apk/opt` Task's Definition in Raw Data mode and copy that to your clipboard
- hover over to [taskcluster create](https://tools.taskcluster.net/task-creator/) page
- trim the existing dummy tutorial task there and paste the task from your clipboard
- edit it:
    - update the timestamps (the time there is UTC)
    - make sure you specify at least 1h of deadline so that the task doesn't fail for having a deadline in the past
    - remove all dependencies strings from `task.dependencies` and add instead the taskGroupId string
- submit it
- since the taskGroupId is still pointing to the original graph, it will show up in the graph there as well as a clone of previous `push-apk/opt`

In the eventuality of a failure of pushapk_scriptworker, there are [instructions to manually publish APKs](https://github.com/mozilla-releng/mozapkpublisher#what-to-do-when-pushapk_scriptworker-doesnt-work).

## Procedure to ship Fennec, even though PushApk can't work

Made official by [bug 1384083](https://bugzilla.mozilla.org/show_bug.cgi?id=1384083).

1. Release Duty folks agree that PushApk can't publish anything because of reason X.
2. Ask Release Management to publish the APK manually (that is to say with [mozapkpublisher](https://github.com/mozilla-releng/mozapkpublisher), on a local computer). For historical reasons[3], some people in the Release Management team have the rights to publish APKs onto Google Play. See [documented technical steps](https://github.com/mozilla-releng/mozapkpublisher#what-to-do-when-pushapk_scriptworker-doesnt-work).
3. If a technical issue comes up, Release Management should ask Release Engineering[4] to publish the APK manually. This may require Release Management to grant write access[5] to Release Engineering for a given period of time.
4. If that doesn't work, Release Duty should ask Release Management to publish the APK via the Web interface. This way is the riskiest one. MozApkPublisher (and pushapk_scriptworker) [provides extra checks](https://johanlorenzo.github.io/blog/2017/06/07/part-2-how-mozilla-publishes-apks-onto-google-play-store-in-a-reasonably-secure-and-automated-way.html#4-mozapkpublisher-locales-and-google-play) that Google Play doesn't do. Somebody from Release Management may have to grant access Release Management to upload via the web interface.
