"""Run with uv run --locked python -m jeff.coordination."""

import argparse
import sys

from . import mailbox


def parser():
    root = argparse.ArgumentParser(description="Local Markdown mailbox; identities are not authentication.")
    root.add_argument("--board", help="explicit board path; default: shared Git main-root/.coord")
    commands = root.add_subparsers(dest="command", required=True)
    commands.add_parser("init", help="initialize directories/format marker without replaying assignments")
    send = commands.add_parser("send", help="publish an immutable message from a UTF-8 Markdown body file")
    send.add_argument("--sender", required=True, choices=mailbox.PARTICIPANTS)
    send.add_argument("--recipient", required=True, choices=mailbox.PARTICIPANTS)
    send.add_argument("--kind", required=True, choices=mailbox.KINDS)
    send.add_argument("--subject", required=True)
    send.add_argument("--body-file", required=True)
    send.add_argument("--task-id")
    send.add_argument("--reply-to")
    send.add_argument("--supersedes")
    inbox = commands.add_parser("inbox", help="list unread and acknowledged/blocked outstanding messages")
    inbox.add_argument("--recipient", required=True, choices=mailbox.PARTICIPANTS)
    inbox.add_argument("--all", action="store_true", help="also include completed/declined messages")
    read = commands.add_parser("read", help="display a message; does NOT acknowledge it")
    read.add_argument("message_id")
    actions = {
        "ack": ("acknowledged", "attest that you actually read the message; NOT completion"),
        "complete": ("completed", "record completion after acknowledgement"),
        "block": ("blocked", "record a blocker after acknowledgement; remains outstanding"),
        "decline": ("declined", "record declining after acknowledgement"),
    }
    for name, (status, help_text) in actions.items():
        action = commands.add_parser(name, help=help_text)
        action.add_argument("message_id")
        action.add_argument("--recipient", required=True, choices=mailbox.PARTICIPANTS)
        action.add_argument("--note", default="", help="optional short explanation or Markdown evidence link")
        action.set_defaults(status=status)
    return root


def main():
    args = parser().parse_args()
    try:
        board = mailbox.board_path(args.board)
        if args.command == "init":
            print(mailbox.init(board))
        elif args.command == "send":
            print(mailbox.send(
                board, args.sender, args.recipient, args.kind, args.subject,
                mailbox.read_text(args.body_file), args.task_id, args.reply_to, args.supersedes,
            ))
        elif args.command == "inbox":
            rows = mailbox.inbox(board, args.recipient, args.all)
            print(f"Board: {board}")
            print("ID\tSTATE\tFROM\tCREATED (UTC)\tSUBJECT")
            for meta, state in rows:
                label = "acknowledged-outstanding" if state == "acknowledged" else state
                print(f"{meta['id']}\t{label}\t{meta['sender']}\t{meta['created_at']}\t{meta['subject']}")
            if not rows:
                print("(empty)")
        elif args.command == "read":
            mailbox.check_board(board)
            meta, body = mailbox.load_message(board, args.message_id)
            print(mailbox.encode(meta, body), end="")
        else:
            print(mailbox.record(board, args.recipient, args.message_id, args.status, args.note))
        return 0
    except (mailbox.MailboxError, OSError, UnicodeError) as exc:
        print(f"mailbox: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
