from pathlib import Path

from lotto_lab.parsers.wclc_parser import parse_draws


def test_parse_draws():
    fixture_path = (
        Path(__file__).parent
        / "fixtures"
        / "western_649_sample.html"
    )

    html = fixture_path.read_text(encoding="utf-8")

    results = parse_draws(html)

    assert len(results["raw_draws"]) == 2
    assert len(results["parse_errors"]) == 0

    assert results["raw_draws"][0] == {
    "raw_date": "Saturday, August 29, 2026",
    "raw_numbers": ["2", "6", "26", "33", "34", "49"],
    "raw_bonus": "19",
}

    assert results["raw_draws"][1] == {
        "raw_date": "Wednesday, August 26, 2026",
        "raw_numbers": ["3", "14", "16", "20", "36", "46"],
        "raw_bonus": "2",
    }

def test_parse_draws_missing_bonus():
    html = """
    <div class="pastWinNum">
        <div class="pastWinNumDate">
            <h4>Saturday, August 29, 2026</h4>
        </div>
        <ul>
            <li class="pastWinNumber">2</li>
            <li class="pastWinNumber">6</li>
            <li class="pastWinNumber">26</li>
            <li class="pastWinNumber">33</li>
            <li class="pastWinNumber">34</li>
            <li class="pastWinNumber">49</li>
        </ul>
        <span class="pastWinNumberBonusText">Bonus</span>19
    </div>

    <div class="pastWinNum">
        <div class="pastWinNumDate">
            <h4>Wednesday, August 26, 2026</h4>
        </div>
        <ul>
            <li class="pastWinNumber">3</li>
            <li class="pastWinNumber">14</li>
            <li class="pastWinNumber">16</li>
            <li class="pastWinNumber">20</li>
            <li class="pastWinNumber">36</li>
            <li class="pastWinNumber">46</li>
        </ul>
        <!-- Bonus tag intentionally missing -->
    </div>
    """

    result = parse_draws(html)

    assert len(result["raw_draws"]) == 1
    assert len(result["parse_errors"]) == 1

    assert result["raw_draws"][0]["raw_date"] == "Saturday, August 29, 2026"

    assert result["parse_errors"][0]["raw_date"] == "Wednesday, August 26, 2026"
    assert result["parse_errors"][0]["reason"] == "Missing bonus tag"