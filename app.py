from __future__ import annotations

import argparse
import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("tasks.json")


def load_tasks() -> list[dict]:
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            tasks = json.load(file)
        if isinstance(tasks, list):
            return tasks
    except (json.JSONDecodeError, OSError):
        pass

    return []


def save_tasks(tasks: list[dict]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=2)
        file.write("\n")


def next_id(tasks: list[dict]) -> int:
    if not tasks:
        return 1
    return max(task.get("id", 0) for task in tasks) + 1


def add_task(title: str) -> str:
    title = title.strip()
    if not title:
        return "할 일을 입력해주세요."

    tasks = load_tasks()
    tasks.append({"id": next_id(tasks), "title": title, "done": False})
    save_tasks(tasks)
    return f"추가 완료: {title}"


def list_tasks() -> list[dict]:
    return load_tasks()


def complete_task(task_id: int) -> str:
    tasks = load_tasks()
    for task in tasks:
        if task.get("id") == task_id:
            task["done"] = True
            save_tasks(tasks)
            return f"완료 처리: {task['title']}"
    return f"ID {task_id}번 할 일을 찾을 수 없습니다."


def delete_task(task_id: int) -> str:
    tasks = load_tasks()
    for index, task in enumerate(tasks):
        if task.get("id") == task_id:
            removed = tasks.pop(index)
            save_tasks(tasks)
            return f"삭제 완료: {removed['title']}"
    return f"ID {task_id}번 할 일을 찾을 수 없습니다."


def print_task_list(tasks: list[dict]) -> None:
    if not tasks:
        print("등록된 할 일이 없습니다.")
        return

    print("\n현재 할 일 목록")
    print("-" * 40)
    for task in tasks:
        status = "✅ 완료" if task.get("done") else "⏳ 진행 중"
        print(f"{task.get('id', 0)}. [{status}] {task.get('title', '')}")
    print("-" * 40)


def interactive_menu() -> None:
    while True:
        print("\n=== 할 일 관리 프로그램 ===")
        print("1. 추가")
        print("2. 목록 보기")
        print("3. 완료 처리")
        print("4. 삭제")
        print("5. 종료")

        choice = input("선택하세요: ").strip()

        if choice == "1":
            title = input("할 일 내용을 입력하세요: ").strip()
            print(add_task(title))
        elif choice == "2":
            print_task_list(list_tasks())
        elif choice == "3":
            task_id = input("완료할 할 일 ID를 입력하세요: ").strip()
            if task_id.isdigit():
                print(complete_task(int(task_id)))
            else:
                print("숫자를 입력해주세요.")
        elif choice == "4":
            task_id = input("삭제할 할 일 ID를 입력하세요: ").strip()
            if task_id.isdigit():
                print(delete_task(int(task_id)))
            else:
                print("숫자를 입력해주세요.")
        elif choice == "5":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="간단한 할 일 관리 프로그램")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="할 일 추가")
    add_parser.add_argument("title", help="추가할 할 일 내용")

    list_parser = subparsers.add_parser("list", help="할 일 목록 보기")
    list_parser.set_defaults(command="list")

    done_parser = subparsers.add_parser("done", help="할 일 완료 처리")
    done_parser.add_argument("id", type=int, help="완료할 할 일 ID")

    delete_parser = subparsers.add_parser("delete", help="할 일 삭제")
    delete_parser.add_argument("id", type=int, help="삭제할 할 일 ID")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not hasattr(args, "command") or args.command is None:
        interactive_menu()
        return

    if args.command == "add":
        print(add_task(args.title))
    elif args.command == "list":
        print_task_list(list_tasks())
    elif args.command == "done":
        print(complete_task(args.id))
    elif args.command == "delete":
        print(delete_task(args.id))


if __name__ == "__main__":
    main()
