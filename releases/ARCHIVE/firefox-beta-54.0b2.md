# Beta: Firefox 54.0b2

### Started: 2017-04-24

## Build 1

### Beta Graph
[task group](https://tools.taskcluster.net/push-inspector/#/ig9LC1C4RuiY98vEazrXgQ)


#### Status
- [x] [submit to Shipit](https://wiki.mozilla.org/Release:Release_Automation_on_Mercurial:Starting_a_Release#Submit_to_Ship_It)
- [x] [emailed beta-cdntest](../how-tos/relpro.md#1-email-drivers-re-release-live-on-test-channel)
- [x] [published release tasks](../how-tos/relpro.md#3-publish-release)
- [x] Update "Firefoxsignoff" rule in Balrog

### Issues
- SPECIAL REQUIREMENT: [Bug 1358177](https://bugzil.la/1358177) - Firefox 54.0b2: 'my' locale submit complete MAR metadata to balrog
- Ship-it submission failed due to 'Retrying because of: 503 Server Error: Service Unavailable' with 12 attemps. Graph eventually submitted but reported as failed in Ship-it UI
- A 10-tasks bunch stalled for 2-3h for some reason. 4 beetmover jobs and 6 funsize jobs (signing, publishing and update generators. Canceled all of them and reran them
- bbb lag in marking shipped?


