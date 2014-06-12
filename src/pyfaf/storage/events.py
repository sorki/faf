from sqlalchemy import event
from sqlalchemy.orm import mapper
from sqlalchemy.orm.session import Session

from . import ReportBacktrace


@event.listens_for(Session, "before_flush")
def update_backtrace_quality(session, flush_context, instances):
    """
    Compute and store backtrace quality information
    """

    for obj in [c for c in session.new if isinstance(c, ReportBacktrace)]:
        if isinstance(obj, ReportBacktrace):
            obj.quality = obj.compute_quality()


@event.listens_for(mapper, 'before_delete')
def before_delete(mapper, connection, target):
    """
    Remove lobs associated with target to be deleted.
    """

    for lobname, size in target.__lobs__.items():
        if target.has_lob(lobname):
            target.del_lob(lobname)
