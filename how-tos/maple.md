# maple

Last updated 2017-10-11

Currently, maple is our taskcluster relpro migration area.

Aki's on PTO 2017-10-12 - 2017-10-13, so here's a brain dump.

---
## Current status

### Trello

The [Trello board](https://trello.com/b/EGWsGSXT/tc-migration-release-h2-2017) has the latest human tasks. `Fixed on maple` currently means we're able to generate the right graph... we'll have additional work to get this green end-to-end.

Please feel free to add tasks there if we're missing any!

### open bugs

- [bug 1407817](https://bugzilla.mozilla.org/show_bug.cgi?id=1407817) has some missing buildbot-configs and in-tree patches for fennec relpro on maple.

Random thoughts:
- Should we switch our properties to dashed-words instead of `underscore_words`?
- Should we rename `candidates_fennec` to `promote_fennec` ?

---

### Dep vs release

Right now, we're set up differently than jamun, in that we're signing with dep scopes. There are a couple approaches we can take:

1. Proceed with dep scopes, and fix anything that prevents us from doing an end-to-end staging release
1. Turn on release signing, and fix staging releases with dep scopes later.

#### Dep scopes

If we proceed with dep scopes,

- we will need dep scriptworker pools for {beetmover,balrog,pushapk}. These don't have to be large. They'll have dep creds only, and will verify chain of trust artifacts, but not the cot signatures. This is because dep signing doesn't sign its cot artifacts.
- we'll have to deal with update verify and other mar signature checks
- we'll have to patch pushapk to enable dep scope -- this will be a dry-run, and we could check for the dep apk signature.

This have more work items, but we'll end up with a staging release that we can run anywhere, even try!

#### Release scopes

- We'll have to deal with maple not having the release signing scopes -- just a taskcluster bug away
- we'll have to update taskcluster/taskgraph/util/scriptworker.py to enable release signing

This may be less work, but we'll be further away from our end goal when we're done.

---

### Scriptworker or encrypted env vars

We can either use beetmover scriptworker + balrog scriptworker, or keep using encrypted env vars.

#### beetmover+balrog scriptworker

- balrog scriptworker needs release support
- beetmover scriptworker needs push to releases support
- we have to cot-enable *everything* upstream of these tasks. We have balrog+beetmover tasks in the recompression tasks way at the end of the graph -- they'll need to be part of the chain!

This may be more work, but avoids some hacks and is where we want to end up.

#### encrypted env vars

- we can probably add some inputs into the relpro action for env vars, allowing us to generate these before submitting the action task.
- we'll need to make sure the appropriate docker-image tasks run in the promote action. I added a `do_not_optimize` property so we can avoid optimizing the docker-image task out of the graph.

This may be less work, but we'll be further away from our end goal when we're done.

---
## action task info

As of this writing, we have a single action for release promotion, the [`release_promotion_action`](https://hg.mozilla.org/projects/maple/file/tip/taskcluster/taskgraph/actions/release_promotion.py).

To trigger:
- go to [maple on treeherder](https://treeherder.mozilla.org/#/jobs?repo=maple)
- choose a good revision; it must have a green on-push decision task
- Open the release promotion dialog: Top right -> down-arrow -> Custom Push Action -> Release Promotion.
- Fill in the appropriate payload (see below for docs / examples); Trigger.

### release promotion properties

(We may want to follow the [tree rules](https://hg.mozilla.org/projects/maple/file/tip/taskcluster/taskgraph/util/schema.py#l141) and make this yaml schema only accept dashes instead of underscores?)

- `build_number`: int, required. e.g. 58.0b1 build `BUILD_NUMBER`. Defaults to 1.
- `revision`: string, optional. The revision to promote. It'll default to the one you chose in treeherder. The action uses this to find the decision task, which we need for `label-to-taskid.json`, `actions.json`, and `task-graph.json`.
- `release_promotion_flavor`: enum, required. Must be a key of [`RELEASE_PROMOTION_CONFIG`](https://hg.mozilla.org/projects/maple/file/tip/taskcluster/taskgraph/actions/release_promotion.py#l21), e.g. `{promote,publish}_{fennec,firefox}` (I'm leaving devedition for later, for now). Each specifies defaults for `target_tasks_method`, `previous_graph_kinds`, and `do_not_optimize`. We're able to override those values via the input properties in staging, but in production we may want to remove that ability.
- `do_not_optimize`: array, optional: task labels to force to run. I added this so we could force a re-run of docker-image tasks, so we get new antivirus definitions. This will override the release promotion flavor's default `do_not_optimize`.
- `target_tasks_method`: string, optional. Override the release promotion flavor's default `target_tasks_method`; these are defined in [`target_tasks.py`](https://hg.mozilla.org/projects/maple/file/tip/taskcluster/taskgraph/target_tasks.py)
- `previous_graph_kinds`: array, optional. Build the target graph that you want, and then point at the `previous_graph_ids` and replace these kinds with tasks from those graphs. Essentially, this allows us to point at the on-push builds as dependencies in the promotion graph. If specified, this would override the release promotion flavor's defaults.
- `previous_graph_ids`: array, optional. These are the decision / action taskIds that we want to use to replace parts of our graph. For promotion, this would be the on-push decision task. For publishing, this would be the [on-push-decision, promotion-action] taskIds. Any labels that are in both graphs will be replaced with the rightmost graph's taskIds. We don't have to specify this for promotion; I haven't figured out a way to auto-populate this for publishing, yet. Maybe we can add an index for the promotion action task?

---
## how-to

---
### diff taskgraphs

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
### debug release promotion action

We can use `./mach taskgraph test-action-callback` to debug.

I used

```
./mach taskgraph test-action-callback --task-group-id LR-xH1ViTTi2jrI-N1Mf2A --input /src/gecko/params/promote_fennec.yml -p /src/gecko/params/maple-fennec-candidates.yml release_promotion_action > ../promote.json
```

`promote_fennec.yml`:
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
## hg / git - how Aki's muddling through

I'm open to how we do this; I'm absolutely certain my method is not an ideal one.

I like hg bookmarks for smaller projects, but for big ones like this one, I prefer git's rebase behavior to keep my patch queue sane. However, I haven't solved the push-to-hg part yet, so I'm working on maple, landing when I have a probably-good patch, debugging, and then rebasing my work on github.

### Github
- fork [gecko-dev](https://github.com/mozilla/gecko-dev/)
- pull in [gecko-projects](https://github.com/mozilla/gecko-projects/) to your fork, by cloning, adding a remote, and fetching
- after an m-c to maple merge, I pull gecko-dev's `master` branch and gecko-project's `maple` branch. Then I update to my `maple-staging` branch, and `git rebase -i master` and deal with any conflicts.
- then I diff against `maple`. Sometimes it's easiest to export the revs from hg and `patch -p1 < patchfile` and `git commit`, then `git rebase -i master` to clean up the patches.

I haven't tried cinnabar; it's based off a different set of changesets and doesn't follow maple. However, it would allow for pushing to hg.

### Hg

Bookmarks are good for a single branch. I tend to clump all my unlanded patches into a single bookmark, `hg histedit` to edit the patches, and `hg rebase -b BOOKMARK -d maple` to rebase my bookmark against maple. Once the patches look good, I land and move over to git for my patch queue.
