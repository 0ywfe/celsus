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


def test_macro_definitions_nothing_uses_are_dropped_and_used_ones_kept():
    # 2602.06198 defines 10,824 number macros and uses 1,128: two thirds of a 651k-character paper, sent on every call
    from paper_replicator.ingest import prune_macros
    tex = (r"\newcommand{\usedN}{75,843}" "\n"
           r"\newcommand{\unusedN}{101,093}" "\n"
           r"\newcommand\viaOther{\usedInner\%}" "\n"
           r"\newcommand{\usedInner}{34.7}" "\n"
           r"\providecommand{\withArgs}[2][x]{#1 and {#2}}" "\n"
           r"\renewcommand{\topfraction}{0.9}" "\n"
           r"\begin{document} We keep \usedN{} rows; \viaOther lost; \withArgs{a}. \end{document}")
    out = prune_macros(tex)
    assert r"\unusedN" not in out and "101,093" not in out
    for kept in (r"\newcommand{\usedN}{75,843}", r"\newcommand\viaOther{\usedInner\%}",
                 r"\newcommand{\usedInner}{34.7}", r"\providecommand{\withArgs}[2][x]{#1 and {#2}}",
                 r"\renewcommand{\topfraction}{0.9}", r"\begin{document} We keep"):
        assert kept in out, kept


def test_a_definition_that_cannot_be_read_is_kept():
    from paper_replicator.ingest import prune_macros
    tex = r"\newcommand{\broken}{unclosed \begin{document} text \end{document}"
    assert prune_macros(tex) == tex
