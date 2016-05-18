def main(lines, args):
    return ('server', lines)
    
def server(attr, args):
    return ('pr', ' '.join(attr))

def pr(lines, args):
    print lines
