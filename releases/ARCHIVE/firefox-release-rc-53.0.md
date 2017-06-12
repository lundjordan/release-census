# RC Release: Firefox 53.0

### Started: 2017-04-10

## Build 1

### RC graph 1
[task group](https://tools.taskcluster.net/push-inspector/#/p6Q9UsUrS9eSv1s4z0Cg3A)

#### Status
- [x] [submit to Shipit](https://wiki.mozilla.org/Release:Release_Automation_on_Mercurial:Starting_a_Release#Submit_to_Ship_It)
- [ ] [emailed beta-cdntest](../how-tos/relpro.md#1-email-drivers-re-release-live-on-test-channel)
- [ ] [publish in Balrog on Beta channel](../how-tos/relpro.md#3-publish-release)

### RC graph 2
task graph url: unknown

#### Status
- [ ] [pushed to mirrors/releases](../how-tos/relpro.md#2-push-to-releases-dir-mirrors)
- [ ] [published release tasks](../how-tos/relpro.md#3-publish-release)

### Issues
- SPECIAL REQUIREMENT: [Bug 1354115](https://bugzil.la/1354115) - remove special WebSense rules for non-blacklisted and unknown WebSense users
- [Bug 1318919](https://bugzil.la/1318919) - we forgot we had to update m-r for tc linux
- docker image hg clone timeouts https://github.com/mozilla/releasetasks/pull/229
- [Bug 1355404](https://bugzil.la/1355404) busted linux hg clones again for l10n

:bomb: _aborted release. starting new build num_ :bomb:

## Build 2

### RC graph 1
task graph url: unknown

#### Status
- [ ] [submit to Shipit](https://wiki.mozilla.org/Release:Release_Automation_on_Mercurial:Starting_a_Release#Submit_to_Ship_It)
- [ ] [emailed beta-cdntest](../how-tos/relpro.md#1-email-drivers-re-release-live-on-test-channel)
- [ ] [publish in Balrog on Beta channel](../how-tos/relpro.md#3-publish-release)

### RC graph 2
task graph url: unknown

#### Status
- [ ] [pushed to mirrors/releases](../how-tos/relpro.md#2-push-to-releases-dir-mirrors)
- [ ] [published release tasks](../how-tos/relpro.md#3-publish-release)

### Issues
- releaserunner did not pick the latest changes of releasetasks. cancelled the build

:bomb: _aborted release. starting new build num_ :bomb:

## Build 3

### RC graph 1
[task group](https://tools.taskcluster.net/push-inspector/#/thD9fmrUQv6ECT7eY_xNtQ)

#### Status
- [x] [submit to Shipit](https://wiki.mozilla.org/Release:Release_Automation_on_Mercurial:Starting_a_Release#Submit_to_Ship_It)
- [x] [emailed beta-cdntest](../how-tos/relpro.md#1-email-drivers-re-release-live-on-test-channel)
- [x] [publish in Balrog on Beta channel](../how-tos/relpro.md#3-publish-release)

### RC graph 2
task graph url: unknown

#### Status
- [ ] [pushed to mirrors/releases](../how-tos/relpro.md#2-push-to-releases-dir-mirrors)
- [ ] [published release tasks](../how-tos/relpro.md#3-publish-release)

### Issues
- Even with newer docker images and unified repo, docker images generation is flake https://tools.taskcluster.net/task-inspector/\#JS5zL2rkRi2jkj2ZofoROQ/1 

:bomb: _aborted release. starting new build num_ :bomb:

## Build 4

### RC graph 1
[task group](https://tools.taskcluster.net/push-inspector/#/z_-Tl0p4Rxu6eV3whAlKrw)

#### Status
- [x] [submit to Shipit](https://wiki.mozilla.org/Release:Release_Automation_on_Mercurial:Starting_a_Release#Submit_to_Ship_It)
- [ ] [emailed beta-cdntest](../how-tos/relpro.md#1-email-drivers-re-release-live-on-test-channel)
- [ ] [publish in Balrog on Beta channel](../how-tos/relpro.md#3-publish-release)

### RC graph 2
task graph url: unknown

#### Status
- [ ] [pushed to mirrors/releases](../how-tos/relpro.md#2-push-to-releases-dir-mirrors)
- [ ] [published release tasks](../how-tos/relpro.md#3-publish-release)

### Issues
- Busted releaserunner -- broken docker image creation due to esr45 branch releasetasks

:bomb: _aborted release. starting new build num_ :bomb:

## Build 5

### RC graph 1
[task group](https://tools.taskcluster.net/push-inspector/#/3K7wkmRLSG6MsRZnrFYq6Q)

#### Status
- [x] [submit to Shipit](https://wiki.mozilla.org/Release:Release_Automation_on_Mercurial:Starting_a_Release#Submit_to_Ship_It)
- [x] [emailed beta-cdntest](../how-tos/relpro.md#1-email-drivers-re-release-live-on-test-channel)
- [x] [publish in Balrog on Beta channel](../how-tos/relpro.md#3-publish-release)

### RC graph 2
task graph url: unknown

#### Status
- [ ] [pushed to mirrors/releases](../how-tos/relpro.md#2-push-to-releases-dir-mirrors)
- [ ] [published release tasks](../how-tos/relpro.md#3-publish-release)

### Issues
- none

:bomb: _aborted release. starting new build num_ :bomb:

## Build 6

### RC graph 1
[task group](https://tools.taskcluster.net/push-inspector/#/dMnCiwCrRqucv7DS-bPOqQ)

#### Status
- [x] [submit to Shipit](https://wiki.mozilla.org/Release:Release_Automation_on_Mercurial:Starting_a_Release#Submit_to_Ship_It)
- [x] [emailed beta-cdntest](../how-tos/relpro.md#1-email-drivers-re-release-live-on-test-channel)
- [x] [publish in Balrog on Beta channel](../how-tos/relpro.md#3-publish-release)

### RC graph 2
[task group](https://tools.taskcluster.net/push-inspector/#/FH3KauqaRfuuAkelDT6Cow)

#### Status
- [x] [pushed to mirrors/releases](../how-tos/relpro.md#2-push-to-releases-dir-mirrors)
- [x] [published release tasks](../how-tos/relpro.md#3-publish-release)

### Issues
- [Bug 1357548](https://bugzil.la/1357548) - we need to get rid of opt-linux64 in releasetasks
- F31UZeLQT7q4viqBpvQpuw was complete without push to mirrors - human error? [jlorenzo] Yes, sorry about that :(
- pending uptake monitoring https://github.com/mozilla-releng/build-cloud-tools/pull/288
- SPECIAL REQUIREMENT: [Bug 1354736](https://bugzil.la/1354736) - Setup WNP for Firefox 53.0 release
- bbb out of sync - tasks ran but stayed pending. saw green in https://secure.pub.build.mozilla.org/buildapi/self-serve/mozilla-release
- no reminder about 25% throttling + 0% scheduled update; https://github.com/mozilla/releasewarrior/pull/72
- fallback mapping steps https://github.com/mozilla/releasewarrior/pull/73
- wnp - not doc'ed?


