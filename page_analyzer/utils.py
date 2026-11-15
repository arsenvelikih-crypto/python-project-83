# Тримминг текста до указанной длины
def truncate_text(text, max_length=200):
    if text and len(text) > max_length:
        return text[:max_length] + "..."
    return text