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
# Actions

## 1. email drivers re: release live on test channel

### why
* cdntest and localtest channels serve releases from the releases dir (mirrors/cdn) or candidates dir depending on the release and channel. They are testing channels used before we serve from the _real_ update channel
* we should notify drivers once updates are available on the ${branch}-{cdntest,localtest} channel because we don't have taskcluster email notifications yet

### when
* Desktop Firefox Betas
    * look in taskgraph for task with name `mozilla-beta beta final verification`
        * once this task has run successfully, that means we have 1) pushed to releases dir 2) and verified beta-cdntest is serving the release from there
* Desktop Firefox Release-Candidates
    * context: RCs are m-r releases that are served to beta uses prior to release channel users. RCs use `beta-cdntest` and `release-cdntest` for QA.
    * `beta-cdntest` serves updates from the candidates/ dir. We should notify drivers once all artifacts are available there. we don't worry about `release-cdntest` because that is not automatic in automation
        * look in taskgraph graph 1 for task with name `mozilla-release beta final verification`
        * once this task has run successfully, that means 1) the release has finished uploading all artifacts to candidates dir 2) and verified beta-cdntest is serving the release from there
* Desktop Firefox Releases (dot releases)
    * `release-localtest` serves updates from the candidates/ dir. We should notify drivers once all artifacts are available there. Again, release-cdntest depends on a human decision (not automatic) in automation so no email required.
        * look in taskgraph graph for task with name `firefox mozilla-release push to releases human decision task`.
        * this task should be the only task left that is blocking the graph (aside from the post release human task)
        * all other en-us, l10n, partial, and partner artifact generating tasks should be finished.
* Desktop Firefox ESRs
    * `esr-localtest` serves updates from the candidates/ dir. We should notify drivers once all artifacts are available there. Again, esr-cdntest depends on a human decision (not automatic) in automation so no email required.
        * look in taskgraph graph for task with name `firefox mozilla-esr push to releases human decision task`.
        * this task should be the only task left that is blocking the graph (aside from the post release human task)
        * all other en-us, l10n, partial, and partner artifact generating tasks should be finished.

### how
* Desktop Firefox Betas
    * email release-drivers@mozilla.org with subject only email `[desktop] Firefox Beta $version updates are available on the beta-cdntest channel now <EOM>`
* Desktop Firefox Release-Candidates
    * email release-drivers@mozilla.org with subject only email `[desktop] Firefox RC Release $version updates are available on the beta-cdntest channel now <EOM>`
* Desktop Firefox Releases (dot releases)
    * email release-drivers@mozilla.org with subject only email `[desktop] Firefox Release $version updates are available on the release-localtest channel now <EOM>`
* Desktop Firefox ESRs
    * email release-drivers@mozilla.org with subject only email `[desktop] Firefox ESR $version updates are available on the esr-localtest channel now <EOM>`


## 2. push to releases dir (mirrors)

### why
* some releases don't automatically push releases to the releases dir automatically. They instead wait on a human decision (sign off) to dictate when candidates dir looks good and we are ready to copy/push to releases dir

### when
* Desktop Firefox Release-Candidate Releases
    * release-cdntest channel serves updates from releases dir so it depends on this step unlike RC beta-cdntest channel
    * wait for sign off from release-drivers with email like: `[desktop] Please push ${version} to ${channel}` where version is like `46.0 build 3` and channel is like `release-cdntest` or `cdntest` or `mirrors` or `releases`
        * note: if they do not explicitly ask for `release-cdntest` it is okay to assume if you are confident but please reply with something like `pushed and please use explicit name when requesting next time: release-cdntest channel :)`
* Desktop Firefox Releases (dot releases)
    * wait for sign off from release-drivers with email like: `[desktop] Please push ${version} to {cdntest,releases,mirrors}` where version is like: `46.0.1 build 5`, and channel is like: `release-cdntest` or `cdntest` or `mirrors` or `releases`
        * note: if they do not explicitly ask for `release-cdntest` it is okay to assume if you are confident but please reply with something like `pushed and please use explicit name when requesting next time: release-cdntest channel :)`
* Desktop Firefox ESRs
    * wait for sign off from release-drivers with email like: `[desktop] Please push ${version} to {cdntest,releases,mirrors}` where version is like: `38.0esr` or `38.2.0esr`, and channel is like: `esr-cdntest` or `cdntest` or `mirrors` or `releases`
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
$ python releasetasks_graph_gen.py --release-runner-ini=../../../release-runner.ini --branch-and-product-config=/home/cltbld/releasetasks/releasetasks/release_configs/prod_mozilla-release_firefox_rc_graph_2.yml --common-task-id=$TASK_TASKID_FROM_GRAPH1 --dry-run
# call releasetasks_graph_gen.py for reals which will submit the graph to Taskcluster
$ python releasetasks_graph_gen.py --release-runner-ini=../../../release-runner.ini --branch-and-product-config=/home/cltbld/releasetasks/releasetasks/release_configs/prod_mozilla-release_firefox_rc_graph_2.yml --common-task-id=$TASK_TASKID_FROM_GRAPH1
```

* Desktop Firefox Releases (dot releases)
    * wait for sign off from release-drivers with email like: `[desktop] Please push ${version} to {cdntest,releases,mirrors}` where version is like: `46.0.1 build 5`, and channel is like: `release-cdntest` or `cdntest` or `mirrors` or `releases`
        * note: if they do not explicitly ask for `release-cdntest` it is okay to assume if you are confident but please reply with something like `pushed and please use explicit name when requesting next time: release-cdntest channel :)`
    * get taskid from task with name `firefox mozilla-release push to releases human decision task` in task graph
    * This task is blocking `[beetmover] firefox mozilla-release push to releases`
    * To resolve the human decision task run the following:
```bash
 tctalker --conf ~/.taskcluster/relpro.json report_completed $TASK_ID
```

* Desktop Firefox ESRs
    * wait for sign off from release-drivers with email like: `[desktop] Please push ${version} to {cdntest,releases,mirrors}` where version is like: `38.0esr` or `38.2.0esr`, and channel is like: `esr-cdntest` or `cdntest` or `mirrors` or `releases`
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
$ python releasetasks_graph_gen.py --release-runner-ini=../../../release-runner.ini --branch-and-product-config=/home/cltbld/releasetasks/releasetasks/release_configs/prod_mozilla-esr45_firefox_rc_graph_2.yml --common-task-id=$TASK_TASKID_FROM_GRAPH1 --dry-run
# call releasetasks_graph_gen.py for reals which will submit the graph to Taskcluster
$ python releasetasks_graph_gen.py --release-runner-ini=../../../release-runner.ini --branch-and-product-config=/home/cltbld/releasetasks/releasetasks/release_configs/prod_mozilla-esr45_firefox_rc_graph_2.yml --common-task-id=$TASK_TASKID_FROM_GRAPH1
```


## 3. publish release

### why
* the publish release human decision task makes the release go _live_. it
  requires sign off from rel-man / QE. It triggers the publish to balrog task
  for all graph types, plus the update bouncer aliases and bump version tasks
  for betas and RC graph2 graphs.

### when
* Desktop Firefox Betas
    * Wait for email from RelMan or QE with subject request like `please push Firefox 47.0b2 to the beta channel`
    * sanity check all update verify and the final verify task has completed successfully in the graph
* Desktop Firefox Release-Candidate (beta release prior to release release)
    * Wait for email from RelMan or QE with subject request like `please push Firefox 46.0 to the beta channel`
    * sanity check all beta update verify and the beta final verify task has completed successfully in graph 1
* Desktop Firefox Release and Release-Candidate (RC and dot releases both push to release channel)
    * Wait for email from RelMan or QE with subject request like `please push Firefox 46.0 to the release channel`
    * sanity check all release update verify tasks from graph 1 and the release final verify task has completed successfully from graph 2
* Desktop Firefox ESRs
    * Wait for email from RelMan or QE with subject request like `please push Firefox 45.2.0esr to the esr channel`
    * sanity check all release update verify tasks from graph 1 and the release final verify task has completed successfully from graph 2

### how
* Desktop Firefox Betas, Desktop Firefox Release-Candidate (beta release prior to release release) and Desktop Firefox dot Releases
    * go to the task graph (there is only one) and find taskId of `publish release human decision task`
    * Resolve the "publish release human decision" task using the command below
    * reply to RelMan's email as soon as this step is completed
* Desktop Firefox Release and Release-Candidate (RC releases push to release channel)
    * go to the task graph #2 and find taskId of `publish release human decision task`
    * Resolve the "publish release human decision" task using the command below
    * reply to RelMan's email as soon as this step is completed
* Desktop Firefox ESRs
    * depending on timing you may have 1 or 2 graphs. Go to the latest one and
      find taskId of `publish release human decision task`
    * Resolve the "publish release human decision" task using the command below
    * reply to RelMan's email as soon as this step is completed
```bash
 tctalker --conf ~/.taskcluster/relpro.json report_completed $TASK_ID
```

## 4. post release step

### why
* releases are needed to be marked as "shipped" in Ship-it to make the partial
  guessing algorithm work and make sure the product-details site has correct information
  about releases.

### when
* immediately after running `publish release` human decision step

### how
* Desktop Firefox Betas, Desktop Firefox Release, Desktop Firefox dot Releases, Desktop Firefox ESRs
    * it is done automatically so just sanity check that the `<product> <channel> mark release as shipped` has completed successfully in the graph
* Other *not* release-promotion based releases (Thunderbird, Fennec, etc) are needed to be marked as shipped on Ship It. To do so, visit
  https://ship-it.mozilla.org/releases.html, find the release in question, and
  click the "Shipped!" button.
