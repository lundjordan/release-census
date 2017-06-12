# Release: Firefox 53.0.2

### Started: 2017-05-04

## Build 1

### Release Graph
[task group](https://tools.taskcluster.net/push-inspector/#/kzUwQOlpRmGCT-0z0GsTxw)

#### Status
- [x] [submit to Shipit](https://wiki.mozilla.org/Release:Release_Automation_on_Mercurial:Starting_a_Release#Submit_to_Ship_It)
- [x] [pushed to mirrors/releases](../how-tos/relpro.md#2-push-to-releases-dir-mirrors)
- [x] [published release tasks](../how-tos/relpro.md#3-publish-release)

### Issues
- SPECIAL REQUIREMENT: if we decide to ship a dot release, we need to keep the WNP around for users updating from <53.0 : https://bugzilla.mozilla.org/show_bug.cgi?id=1354736#c26
- SPECIAL REQUIREMENT: after shipping 53.0.1, [repack the funnelcake](https://gist.github.com/escapewindow/5dba93a02bb346f5ac3677477106a46f/#funnelcake-still-live-when-we-do-a-chemspilldot-release-eg-5301)
- Missing WNP blobs added manually. More on this [here](https://bugzilla.mozilla.org/show_bug.cgi?id=1354736#c28)
- added a FUTURE/firefox-release-53.0.1.json but we skipped that version


