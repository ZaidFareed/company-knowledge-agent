from pathlib import Path
import tempfile
import unittest

from knowledge_agent.search import Passage, load_passages, search


class SearchTests(unittest.TestCase):
    def test_source_lines_and_nested_documents(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            (folder / "hr").mkdir()
            (folder / "hr" / "policy.md").write_text("# Policy\n\nAnnual leave: 22 days.\nAsk your manager.\n", encoding="utf-8")
            (folder / "ignore.csv").write_text("Annual leave: 99 days", encoding="utf-8")
            passages = load_passages(folder)
            match = search("How many days of annual leave?", passages)[0]
            self.assertEqual(match.passage.source, "hr/policy.md")
            self.assertEqual((match.passage.start_line, match.passage.end_line), (3, 4))
            self.assertEqual(len(passages), 2)

    def test_relevance_ranking(self):
        passages = [Passage("a.md", 1, 1, "Remote equipment purchases"), Passage("b.md", 1, 1, "Remote work requires manager approval")]
        self.assertEqual(search("remote work approval", passages)[0].passage.source, "b.md")

    def test_missing_evidence(self):
        self.assertEqual(search("pension", [Passage("a.md", 1, 1, "Annual leave: 22 days")]), [])

    def test_empty_question(self):
        self.assertEqual(search("the and", []), [])

    def test_invalid_limit(self):
        with self.assertRaises(ValueError):
            search("leave", [], 0)

    def test_missing_folder(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                load_passages(Path(directory) / "missing")


if __name__ == "__main__":
    unittest.main()
