import os
import json
import logging
import re
import sys

from releasewarrior.config import ARCHIVED_RELEASES_PATH, ORDERED_HUMAN_TASKS, RELEASES_PATH

logger = logging.getLogger('releasewarrior')

BUG_RE = r'(?<!\[)\b[bB][uU][gG]\s*(\d+)(?!\]\(http)\b'  # Don't match already linked bugs
BUG_REPLACE = r'[Bug \1](https://bugzil.la/\1)'


def get_current_releases():
    current_releases = {}
    for root, dirs, files in os.walk(RELEASES_PATH):
        for f in [data_file for data_file in files if data_file.endswith(".json")]:
            abs_f = os.path.join(RELEASES_PATH, f)
            if os.path.exists(abs_f):
                with open(abs_f) as data_f:
                    data = json.load(data_f)
                    current_releases[abs_f] = data
    return current_releases


def get_complete_releases():
    logger.info("getting complete releases")
    completed_releases = {}
    for abs_release_file, release_data in get_current_releases().items():
        if all(release_data["builds"][-1]["human_tasks"].values()):
            # this release is complete!
            completed_releases[abs_release_file] = release_data
    return completed_releases


def get_incomplete_releases():
    logger.info("getting incomplete releases")
    incomplete_releases = {}
    for abs_release_file, release_data in get_current_releases().items():
        if not all(release_data["builds"][-1]["human_tasks"].values()):
            # this release is complete!
            incomplete_releases[abs_release_file] = release_data
    return incomplete_releases


def ensure_branch_and_version_are_valid(branch, version):
    mismatch = False
    if branch == 'beta' and 'b' not in version:
        logger.error("beta specified but 'b' not found in version.")
        mismatch = True
    if branch == 'devedition' and 'b' not in version:
        logger.error("devedition specified but 'b' not found in version.")
        mismatch = True
    elif branch in ['release', 'release-rc']:
        if re.search('[a-zA-Z]', version):
            logger.error("%s specified but an alpha char was found in version", branch)
            mismatch = True
        elif branch == 'release-rc' and version.count('.') != 1:
            logger.error("release specified but version does not have 1 dot in it.")
            mismatch = True
    elif branch == 'esr' and 'esr' not in version:
        logger.error("esr specified but 'esr' not found in version.")
        mismatch = True
    if mismatch:
        logger.error("Was there a mistake?")
        sys.exit(1)


def _get_checkbox_value(nick, args):
    if args.checkboxes and nick in args.checkboxes:
        return (nick, True)
    return (nick, False)


def get_update_data(args):
    build_data = [
        ("graphid", args.graphid),
        ("graphid_2", args.graphid_2),
        ("aborted", args.aborted),
        ("issues", args.issues),
    ]
    human_tasks_data = [_get_checkbox_value(x, args) for x in ORDERED_HUMAN_TASKS]
    update_data = {"human_tasks": {}}
    for key, value in build_data:
        if value:
            update_data[key] = value
    for key, value in human_tasks_data:
        if value:
            update_data["human_tasks"][key] = value
    return update_data


def data_unchanged(new_data, current_data):
    # TODO - make this more generic and elegant
    for index in range(0, len(new_data['builds'])):
        for new_data_key, new_data_value in new_data["builds"][index].items():
            current_data_value = current_data["builds"][index][new_data_key]
            # look for unique issue lists
            if new_data_key == "issues":
                if list(set(new_data_value) - set(current_data_value)):
                    return False
            elif new_data_key == "human_tasks":
                for task_key, task_value in new_data["builds"][index]["human_tasks"].items():
                    current_task_value = current_data["builds"][index]["human_tasks"][task_key]
                    if task_value != current_task_value:
                        return False
            # look for unique data strings
            elif new_data_value != current_data_value:
                return False
    return True


def release_exists(data_file, ignore_archive=False):
    searchpaths = [RELEASES_PATH] if ignore_archive else [RELEASES_PATH, ARCHIVED_RELEASES_PATH]
    data_exists = False

    def exists_in_searchpaths(target):
        for searchpath in searchpaths:
            if os.path.exists(os.path.join(searchpath, target)):
                return True
        return False

    if exists_in_searchpaths(data_file):
        data_exists = True

    return data_exists


def get_remaining_tasks_ordered(release_human_tasks):
    # TODO - human_tasks is a dict so we lose order. find a better way to put back in order
    # this is a hack because ORDERED_HUMAN_TASKS is hardcoded and may get out of date
    remaining_tasks = [task for task, done in release_human_tasks.items() if not done]
    return [ordered_task for ordered_task in ORDERED_HUMAN_TASKS if ordered_task in remaining_tasks]


def convert_bugs_to_links(arr_of_strings):
    """ This function linkifies Bug entries in issue lists for formatting into
        markdown format.
    """
    new_data = []
    for item in arr_of_strings:
        new_data.append(re.sub(BUG_RE, BUG_REPLACE, item))
    return new_data
