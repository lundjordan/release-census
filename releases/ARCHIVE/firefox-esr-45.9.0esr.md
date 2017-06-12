# ESR: Firefox 45.9.0esr

### Started: 2017-04-12

## Build 1

### ESR Graph 1
[task group](https://tools.taskcluster.net/push-inspector/#/rm5NvTZgStiq7dKHTbCvTg)

#### Status
- [x] [submit to Shipit](https://wiki.mozilla.org/Release:Release_Automation_on_Mercurial:Starting_a_Release#Submit_to_Ship_It)

### ESR Graph 2
task graph url: unknown

#### Status
- [ ] [emailed esr-localtest](../how-tos/relpro.md#1-email-drivers-re-release-live-on-test-channel)
- [ ] [pushed to mirrors/releases](../how-tos/relpro.md#2-push-to-releases-dir-mirrors)
- [ ] [published release tasks](../how-tos/relpro.md#3-publish-release)

### Issues
- releasetasks needs to be on the esr45 branch (on bm85) otherwise the release graph is too recent. We also need to backport the unified repo patch on that branch. Build1 aborted 

:bomb: _aborted release. starting new build num_ :bomb:

## Build 2

### ESR Graph 1
[task group](https://tools.taskcluster.net/push-inspector/#/3z_e5XQGTcGyOqLQFi5-UQ)

#### Status
- [x] [submit to Shipit](https://wiki.mozilla.org/Release:Release_Automation_on_Mercurial:Starting_a_Release#Submit_to_Ship_It)

### ESR Graph 2
task graph url: unknown

#### Status
- [ ] [emailed esr-localtest](../how-tos/relpro.md#1-email-drivers-re-release-live-on-test-channel)
- [ ] [pushed to mirrors/releases](../how-tos/relpro.md#2-push-to-releases-dir-mirrors)
- [ ] [published release tasks](../how-tos/relpro.md#3-publish-release)

### Issues
- Cannot clone the unified repo with the hg client included in taskcluster/image)builder:0.1.3. Created a new image docker with hg 4.1.1. Build2 aborted 

:bomb: _aborted release. starting new build num_ :bomb:

## Build 3

### ESR Graph 1
[task group](https://tools.taskcluster.net/push-inspector/#/CIxM8m3cTXieaAiCFP0PXw)

#### Status
- [x] [submit to Shipit](https://wiki.mozilla.org/Release:Release_Automation_on_Mercurial:Starting_a_Release#Submit_to_Ship_It)

### ESR Graph 2
[task group](https://tools.taskcluster.net/push-inspector/#/5-A6yeP6QOqH38DlEHcQbg)

#### Status
- [x] [emailed esr-localtest](../how-tos/relpro.md#1-email-drivers-re-release-live-on-test-channel)
- [x] [pushed to mirrors/releases](../how-tos/relpro.md#2-push-to-releases-dir-mirrors)
- [x] [published release tasks](../how-tos/relpro.md#3-publish-release)

### Issues
- none


