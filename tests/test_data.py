import sys
from pathlib import Path

# Add parent directory to path so pytest can find quantlib
sys.path.insert(0, str(Path(__file__).parent.parent))


import numpy as np
import pandas as pd
import pytest

from quantlib.data import check_prices, write_manifest, verify_manifest, load_prices


@pytest.fixture
def clean():
    idx = pd.bdate_range("2020-01-01", periods=50)
    close = pd.Series(100 * np.exp(np.cumsum(np.full(50, 0.001))), index=idx)
    return pd.DataFrame({"Open": close, "High": close * 1.01, "Low": close * 0.99,
                         "Close": close, "Volume": 1_000_000.0})


def test_clean_data_passes(clean):
    assert check_prices(clean) == []


def test_catches_nan(clean):
    clean.iloc[10, 3] = np.nan
    assert any("missing" in p for p in check_prices(clean))


def test_catches_jump(clean):
    clean.iloc[20:, :4] *= 3
    assert any("daily moves" in p for p in check_prices(clean))


def test_catches_bad_high(clean):
    clean.iloc[5, clean.columns.get_loc("High")] = 1.0
    assert any("High below" in p for p in check_prices(clean))


def test_catches_duplicate_dates(clean):
    assert any("duplicate" in p for p in check_prices(pd.concat([clean, clean.iloc[[3]]]).sort_index()))


def test_catches_gap(clean):
    assert any("gaps" in p for p in check_prices(clean.drop(clean.index[10:20])))


def test_manifest_detects_tampering(clean, tmp_path):
    clean.to_csv(tmp_path / "AAA.csv")
    write_manifest(["AAA"], tmp_path)
    assert verify_manifest(tmp_path)
    (tmp_path / "AAA.csv").write_text("tampered")
    assert not verify_manifest(tmp_path)


def test_load_uses_cache_without_network(clean, tmp_path):
    clean.to_csv(tmp_path / "AAA.csv")
    out = load_prices("AAA", "2020-01-01", "2020-03-01", cache_dir=tmp_path)
    assert len(out) == 50
