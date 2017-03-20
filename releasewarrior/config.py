import os

# REPO_PATH == abs path to dir that contains .git
REPO_PATH = os.getcwd()  # overwrite this to use `releaese` commands outside of base repo dir
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
KNOWN_CHECKBOXES = (
    ('submitted_shipit', 'shipit'),
    ('emailed_localtest', 'localtest'),
    ('emailed_cdntest', 'cdntest'),
    ('pushed_mirrors', 'mirrors'),
    ('published_release', 'publish'),
    ('published_rc_to_beta', 'beta'),
)
ALL_CHECKBOXES = tuple([item for sublist in KNOWN_CHECKBOXES for item in sublist])
ORDERED_HUMAN_TASKS = tuple([sublist[0] for sublist in KNOWN_CHECKBOXES])
