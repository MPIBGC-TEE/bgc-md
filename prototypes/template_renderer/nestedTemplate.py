def template(data):
    rel=Text('data=')
    rel+=Text(str(data))
    rel+=render(Path("template.py"),data)
    return rel

