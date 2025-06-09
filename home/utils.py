import re

def format_text(text):
    """
    Formats the input text using simple Markdown-like indicators for HTML output.

    Supported indicators:
    - Bold:        **text**
    - Italic:      *text*
    - Underline:   __text__
    - Strikethrough: ~~text~~
    - Inline Code: `code`
    - Code Block:
        ```python
        your_code_here
        ```
    - Headings:    # Heading 1, ## Heading 2, ### Heading 3
    - Unordered List: - List Item
    - Links:       [Link Text](URL)
    - Blockquote:  > Quoted text

    Args:
        text (str): The input text with formatting indicators.

    Returns:
        str: The formatted text in HTML.
    """

    # --- Block-level formatting (process before inline to avoid conflicts) ---

    # Code Blocks (multi-line, capture language if specified)
    # This regex looks for ``` followed by an optional language, then newlines,
    # then the code content (non-greedy), then ```
    text = re.sub(r'```(\w*)\n(.*?)```', r'<pre><code class="language-\1">\2</code></pre>', text, flags=re.DOTALL)

    # Blockquote
    # Looks for lines starting with '> ' and wraps them in <blockquote><p>
    text = re.sub(r'^> (.*)$', r'<blockquote><p>\1</p></blockquote>', text, flags=re.MULTILINE)

    # Headings (order matters: process H3, then H2, then H1 to avoid partial matches)
    text = re.sub(r'^### (.*)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.*)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)

    # Unordered Lists (process individual list items, then wrap in <ul> later)
    # This will convert each list item to a <li> tag.
    # We'll need a separate step to wrap these in <ul> tags.
    list_items = []
    def replace_list_item(match):
        list_items.append(f'<li>{match.group(1)}</li>')
        return '[[LIST_ITEM_PLACEHOLDER]]' # Use a placeholder for now
    text = re.sub(r'^- (.*)$', replace_list_item, text, flags=re.MULTILINE)

    # --- Inline formatting ---

    # Links: [Link Text](URL)
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)

    # Bold: **text**
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)

    # Italic: *text* (must be processed after bold to avoid matching ** as * *)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)

    # Underline: __text__
    text = re.sub(r'__(.*?)__', r'<u>\1</u>', text)

    # Strikethrough: ~~text~~
    text = re.sub(r'~~(.*?)~~', r'<del>\1</del>', text)

    # Inline Code: `code`
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)

    # --- Post-processing for lists ---
    # Now, wrap the collected list items in <ul> tags.
    # This is a bit more complex as we need to handle contiguous list items.
    # A simpler approach for this function is to assume list items are on separate lines
    # and then wrap them. For a true Markdown parser, this would be more robust.
    if list_items:
        # Find blocks of placeholders and replace them with a single <ul> block
        # This simple approach assumes no other text intersperses list items.
        # For more complex scenarios, a state machine or more advanced parsing would be needed.
        formatted_list = '<ul>\n' + '\n'.join(list_items) + '\n</ul>'
        text = text.replace('[[LIST_ITEM_PLACEHOLDER]]', formatted_list, 1) # Replace first placeholder
        text = text.replace('[[LIST_ITEM_PLACEHOLDER]]', '') # Remove any remaining placeholders if they were not part of the first block

    return text
