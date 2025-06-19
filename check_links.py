import os
from bs4 import BeautifulSoup

def find_broken_links(html_dir):
    broken_links = []
    html_files = [f for f in os.listdir(html_dir) if f.endswith('.html')]

    for filename in html_files:
        filepath = os.path.join(html_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']

            # Check only internal links (not starting with http, #, mailto, etc.)
            if href and not href.startswith(('http', '#', 'mailto:', 'tel:')):
                # Construct the absolute path to the linked file
                # Handles cases like "page.html" and "../css/style.css"
                # For this project, all html links are within the same directory or are simple filenames

                linked_file_path = os.path.normpath(os.path.join(html_dir, href))

                # Check if the linked file exists
                if not os.path.exists(linked_file_path):
                    broken_links.append(f"In {filename}: Link to '{href}' (resolved as '{linked_file_path}') is broken.")

    return broken_links

if __name__ == "__main__":
    html_directory = "html"
    errors = find_broken_links(html_directory)
    if errors:
        print("Broken internal links found:")
        for error in errors:
            print(error)
    else:
        print("No broken internal links found.")
