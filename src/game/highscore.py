import json
import os

class HighScoreManager:
    def __init__(self, file_path="highscore.json"):
        self.file_path = file_path
        self.high_scores = self.load_high_scores()

    def load_high_scores(self):
        if not os.path.exists(self.file_path):
            return {"single_player": []}
        with open(self.file_path, "r") as f:
            data = json.load(f)
            for entry in data.get("single_player", []):
                if "score" in entry:
                    entry["score"] = int(entry["score"])
            return data

    def save_high_scores(self):
        with open(self.file_path, "w") as f:
            json.dump(self.high_scores, f, indent=4)

    def get_high_scores(self):
        """Trả về top 10 single-player."""
        scores = self.high_scores.get("single_player", [])
        for entry in scores:
            entry["score"] = int(entry["score"])
        return sorted(scores, key=lambda x: x["score"], reverse=True)[:10]

    def qualifies(self, score: int) -> bool:
        """
        Kiểm tra xem score có đủ vào top 10 không,
        mà không thêm vào file.
        """
        score = int(score)
        top10 = self.get_high_scores()
        if len(top10) < 10:
            return True
        return score > top10[-1]["score"]

    def update_high_score(self, score, name="Player") -> None:
        """
        Thêm vào danh sách và lưu, sau khi đã biết tên thực của người chơi.
        """
        score = int(score)
        if "single_player" not in self.high_scores:
            self.high_scores["single_player"] = []
        self.high_scores["single_player"].append({"score": score, "name": name})
        # chỉ giữ top 10
        self.high_scores["single_player"] = sorted(
            self.high_scores["single_player"],
            key=lambda x: x["score"],
            reverse=True
        )[:10]
        self.save_high_scores()

    def get_score_by_rank(self, rank: int) -> int:
        """
        Trả về điểm số tương ứng với hạng (rank) trong top 10.
        Rank bắt đầu từ 1 (hạng nhất).
        """
        scores = self.get_high_scores()
        if 1 <= rank <= len(scores):
            return scores[rank - 1]["score"]
        return 0  # Nếu rank không tồn tại

    def get_player_rank(self, score: int) -> int:
        """
        Trả về hạng của điểm số này trong bảng xếp hạng.
        Nếu không lọt top 10 thì trả về -1.
        """
        score = int(score)
        scores = self.get_high_scores()
        for index, entry in enumerate(scores):
            if score >= entry["score"]:
                return index + 1  # Rank bắt đầu từ 1 trong khi đó index ds bắt đầu từ 0 nên + 1
        if len(scores) < 10:
            return len(scores) + 1  # Khi ds < 10
        return -1  # Không đủ điểm lọt bảng

    def get_next_target_score(self, player_score: int, high_scores: list[dict]) -> int:

        if not high_scores:
            return 0  # Aim for the first entry

        lowest_higher_score = float('inf')
        for entry in high_scores:
            if player_score < entry["score"]:
                lowest_higher_score = min(lowest_higher_score, entry["score"])

        if lowest_higher_score == float('inf'):
            # Player's score is already in the top 10 or higher than all.
            return high_scores[0]["score"] if high_scores else 0
        else:
            return int(lowest_higher_score)



