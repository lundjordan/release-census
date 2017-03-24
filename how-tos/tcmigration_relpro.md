# Pre-requirements

## understanding release promotion
* this task is optional and refers to understanding how our tcmigration works as well as how release promotion works
* the original release workflow diagram before Buildbot -> Taskcluster migration, as to November 2015, can be found [here](https://www.lucidchart.com/documents/view/b733c8be-e607-445f-824a-f3353c287294)
* the up-to-date version of it, as to September 2016, is itteratively divided in two. First graph depicts the logic pieces and all tasks in Taskcluster, but lacks the dependencies between the tasks within the graph, and can be found [here](https://www.lucidchart.com/documents/view/1b59f91d-1dfa-4d1e-8a50-d2d2759a3fff)
* the follow-up version of it, with all the tasks and graph dependencies can be found [here](https://www.lucidchart.com/documents/view/29588c49-c18c-4800-be84-cca359d89ffc)
  * A "higher level" diagram of the release process is also available in the [Releng docs](http://moz-releng-docs.readthedocs.io/en/latest/release_workflows/index.html).
* we will be adding soon more information here about processing the Fennec / Desktop processes within the tcmigration / relpro
