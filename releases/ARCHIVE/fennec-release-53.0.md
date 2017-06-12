# Fennec 53.0

### Started 2017-04-12

## Build 1

### Release Graph
[task group](https://tools.taskcluster.net/push-inspector/#/gc6UVbqRQjW75dwe8tTCrA)

### Release graph 2
[task group](https://tools.taskcluster.net/push-inspector/#/RIu_mZG9RdmPr1QQ8MUB1w)

### Status
- [x] [submit to Shipit](https://wiki.mozilla.org/Release:Release_Automation_on_Mercurial:Starting_a_Release#Submit_to_Ship_It)
- [x] [manually kick off graph](https://github.com/mozilla/releasewarrior/blob/master/how-tos/fennec-temp-relpro.md#start-off-the-fennec-graph)
- [x] emailed release-localtest
- [x] [run pushapk](https://github.com/mozilla/releasewarrior/blob/master/how-tos/fennec-temp-relpro.md#run-pushapk-manually)
- [x] [push to mirrors and publish release](https://github.com/mozilla/releasewarrior/blob/master/how-tos/fennec-temp-relpro.md#steps-after-qa-signed-off)

### Issues
- SPECIAL REQUIREMENT: After the dry-run task passed, do [bug 1354038](https://bugzil.la/1354038)
- [bug 1355342](https://bugzil.la/1355342) - Busted releaserunner -- Failed CalledProcessError
- we didn't uplift all locales. aki landed [some fixes](https://hg.mozilla.org/build/braindump/log/default/releases-related/beta2release_l10n.sh) and doc updates; we should retry the l10n repacks after
- [Bug 1357288](https://bugzil.la/1357288) - updates are turned off on tc fennec
- Accidentally pushed to 100% instead of rolling out to 10. Fixed in [Bug 1354038](https://bugzil.la/1354038)


