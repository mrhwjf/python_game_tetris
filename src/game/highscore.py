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

    def qualifies(self, score) -> bool:
        """
        Kiểm tra xem score có đủ vào top 10 không,
        mà không thêm vào file.
        """
        score = int(score)
        top10 = self.get_high_scores()
        return score > top10[0]["score"]

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
