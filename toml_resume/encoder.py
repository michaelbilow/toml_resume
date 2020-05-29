from toml.encoder import _dump_str, TomlArraySeparatorEncoder

LINE_LENGTH = 90


def _dump_multiline_string(s):
    if len(s) < LINE_LENGTH:
        return _dump_str(s)
    else:
        words = s.split(" ")
        lines = [words[0]]
        for word in words[1:]:
            current_line = lines[-1]
            word_length = len(word)
            current_line_length = len(current_line)
            if word_length + current_line_length <= LINE_LENGTH:
                lines[-1] += f" {word}"
            else:
                lines.append(word)
        output_lines = " \\\n".join(lines)
        output = f'"""\n{output_lines}"""'
        return output


neat_encoder = TomlArraySeparatorEncoder(separator=",\n")
neat_encoder.dump_funcs[str] = _dump_multiline_string
