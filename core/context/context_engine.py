import os

class ContextEngine:
    def __init__(self, base_path="."):
        self.base_path = base_path
        self.ignore_dirs = {'.git', 'venv', '__pycache__', '.idea', '.vscode'}

    def load_files(self):
        context = ''

        # Note the 'dirs' added here in the middle
        for root, dirs, files in os.walk(self.base_path):
            
            # This is the magic line that actually skips 'venv', '.git', etc.
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]

            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)

                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            content = f.read()
                            # Use relpath so the LLM sees 'core/model_router.py' instead of just 'model_router.py'
                            rel_path = os.path.relpath(path, self.base_path)
                            context += f"\n\n# File: {rel_path}\n{content}"
                    except:
                        pass

        return context

    def get_context(self, user_input):
        return self.load_files()