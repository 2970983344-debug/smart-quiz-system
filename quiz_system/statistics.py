from collections import defaultdict


def calculate_statistics(records):
    """Calculate global and per-category learning statistics.

    Each record represents one submitted answer. The function is intentionally
    pure so it is easy to test and reuse.
    """
    total = len(records)
    correct = sum(1 for item in records if item.get("is_correct"))
    wrong = total - correct
    accuracy = _safe_rate(correct, total)

    category_bucket = defaultdict(lambda: {"total": 0, "correct": 0})
    for item in records:
        category = item.get("category", "未分类")
        category_bucket[category]["total"] += 1
        if item.get("is_correct"):
            category_bucket[category]["correct"] += 1

    category_stats = {}
    for category, values in category_bucket.items():
        category_stats[category] = {
            "total": values["total"],
            "correct": values["correct"],
            "wrong": values["total"] - values["correct"],
            "accuracy": _safe_rate(values["correct"], values["total"]),
        }

    return {
        "total": total,
        "correct": correct,
        "wrong": wrong,
        "accuracy": accuracy,
        "categories": category_stats,
    }


def print_statistics(records):
    """Print statistics in a CLI-friendly format."""
    stats = calculate_statistics(records)
    print("\n====== 学习统计 ======")
    print(f"总做题数：{stats['total']}")
    print(f"正确题数：{stats['correct']}")
    print(f"错误题数：{stats['wrong']}")
    print(f"正确率：{stats['accuracy']:.2f}%")

    print("\n------ 各分类正确率 ------")
    if not stats["categories"]:
        print("暂无分类统计。")
        return

    for category, item in stats["categories"].items():
        print(
            f"{category}：{item['correct']}/{item['total']} "
            f"正确率 {item['accuracy']:.2f}%"
        )


def _safe_rate(numerator, denominator):
    if denominator == 0:
        return 0.0
    return numerator / denominator * 100
