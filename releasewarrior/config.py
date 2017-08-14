import os

SEARCH_PATH = (
    os.path.abspath(os.path.join(os.path.realpath(__file__), '..', '..')),
    os.getcwd(),
)


def find_repo_path(search_path):
    for path in search_path:
        if os.path.exists(os.path.join(path, '.git')):
            with open(os.path.join(path, '.git', 'config')) as fh:
                if 'mozilla/releasewarrior' in fh.read():
                    return path
    else:
        raise Exception("Can't find releasewarrior.git in {}!".format(search_path))


REPO_PATH = find_repo_path(SEARCH_PATH)  # abs path to dir that contains .git
TEMPLATES_PATH = os.path.join(REPO_PATH, 'templates')
RELEASES_PATH = os.path.join(REPO_PATH, 'releases')
FUTURE_RELEASES_PATH = os.path.join(REPO_PATH, 'releases', 'FUTURE')
ARCHIVED_RELEASES_PATH = os.path.join(REPO_PATH, 'releases', 'ARCHIVE')
POSTMORTEMS_PATH = os.path.join(REPO_PATH, 'releases', 'POSTMORTEMS')
LOG_PATH = os.path.join(REPO_PATH, 'logs')


WIKI_TEMPLATES = {
    'firefox': {
        'beta': os.path.join(TEMPLATES_PATH, 'firefox_beta.md.tmpl'),
        'release': os.path.join(TEMPLATES_PATH, 'firefox_release.md.tmpl'),
        'release-rc': os.path.join(TEMPLATES_PATH, 'firefox_release-rc.md.tmpl'),
        'esr': os.path.join(TEMPLATES_PATH, 'firefox_esr.md.tmpl'),
    },
    'devedition': {
        'devedition': os.path.join(TEMPLATES_PATH, 'devedition.md.tmpl'),
    },
    'fennec': {
        'beta': os.path.join(TEMPLATES_PATH, 'fennec_beta.md.tmpl'),
        'release': os.path.join(TEMPLATES_PATH, 'fennec_release.md.tmpl'),
        'esr': os.path.join(TEMPLATES_PATH, 'fennec_esr.md.tmpl'),
    },
    'thunderbird': {
        'beta': os.path.join(TEMPLATES_PATH, 'thunderbird_beta.md.tmpl'),
        'release': os.path.join(TEMPLATES_PATH, 'thunderbird_release.md.tmpl'),
        'esr': os.path.join(TEMPLATES_PATH, 'thunderbird_esr.md.tmpl'),
    },
    "postmortem": os.path.join(TEMPLATES_PATH, 'postmortem.md.tmpl')
}

DATA_TEMPLATES = {
    'firefox': {
        'beta': os.path.join(TEMPLATES_PATH, 'firefox_beta.json.tmpl'),
        'release': os.path.join(TEMPLATES_PATH, 'firefox_release.json.tmpl'),
        'release-rc': os.path.join(TEMPLATES_PATH, 'firefox_release-rc.json.tmpl'),
        'esr': os.path.join(TEMPLATES_PATH, 'firefox_esr.json.tmpl'),
    },
    'devedition': {
        'devedition': os.path.join(TEMPLATES_PATH, 'devedition.json.tmpl'),
    },
    'fennec': {
        'beta': os.path.join(TEMPLATES_PATH, 'fennec_beta.json.tmpl'),
        'release': os.path.join(TEMPLATES_PATH, 'fennec_release.json.tmpl'),
        'esr': os.path.join(TEMPLATES_PATH, 'fennec_esr.json.tmpl'),
    },
    'thunderbird': {
        'beta': os.path.join(TEMPLATES_PATH, 'thunderbird_beta.json.tmpl'),
        'release': os.path.join(TEMPLATES_PATH, 'thunderbird_release.json.tmpl'),
        'esr': os.path.join(TEMPLATES_PATH, 'thunderbird_esr.json.tmpl'),
    }
}


# The official json nick, followed by human-friendly alias(es)
# These should be specified in order.
ORDERED_HUMAN_TASKS = (
    'shipit',
    'graph',
    'localtest',
    'beta',
    'betasignoff',
    'wnp',
    'mirrors',
    'pushapk',
    'publish',
    'signoff',
)
