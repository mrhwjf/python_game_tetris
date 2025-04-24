import json
import os

class HighScoreManager:
    def __init__(self):
        self.file_path = "highscore.json"
        self.high_scores = self.load_high_scores()

    def load_high_scores(self):
        if not os.path.exists(self.file_path):
            return {"single_player": []}
        with open(self.file_path, "r") as f:
            data = json.load(f)
            # ensure scores are ints
            for entry in data.get("single_player", []):
                if "score" in entry:
                    entry["score"] = int(entry["score"])
            return data

    def save_high_scores(self):
        with open(self.file_path, "w") as f:
            json.dump(self.high_scores, f, indent=4)

    def get_high_scores(self):
        """Trả về top 10 single-player, giữ nguyên duplicates."""
        scores = self.high_scores.get("single_player", [])
        # đảm bảo score là int
        for entry in scores:
            entry["score"] = int(entry["score"])
        # sort descending và lấy 10
        return sorted(scores, key=lambda x: x["score"], reverse=True)[:10]

    def update_high_score(self, score, name="Player") -> bool:
        if score is None or not isinstance(score, (int, float, str)):
            raise ValueError("Score must be a number, not None")
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
        # trả về xem entry vừa thêm có phải top 1 không
        top10 = self.get_high_scores()
        return top10 and top10[0]["score"] == score
