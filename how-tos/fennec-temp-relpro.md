# Forewords

These steps are meant to be specifically for Fennec-53.0b1.

# High-level steps

1. noop ship-it
2. skip source
3. start off the Fenenc graph
4. run pushapk manually
5. mark release as shipped in ship-it

# Detailed descriptions

## Noop ship-it

Nothing to do here but notice there should be a Fennec build under [this section](https://ship-it.mozilla.org/releases.html#reviewed-tab).
Grab the `builduild number`, the `revision` and the `version` from the Ship-it entry.

## Skip source

Nothing to do here for the moment. The source builder needs to be fixed so for the moment it is turned off.

## Start off the Fenenc graph

The way this works is by triggering a graph that contains most of the builders (sans source builder, checksums and others which are still under development).
One of the tasks is a `decision task` which will, at its turn, generate another graph for which all the tasks
will have their TaskGroupId set to the decision task. That is the nightly graph that builds, signs and beetmoves stuff to S3.

* Follow the following set of instructions:

```bash
$ ssh `whoami`@buildbot-master85.bb.releng.scl3.mozilla.com  # host we release-runner and you generate/submit new release promotion graphs
$ sudo su - cltbld
$ cd /home/cltbld/releasetasks/
$ git pull origin master  # make sure we are up to date. note: make sure this is on master and clean first
$ cd /builds/releaserunner/tools/buildfarm/release/
$ hg pull -u # make sure we are up to date. note: make sure this is on default and clean first
$ source /builds/releaserunner/bin/activate
# call releasetasks_graph_gen.py with --dry-run and sanity check the graph output that would be submitted
$ python releasetasks_graph_gen.py --release-runner-ini=../../../release-runner.ini --branch-and-product-config=/home/cltbld/releasetasks/releasetasks/release_configs/prod_mozilla-beta_fennec_full_graph.yml  --version TODO --build-number TODO --mozilla-revision TODO --dry-run
# call releasetasks_graph_gen.py for reals which will submit the graph to Taskcluster
$ python releasetasks_graph_gen.py --release-runner-ini=../../../release-runner.ini --branch-and-product-config=/home/cltbld/releasetasks/releasetasks/release_configs/prod_mozilla-beta_fennec_full_graph.yml  --version TODO --build-number TODO --mozilla-revision TODO
```

* The resulted graphid should be tracked in releasewarrior
* Once the decision-task generated graph is green and all artifacts are under [candidates](http://archive.mozilla.org/pub/mobile/candidates/) for that given version, send a heads-up email like [this](https://github.com/mozilla/releasewarrior/blob/master/how-tos/relpro.md#why)
to release drivers specifying the updates are now available on the `beta-localtest` channel.

*Disclaimer*

If for some reason any of the steps above fail, we still have a fall-back option by using the manual hook to trigger the nightly graph that will ensure the build/signing/beetmoving artifacts to S3.
The hook that triggers the Fennec graph is [here](https://tools.taskcluster.net/hooks/#project-releng/candidates-fennec-beta).
* alter GECKO_HEAD_REF, GECKO_HEAD_REV to corresponding changeset from Ship-it
* bump the buildnumber to correspond to Ship-it
* trigger hook!

## Run pushapk manually

### Use pushapk_scriptworker

1. Fetch the [base task definition](https://github.com/mozilla-releng/pushapkscript/blob/master/task_example.json)
2. Paste it onto [TC's task creator](https://tools.taskcluster.net/task-creator/)
3. Modify the [fields that need to be changed](https://github.com/mozilla-releng/pushapkscript#taskjson):
  * For the APKs locations, use the signed tasks.
  * Use the scope `'project:releng:googleplay:beta'`
  * Change `google_play_track` to `production`
  * Keep `dry_run` to `true`
4. You may want to attach this task to the rest of the graph. To do so, add in your task definition:
```
schedulerId: gecko-level-3
taskGroupId: $ACTUAL_TASKGROUP_ID
```
5. If everything passed, create second task with the same definition, but flip `dry_run` to false.

### Fallback steps

In the eventuality of a failure of pushapk_scriptworker, there are [instructions to manually publish APKs](https://github.com/mozilla-releng/mozapkpublisher#what-to-do-when-pushapk_scriptworker-doesnt-work).

#### manually run l10n-bumper
```
ssh buildbot-master01.bb.releng.use1.mozilla.com
sudo su - cltbld
cd /builds/l10n-bumper
/tools/python27/bin/python2.7 mozharness/scripts/l10n_bumper.py -c l10n_bumper/mozilla-beta.py
```

## Mark release as shipped in ship-it
