"""매일 운동 루틴을 터미널에서 관리하는 간단한 프로그램."""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

DATA_FILE = Path(__file__).with_name("workout_data.json")
DEFAULT_ROUTINE = [
    "가벼운 스트레칭 (5분)", "스쿼트 (3세트 × 15회)", "푸시업 (3세트 × 10회)",
    "빠르게 걷기 (20분)", "마무리 스트레칭 (5분)",
]


def load_data() -> dict:
    if DATA_FILE.exists():
        try:
            with DATA_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
            if isinstance(data, dict):
                return data
        except (OSError, json.JSONDecodeError):
            pass
    return {"routine": DEFAULT_ROUTINE.copy(), "history": {}}


def save_data(data: dict) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")


def today() -> str:
    return date.today().isoformat()


def show_routine(data: dict) -> None:
    completed = data.get("history", {}).get(today(), [])
    routine = data.get("routine", [])
    print(f"\n오늘의 운동 루틴 ({today()})\n" + "-" * 36)
    for number, exercise in enumerate(routine, start=1):
        status = "완료" if number in completed else "미완료"
        print(f"{number}. [{status}] {exercise}")
    print("-" * 36 + f"\n진행률: {len(completed)} / {len(routine)} 완료")


def add_exercise(data: dict, exercise: str) -> None:
    exercise = exercise.strip()
    if not exercise:
        print("운동 내용을 입력해 주세요.")
        return
    data["routine"].append(exercise)
    save_data(data)
    print(f"루틴에 추가했습니다: {exercise}")


def toggle_done(data: dict, number: int) -> None:
    if number < 1 or number > len(data["routine"]):
        print("올바른 운동 번호를 입력해 주세요.")
        return
    history = data.setdefault("history", {})
    completed = history.setdefault(today(), [])
    if number in completed:
        completed.remove(number)
        message = "완료를 취소했습니다"
    else:
        completed.append(number)
        completed.sort()
        message = "완료했습니다"
    save_data(data)
    print(f"{number}번 운동을 {message}.")


def interactive_menu() -> None:
    data = load_data()
    while True:
        print("\n=== 핏로그: 매일 운동 루틴 ===\n1. 오늘 루틴 보기  2. 운동 추가  3. 완료 체크  4. 종료")
        choice = input("선택: ").strip()
        if choice == "1": show_routine(data)
        elif choice == "2": add_exercise(data, input("추가할 운동: "))
        elif choice == "3":
            try: toggle_done(data, int(input("운동 번호: ")))
            except ValueError: print("숫자를 입력해 주세요.")
        elif choice == "4":
            print("오늘도 수고하셨습니다!")
            return
        else: print("1~4 중에서 선택해 주세요.")


def main() -> None:
    parser = argparse.ArgumentParser(description="매일 운동 루틴 관리")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("list", help="오늘의 루틴 보기")
    add = sub.add_parser("add", help="운동 추가"); add.add_argument("exercise", help="추가할 운동")
    done = sub.add_parser("done", help="운동 완료 체크 또는 취소"); done.add_argument("number", type=int, help="운동 번호")
    args = parser.parse_args(); data = load_data()
    if args.command == "list": show_routine(data)
    elif args.command == "add": add_exercise(data, args.exercise)
    elif args.command == "done": toggle_done(data, args.number)
    else: interactive_menu()


if __name__ == "__main__":
    main()
