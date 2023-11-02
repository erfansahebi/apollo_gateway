from uuid import uuid4
from werkzeug import Request
from apollo_shared.utils import Context


def start_context(request: Request) -> Context:
    return Context(
        request_id=str(uuid4()),
        token=None if request.authorization is None else str(request.authorization).strip(),
        user_id=None,
    )


def get_context(request: Request) -> Context | None:
    context = request.context
    return context.dict() if not isinstance(context, dict) else context
