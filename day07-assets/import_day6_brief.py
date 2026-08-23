#!/usr/bin/env python3
"""Validate a Day 6 shorts brief and turn its five narrations into script.txt."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


EXPECTED_IDS = [f"C{i}" for i in range(1, 6)]
EXPECTED_ROLES = ["훅", "반전", "원리 A", "원리 B", "엔딩"]
REQUIRED_SCENE_KEYS = {"id", "role", "narration", "visual", "planned_seconds"}


def fail(message: str) -> None:
    raise ValueError(message)


def load_and_validate(source: Path) -> dict:
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"Day 6 전달 파일을 찾지 못했습니다: {source}")
    except json.JSONDecodeError as error:
        fail(f"brief.json 문법이 올바르지 않습니다: {error}")

    if data.get("schema_version") != "shorts-brief-v1":
        fail("schema_version이 shorts-brief-v1이 아닙니다. Day 6에서 JSON 검사를 다시 하세요.")

    for key in ("title", "audience", "contrast", "message", "tone", "selected_hook", "target_seconds"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            fail(f"필수 항목이 비어 있습니다: {key}")
    if data["target_seconds"] != "20-23":
        fail("target_seconds는 20-23이어야 합니다.")

    scenes = data.get("scenes")
    if not isinstance(scenes, list) or len(scenes) != 5:
        fail("scenes는 C1부터 C5까지 정확히 5개여야 합니다.")
    if [scene.get("id") for scene in scenes] != EXPECTED_IDS:
        fail("scene id 순서는 C1, C2, C3, C4, C5여야 합니다.")
    if [scene.get("role") for scene in scenes] != EXPECTED_ROLES:
        fail("scene role 순서는 훅, 반전, 원리 A, 원리 B, 엔딩이어야 합니다.")

    planned_total = 0.0
    for index, scene in enumerate(scenes, start=1):
        missing = REQUIRED_SCENE_KEYS - set(scene)
        if missing:
            fail(f"C{index}에 빠진 항목이 있습니다: {', '.join(sorted(missing))}")
        for key in ("role", "visual"):
            if not isinstance(scene[key], str) or not scene[key].strip():
                fail(f"C{index} {key}이(가) 비어 있습니다.")
        narration = scene["narration"]
        if not isinstance(narration, str) or not narration.strip() or "\n" in narration.strip():
            fail(f"C{index} narration은 비어 있지 않은 한 문장이어야 합니다.")
        if any(mark in narration.strip()[:-1] for mark in ".!?。！？"):
            fail(f"C{index} narration에 두 문장 이상이 있습니다. 한 문장으로 줄이세요.")
        seconds = scene["planned_seconds"]
        if not isinstance(seconds, (int, float)) or isinstance(seconds, bool) or seconds <= 0 or seconds > 5:
            fail(f"C{index} planned_seconds는 0보다 크고 5 이하여야 합니다.")
        planned_total += float(seconds)

    if not 20 <= planned_total <= 23:
        fail(f"planned_seconds 합계가 {planned_total:g}초입니다. 20~23초여야 합니다.")
    if data["selected_hook"].strip() != scenes[0]["narration"].strip():
        fail("selected_hook과 C1 narration이 서로 다릅니다.")

    data["_planned_total"] = planned_total
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Day 6 brief.json을 Day 7 대본으로 안전하게 가져옵니다.")
    parser.add_argument("source", type=Path, help="예: day06-handoff/brief.json")
    parser.add_argument("output_dir", type=Path, help="예: my-short")
    args = parser.parse_args()

    try:
        data = load_and_validate(args.source)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        script_path = args.output_dir / "script.txt"
        if script_path.exists():
            fail(f"기존 대본을 덮어쓰지 않았습니다: {script_path}")

        narrations = [scene["narration"].strip() for scene in data["scenes"]]
        script_path.write_text("\n".join(narrations) + "\n", encoding="utf-8")
        shutil.copy2(args.source, args.output_dir / "day6-brief.json")
        summary = (
            "# Day 6 → Day 7 전달 확인\n\n"
            f"- 주제: {data['title']}\n"
            f"- 대상: {data['audience']}\n"
            f"- 선택 훅: {data['selected_hook']}\n"
            f"- 장면: {', '.join(EXPECTED_IDS)}\n"
            f"- 기획 합계: {data['_planned_total']:g}초\n"
            "- 다음 검사: Typecast 실제 낭독 뒤 컷마다 5초 이하인지 다시 측정\n"
        )
        (args.output_dir / "handoff-summary.md").write_text(summary, encoding="utf-8")
    except (OSError, ValueError) as error:
        print(f"전달 실패: {error}", file=sys.stderr)
        return 1

    print("Day 6 전달 검사 통과: shorts-brief-v1 / C1~C5 / 20~23초")
    print(f"Day 7 대본 생성: {script_path}")
    print("실제 낭독 시간은 Typecast 합성 뒤 다시 측정하세요.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
