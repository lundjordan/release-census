# ESR: Firefox 52.1.2esr

### Started: 2017-05-17

## Build 1

### ESR Graph 1
[task group](https://tools.taskcluster.net/push-inspector/#/RqgTdxaXS6S3wg9jACFxPw)

#### Status
- [x] [submit to Shipit](https://wiki.mozilla.org/Release:Release_Automation_on_Mercurial:Starting_a_Release#Submit_to_Ship_It)

### ESR Graph 2
task graph url: unknown

#### Status
- [x] [pushed to mirrors/releases](../how-tos/relpro.md#2-push-to-releases-dir-mirrors)
- [x] [published release tasks](../how-tos/relpro.md#3-publish-release)

### Issues
- hit 'Sanity checks failed. Errors: list indices must be integers, not str' on shipit - fallout from https://hg.mozilla.org/build/tools/rev/8a9951b2888c ?
- [Bug 1366293](https://bugzil.la/1366293) - version bump failing, most likely due to relbranch side effect.


