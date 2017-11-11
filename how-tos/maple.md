# maple

Last updated 2017-11-10

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

---
# how-to
## Trigger relpro: promote

Launch a new promotion graph using [ship-it dev](https://ship-it-dev.allizom.org/).

1. Click "Ship a new release"
1. Fennec or Firefox
1. The version will be displayed [here](https://hg.mozilla.org/projects/maple/file/tip/browser/config/version_display.txt) -- `58.0b6` as of this writing.
1. The branch is `projects/maple`
1. Enter the maple revision... probably the latest from [here](https://hg.mozilla.org/projects/maple/summary)
1. Click "Gimme a <product>"
1. Click "View releases" -> "Submitted"
1. Click "Ready" and "Do eet"
1. The new relpro action should be on [treeherder](https://treeherder.mozilla.org/#/jobs?repo=maple) as a new `Relpro` symbol; click it
1. the taskId is on the lower left. Clicking on it will bring you to the log
1. pasting the taskid into the url `https://tools.taskcluster.net/groups/TASKID` will bring you to the promotion graph

## Trigger relpro: publish

```bash
ssh buildbot-master83.bb.releng.scl3.mozilla.com
sudo su - cltbld
cd /builds/releaserunner3/
source bin/activate
# set the action task id to the taskId of the promotion relpro action
ACTION_TASK_ID=M1QFL1R7RWCTReFLsRWmGw
# This should be `publish_fennec` or `maple_desktop_promotion`
ACTION_FLAVOR=publish_fennec
python tools/buildfarm/release/trigger_action.py --action-task-id $ACTION_TASK_ID --release-runner-config /builds/releaserunner3/release-runner.yml --action-flavor $ACTION_FLAVOR
```

The action should show up on treeherder; its taskId is the graph's group id as above.

---
## diff taskgraphs

[`taskgraph-gen.py`](https://hg.mozilla.org/build/braindump/file/tip/taskcluster/taskgraph-diff/taskgraph-gen.py) lets you generate a bunch of graphs from a given revision. Once you generate graphs from 2 revisions, [`taskgraph-diff.py`](https://hg.mozilla.org/build/braindump/file/tip/taskcluster/taskgraph-diff/taskgraph-diff.py) lets you diff the two sets of graphs. This means you can diff the graphs generated from tip of central against the tip of maple, or from the tip of maple against maple + your patch, or whatever.

e.g.

```
# First create virtualenv with dictdiffer and activate it
# Then run:
cd mozilla-unified
hg up -r central
../taskgraph-diff/taskgraph-gen.py --overwrite central
hg up -r maple
../taskgraph-diff/taskgraph-gen.py --overwrite maple
../taskgraph-diff/taskgraph-diff.py central maple
# diffs are in ../taskgraph-diff/json/maple/*.diff
```

In the above example, I've softlinked my `braindump/taskcluster/taskgraph-diff` directory to be a sibling of `mozilla-unified`.

Caveats:

- the diffs are kind of interesting to read. They're [dictdiffer](https://dictdiffer.readthedocs.io/en/latest) diffs [1]. Once you get the hang of them they work.
- the params are checked in along with the scripts. These will break over time as people add and remove required parameters. Also, if we rename our `target_tasks_methods` we'll see breakage.

We have a [`params_pre_buildnum`](https://hg.mozilla.org/build/braindump/file/tip/taskcluster/taskgraph-diff/params-pre-buildnum) directory we can use if we're generating task graphs from a pre-[bug 1415391](https://bugzilla.mozilla.org/show_bug.cgi?id=1415391) revision.

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
- Naming: promote/push/ship? prmote/publish/ship? I'm thinking `ACTION_PRODUCT`, so `promote_fennec` or `push_firefox` or `ship_devedition`
