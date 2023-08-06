from __future__ import annotations

import os
from contextlib import contextmanager
from datetime import datetime
from functools import partial
from typing import Iterable

from psycopg.types.json import Jsonb

from .args import detect_args
from .client import Client
from .sigterm import deregister
from .sigterm import register
from .queries import first_row
from .queries import first_value
from .util import coalesce


__all__ = [
    "Experiment",
    "Run",
    "experiment_add_relationship",
    "experiment_add_tags",
    "experiment_remove_relationship",
    "experiment_remove_tags",
    "experiment_set_comment",
    "experiment_set_name",
    "experiment_set_tags",
    "run_add_env",
    "run_add_metrics",
    "run_add_params",
    "run_add_relationship",
    "run_add_tags",
    "run_from_env",
    "run_remove_env",
    "run_remove_params",
    "run_remove_relationship",
    "run_remove_tags",
    "run_set_comment",
    "run_set_created",
    "run_set_env",
    "run_set_params",
    "run_set_started",
    "run_set_status",
    "run_set_tags",
    "run_set_updated",
]


def _jsonb(obj):
    """
    Return `Jsonb(obj)` if it is not None.
    """
    if obj is None:
        return None
    return Jsonb(obj)


def _jsonb_tags(tags: Iterable[str]):
    """
    Return `Jsonb({tag: True, ...})` if it is not None.
    """
    if tags is None:
        return None
    return Jsonb({tag: True for tag in tags})


def _query_jsonb_add_keys(table, col):
    return f"UPDATE {table} SET {col} = COALESCE({col}, '{{}}'::jsonb) || %s WHERE id = %s;"


def _query_jsonb_remove_keys(table, col):
    return f"UPDATE {table} SET {col} = {col} - %s::text[] WHERE id = %s;"


def experiment_set_name(client: Client, experiment_id: int, name: str | None):
    """
    Set an experiment name.
    """
    if name is None:
        return
    query = "UPDATE experiments SET name = %s WHERE id = %s;"
    with client.cursor() as cursor:
        cursor.execute(query, (name, experiment_id))


def experiment_set_comment(client: Client, experiment_id: int, comment: str):
    """
    Set an experiment comment.
    """
    if comment is None:
        return
    query = "UPDATE experiments SET comment = %s WHERE id = %s;"
    with client.cursor() as cursor:
        cursor.execute(query, (comment, experiment_id))


def experiment_set_tags(client: Client, experiment_id: int, *tags: str):
    """
    Set tags of an experiment.
    """
    query = "UPDATE experiments SET tags = %s WHERE id = %s;"
    with client.cursor() as cursor:
        cursor.execute(query, (_jsonb_tags(tags), experiment_id))


def experiment_add_tags(client: Client, experiment_id: int, *tags: str):
    """
    Add tags to an experiment.
    """
    if not tags:
        return
    query = _query_jsonb_add_keys("experiments", "tags")
    with client.cursor() as cursor:
        cursor.execute(query, (_jsonb_tags(tags), experiment_id))


def experiment_remove_tags(client: Client, experiment_id: int, *tags: str):
    """
    Remove tags from an experiment.
    """
    if not tags:
        return
    query = _query_jsonb_remove_keys("experiments", "tags")
    with client.cursor() as cursor:
        cursor.execute(query, (list(tags), experiment_id))


def experiment_add_relationship(client: Client, from_id: int, kind: str, to_id: int):
    """
    Add a relationship between two experiments.
    """
    query = """
        INSERT INTO experiment_relationships (from_id, kind, to_id)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING;
    """
    with client.cursor() as cursor:
        cursor.execute(query, (from_id, kind, to_id))


def experiment_remove_relationship(client: Client, from_id: int, kind: str, to_id: int):
    """
    Remove a relationship between two experiments.
    """
    query = """
        DELETE FROM experiment_relationships WHERE from_id = %s AND kind = %s AND to_id = %s;
    """
    with client.cursor() as cursor:
        cursor.execute(query, (from_id, kind, to_id))


class Experiment:
    """
    Helper class to create experiments, as well as runs for experiments.

    Note:
        Parameters comment and tags
        are ignored if the experiment already exists.

    Parameters:
        client: Client object to use
        experiment_id: ID of the experiment; may be None if name is given
        name: name of the experiment; may be None if experiment_id is given
        comment: text comment;
            see `experiment_set_comment` for details
        tags: list of experiment tags;
            see `experiment_set_tags` for details
    """
    def __init__(
        self,
        client: Client,
        experiment_id: int | None = None,
        name: str | None = None,
        comment: str | None = None,
        tags: Iterable[str] | None = None,
    ):
        if experiment_id is None and name is None:
            raise ValueError("need either experiment_id or name")
        self.client = client
        with self.client.cursor() as cursor:
            query = """
                SELECT id, name FROM experiments
                WHERE (id = %(id)s OR %(id)s IS NULL)
                AND (name = %(name)s OR %(name)s IS NULL);
            """
            row = first_row(cursor, query, {"id": experiment_id, "name": name})
            # need to create the experiment first
            if row is None:
                if experiment_id is None:
                    # only name is given
                    query = """
                        INSERT INTO experiments (name)
                        VALUES (%s) RETURNING id, name;
                    """
                    row = first_row(cursor, query, (name,))
                else:
                    # both id and name are given
                    query = """
                        INSERT INTO experiments (id, name)
                        VALUES (%s, %s) RETURNING id, name;
                    """
                    row = first_row(cursor, query, (experiment_id, name))
            old_experiment_id, old_name = row
            experiment_id = coalesce(experiment_id, old_experiment_id)
            name = coalesce(name, old_name)
            if experiment_id != old_experiment_id or name != old_name:
                raise ValueError(
                    f"experiment {experiment_id} \"{name}\" conflicts with "
                    f"experiment {old_experiment_id} \"{old_name}\""
                    )
            self.id = experiment_id
            self.set_name(name)
            self.set_comment(comment)
            if tags is not None:
                self.set_tags(tags)

    def set_name(self, name: str):
        """
        Set the experiment name.
        """
        experiment_set_name(self.client, self.id, name)

    def set_comment(self, comment: str):
        """
        Set the experiment comment.
        """
        experiment_set_comment(self.client, self.id, comment)

    def set_tags(self, *tags: str):
        """
        Set tags of the experiment.
        """
        experiment_set_tags(self.client, self.id, *tags)

    def add_tags(self, *tags: str):
        """
        Add tags to the experiment.
        """
        experiment_add_tags(self.client, self.id, *tags)

    def remove_tags(self, *tags: str):
        """
        Remove tags from the experiment.
        """
        experiment_remove_tags(self.client, self.id, *tags)

    def add_relationship(self, kind: str, to_id: int):
        """
        Add a relationship to another experiment.
        """
        experiment_add_relationship(self.client, self.id, kind, to_id)

    def remove_relationship(self, kind: str, to_id: int):
        """
        Remove a relationship to another experiment.
        """
        experiment_remove_relationship(self.client, self.id, kind, to_id)

    def get_run(
        self,
        run_id: int | str | None = None,
        status: str | None = None,
        comment: str | None = None,
        tags: Iterable[str] | None = None,
        params: 'auto' | dict | None = None,
        env: 'auto' | dict | None = None,
        updated: 'auto' | datetime | None = None,
    ) -> Run :
        """
        Get a Run object, see its documentation for more details.
        """
        return Run(
            client=self.client,
            experiment_id=self.id,
            run_id=run_id,
            status=status,
            comment=comment,
            tags=tags,
            params=params,
            env=env,
            updated=updated,
        )


def run_set_status(client: Client, run_id: int, status: str | None):
    """
    Set a run status to one of the following:
        - `BOOT_FAIL`
        - `CANCELLED`
        - `CONFIGURING`
        - `COMPLETED`
        - `COMPLETING`
        - `DEADLINE`
        - `FAILED`
        - `NODE_FAIL`
        - `OUT_OF_MEMORY`
        - `PENDING`
        - `PREEMPTED`
        - `RESV_DEL_HOLD`
        - `REQUEUE_FED`
        - `REQUEUE_HOLD`
        - `REQUEUED`
        - `RESIZING`
        - `REVOKED`
        - `RUNNING`
        - `SIGNALING`
        - `SPECIAL_EXIT`
        - `STAGE_OUT`
        - `STOPPED`
        - `SUSPENDED`
        - `TIMEOUT`

    Does nothing if status is None.
    """
    if status is None:
        return
    query = "UPDATE runs SET status = %s WHERE id = %s;"
    with client.cursor() as cursor:
        cursor.execute(query, (status, run_id))


def _now() -> datetime:
    return datetime.now().astimezone()


def _resolve_datetime(dt: 'auto' | datetime | None = 'auto'):
    if dt == 'auto':
        dt = _now()
    return dt


def _run_set_timestamp(
    client: Client,
    column: str,
    run_id: int,
    dt: 'auto' | datetime | None = 'auto',
):
    """
    Set a timestamp for an existing run.

    Parameters:
        client: the Client to use
        column: which column to update
        run_id: which existing run to update
        dt: the timestamp, may be `'auto'` (set to now),
            timezone aware `datetime` None (do nothing)
    """
    dt = _resolve_datetime(dt)
    if dt is None:
        return
    query = f"UPDATE runs SET {column} = %s WHERE id = %s;"
    with client.cursor() as cursor:
        cursor.execute(query, (dt, run_id))


def run_set_created(
    client: Client,
    run_id: int,
    dt: 'auto' | datetime | None = 'auto',
):
    """
    Set time_created for an existing run.

    Parameters:
        client: the Client to use
        run_id: which existing run to update
        dt: the timestamp, may be `'auto'` (set to now),
            timezone aware `datetime`, or None (do nothing)
    """
    _run_set_timestamp(client, "time_created", run_id, dt)


def run_set_started(
    client: Client,
    run_id: int,
    dt: 'auto' | datetime | None = 'auto',
):
    """
    Set time_started for an existing run.

    Parameters:
        client: the Client to use
        run_id: which existing run to update
        dt: the timestamp, may be `'auto'` (set to now),
            timezone aware `datetime`, or None (do nothing)
    """
    _run_set_timestamp(client, "time_started", run_id, dt)


def run_set_updated(
    client: Client,
    run_id: int,
    dt: 'auto' | datetime | None = 'auto',
):
    """
    Set time_updated for an existing run.

    Parameters:
        client: the Client to use
        run_id: which existing run to update
        dt: the timestamp, may be `'auto'` (set to now),
            timezone aware `datetime`, or None (do nothing)
    """
    _run_set_timestamp(client, "time_updated", run_id, dt)


def run_set_comment(client: Client, run_id: int, comment: str | None):
    """
    Set the comment for an existing run.
    If comment is None, do nothing.
    """
    if comment is None:
        return
    query = "UPDATE runs SET comment = %s WHERE id = %s;"
    with client.cursor() as cursor:
        cursor.execute(query, (comment, run_id))


def run_set_tags(
    client: Client,
    run_id: int,
    *tags: str,
):
    """
    Set the tags of an existing run.

    Parameters:
        client: the Client to use
        run_id: which existing run to update
        tags: the tags
    """
    if tags is None:
        return
    query = "UPDATE runs SET tags = %s WHERE id = %s;"
    with client.cursor() as cursor:
        cursor.execute(query, (_jsonb_tags(tags), run_id))


def run_add_tags(
    client: Client,
    run_id: int,
    *tags: str,
):
    """
    Add tags to an existing run.
    
    Parameters:
        client: the Client to use
        run_id: which existing run to update
        tags: tags to add
    """
    query = _query_jsonb_add_keys("runs", "tags")
    with client.cursor() as cursor:
        cursor.execute(query, (_jsonb_tags(tags), run_id))


def run_remove_tags(
    client: Client,
    run_id: int,
    *tags: str,
):
    """
    Remove tags from an existing run.
    
    Parameters:
        client: the Client to use
        run_id: which existing run to update
        tags: tags to remove
    """
    query = _query_jsonb_remove_keys("runs", "tags")
    with client.cursor() as cursor:
        cursor.execute(query, (list(tags), run_id))


def run_set_params(
    client: Client,
    run_id: int,
    params: 'auto' | dict | None = 'auto',
):
    """
    Set run parameters.
    See `sqltrack.args.detect_args` for details on detection in auto mode.

    Parameters:
        client: the Client to use
        run_id: which existing run to update
        params: the parameters, may be `'auto'` (detect parameters),
            `dict`, or None (do nothing)
    """
    if params == 'auto':
        params = detect_args()
    if params is None:
        return
    query = "UPDATE runs SET params = %s WHERE id = %s;"
    with client.cursor() as cursor:
        cursor.execute(query, (_jsonb(params), run_id))


def run_add_params(
    client: Client,
    run_id: int,
    params: 'auto' | dict | None = 'auto',
):
    """
    Add some parameters to an existing run.
    See `sqltrack.args.detect_args` for details on detection in auto mode.

    Parameters:
        client: the Client to use
        run_id: which existing run to update
        params: the parameters, may be `'auto'` (detect parameters),
            `dict`, or None (do nothing)
    """
    if params == 'auto':
        params = detect_args()
    if not params:
        return
    query = _query_jsonb_add_keys("runs", "params")
    with client.cursor() as cursor:
        cursor.execute(query, (_jsonb(params), run_id))


def run_remove_params(
    client: Client,
    run_id: int,
    *params: str,
):
    """
    Remove some parameters from an existing run.

    Parameters:
        client: the Client to use
        run_id: which existing run to update
        params: names to remove from parameters
    """
    if not params:
        return
    query = _query_jsonb_remove_keys("runs", "params")
    with client.cursor() as cursor:
        cursor.execute(query, (list(params), run_id))


def _resolve_env(env: 'auto' | dict | None = 'auto',):
    if env == 'auto':
        env = dict(os.environ)
    return env


def run_set_env(
    client: Client,
    run_id: int,
    env: 'auto' | dict | None = 'auto',
):
    """
    Set run environment.

    Parameters:
        client: the Client to use
        run_id: which existing run to update
        env: the environment, may be `'auto'` (set to `os.environ`),
            `dict`, or None (do nothing)
    """
    env = _resolve_env(env)
    if env is None:
        return
    query = "UPDATE runs SET env = %s WHERE id = %s;"
    with client.cursor() as cursor:
        cursor.execute(query, (_jsonb(env), run_id))


def run_add_env(
    client: Client,
    run_id: int,
    env: 'auto' | dict | None = 'auto',
):
    """
    Add some environment variables to an existing run.

    Parameters:
        client: the Client to use
        run_id: which existing run to update
        env: the environment, may be `'auto'` (set to `os.environ`),
            `dict`, or None (do nothing)
    """
    env = _resolve_env(env)
    if env is None:
        return
    query = _query_jsonb_add_keys("runs", "env")
    with client.cursor() as cursor:
        cursor.execute(query, (_jsonb(env), run_id))


def run_remove_env(
    client: Client,
    run_id: int,
    *env: str,
):
    """
    Remove some environment variables from an existing run.

    Parameters:
        client: the Client to use
        run_id: which existing run to update
        env: names to remove from env
    """
    query = _query_jsonb_remove_keys("runs", "env")
    with client.cursor() as cursor:
        cursor.execute(query, (list(env), run_id))


def run_add_metrics(client: Client, run_id: int, step: int = 0, progress: float = 0.0, **metrics):
    """
    Add metrics to a run.
    """
    query = f"""
        INSERT INTO metrics(run_id, step, progress, {", ".join(metrics)})
        VALUES (%s, %s, %s, {", ".join(("%s" for _ in metrics))})
        ON CONFLICT (run_id, step, progress) DO UPDATE
        SET {", ".join((f"{k} = excluded.{k}" for k in metrics))};
    """
    with client.cursor() as cursor:
        cursor.execute(query, (run_id, step, progress) + tuple(metrics.values()))
        query = "UPDATE runs SET time_updated = %s WHERE id = %s;"
        cursor.execute(query, (_now(), run_id))


def run_add_relationship(client: Client, from_id: int, kind: str, to_id: int):
    """
    Add a relationship between two runs.
    """
    query = """
        INSERT INTO run_relationships (from_id, kind, to_id)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING;
    """
    with client.cursor() as cursor:
        cursor.execute(query, (from_id, kind, to_id))


def run_remove_relationship(client: Client, from_id: int, kind: str, to_id: int):
    """
    Remove a relationship between two runs.
    """
    query = """
        DELETE FROM run_relationships
        WHERE from_id = %s AND kind = %s AND to_id = %s;
    """
    with client.cursor() as cursor:
        cursor.execute(query, (from_id, kind, to_id))


class Run:
    """
    Helper class to manage runs.

    Note:
        If `run_id` is None, a new run with an unused ID is created.
        If an unused `run_id` is given a new run with that ID is created
        and comment, tags, params, and env are set to the given values.
        Those additional parameters are ignored if an existing `run_id` is given.

    Parameters:
        client: Client object to use
        experiment_id: ID of the experiment;
            may be None if an existing run_id is given
        run_id: ID of the run; if None an unused ID is chosen;
            if string then load ID from that environment variable
        comment: just some text comment;
            see `run_set_comment` for details
        tags: list of run tags;
            see `run_set_tags` for details
        params: run parameters;
            see `run_set_params` for details
        env: environment variables;
            see `run_set_env` for details
        updated: update timestamp;
            see `run_set_updated` for details
    """
    def __init__(
        self,
        client: Client,
        experiment_id: int | None = None,
        run_id: int | str | None = None,
        status: str | None = None,
        comment: str | None = None,
        tags: Iterable[str] | None = None,
        params: 'auto' | dict | None = None,
        env: 'auto' | dict | None = None,
        updated: 'auto' | datetime | None = None,
    ):
        if isinstance(run_id, str):
            run_id = int(os.getenv(run_id))
        if experiment_id is None and run_id is None:
            raise ValueError("need either experiment_id or run_id")
        self.client = client
        with self.client.cursor() as cursor:
            # create the run or confirm run with id already exists
            if run_id is None:
                # create run with next ID
                query = """
                    INSERT INTO runs (experiment_id)
                    VALUES (%s) RETURNING id;
                """
                run_id = first_value(cursor, query, (experiment_id,))
            else:
                # check if run with this ID already exists
                row = first_row(
                    cursor,
                    "SELECT id, experiment_id FROM runs WHERE id = %s;",
                    (run_id,),
                )
                if row is not None:
                    run_id, real_experiment_id = row
                    experiment_id = coalesce(experiment_id, real_experiment_id)
                    if experiment_id != real_experiment_id:
                        raise ValueError(
                            f"run {run_id} belongs to experiment "
                            f"{real_experiment_id}, not {experiment_id}"
                        )
                elif experiment_id is None:
                    # need experiment ID if run doesn't exist yet
                    raise ValueError(f"run {run_id} does not exist and no experiment ID given")
                else:
                    # create new run with this ID
                    query = """
                        INSERT INTO runs (id, experiment_id)
                        VALUES (%s, %s) RETURNING id;
                    """
                    run_id = first_value(cursor, query, (run_id, experiment_id))
            self.id = run_id
            self.experiment_id = experiment_id
            self.set_status(status)
            self.set_comment(comment)
            if tags is not None:
                self.set_tags(*tags)
            self.set_params(params)
            self.set_env(env)
            self.set_updated(updated)


    def set_status(self, status: str):
        """
        Set the run status.
        See `run_set_status` for details.
        """
        run_set_status(self.client, self.id, status)

    def set_created(self, dt: 'auto' | datetime | None = 'auto'):
        """
        Set time_created for the run.
        See `run_set_created` for details.
        """
        run_set_created(self.client, self.id, dt)

    def set_started(self, dt: 'auto' | datetime | None = 'auto'):
        """
        Set time_started for the run.
        See `run_set_started` for details.
        """
        run_set_started(self.client, self.id, dt)

    def set_updated(self, dt: 'auto' | datetime | None = 'auto'):
        """
        Set time_updated for the run.
        See `run_set_updated` for details.
        """
        run_set_updated(self.client, self.id, dt)

    def set_comment(self, comment: str):
        """
        Set the run comment.
        """
        run_set_comment(self.client, self.id, comment)

    def set_tags(self, *tags: str):
        """
        Set the run tags.
        """
        run_set_tags(self.client, self.id, *tags)

    def add_tags(self, *tags: str):
        """
        Add tags to the run.
        """
        run_add_tags(self.client, self.id, *tags)

    def remove_tags(self, *tags: str):
        """
        Remove tags from the run.
        """
        run_remove_tags(self.client, self.id, *tags)

    def set_params(self, params: 'auto' | dict | None = 'auto'):
        """
        Set the run parameters.
        See `run_set_params` for details.
        """
        run_set_params(self.client, self.id, params)

    def add_params(self, params: 'auto' | dict | None = 'auto'):
        """
        Add parameters to the run.
        See `run_add_params` for details.
        """
        run_set_params(self.client, self.id, params)

    def remove_params(self, params: 'auto' | dict | None = 'auto'):
        """
        Remove parameters from the run.
        See `run_remove_params` for details.
        """
        run_remove_params(self.client, self.id, params)

    def set_env(self, env: 'auto' | dict | None = 'auto'):
        """
        Set the run environment.
        See `run_set_env` for details.
        """
        run_set_env(self.client, self.id, env)

    def add_env(self, env: 'auto' | dict | None = 'auto'):
        """
        Add environment variables to the run.
        See `run_add_env` for details.
        """
        run_add_env(self.client, self.id, env)

    def remove_env(self, env: 'auto' | dict | None = 'auto'):
        """
        Remove environment variables from the run.
        See `run_remove_env` for details.
        """
        run_remove_env(self.client, self.id, env)

    def add_relationship(self, kind: str, to_id: int):
        """
        Add a relationship to another run.
        """
        run_add_relationship(self.client, self.id, kind, to_id)

    def remove_relationship(self, kind: str, to_id: int):
        """
        Remove a relationship to another run.
        """
        run_remove_relationship(self.client, self.id, kind, to_id)

    def add_metrics(
        self,
        step: int = 0,
        progress: float = 0.0,
        set_updated: 'auto' | datetime | None = 'auto',
        **metrics,
    ):
        """
        Add metrics to the run.
        See `run_add_metrics` for details.
        """
        with self.client.connect():
            run_add_metrics(self.client, self.id, step, progress, **metrics)
            self.set_updated(set_updated)

    def start(
        self,
        terminated="CANCELLED",
        started: 'auto' | datetime | None = 'auto',
        updated: 'auto' | datetime | None = 'auto',
        env: 'auto' | dict | None = None,
    ):
        """
        Start the run, setting its status to RUNNING,
        among other values like `time_started`, depending on parameters.

        Parameters:
            terminated: status in case SIGTERM is received during the run;
                see also `sqltrack.sigterm`
            started: what to do about time_started;
                see `run_set_started` for details
            updated: what to do about time_updated;
                see `run_set_updated` for details
            env: control what to do about the run's env;
                see `run_set_env` for details
        """
        register(self.id, partial(self.stop, status=terminated))
        with self.client.connect():
            self.set_status("RUNNING")
            self.set_env(env)
            self.set_started(started)
            self.set_updated(updated)

    def stop(
        self,
        status="COMPLETED",
        updated: 'auto' | datetime | None = 'auto',
    ):
        """
        Stop the run, setting its status to COMPLETED and
        `time_started` to now (default), depending on parameters.

        Parameters:
            status: status to set (default: COMPLETED);
                see `run_set_status` for details
            updated: what to do about time_updated;
                see `run_set_updated` for details
        """
        deregister(self.id)
        with self.client.connect():
            self.set_status(status)
            self.set_updated(updated)

    @contextmanager
    def track(
        self,
        normal="COMPLETED",
        exception="FAILED",
        interrupt="CANCELLED",
        terminated="CANCELLED",
        started: 'auto' | datetime | None = 'auto',
        updated: 'auto' | datetime | None = 'auto',
        env: 'auto' | dict | None = None,
    ):
        """
        A context manager to track the execution of the run.
        This is equivalent to calling start and stop separately
        with the appropriate status value.

        Parameters:
            normal: status in case the run completes normally
            exception: status in case an exception occurs
            interrupt: status in case SIGINT is received during the run
            terminated: status in case SIGTERM is received during the run;
                see also `sqltrack.sigterm`
            started: what to do about time_started;
                see `run_set_started` for details
            updated: what to do about time_updated;
                see `run_set_started` for details
            env: control what to do about the run's env;
                see `run_set_env` for details
        """
        self.start(
            started=started,
            updated=updated,
            env=env,
            terminated=terminated,
        )
        stopped = False
        try:
            yield self
        except KeyboardInterrupt:
            stopped = True
            self.stop(status=interrupt)
            raise
        except:
            stopped = True
            self.stop(status=exception)
            raise
        finally:
            if not stopped:
                self.stop(status=normal)


def run_from_env(client: Client) -> Run:
    """
    Get the Run object defined by environment variables.
    The experiment is defined by at least one or both of
    `SQLTRACK_EXPERIMENT_NAME` and `SQLTRACK_EXPERIMENT_ID`,
    and optionally `SQLTRACK_RUN_ID`.
    """
    exp_name = os.getenv("SQLTRACK_EXPERIMENT_NAME")
    exp_id = int(os.getenv("SQLTRACK_EXPERIMENT_ID"))
    run_id = int(os.getenv("SQLTRACK_RUN_ID"))
    exp = Experiment(client, experiment_id=exp_id, name=exp_name)
    return exp.get_run(run_id=run_id)
