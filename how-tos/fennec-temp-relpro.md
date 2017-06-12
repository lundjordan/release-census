# Forewords

These steps are meant to be specifically for Fennec-53.0b1.

# High-level steps

1. noop ship-it
2. skip source
3. start off the Fennec graph
4. steps after QA signed off

# Detailed descriptions

## Noop ship-it

Nothing to do here but notice there should be a Fennec build under [this section](https://ship-it.mozilla.org/releases.html#reviewed-tab).
Grab the `builduild number`, the `revision` and the `version` from the Ship-it entry.

## Skip source

Nothing to do here for the moment. The source builder needs to be fixed so for the moment it is turned off.

## Start off the Fennec graph

The way this works is by triggering a graph that contains most of the builders (sans source builder, checksums and others which are still under development).
One of the tasks is a `decision task` which will, at its turn, generate another graph for which all the tasks
will have their TaskGroupId set to the decision task. That is the nightly graph that builds, signs and beetmoves stuff to S3.

* Follow the following set of instructions:

```bash
ssh `whoami`@buildbot-master85.bb.releng.scl3.mozilla.com  # host we release-runner and you generate/submit new release promotion graphs
sudo su - cltbld
BRANCH=beta  # use release for release
VERSION=54.0b14
BUILD_NUMBER=1
REVISION=1234456
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
python releasetasks_graph_gen.py --release-runner-ini=../../../release-runner.ini --branch-and-product-config=/home/cltbld/releasetasks/releasetasks/release_configs/prod_mozilla-${BRANCH}_fennec_full_graph.yml  --version $VERSION --build-number $BUILD_NUMBER --mozilla-revision $REVISION --dry-run
# call releasetasks_graph_gen.py for reals which will submit the graph to Taskcluster
python releasetasks_graph_gen.py --release-runner-ini=../../../release-runner.ini --branch-and-product-config=/home/cltbld/releasetasks/releasetasks/release_configs/prod_mozilla-${BRANCH}_fennec_full_graph.yml  --version $VERSION --build-number $BUILD_NUMBER --mozilla-revision $REVISION
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

*If this is the solution you end up doing - we will also need the following*:
* trigger another subgraph containing all the steps after push-to-releases, included. This can be done similarly with the above commands via releasetasks, but toggling to `False` all variables from [here](https://github.com/mozilla/releasetasks/blob/master/releasetasks/release_configs/prod_mozilla-beta_fennec_full_graph.yml)

## Steps after QA signed off

There are 2 "human decision" (aka "breakpoint") tasks to resolve *at the same time* (the order doesn't matter, though). One is in the first graph (the one kicked off by releasetasks), it's called `fennec mozilla-beta push to releases human decision task`. The other is in the Chain Of Trust graph, look for `android-push-apk-breakpoint/opt`.

### PushApk: Fallback steps

If pushapk's task expires in graph 1, do the following:

- select the task definition and copy it
- edit it:
    - update the timestamps
    - remove the breakpoint dependency from `task.dependencies`
    - I'm not sure "edit and recreate" will work, since the taskGroupId will change?
- resubmit it

In the eventuality of a failure of pushapk_scriptworker, there are [instructions to manually publish APKs](https://github.com/mozilla-releng/mozapkpublisher#what-to-do-when-pushapk_scriptworker-doesnt-work).

#### manually run l10n-bumper
```
ssh buildbot-master01.bb.releng.use1.mozilla.com
sudo su - cltbld
cd /builds/l10n-bumper
/tools/python27/bin/python2.7 mozharness/scripts/l10n_bumper.py -c l10n_bumper/mozilla-beta.py
```
