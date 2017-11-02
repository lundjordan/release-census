# Forewords

These steps are meant to be specifically for Fennec-58.0bN.

# High-level steps

1. ship-it
1. steps after QA signed off

# Detailed descriptions

## ship-it

Ship-it should be hooked up as normal, using release-runner3.

### Relpro action task

There will be a "Relpro" action task that shows up in Treeherder. This will be part of the on-push graph, but it will generate a new Promotion graph. The promotion graph's `taskGroupId` will be the same as the action task's `taskId`. This graph will contain all the promotion tasks that are needed to build and push Fennec to candidates.

## Publish Release

First, we need to kick off the publish action task. Then we need to resolve the push-apk-breakpoint task in the publish graph.

### Kick off publish action task

```bash
ssh buildbot-master85.bb.releng.scl3.mozilla.com
sudo su - cltbld
cd /builds/releaserunner3/
source bin/activate
# set the action task id to the `taskId` of the `promote_fennec` relpro action
ACTION_TASK_ID=M1QFL1R7RWCTReFLsRWmGw
python tools/buildfarm/release/trigger_action.py --action-task-id $ACTION_TASK_ID --release-runner-config /builds/releaserunner3/release-runner.yml --action-flavor publish_fennec
```

This will show you a task definition and ask if you want to submit it (y/n). If you're ready to publish, choose `y`. The publish action `taskId` will be near the bottom of the output; this will match the publish graph's `taskGroupId`.

### Resolve push-apk-breakpoint task

In the publish graph there will be a `push-apk-breakpoint` task. Find this, and resolve it by

```bash
taskcluster task complete -- TASKID
```
