# Welcome to releaseduty Day1 checklist and FAQ section!

## Intro
If you're reading this page it means that you're ramping up as an official releaseduty squirrel within Mozilla Releng, so please allow us to give you a warm welcome!

Releaseduty is a designated pass-the-token role that we assign every 6 weeks to members of the team. Role mainly entails handling all the coordination and communication with other teams (such as QE, RelMan, etc) as well as doing all the
mechanics to make sure the release workflow is as smooth as possible. While this role can get quite disruptive at times, we prefer this approach of delegating this responsability to a small set of people that can own this, while we shield the others from interruptions so that they can better focus
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
- [TB release drivers mailing list](thunderbird-drivers@mozilla.org)
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

## FAQ


