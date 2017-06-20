import abc
import os
import sys
import logging
import json
import datetime
import re
import getpass
from copy import deepcopy

from git import Repo
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from releasewarrior.helpers import ensure_branch_and_version_are_valid, release_exists
from releasewarrior.helpers import get_remaining_tasks_ordered
from releasewarrior.helpers import get_update_data, data_unchanged, get_complete_releases
from releasewarrior.helpers import get_incomplete_releases
from releasewarrior.helpers import convert_bugs_to_links
from releasewarrior.config import REPO_PATH, RELEASES_PATH, TEMPLATES_PATH, ARCHIVED_RELEASES_PATH, \
    FUTURE_RELEASES_PATH
from releasewarrior.config import DATA_TEMPLATES, WIKI_TEMPLATES, POSTMORTEMS_PATH

logger = logging.getLogger('releasewarrior')

_UPSTREAM_REPO_URL = re.compile(r'((?:https|ssh)://|git@)github\.com[:/]mozilla/releasewarrior(\.git)?')
_SIMPLIFIED_REPO_URL = 'github.com/mozilla/releasewarrior' # Used only to simplify what's logged out

class Command(metaclass=abc.ABCMeta):
    repo = Repo(REPO_PATH)
    product = None
    branch = None
    version = None
    abs_data_file = None
    abs_wiki_file = None
    wiki_template_file = None
    commit_msg = None
    save_data_file = True  # sync doesn't touch data file
    summary = []

    def pre_run_check(self):
        """ensures repo is clean and local repo is in sync with remote origin"""

        if self.repo.is_dirty():
            logger.warning("releasewarrior repo dirty")

        upstream = self._find_upstream_repo()
        logger.info('fetching new csets from {}/master'.format(upstream))

        # TODO - we should allow csets to exist locally that are not on remote.
        logger.info("ensuring releasewarrior repo is up to date and in sync with {}".format(upstream))

        upstream.fetch()
        commits_behind = list(self.repo.iter_commits('master..{}/master'.format(upstream)))
        if commits_behind:
            logger.error('local master is behind {}/master. aborting run to be safe.'.format(upstream))
            sys.exit(1)

        # making sure release directories exist
        for directory in [RELEASES_PATH, ARCHIVED_RELEASES_PATH, POSTMORTEMS_PATH]:
            if not os.path.exists(directory):
                os.makedirs(directory)

    def _find_upstream_repo(self):
        upstream_repos = [
            repo for repo in self.repo.remotes if _UPSTREAM_REPO_URL.match(repo.url) is not None
        ]
        number_of_repos_found = len(upstream_repos)
        if number_of_repos_found == 0:
            raise Exception('No remote repository pointed to "{}" found!'.format(_SIMPLIFIED_REPO_URL))
        elif number_of_repos_found > 1:
            raise Exception('More than one repository is pointed to "{}". Found repos: {}'.format(_SIMPLIFIED_REPO_URL, upstream_repos))

        correct_repo = upstream_repos[0]
        logger.debug('{} is detected as being the remote repository pointed to "{}"'.format(correct_repo, _SIMPLIFIED_REPO_URL))
        return correct_repo


    @abc.abstractmethod
    def generate_data(self):
        """generates data file based on command arguments"""

    def generate_wiki(self, data, wiki_template):
        """generates wiki file based on data file and wiki template"""
        env = Environment(loader=FileSystemLoader(TEMPLATES_PATH),
                          undefined=StrictUndefined, trim_blocks=True)
        for b in data.get('builds', []):
            b['issues'] = convert_bugs_to_links(b['issues'])
        template = env.get_template(wiki_template)
        return template.render(**data)

    def run(self):
        """run sub command"""
        data = self.generate_data()
        wiki = self.generate_wiki(data, os.path.basename(self.wiki_template_file))

        if self.save_data_file:
            # save data to actual data_path
            logger.info("writing to data file: %s", self.abs_data_file)
            with open(self.abs_data_file, 'w') as data_file:
                json.dump(data, data_file, indent=4, sort_keys=True)

        # save wiki to actual wiki_path
        logger.info("writing to wiki file: %s", self.abs_wiki_file)
        with open(self.abs_wiki_file, 'w') as wp:
            wp.write(wiki)

    def add_and_commit(self, files, msg):
        self.repo.index.add(files)

        if not self.repo.index.diff("HEAD"):
            logger.warning("nothing staged for commit. has the data or wiki file changed?")
            sys.exit(1)

        logger.info("committing changes with message: %s", msg)
        commit = self.repo.index.commit(msg)
        for patch in self.repo.commit("HEAD~1").diff(commit, create_patch=True):
            logger.info(patch)


class CreateRelease(Command):

    def __init__(self, args):
        self.product = args.product
        self.branch = args.branch
        self.version = args.version
        self.abs_data_file = os.path.join(
            RELEASES_PATH, "{}-{}-{}.json".format(self.product, self.branch, self.version)
        )
        self.abs_future_data_file = os.path.join(
            FUTURE_RELEASES_PATH, "{}-{}-{}.json".format(self.product, self.branch, self.version)
        )
        self.abs_wiki_file = os.path.join(
            RELEASES_PATH, "{}-{}-{}.md".format(self.product, self.branch, self.version)
        )
        self.wiki_template_file = WIKI_TEMPLATES[self.product][self.branch]
        self.commit_msg = "started tracking {} {} release. created {} wiki and data file".format(
            self.product, self.version, os.path.basename(self.abs_wiki_file)
        )
        self.pre_run_check()

    def generate_data(self):
        data = {}

        logger.info("grabbing initial data for release from template")
        with open(DATA_TEMPLATES[self.product][self.branch]) as data_template:
            data.update(json.load(data_template))

        logger.info("adding custom initial data: version and date")
        data["version"] = self.version
        data["date"] = datetime.date.today().strftime("%Y-%m-%d")

        if os.path.exists(self.abs_future_data_file):
            logger.info("adding custom initial issues data from FUTURE/ file")
            with open(self.abs_future_data_file) as future_data_file:
                data["builds"][0]["issues"] = json.load(future_data_file)["issues"]

            logger.info("removing FUTURE/ data file: {}".format(self.abs_future_data_file))
            self.repo.index.remove([self.abs_future_data_file])

        return data

    def pre_run_check(self):
        super().pre_run_check()

        ensure_branch_and_version_are_valid(self.branch, self.version)

        if release_exists(os.path.basename(self.abs_data_file)):
            logger.error("release already exists! Ensure %s doesn't exist in %s or %s dirs",
                         os.path.basename(self.abs_data_file), RELEASES_PATH, ARCHIVED_RELEASES_PATH)
            sys.exit(1)

    def run(self):
        super().run()

        self.add_and_commit([self.abs_data_file, self.abs_wiki_file], self.commit_msg)


class UpdateRelease(Command):

    def __init__(self, args):
        self.product = args.product
        self.branch = args.branch
        self.version = args.version
        self.abs_data_file = os.path.join(
            RELEASES_PATH, "{}-{}-{}.json".format(self.product, self.branch, self.version)
        )
        self.abs_wiki_file = os.path.join(
            RELEASES_PATH, "{}-{}-{}.md".format(self.product, self.branch, self.version)
        )
        self.wiki_template_file = WIKI_TEMPLATES[self.product][self.branch]
        self.changes = get_update_data(args)
        self.commit_msg = "updating {} {} release. updated {} wiki".format(
            self.product, self.version, os.path.basename(self.abs_wiki_file)
        )

        self.pre_run_check()

    def generate_data(self):
        new_data = {}
        current_data = {}

        logger.info("grabbing current data about release")
        with open(self.abs_data_file) as current_data_f:
            current_data.update(json.load(current_data_f))
            new_data.update(deepcopy(current_data))

        logger.info("updating with custom update data")
        for key_change, key_value in self.changes.items():
            if key_change == "issues":
                owned_key_value = ["{}: {}".format(getpass.getuser(), k) for k in key_value]
                new_data['builds'][-1]["issues"].extend(owned_key_value)
            elif key_change == "human_tasks":
                new_data['builds'][-1]["human_tasks"].update(key_value)
            else:
                new_data['builds'][-1][key_change] = key_value

        if new_data["builds"][-1]["aborted"]:
            logger.info("most recent buildnum has been aborted, starting a new buildnum")
            template_buildnum_data = {}
            with open(DATA_TEMPLATES[self.product][self.branch]) as data_template:
                template_buildnum_data.update(json.load(data_template)["builds"][0])
            new_data["builds"].append(template_buildnum_data)
            new_data["builds"][-1]["buildnum"] = len(new_data["builds"])

        if data_unchanged(new_data, current_data):
            logger.warning("no changes found in update call after regenerating data file.")
            logger.warning("nothing to commit. aborting.")
            sys.exit(1)

        return new_data

    def pre_run_check(self):
        super().pre_run_check()

        ensure_branch_and_version_are_valid(self.branch, self.version)

        if not release_exists(os.path.basename(self.abs_data_file), ignore_archive=True):
            logger.error("release doesn't exist! Ensure %s exists."
                         "Use the `create` command to create initial data and wiki.",
                         self.abs_data_file)
            sys.exit(1)

    def run(self):
        super().run()
        self.add_and_commit([self.abs_data_file, self.abs_wiki_file], self.commit_msg)


class SyncRelease(Command):

    def __init__(self, args):
        self.product = args.product
        self.branch = args.branch
        self.version = args.version
        self.abs_data_file = os.path.join(
            RELEASES_PATH, "{}-{}-{}.json".format(self.product, self.branch, self.version)
        )
        self.abs_wiki_file = os.path.join(
            RELEASES_PATH, "{}-{}-{}.md".format(self.product, self.branch, self.version)
        )
        self.wiki_template_file = WIKI_TEMPLATES[self.product][self.branch]
        self.commit_msg = "generating wiki for {} {} release with changes in current data file".format(
            self.product, self.version,
        )
        self.save_data_file = False

        self.pre_run_check()

    def generate_data(self):
        current_data = {}

        logger.info("grabbing data for release from current data file")
        with open(self.abs_data_file) as current_data_f:
            current_data.update(json.load(current_data_f))

        return current_data

    def pre_run_check(self):
        super().pre_run_check()

        ensure_branch_and_version_are_valid(self.branch, self.version)

        if not release_exists(os.path.basename(self.abs_data_file), ignore_archive=True):
            logger.error("release doesn't exist! Ensure %s exists."
                         "Use the `create` command to create initial data and wiki.",
                         self.abs_data_file)
            sys.exit(1)

    def run(self):
        super().run()
        self.add_and_commit([self.abs_data_file, self.abs_wiki_file], self.commit_msg)


class Postmortem(Command):

    def __init__(self, args):
        self.date = "{:%Y-%m-%d}".format(args.date)
        self.abs_data_file = os.path.join(POSTMORTEMS_PATH, "{}.json".format(self.date))
        self.abs_wiki_file = os.path.join(POSTMORTEMS_PATH, "{}.md".format(self.date))
        self.wiki_template_file = WIKI_TEMPLATES["postmortem"]
        self.completed_releases = get_complete_releases()
        self.incomplete_releases = get_incomplete_releases()
        self.commit_msg = "updating postmortem. updated {} wiki".format(
            os.path.basename(self.abs_wiki_file)
        )

        self.pre_run_check()

    def generate_data(self):
        new_data = {
            "complete_releases": [],
            "incomplete_releases": [],
            "date": self.date,
        }

        logger.info("grabbing current data about postmortem")
        if os.path.exists(self.abs_data_file):
            with open(self.abs_data_file) as current_data_f:
                new_data.update(deepcopy(json.load(current_data_f)))

        logger.info("updating postmortem with recently completed releases.")
        completed_releases = sorted(self.completed_releases.values(), key=lambda r: r["date"])
        incomplete_releases = sorted(self.incomplete_releases.values(), key=lambda r: r["date"])
        for release in completed_releases + incomplete_releases:
            postmortem_release = {
                "version": release['version'],
                "product": release['product'],
                "date": release['date'],
                "builds": []
            }
            for build in release["builds"]:
                postmortem_release["builds"].append({
                    "buildnum": build["buildnum"],
                    "issues": build["issues"],
                })
            if release in completed_releases:
                new_data["complete_releases"].append(postmortem_release)
            else:
                new_data["incomplete_releases"].append(postmortem_release)

        return new_data

    def pre_run_check(self):
        super().pre_run_check()

        if not self.completed_releases and not self.incomplete_releases:
            logger.error("no current releases found in %s. "
                         "Use the `create` command to create releases; "
                         "use the `update` complete current release's human_tasks.",
                         RELEASES_PATH)
            sys.exit(1)

    def run(self):
        super().run()

        self.archive_completed()
        self.add_and_commit([self.abs_data_file, self.abs_wiki_file], self.commit_msg)

    def archive_completed(self):
        """moves completed releases to archive directory"""
        for abs_data_file in self.completed_releases.keys():
            archive_data_dest = os.path.join(ARCHIVED_RELEASES_PATH, os.path.basename(abs_data_file))
            self.repo.index.move([abs_data_file, archive_data_dest])

            abs_wiki_file = abs_data_file.replace(".json", ".md")
            archive_wiki_dest = os.path.join(ARCHIVED_RELEASES_PATH, os.path.basename(abs_wiki_file))
            self.repo.index.move([abs_wiki_file, archive_wiki_dest])



class Status(Command):

    def __init__(self, args):
        self.pattern = args.pattern
        self.incomplete_releases = get_incomplete_releases()
        self.pre_run_check()

    def pre_run_check(self):
        super().pre_run_check()
        if not self.incomplete_releases:
            logger.info("no current releases in flight")
            sys.exit(1)

    def generate_data(self):
        pass

    def run(self):

        for release in self.incomplete_releases.values():
            if self.pattern:
                if not re.search(
                        self.pattern,
                        "{} {}".format(release["product"], release["version"]),
                        flags=re.IGNORECASE):
                    continue
            remaining_tasks_ordered = get_remaining_tasks_ordered(release["builds"][-1]["human_tasks"])
            curr_build = release["builds"][-1]
            issues = [issue for issue in curr_build["issues"]]

            logger.info("=" * 79)
            logger.info("RELEASE IN FLIGHT: %s %s build%s %s",
                release["product"], release["version"], curr_build["buildnum"],
                release["date"])
            if curr_build.get("graphid"):
                logger.info("Graph: https://tools.taskcluster.net/task-group-inspector/#/%s", curr_build["graphid"])
            if curr_build.get("graphid_2"):
                logger.info("Graph 2: https://tools.taskcluster.net/task-group-inspector/#/%s", curr_build["graphid_2"])
            logger.info("\tincomplete human tasks:")
            for task in remaining_tasks_ordered:
                logger.info("\t\t* %s", task)
            logger.info("\tlatest issues:")
            for issue in issues:
                logger.info("\t\t* %s", issue)
