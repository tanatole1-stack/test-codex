import os, csv, unittest, subprocess, sys, tempfile
from pmu_extractor.config import CSV_COLUMNS, DIAG_COLUMNS

class TestFormats(unittest.TestCase):
    def test_columns_strict(self):
        self.assertEqual(CSV_COLUMNS[0], "Reunion")
        self.assertEqual(CSV_COLUMNS[-1], "Non_Partants")

    def test_mock_run_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            outdir = os.path.join(d, "out")
            cmd = [sys.executable, "main.py",
                   "--date", "12 janvier 2026",
                   "--reunions", "R1",
                   "--turfomania", "dummy.pdf",
                   "--mock",
                   "--outdir", outdir]
            subprocess.check_call(cmd)
            csv_path = os.path.join(outdir, "resultats.csv")
            self.assertTrue(os.path.exists(csv_path))
            with open(csv_path, "r", encoding="utf-8") as f:
                r = csv.reader(f)
                header = next(r)
            self.assertEqual(header, CSV_COLUMNS)
            dpath = os.path.join(outdir, "diagnostics.csv")
            with open(dpath, "r", encoding="utf-8") as f:
                r = csv.reader(f)
                header2 = next(r)
            self.assertEqual(header2, DIAG_COLUMNS)

if __name__ == "__main__":
    unittest.main()
