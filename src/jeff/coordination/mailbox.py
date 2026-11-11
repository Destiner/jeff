"""Local, cooperative Markdown mailboxes. Identities are conventions, not auth."""

from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile
from uuid import UUID, uuid4


PARTICIPANTS = ("lead", "model", "data", "evaluation", "research", "release", "infra")
KINDS = ("task", "direction", "report", "update", "blocker")
STATES = ("acknowledged", "blocked", "completed", "declined")
TERMINAL = ("completed", "declined")
VERSION = "1"


class MailboxError(ValueError):
    pass


class AlreadyExists(MailboxError):
    pass


def require(condition, message):
    if not condition:
        raise MailboxError(message)


def safe_path(path):
    path = Path(os.path.abspath(Path(path).expanduser()))
    for part in (*reversed(path.parents), path):
        require(not part.is_symlink(), f"symlink not allowed: {part}")
    return path


def board_path(explicit=None):
    if explicit is not None:
        return safe_path(explicit)
    result = subprocess.run(
        ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
        capture_output=True, text=True, check=False,
    )
    require(result.returncode == 0, "outside a Git checkout; supply --board PATH")
    common = Path(result.stdout.strip())
    require(common.name == ".git", "nonstandard Git layout; supply --board PATH")
    return safe_path(common.parent / ".coord")


def identity(value):
    require(value in PARTICIPANTS, f"unknown participant: {value!r}")


def identifier(value):
    require(isinstance(value, str), "message ID must be a string")
    try:
        parsed = UUID(value)
    except ValueError as exc:
        raise MailboxError(f"invalid message ID: {value!r}") from exc
    require(parsed.version == 4 and str(parsed) == value, "ID must be a canonical UUIDv4")


def short_text(value, name, maximum=240):
    require(isinstance(value, str) and bool(value.strip()), f"{name} must be nonempty text")
    require(len(value) <= maximum and not any(ord(c) < 32 or ord(c) == 127 for c in value),
            f"{name} must be one line, at most {maximum} characters, without control characters")


def timestamp(value):
    require(isinstance(value, str) and re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{6}Z", value),
            "timestamp must be UTC YYYY-MM-DDTHH:MM:SS.ffffffZ")
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError as exc:
        raise MailboxError(f"invalid timestamp: {value!r}") from exc


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def keys(meta, record_type, required, optional=()):
    require(isinstance(meta, dict), "metadata must be a JSON object")
    required = set(required) | {"schema_version", "record_type"}
    require(required <= meta.keys() <= required | set(optional), "missing or unknown metadata fields")
    require(meta["schema_version"] == VERSION, "unsupported schema_version")
    require(meta["record_type"] == record_type, f"expected {record_type} record")


def encode(meta, body):
    return "```json\n" + json.dumps(meta, ensure_ascii=False, indent=2) + "\n```\n\n" + body.rstrip() + "\n"


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def invalid_constant(value):
    raise MailboxError(f"invalid JSON constant: {value}")


def read_text(path):
    path = safe_path(path)
    require(path.is_file(), f"missing or nonregular file: {path}")
    with path.open(encoding="utf-8") as stream:
        return stream.read()


def decode(path):
    try:
        text = read_text(path)
        require(text.startswith("```json\n"), "expected opening JSON metadata fence")
        metadata, separator, body = text[8:].partition("\n```\n\n")
        require(bool(separator), "expected metadata closing fence and blank line")
        meta = json.loads(metadata, object_pairs_hook=unique_keys, parse_constant=invalid_constant)
        require(isinstance(meta, dict), "metadata must be a JSON object")
        return meta, body
    except (ValueError, OSError) as exc:
        raise MailboxError(f"{path}: {exc}") from exc


def publish(path, text, replace=False):
    path = safe_path(path)
    descriptor, temporary = tempfile.mkstemp(prefix=".pending-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        if replace:
            os.replace(temporary, path)
        else:
            try:
                os.link(temporary, path)
            except FileExistsError as exc:
                raise AlreadyExists(f"refusing to overwrite existing file: {path}") from exc
        try:
            directory = os.open(path.parent, os.O_RDONLY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
        except OSError as exc:
            raise MailboxError(f"published {path}; durability uncertain: {exc}; inspect before retrying") from exc
    finally:
        if os.path.exists(temporary):
            try:
                os.unlink(temporary)
            except OSError as exc:
                raise MailboxError(f"publication attempted for {path}; temp cleanup failed: {exc}; inspect before retrying") from exc


def init(board):
    board = safe_path(board)
    board.mkdir(parents=True, exist_ok=True)
    marker = board / "board.md"
    if marker.exists() or marker.is_symlink():
        check_marker(board)
    else:
        try:
            publish(marker, encode({"schema_version": VERSION, "record_type": "board"},
                                   "# Jeff mailbox\n\nLocal lead ↔ owner messages; no authentication or automatic delivery."))
        except AlreadyExists:
            # Another initializer may have won the no-clobber publication.
            check_marker(board)
    for path in [board / "messages", board / "receipts", *(board / "receipts" / p for p in PARTICIPANTS)]:
        safe_path(path).mkdir(exist_ok=True)
    return board


def check_marker(board):
    meta, _ = decode(board / "board.md")
    keys(meta, "board", ())


def check_board(board):
    safe_path(board)
    check_marker(board)
    for path in (board / "messages", board / "receipts"):
        require(safe_path(path).is_dir(), f"uninitialized board; missing directory: {path}")


def message_path(board, message_id):
    identifier(message_id)
    return safe_path(board / "messages" / f"{message_id}.md")


def validate_message(meta, body, message_id):
    keys(meta, "message", ("id", "sender", "recipient", "kind", "created_at", "subject"),
         ("task_id", "reply_to", "supersedes"))
    identifier(meta["id"])
    require(meta["id"] == message_id, "message ID does not match filename")
    identity(meta["sender"])
    identity(meta["recipient"])
    require((meta["sender"] == "lead") != (meta["recipient"] == "lead"), "only lead ↔ team routing is allowed")
    require(meta["kind"] in KINDS, "unknown message kind")
    timestamp(meta["created_at"])
    short_text(meta["subject"], "subject")
    require(bool(body.strip()), "message body must not be empty")
    if "task_id" in meta:
        short_text(meta["task_id"], "task_id", 80)
    for field in ("reply_to", "supersedes"):
        if field in meta:
            identifier(meta[field])
            require(meta[field] != message_id, "message cannot reference itself")


def load_message(board, message_id):
    # Iterative traversal bounds stack use and rejects edited-in reference cycles.
    cache, active = {}, set()
    pending = [(message_id, False)]
    while pending:
        current, finishing = pending.pop()
        if finishing:
            active.remove(current)
            continue
        require(current not in active, f"cyclic message reference: {current}")
        if current in cache:
            continue
        meta, body = decode(message_path(board, current))
        validate_message(meta, body, current)
        cache[current] = (meta, body)
        active.add(current)
        pending.append((current, True))
        for field in ("reply_to", "supersedes"):
            if field in meta:
                pending.append((meta[field], False))
    for meta, _ in cache.values():
        for field in ("reply_to", "supersedes"):
            if field in meta:
                reference = cache[meta[field]][0]
                expected = (reference["recipient"], reference["sender"]) if field == "reply_to" else (reference["sender"], reference["recipient"])
                require((meta["sender"], meta["recipient"]) == expected, f"{field} endpoints do not match: {meta['id']}")
    return cache[message_id]


def send(board, sender, recipient, kind, subject, body, task_id=None, reply_to=None, supersedes=None):
    check_board(board)
    message_id = str(uuid4())
    meta = {"schema_version": VERSION, "record_type": "message", "id": message_id,
            "sender": sender, "recipient": recipient, "kind": kind, "created_at": now(), "subject": subject}
    for field, value in (("task_id", task_id), ("reply_to", reply_to), ("supersedes", supersedes)):
        if value is not None:
            meta[field] = value
    validate_message(meta, body, message_id)
    for field in ("reply_to", "supersedes"):
        if field in meta:
            reference, _ = load_message(board, meta[field])
            expected = (reference["recipient"], reference["sender"]) if field == "reply_to" else (reference["sender"], reference["recipient"])
            require((sender, recipient) == expected, f"{field} endpoints do not match")
    publish(message_path(board, message_id), encode(meta, body))
    return message_id


def receipt_path(board, recipient, message_id):
    identity(recipient)
    identifier(message_id)
    directory = safe_path(board / "receipts" / recipient)
    require(directory.is_dir(), f"uninitialized receipt directory: {directory}")
    return safe_path(directory / f"{message_id}.md")


def load_receipt(board, recipient, message_id):
    path = receipt_path(board, recipient, message_id)
    if not path.exists():
        return None
    meta, body = decode(path)
    keys(meta, "receipt", ("message_id", "recipient", "status", "acknowledged_at", "updated_at"))
    require(meta["message_id"] == message_id and meta["recipient"] == recipient, "receipt identity mismatch")
    require(meta["status"] in STATES, "unknown receipt status")
    timestamp(meta["acknowledged_at"])
    timestamp(meta["updated_at"])
    return meta, body


@contextmanager
def recipient_lock(board, recipient):
    path = safe_path(board / "receipts" / recipient / ".lock")
    descriptor = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600)
    try:
        require(stat.S_ISREG(os.fstat(descriptor).st_mode), f"nonregular lock file: {path}")
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        os.close(descriptor)


def record(board, recipient, message_id, status, explanation=""):
    check_board(board)
    identity(recipient)
    require(status in STATES, "unknown receipt status")
    message, _ = load_message(board, message_id)
    require(message["recipient"] == recipient, "only the message recipient may write its receipt")
    with recipient_lock(board, recipient):
        previous = load_receipt(board, recipient, message_id)
        if previous:
            old, old_body = previous
            if old["status"] == status:
                require(not explanation or explanation.strip() == old_body.strip(),
                        "same-state retry cannot change the explanation; send a follow-up message")
                return old["status"]
            require(old["status"] not in TERMINAL, "terminal receipt cannot change; send a new message")
            require(status != "acknowledged", "acknowledgement cannot regress an existing disposition")
        else:
            require(status == "acknowledged", "read and acknowledge the message before recording a disposition")
        instant = now()
        meta = {"schema_version": VERSION, "record_type": "receipt", "message_id": message_id,
                "recipient": recipient, "status": status,
                "acknowledged_at": previous[0]["acknowledged_at"] if previous else instant,
                "updated_at": instant}
        publish(receipt_path(board, recipient, message_id), encode(meta, explanation), replace=previous is not None)
        return status


def inbox(board, recipient, include_closed=False):
    check_board(board)
    identity(recipient)
    rows = []
    for path in sorted((board / "messages").iterdir()):
        if path.name.startswith(".pending-"):
            continue
        require(path.suffix == ".md", f"unexpected entry in messages: {path}")
        meta, _ = load_message(board, path.stem)
        if meta["recipient"] != recipient:
            continue
        receipt = load_receipt(board, recipient, meta["id"])
        status = receipt[0]["status"] if receipt else "unread"
        if include_closed or status not in TERMINAL:
            rows.append((meta, status))
    return sorted(rows, key=lambda row: (row[0]["created_at"], row[0]["id"]))
