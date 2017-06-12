# Beta: Firefox 54.0b4

### Started: 2017-05-01

## Build 1

### Beta Graph
[task group](https://tools.taskcluster.net/push-inspector/#/hK6cgcAkQgaqDH3PB9MGNw)


#### Status
- [x] [submit to Shipit](https://wiki.mozilla.org/Release:Release_Automation_on_Mercurial:Starting_a_Release#Submit_to_Ship_It)
- [x] [emailed beta-cdntest](../how-tos/relpro.md#1-email-drivers-re-release-live-on-test-channel)
- [x] [published release tasks](../how-tos/relpro.md#3-publish-release)
- [x] Update "Firefoxsignoff" rule in Balrog

### Issues
- Error stashed as MAR in 54.0b4 for te locale in Mac updates makes final verification fail - [Bug 1361255](https://bugzil.la/1361255). Eventually removed partial mar for that specific 54.0b3->54.0b4 update so that Mac users on te locale will get a complete mar instead of a partial mar.


