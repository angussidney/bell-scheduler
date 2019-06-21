def system_wide_template_variables():
    return dict(
        docs="https://angussidney.github.io/bell-scheduler/#"
    )


def check_file(file):
    return '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() == "wav"
