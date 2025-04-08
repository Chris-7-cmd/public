from textnode import TextNode, TextType

def main():

    node = TextNode("This is some anchor text", TextType.LINK, "hhtps://www.boot.dev")
    print(node)

    identical_node = TextNode("his is some anchor text", TextType.LINK, "hhtps://www.boot.dev")
    different_node = TextNode("Different text", TextType.TEXT, None)

    print(f"Nodes are equal: {node == identical_node}")
    print(f"Nodes are diffferent: {node == different_node}")

if __name__ == "__main__":
    main() 