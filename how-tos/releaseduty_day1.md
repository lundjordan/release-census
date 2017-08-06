# Welcome to releaseduty Day1 checklist and FAQ section!

## Intro
If you're reading this page it means that you're ramping up as an official releaseduty squirrel within Mozilla RelEng, so please allow us to give you a warm welcome!

Releaseduty is a designated pass-the-token role that we assign every 6 weeks to members of the team. Role mainly entails handling all the coordination and communication with other teams (such as QE, RelMan, etc) as well as doing all the
mechanics to make sure the release work flow is as smooth as possible. While this role can get quite disruptive at times, we prefer this approach of delegating this responsibility to a small set of people that can own this, while we shield the others from interruptions so that they can better focus
on improving our automation and work on other RelEng infra-related projects.

Being releaseduty means a couple of things:
- handle communication/coordination with other teams
- handle all incoming releases
- fix and debug any potential errors that might have slipped in the automation
- develop and continuously improve the Release Automation process

## Communication

In order to do an awesome squirrel job, you need to pay attention do a few communication channels. Some of them are quite spammy so please ensure you're enabling good email filters.
Most of the steps/large milestones of a release are happening via email. Rest of debugging, communication and coordination takes place in a few IRC channels. The automation status is collected mostly on email.
Therefore, you ought to be present and pay attention to conversations happening in:
- **_#releaseduty_** (main RelEng dedicated communication channel for releaseduty)
- **_#release-drivers_** (where QE and RelMan usually coordinate, good to pay attention do this as well)
- **_#tbdrivers_** (where TB drivers discuss Thunderbird releases)
- **_#release-notifications_** (very spammy channel where all release automation notifications are being sent)
- **_#release-notifications-dev_** (spammy channel where all staging releases notifications are being sent)
- **_#releng_** (public RelEng channel where many non-releaseduty topics are also discussed)
- **_#relman_** (optional - about to be retired soon, where RelMan hangs out around usually)

Moreover, you need these mailing list subscriptions:
- [release-automation-notifications](https://groups.google.com/a/mozilla.com/forum/?hl=en#!forum/release-automation-notifications)
- [release-automation-notifications-dev](https://groups.google.com/a/mozilla.com/forum/#!forum/release-automation-notifications-dev)
- [releng internal mailing list](release@mozilla.com)
- [release drivers mailing list](release-drivers@mozilla.org)
- [thunderbird release drivers mailing list](thunderbird-drivers@mozilla.org)
- [release-automation-notifications-thunderbird](https://mail.mozilla.org/listinfo/release-automation-notifications-thunderbird)

Meeting-wise, there is a bunch of meetings to you need to take part as releaseduty-squirrel. To view those meetings in your calendar you need to subscribe/be added to the following calendars:
- **_Public - Release Engineering_** (so that you attend the weekly post-mortem meeting)
- **_Releases Scheduling_** (so that you can attend the Tuesday/Thursday channel meetings)


## Access

Since releaseduty handles releases, several pieces are obviously protected and private with no public access. In order to do your job, you need to be granted access to a bare minimum:
- write access to [releasewarrior](https://github.com/mozilla/releasewarrior/) repo
- r/w access to [Balrog](https://aus4-admin.mozilla.org/)
- read access to [Ship-it](http://ship-it.mozilla.org/)
There are a few more other places where access is needed (such as [bouncer](https://bounceradmin.mozilla.com/admin/), etc) but we're trying to keep those access-list short so addings can be done in time depending on necessities.

## Tools

In order to be productive squirrels, we've developed a bunch of tools to help us out. You may consider these as the bread & butter of the releaseduty squirrels:
- [releasewarrior](https://github.com/mozilla/releasewarrior/) to help us keep track of the releases in flight and generating the post-mortem
- [tasckluster-cli](https://github.com/taskcluster/taskcluster-client.py) to help us deal with TC jobs (rerun/cancel/etc operations)

## Misc

- issues regarding specific releases/WNP are filed under [Release Engineering:Releases](https://bugzilla.mozilla.org/enter_bug.cgi?product=Release%20Engineering&component=Releases)
- issues regarding automation are filed under [Release Engineering:Release Automation](https://bugzilla.mozilla.org/enter_bug.cgi?product=Release%20Engineering&component=Release%20Automation)
- historically, we've used this [etherpad](https://public.etherpad-mozilla.org/p/releaseduty_handoff) to handoff any information from one squirrely to another when cycle. It's optional but feel free to reuse this

## Other useful resources

- More on [Release Management](https://wiki.mozilla.org/Release_Management)

## FAQ

1. *How does the Ship-it work flow work in terms of shipping a new release?*

RelMan submits a new release form [here](https://ship-it.mozilla.org/), another RelMan reviews that and once it hits 'Ready' + 'Do eeaat' the release enters the 'Reviewed' section and waits to be run.
Since there's a `release-runner.sh` script running in a loop on [bm81](https://hg.mozilla.org/build/puppet/file/default/manifests/moco-nodes.pp#l598), there's a max windows of 60 seconds till the job gets its share, following which it enters the 'Running/Complete' table where we can observe its state.
The "Reviewed" tab goes to "No pending release" yet again.

2. *What does release-promotion refer to?*

'release promotion' is simply the idea that we take an already existing CI build from (e.g. beta) and promote that to being the build we release/ship to users. Prior to this approach, we had always rebuilt Firefox at the start of each new release.
Long story short, release promotion entails taking an existing set of builds that have already been triggered and passed QA and “promoting” them to be used as a release candidate. More on promotion can be found in our wiki [here](https://wiki.mozilla.org/ReleaseEngineering/Release_build_promotion)

3. *What is the train model?*

Since 2012 Mozilla moved to a fixed-schedule release model, otherwise known as the Train Model, in which we released Firefox every six weeks to get features and updates to users faster and move at the speed of the Web. Hence, every six weeks the following merges take place:
[mozilla-beta](http://hg.mozilla.org/releases/mozilla-beta/) => [mozilla-release](http://hg.mozilla.org/releases/mozilla-release/)
[mozilla-central](http://hg.mozilla.org/mozilla-central/) => [mozilla-beta](http://hg.mozilla.org/releases/mozilla-beta/)

We used to have an intermmediate branch, aurora, in between central and beta but that was brought to end-of-life during April-May 2017.

4. *What is a partner repack change for FF?*

Partner repacks refer to 3rd party customized branded versions of Firefox that Mozilla is taking care of for some of its clients. With some exceptions, most of the partner reconfigs lie under private repositories.
Mostly, the partner repacks don't need too much of RelEng interference as all bits are held under private git repos and are directly handled by the partnering companies

5. *Is there calendar-based release scheduled for Thunderbird as for Firefox?*

No. It's irregular. Conversations happen on #tbdrivers and TB mailing list and they trigger their release in Ship-it.

6. *Why don't I see update_verify_beta for dot releases?*

From time to time, a handful of issues precipitate a dot release. When that happens, its behavior slightly varies from a normal release. A normal release (e.g. 43.0, 44.0, etc) has its RC shipped to beta channel first before making it to release
channel - for testing purposes, update verify steps are taking place both ways, hence update_verify_release and update_verify_beta steps. Upon successful testing we ship the RC on the beta channel and then on the release channel,
following which we merge the code for the next release cycle so that the beta release bumps its version. In the lights of this logic, a dot release (e.g. 43.0.1 or 44.0.1) happens a certain amount of time after the official release.
For that reason, a dot release can't be tested in beta channel as the at-that-moment beta version is greater than the dot release version, hence the updater would refuse to downgrade. Therefore, there is only one cycle of update_verify for dot releases (update_verify_release == update_verify in this case).
