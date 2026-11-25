from datetime import datetime, timedelta, timezone

from sqlalchemy import JSON, Column, DateTime, String, Table, select, update

from core.db import metadata, transaction

# 受理时即把冰雕实测和当时的带载参照落到 SQL。
# Redis 只承担投递，worker 重启或换班后仍按原样本恢复。
compute_jobs = Table('compute_jobs', metadata,
    Column('token', String(64), primary_key=True),
    Column('owner', String(100), nullable=False),
    Column('sample', String(160), nullable=False),
    Column('payload', JSON, nullable=False),
    Column('status', String(16), nullable=False),
    Column('result', JSON, nullable=True),
    Column('detail', String(255), nullable=True),
    Column('created_at', DateTime, nullable=False),
    Column('started_at', DateTime, nullable=True))


def now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def create(conn, token, owner, sample, payload):
    conn.execute(compute_jobs.insert().values(token=token, owner=owner, sample=sample,
        payload=payload, status='queued', created_at=now()))


def fetch(conn, token):
    row = conn.execute(select(compute_jobs).where(compute_jobs.c.token == token)).mappings().first()
    return dict(row) if row else None


def lock(conn, token):
    """同一凭据的签认重试在此行锁上排队，只允许一份评分落库。"""
    row = conn.execute(select(compute_jobs).where(compute_jobs.c.token == token)
                       .with_for_update()).mappings().first()
    return dict(row) if row else None


def open_jobs(conn, settled_tokens, settled_samples, limit=20):
    """尚未办完的计算；已签认的凭据和样本都不再列出。"""
    query = select(compute_jobs).where(
        compute_jobs.c.status.in_(('queued', 'running', 'ready', 'rejected')))
    if settled_tokens:
        query = query.where(compute_jobs.c.token.not_in(settled_tokens))
    if settled_samples:
        query = query.where(compute_jobs.c.sample.not_in(settled_samples))
    query = query.order_by(compute_jobs.c.created_at.desc()).limit(limit)
    return [dict(row) for row in conn.execute(query).mappings()]


def claim(token):
    """只有一个 worker 能把 queued 改成 running，重复投递的队列项会被忽略。"""
    with transaction() as conn:
        changed = conn.execute(update(compute_jobs)
            .where((compute_jobs.c.token == token) & (compute_jobs.c.status == 'queued'))
            .values(status='running', started_at=now())).rowcount
        if changed != 1:
            return None
        return fetch(conn, token)


def complete(token, status, result=None, detail=None):
    with transaction() as conn:
        conn.execute(update(compute_jobs)
            .where((compute_jobs.c.token == token) & (compute_jobs.c.status == 'running'))
            .values(status=status, result=result, detail=detail))


def reset_running(stale_seconds=None):
    """启动时把中断在 running 的任务放回队列；运行时只回收超时的任务。"""
    query = update(compute_jobs).where(compute_jobs.c.status == 'running')
    if stale_seconds is not None:
        query = query.where(compute_jobs.c.started_at < now() - timedelta(seconds=stale_seconds))
    with transaction() as conn:
        return conn.execute(query.values(status='queued', started_at=None)).rowcount


def queued_tokens():
    with transaction() as conn:
        return [row[0] for row in conn.execute(
            select(compute_jobs.c.token).where(compute_jobs.c.status == 'queued'))]
