import re
from writer import OutputWriter


class TestOutputWriter:
    def test_creates_file(self, tmp_path):
        path = OutputWriter(tmp_path).save("# Hello\n## Slide", "Tesla")
        assert path.exists()

    def test_file_has_md_extension(self, tmp_path):
        path = OutputWriter(tmp_path).save("content", "Tesla")
        assert path.suffix == ".md"

    def test_filename_contains_slug(self, tmp_path):
        path = OutputWriter(tmp_path).save("content", "Tesla Motors")
        assert "tesla_motors" in path.name

    def test_filename_contains_timestamp(self, tmp_path):
        path = OutputWriter(tmp_path).save("content", "Tesla")
        assert re.search(r"\d{8}_\d{6}", path.name)

    def test_creates_output_dir_if_missing(self, tmp_path):
        new_dir = tmp_path / "subdir" / "outputs"
        OutputWriter(new_dir).save("content", "Tesla")
        assert new_dir.exists()

    def test_file_content_matches_input(self, tmp_path):
        content = "# Tesla Competitive Landscape\n## BYD\n- bullet"
        path = OutputWriter(tmp_path).save(content, "Tesla")
        assert path.read_text(encoding="utf-8") == content

    def test_sanitizes_special_chars_in_company_name(self, tmp_path):
        path = OutputWriter(tmp_path).save("content", "OpenAI (GPT)")
        assert re.match(r"^[a-z0-9_]+_\d{8}_\d{6}\.md$", path.name)
