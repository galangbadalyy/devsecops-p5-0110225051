"""Antarmuka command line untuk TaskManager."""
import argparse
import sys

from .service import TaskService
from .storage import JsonStorage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="taskmanager", description="Pengelola tugas sederhana")
    parser.add_argument("--file", default="tasks.json", help="Lokasi file penyimpanan JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Tambah tugas")
    add.add_argument("title")
    add.add_argument("--priority", default="medium", help="low | medium | high")
    add.add_argument("--due", default=None, help="Tenggat, format YYYY-MM-DD")

    lst = sub.add_parser("list", help="Tampilkan tugas")
    lst.add_argument("--pending", action="store_true", help="Hanya yang belum selesai")

    done = sub.add_parser("done", help="Tandai tugas selesai")
    done.add_argument("id", type=int)

    rm = sub.add_parser("delete", help="Hapus tugas")
    rm.add_argument("id", type=int)

    sub.add_parser("stats", help="Ringkasan statistik")
    return parser


def run(argv=None) -> int:
    args = build_parser().parse_args(argv)
    service = TaskService(JsonStorage(args.file))
    try:
        if args.command == "add":
            task = service.add(args.title, args.priority, args.due)
            print(f"Tugas #{task.id} ditambahkan: {task.title}")
        elif args.command == "list":
            for t in service.list_tasks(only_pending=args.pending):
                mark = "x" if t.done else " "
                print(f"[{mark}] #{t.id} ({t.priority}) {t.title} {t.due_date or ''}".rstrip())
        elif args.command == "done":
            task = service.complete(args.id)
            print(f"Tugas #{task.id} selesai")
        elif args.command == "delete":
            service.delete(args.id)
            print(f"Tugas #{args.id} dihapus")
        elif args.command == "stats":
            for key, value in service.stats().items():
                print(f"{key}: {value}")
    except (ValueError, KeyError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0
