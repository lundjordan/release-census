# maple

Last updated 2017-10-25

Currently, maple is our taskcluster relpro migration area.

---
# Current status

## Trello

The [Trello board](https://trello.com/b/EGWsGSXT/tc-migration-release-h2-2017) has the latest human tasks. `as of Oct25, We're currently getting Fennec relpro green end-to-end, and land the ready fixed-on-maple fennec tasks in production. Others of us are starting on the Firefox in-tree tasks.

Please feel free to add tasks there if we're missing any!

---

## Dep vs release

Right now, we're set up differently than jamun, in that we're signing with dep scopes. The plan is to fix anything that prevents us from doing an end-to-end staging release with dep signing. If that proves too difficult, we can turn on release signing, and fix staging releases with dep scopes later.

If we proceed with Firefox with dep signing, we'll have to deal with update verify and other mar signature checks.

---

## Scriptworker or encrypted env vars

We're going to try to use beetmover scriptworker + balrog scriptworker instead of continuing to use encrypted env vars in the task definitions.

### beetmover+balrog scriptworker

- balrog scriptworker needs release support
- beetmover scriptworker needs firefox candidates/cdns support
- we have to cot-enable *everything* upstream of these tasks. We have balrog+beetmover tasks in the recompression tasks way at the end of the graph -- they'll need to be part of the chain!

This may be more work, but avoids some hacks and is where we want to end up.

### encrypted env vars

- we'll need to make sure the appropriate docker-image tasks run in the promote action. I added a `do_not_optimize` property so we can avoid optimizing the docker-image task out of the graph.
- rail says, "We would need to know the corresponding task IDs - you have to use them to make encrypted env vars work." We could make this work by either generating all the slugids in advance, with the encrypted env vars, and passing that in, or by exposing the private key in taskcluster secrets or something like that. Neither is a great option.

This may or may not be less work, and we'll be further away from our end goal when we're done.

---
# how-to
## Trigger relpro: promote fennec

Launch a new Fennec promotion graph using [ship-it dev](https://ship-it-dev.allizom.org/).

1. Click "Ship a new release"
1. Fennec
1. The version will be displayed [here](https://hg.mozilla.org/projects/maple/file/tip/browser/config/version_display.txt) -- `58.0a1` as of this writing.
1. The branch is `projects/maple`
1. Enter the maple revision... probably the latest from [here](https://hg.mozilla.org/projects/maple/summary)
1. Enter an empty dict `{}` as the l10n changesets -- we'll get the real information from in-tree.
1. Click "Gimme a fennec"
1. Click "View releases" -> "Submitted"
1. Click "Ready" and "Do eet"
1. The new relpro action should be on [treeherder](https://treeherder.mozilla.org/#/jobs?repo=maple) as a new `Relpro` symbol; click it
1. the taskId is on the lower left. Clicking on it will bring you to the log
1. pasting the taskid into the url `https://tools.taskcluster.net/groups/TASKID` will bring you to the `promote_fennec` graph

## Trigger relpro: publish fennec

```bash
ssh buildbot-master83.bb.releng.scl3.mozilla.com
sudo su - cltbld
cd /builds/releaserunner3/
source bin/activate
# set the action task id to the taskId of the `promote_fennec` relpro action
ACTION_TASK_ID=M1QFL1R7RWCTReFLsRWmGw
python tools/buildfarm/release/trigger_action.py --action-task-id $ACTION_TASK_ID --release-runner-config /builds/releaserunner3/release-runner.yml --action-flavor publish_fennec
```

The action should show up on treeherder; its taskId is the graph's group id as above.

---
## diff taskgraphs

- save a maple parameters.yml file as `maple-ci.yml`
- copy it, edit the `target_tasks_method` to `candidates_fennec` and save it as `promote-fennec.yml`
- copy it, edit the `target_tasks_method` to `publish_fennec` and save it as `publish-fennec.yml`

Create different task-graph json files to diff against. For example, on maple,

```bash
./mach taskgraph target-graph -p maple-ci.yml --json > ../maple-clean.json
./mach taskgraph target-graph -p promote-fennec.yml --json > ../maple-promote-fennec-clean.json
./mach taskgraph target-graph -p publish-fennec.yml --json > ../maple-publish-fennec-clean.json
```

Then update to your bookmark, and do the same (but to dirty files). Then you can verify that you haven't added any new tasks where they shouldn't go, but have added the task where it should go.

Before we merge to m-c, we'll need to make sure we haven't broken m-c ci, m-c nightly, m-b ci, m-b `candidates_fennec`, try, etc. So we may want to keep a library of parameters files lying around, and maybe a shell script, so we can perform these checks.

---
## debug release promotion action

We can use `./mach taskgraph test-action-callback` to debug.

I used

```
./mach taskgraph test-action-callback --task-group-id LR-xH1ViTTi2jrI-N1Mf2A --input /src/gecko/params/promote_fennec.yml -p /src/gecko/params/maple-fennec-candidates.yml release_promotion_action > ../promote.json
```

`promote_fennec.yml`:

(This is also the input I use in the action in treeherder)

```yaml
build_number: 1
release_promotion_flavor: promote_fennec
```

`maple-fennec-candidates.yml`:
```yaml
base_repository: https://hg.mozilla.org/mozilla-central
build_date: 1507178755
do_not_optimize: []
existing_tasks: {}
filters:
- check_servo
- target_tasks_method
head_ref: a76bd64bcdd3b360918936a3cfbc5e3e604b1d1c
head_repository: https://hg.mozilla.org/projects/maple
head_rev: a76bd64bcdd3b360918936a3cfbc5e3e604b1d1c
include_nightly: true
level: '3'
message: ' '
moz_build_date: '20171005044555'
optimize_target_tasks: true
owner: asasaki@mozilla.com
project: maple
pushdate: 1507178755
pushlog_id: '13'
release_history: {}
target_tasks_method: candidates_fennec
try_mode: null
try_options: null
try_task_config: null
```

I'm not 100% sure if it's important to use a promotion parameters file or an on-push one.

---
# hg / git - how Aki's muddling through

I'm open to how we do this; I'm absolutely certain my method is not an ideal one.

I like hg bookmarks for smaller projects, but for big ones like this one, I prefer git's rebase behavior to keep my patch queue sane. However, I haven't solved the push-to-hg part yet, so I'm working on maple, landing when I have a probably-good patch, debugging, and then rebasing my work on github.

## Github
- fork [gecko-dev](https://github.com/mozilla/gecko-dev/)
- pull in [gecko-projects](https://github.com/mozilla/gecko-projects/) to your fork, by cloning, adding a remote, and fetching
- after an m-c to maple merge, I pull gecko-dev's `master` branch and gecko-project's `maple` branch. Then I update to my `maple-staging` branch, and `git rebase -i master` and deal with any conflicts.
- then I diff against `maple`. Sometimes it's easiest to export the revs from hg and `patch -p1 < patchfile` and `git commit`, then `git rebase -i master` to clean up the patches.

I haven't tried cinnabar; it's based off a different set of changesets and doesn't follow maple. However, it would allow for pushing to hg.

## Hg

Bookmarks are good for a single branch. I tend to clump all my unlanded patches into a single bookmark, `hg histedit` to edit the patches, and `hg rebase -b BOOKMARK -d maple` to rebase my bookmark against maple. Once the patches look good, I land and move over to git for my patch queue.

---

# Future

Random thoughts:
- Should we switch our [release promotion action properties](https://hg.mozilla.org/projects/maple/file/tip/taskcluster/taskgraph/actions/release_promotion.py#l67) to dashed-words instead of `underscore_words`?
- Should we rename the `candidates_fennec` `target_tasks_method` to `promote_fennec`? We're rebuilding, so it's not really strict promotion, but it matches `promote_firefox` and the future `promote_devedition`...
