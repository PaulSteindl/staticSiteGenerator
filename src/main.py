from textnode import TextNode, TextType

def main():
    textNode = TextNode("This is some anchor text", TextType.LINK, "https://orf.at")
    print(textNode)

if __name__ == "__main__":
    main()