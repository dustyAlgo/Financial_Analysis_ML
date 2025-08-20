#!/usr/bin/env python3
"""
Generate an empty Excel template for company IDs.
The file will be created at data/companies.xlsx with a single column: company_id
"""

from pathlib import Path
import pandas as pd


def main() -> None:
	output_path = Path("data/companies.xlsx")
	output_path.parent.mkdir(parents=True, exist_ok=True)

	df = pd.DataFrame({"company_id": []})
	df.to_excel(output_path, index=False, sheet_name="Companies")

	print(f"✅ Created companies template: {output_path.resolve()}")
	print("➡️  Add your company IDs under the 'company_id' column.")


if __name__ == "__main__":
	main()