import random
from datetime import datetime

from statistics import print_statistics
from storage import (
    ensure_data_files,
    load_favorites,
    load_questions,
    load_records,
    load_wrong_questions,
    save_favorites,
    save_records,
    save_wrong_questions,
)


CATEGORIES = ["Python基础", "计算机网络", "数据结构", "操作系统", "数据库"]
QUESTION_TYPES = {
    "single": "单选题",
    "multiple": "多选题",
    "judge": "判断题",
}


class QuizApp:
    """Command line quiz system.

    The class keeps UI flow in one place while delegating JSON read/write work
    to storage.py and statistics calculation to statistics.py.
    """

    def __init__(self):
        ensure_data_files()
        self.questions = load_questions()

    def run(self):
        """Main menu loop."""
        while True:
            self._print_menu()
            choice = input("请选择功能：").strip()

            if choice == "1":
                self.start_quiz()
            elif choice == "2":
                self.random_practice()
            elif choice == "3":
                self.category_practice()
            elif choice == "4":
                self.view_wrong_questions()
            elif choice == "5":
                self.view_favorites()
            elif choice == "6":
                self.view_statistics()
            elif choice == "0":
                print("已退出，祝你学习顺利！")
                break
            else:
                print("输入无效，请重新选择。")

    def start_quiz(self):
        """Start practice with all questions in original order."""
        self._practice(self.questions)

    def random_practice(self):
        """Start practice with shuffled questions."""
        questions = self.questions[:]
        random.shuffle(questions)
        self._practice(questions)

    def category_practice(self):
        """Let the user pick a category before practicing."""
        category = self._select_category()
        if not category:
            return
        questions = [item for item in self.questions if item["category"] == category]
        self._practice(questions)

    def view_wrong_questions(self):
        """Show questions that were answered incorrectly."""
        wrong_ids = load_wrong_questions()
        questions = self._find_questions_by_ids(wrong_ids)
        print("\n====== 错题本 ======")
        self._display_question_list(questions)

    def view_favorites(self):
        """Show favorite questions."""
        favorite_ids = load_favorites()
        questions = self._find_questions_by_ids(favorite_ids)
        print("\n====== 收藏题目 ======")
        self._display_question_list(questions)

    def view_statistics(self):
        """Show study statistics based on records.json."""
        print_statistics(load_records())

    def _practice(self, questions):
        if not questions:
            print("当前没有可练习的题目。")
            return

        print(f"\n本次练习共 {len(questions)} 题。输入 q 可随时退出。")
        for index, question in enumerate(questions, start=1):
            print(f"\n------ 第 {index}/{len(questions)} 题 ------")
            if not self._ask_question(question):
                break

    def _ask_question(self, question):
        """Display one question, read the answer, and handle result storage."""
        self._print_question(question)
        answer = input("请输入答案：").strip()
        if answer.lower() == "q":
            return False

        normalized_answer = self._normalize_answer(answer, question["type"])
        correct_answer = self._normalize_answer(question["answer"], question["type"])
        is_correct = normalized_answer == correct_answer

        print("回答正确！" if is_correct else "回答错误。")
        print(f"正确答案：{self._format_answer(question['answer'])}")
        print(f"解析：{question.get('explanation', '暂无解析')}")

        self._save_record(question, normalized_answer, is_correct)
        if not is_correct:
            self._add_wrong_question(question["id"])

        favorite_choice = input("是否收藏本题？(y/n)：").strip().lower()
        if favorite_choice == "y":
            self._add_favorite(question["id"])
            print("已加入收藏。")

        return True

    def _print_question(self, question):
        print(f"分类：{question['category']}")
        print(f"题型：{QUESTION_TYPES.get(question['type'], question['type'])}")
        print(f"题目：{question['title']}")

        if question["type"] in ("single", "multiple"):
            for key, value in question.get("options", {}).items():
                print(f"  {key}. {value}")
            if question["type"] == "multiple":
                print("提示：多选题请输入多个选项，例如 AC 或 A,C。")
        elif question["type"] == "judge":
            print("提示：判断题请输入 T/F，或 对/错。")

    def _display_question_list(self, questions):
        if not questions:
            print("暂无题目。")
            return
        for index, question in enumerate(questions, start=1):
            print(f"\n{index}. [{question['category']}] {question['title']}")
            print(f"答案：{self._format_answer(question['answer'])}")
            print(f"解析：{question.get('explanation', '暂无解析')}")

    def _select_category(self):
        print("\n请选择分类：")
        for index, category in enumerate(CATEGORIES, start=1):
            print(f"{index}. {category}")
        choice = input("输入分类编号：").strip()
        if not choice.isdigit():
            print("分类编号无效。")
            return None

        index = int(choice)
        if index < 1 or index > len(CATEGORIES):
            print("分类编号超出范围。")
            return None
        return CATEGORIES[index - 1]

    def _find_questions_by_ids(self, question_ids):
        question_map = {item["id"]: item for item in self.questions}
        return [question_map[item] for item in question_ids if item in question_map]

    def _save_record(self, question, user_answer, is_correct):
        records = load_records()
        records.append(
            {
                "question_id": question["id"],
                "category": question["category"],
                "type": question["type"],
                "user_answer": user_answer,
                "correct_answer": self._normalize_answer(question["answer"], question["type"]),
                "is_correct": is_correct,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
        save_records(records)

    def _add_wrong_question(self, question_id):
        wrong = load_wrong_questions()
        if question_id not in wrong:
            wrong.append(question_id)
            save_wrong_questions(wrong)

    def _add_favorite(self, question_id):
        favorites = load_favorites()
        if question_id not in favorites:
            favorites.append(question_id)
            save_favorites(favorites)

    def _normalize_answer(self, answer, question_type):
        """Normalize answers before comparing.

        Single choice stores one uppercase letter. Multiple choice stores sorted
        letters, so AC and CA are treated as the same answer. Judge questions
        are normalized to T or F.
        """
        if isinstance(answer, list):
            answer = "".join(answer)
        answer = str(answer).strip().upper().replace(",", "").replace("，", "")

        if question_type == "multiple":
            return "".join(sorted(answer))

        if question_type == "judge":
            mapping = {
                "TRUE": "T",
                "T": "T",
                "Y": "T",
                "YES": "T",
                "对": "T",
                "正确": "T",
                "FALSE": "F",
                "F": "F",
                "N": "F",
                "NO": "F",
                "错": "F",
                "错误": "F",
            }
            return mapping.get(answer, answer)

        return answer

    def _format_answer(self, answer):
        if isinstance(answer, list):
            return ",".join(answer)
        return str(answer)

    def _print_menu(self):
        print("\n========== Python 刷题题库系统 ==========")
        print("1. 开始刷题")
        print("2. 随机练习")
        print("3. 按分类练习")
        print("4. 查看错题本")
        print("5. 查看收藏题目")
        print("6. 查看学习统计")
        print("0. 退出系统")
