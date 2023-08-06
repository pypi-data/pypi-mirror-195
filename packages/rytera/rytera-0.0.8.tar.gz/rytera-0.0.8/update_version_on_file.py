if __name__ == '__main__':
    pyproject_path = './pyproject.toml'

    with open(pyproject_path) as f:
        pyproject_lines = f.readlines()

    version_line_index, version_line = next(
        (line_index, line)
        for line_index, line
        in enumerate(pyproject_lines) if "version = " in line
    )

    version_str = version_line[11:-2]
    major, minor, patch = version_str.split('.')
    new_version_str = f"{major}.{minor}.{int(patch)+1}"

    print(f"Current version:  {version_str}")
    print(f"New version:      {new_version_str}")

    pyproject_lines[version_line_index] = f"""version = "{new_version_str}"\n"""

    with open(pyproject_path, 'w') as f:
        for line in pyproject_lines:
            f.write(line)
