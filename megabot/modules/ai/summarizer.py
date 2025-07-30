# megabot/modules/ai/summarizer.py
def summarize_text(text: str, max_len: int = 300) -> str:
    lines = text.strip().split('\n')
    short_lines = [line for line in lines if len(line) > 40]
    summary = '\n'.join(short_lines[:5])
    return summary[:max_len] + '...' if len(summary) > max_len else summary
