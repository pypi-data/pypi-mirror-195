#!/usr/bin/env python

import click

from ..log import echo_info, echo_normal, get_logger, verbosity_option
from ..release import get_gitlab_instance
from . import bdt

logger = get_logger(__name__)


@click.command(
    epilog="""
Examples:

  1. List running jobs on any runners with tag "bob" (default)

     $ bdt gitlab jobs -vv


  2. List running jobs on a runner with tag "macos":

     $ bdt gitlab jobs -vv macos


  2. List running jobs on a runner with tag "macos" and "foo":

     $ bdt gitlab jobs -vv macos foo

"""
)
@click.argument("tags", nargs=-1)
@click.option(
    "-s",
    "--status",
    type=click.Choice(["running", "success", "failed", "canceled"]),
    default="running",
    show_default=True,
    help='The status of jobs we are searching for - one of "running", '
    '"success", "failed" or "canceled"',
)
@verbosity_option()
@bdt.raise_on_error
def jobs(status, tags):
    """Lists jobs on a given runner identified by description."""

    gl = get_gitlab_instance()
    gl.auth()

    tags = tags or ["bob"]

    # search for the runner(s) to affect
    runners = gl.runners.list(tag_list=tags)

    if not runners:
        raise RuntimeError("Cannot find runner with tags = %s" % "|".join(tags))

    for runner in runners:
        jobs = runner.jobs.list(all=True, status=status)
        echo_normal(
            "Runner %s (id=%d) -- %d running"
            % (
                runner.attributes["description"],
                runner.attributes["id"],
                len(jobs),
            )
        )
        for k in jobs:
            echo_info(
                "** job %d: %s (%s), since %s, by %s [%s]"
                % (
                    k.id,
                    k.attributes["project"]["path_with_namespace"],
                    k.attributes["name"],
                    k.attributes["started_at"],
                    k.attributes["user"]["username"],
                    k.attributes["web_url"],
                )
            )
