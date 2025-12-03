import re
import sys



def convert_display_math(text):
    # Replace $$...$$ with \[...\]
    # [\s\S]*? ensures multiline, non-greedy matching
    text = re.sub(r'\$\$([\s\S]*?)\$\$', r'$$\n\1\n$$', text)
    text = re.sub(r'\$([\s\S]*?)\$', r'<div> \1 </div>$$', text)
    text = re.sub(r'\\begin{align\*}', r'\n$$\n\\begin{align}\n', text)
    text = re.sub(r'\\end{align\*}', r'\n\\end{align}\n$$\n', text)

    text = re.sub(r':::warning([\s\S]*?):::', r'<div class="red-box">\1</div>', text)
    text = re.sub(r':::success([\s\S]*?):::', r'<div class="green-box">\1</div>', text)
    text = re.sub(r':::info([\s\S]*?):::', r'<div class="blue-box">\1</div>', text)

    return text



# def flatten_latex_environments(text):
#     # This regex finds \begin{...} ... \end{...} blocks
#     pattern = re.compile(
#         r'(\\begin\{([^\}]+)\})([\s\S]*?)(\\end\{\2\})',
#         re.MULTILINE
#     )

#     def repl(match):
#         begin = match.group(1)
#         content = match.group(3)
#         end = match.group(4)

#         # Remove ALL newlines inside the environment
#         flattened = content.replace('\n', '')

#         return f"{begin}{flattened}{end}"

#     return pattern.sub(repl, text)



def process_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()

    # text = flatten_latex_environments(text)
    text = convert_display_math(text)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Processed: {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_math.py file.md")
        sys.exit(1)

    process_file(sys.argv[1])