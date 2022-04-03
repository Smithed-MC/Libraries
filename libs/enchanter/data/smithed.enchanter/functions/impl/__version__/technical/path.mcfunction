def path(path):
    return generate_path(path).replace('__version__', ctx.project_version)
    