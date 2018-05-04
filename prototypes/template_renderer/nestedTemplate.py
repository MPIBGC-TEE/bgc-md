def template(data):
    rel=Text('data1=')
    rel+=Text(str(data))
    rel+=render(Path("template.py"),data)
    return rel

