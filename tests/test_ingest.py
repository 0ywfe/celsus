import io
import tarfile

from paper_replicator.ingest import flatten, tex_files


def tarball(files):
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
        for name, text in files.items():
            data = text.encode()
            info = tarfile.TarInfo(name)
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))
    return buffer.getvalue()


def test_includes_are_inlined_and_comments_dropped():
    blob = tarball({"main.tex": "\\begin{document}\n\\input{sections/results}\n% secret 9.99\n\\end{document}",
                    "sections/results.tex": "We find $-7.49\\%$. % draft said -8.1"})
    text = flatten(tex_files(blob))
    assert "-7.49\\%" in text
    assert "9.99" not in text and "-8.1" not in text
