class MemoryManager:
    def __init__(self, max_turns=10):
        self.history = []
        self.max_turns = max_turns

    def build_prompt(self, new_input):
        prompt = ""
        for turn in self.history[-self.max_turns:]:
            prompt += f"User:\n{turn['user']}\nAI:\n{turn['ai']}\n"
        prompt += f"User:\n{new_input}\nAI:\n"
        return prompt

    def update(self, user_input, ai_response):
        self.history.append({
            "user": user_input,
            "ai": ai_response
        })

    def reset(self):
        self.history = []
