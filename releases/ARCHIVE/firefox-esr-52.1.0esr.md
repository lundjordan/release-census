# ESR: Firefox 52.1.0esr

### Started: 2017-04-10

## Build 1

### ESR Graph 1
[task group](https://tools.taskcluster.net/push-inspector/#/Qy7Ali2QRAOMRlvybn6G8Q)

#### Status
- [x] [submit to Shipit](https://wiki.mozilla.org/Release:Release_Automation_on_Mercurial:Starting_a_Release#Submit_to_Ship_It)

### ESR Graph 2
task graph url: unknown

#### Status
- [x] [emailed esr-localtest](../how-tos/relpro.md#1-email-drivers-re-release-live-on-test-channel)
- [ ] [pushed to mirrors/releases](../how-tos/relpro.md#2-push-to-releases-dir-mirrors)
- [ ] [published release tasks](../how-tos/relpro.md#3-publish-release)

### Issues
- [Bug 1355305](https://bugzil.la/1355305) - source tarball task missing tc-vcs tarball
- hung windows l10n jobs -- cancelled&reran

:bomb: _aborted release. starting new build num_ :bomb:

## Build 2

### ESR Graph 1
task graph url: unknown

#### Status
- [x] [submit to Shipit](https://wiki.mozilla.org/Release:Release_Automation_on_Mercurial:Starting_a_Release#Submit_to_Ship_It)

### ESR Graph 2
task graph url: unknown

#### Status
- [x] [emailed esr-localtest](../how-tos/relpro.md#1-email-drivers-re-release-live-on-test-channel)
- [ ] [pushed to mirrors/releases](../how-tos/relpro.md#2-push-to-releases-dir-mirrors)
- [ ] [published release tasks](../how-tos/relpro.md#3-publish-release)

### Issues
- Just like build 1, some l10n repacks are falsely stuck in pending. Cancelled the jobs. However, win32 l10n repack 3/12 was really stuck => cancelled and rerun

:bomb: _aborted release. starting new build num_ :bomb:

## Build 3

### ESR Graph 1
[task group](https://tools.taskcluster.net/push-inspector/#/LPXWQp_1TMqtKr8a5k6-Aw)

#### Status
- [x] [submit to Shipit](https://wiki.mozilla.org/Release:Release_Automation_on_Mercurial:Starting_a_Release#Submit_to_Ship_It)

### ESR Graph 2
task graph url: unknown

#### Status
- [x] [emailed esr-localtest](../how-tos/relpro.md#1-email-drivers-re-release-live-on-test-channel)
- [x] [pushed to mirrors/releases](../how-tos/relpro.md#2-push-to-releases-dir-mirrors)
- [x] [published release tasks](../how-tos/relpro.md#3-publish-release)

### Issues
- none


