for releases that have not started yet but require special instructions or reminders, create a json file with the release name as the file name. The file should be a list of 'issues'.


valid filename format (note this is the same format the releasewarrior uses for creating and updating current releases):

* format:
  * $product-$branch-$version.json
* examples:
    * firefox-beta-49.0b1.json
    * firefox-release-rc-48.0.json
    * firefox-release-48.0.1.json
    * firefox-esr-45.3.0esr.md
    * firefox-esr-52.3.0esr.json
    * thunderbird-beta-48.0b1.json
    * fennec-release-48.0.json

valid json format:

```json
{
    "issues": [
        "add a balrog rule to force users to downgrade to firefox 3.0 for funz",
        "drink whiskey after we ship"
    ]
}
```

This works via the following logic:

When a release is created by release warrior, e.g. `release create firefox beta 49.0b1`, warrior will first poll the releases/FUTURE/ dir and look for a matching json file, e.g. `firefox-beta-49.0b1.json`.
If found, the issues will be combined with the standard template as a 'one off' to create the releases/$release.json file and the relaeses/FUTURE/$release.json file is removed. The net benefit here is that we don't:

1. pollute the releases/ dir with future releases
2. give misleading start dates for releases
3. not risk pre-defining md and json files for upcoming releases that deviate from template equivalents that have since then changed

