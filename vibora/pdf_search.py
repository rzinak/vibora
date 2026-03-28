from duckduckgo_search import DDGS


def pdf_search(theme):
    words = theme.split()
    last_word = words[-1]
    keywords = ' '.join(words[:-1]) + f" {last_word}:pdf"
    max_files = 10
    results = DDGS().text(keywords, safesearch='off', max_results=max_files)
    print(f"\nI found these results for '{theme}' I think are most relevant based on what you want:\n")
    for item in results:
        print(f"{item['title']}\n{item['href']}\n")
