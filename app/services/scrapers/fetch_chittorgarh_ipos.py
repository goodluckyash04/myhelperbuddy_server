from datetime import datetime

import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from app.db.models.ipo import IPO

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Accept": "application/json, text/plain, */*",
    "Connection": "keep-alive",
}


def parse_date(date_str: str) -> datetime | None:
    try:
        return datetime.strptime(date_str, "%a, %b %d, %Y")
    except Exception:
        return None


def parse_float(value: str) -> float:
    try:
        return float(value.replace(",", ""))
    except Exception:
        return 0.0


def fetch_and_store_ipos(db: Session):
    current_year = datetime.now().year
    url = f"https://webnodejs.chittorgarh.com/cloud/report/data-read/82/1/7/{current_year}/{current_year}-{str(current_year+1)[2:]}/0/mainboard/0"
    headers["Referer"] = "https://www.chittorgarh.com/"
    headers["Origin"] = "https://www.chittorgarh.com"

    try:
        response = requests.get(url, headers=headers)
        response_2 = requests.get(
            "https://webnodejs.investorgain.com/cloud/ipo/list-read", headers=headers
        )
        response.raise_for_status()
        response_2.raise_for_status()
        data = response.json()
        id_data = response_2.json()
        inserted, updated = 0, 0

        # Fetch all existing IPOs once
        existing_ipos = {
            (ipo.company, ipo.closing_date): ipo for ipo in db.query(IPO).all()
        }

        for row in data.get("reportTableData", []):
            company_html = BeautifulSoup(row["Company"], "html.parser")
            lead_html = BeautifulSoup(row["Lead Manager"], "html.parser")
            company_name = company_html.text.strip()
            closing_date = parse_date(row.get("Closing Date", ""))

            key = (company_name, closing_date)
            ipo = existing_ipos.get(key)

            match = next(
                (
                    x
                    for x in id_data["ipoList"]
                    if x.get("company_short_name", "").lower()
                    == row.get("~IPO", "").replace("IPO", "").strip().lower()
                ),
                {},
            )

            ipo_data = {
                "company": company_name,
                "company_url": company_html.a["href"] if company_html.a else None,
                "logo_url": row.get("~compare_image"),
                "opening_date": parse_date(row.get("Opening Date", "")),
                "closing_date": closing_date,
                "listing_date": parse_date(row.get("Listing Date", "")),
                "listing_at": row.get("Listing at"),
                "issue_price": parse_float(row.get("Issue Price (Rs.)", "0")),
                "total_issue_amount": parse_float(
                    row.get("Total Issue Amount (Incl.Firm reservations) (Rs.cr.)", "0")
                ),
                "lead_manager": lead_html.text.strip(),
                "lead_manager_url": lead_html.a["href"] if lead_html.a else None,
                "url_folder_name": row.get("~URLRewrite_Folder_Name"),
                "short_name": row.get("~IPO"),
                "gmp_id": match.get("id"),
            }

            if ipo:
                # Update existing
                for key, value in ipo_data.items():
                    setattr(ipo, key, value)
                updated += 1
            else:
                db_ipo = IPO(**ipo_data)
                db.add(db_ipo)
                inserted += 1

        db.commit()
        print(f"✅ IPOs inserted: {inserted}, updated: {updated}")
        return True
    except Exception as e:
        db.rollback()
        print("❌ Error while scraping IPOs:", e)
        return False


def fetch_ipo_gmp_detail(gmp_id):
    url = f"https://webnodejs.investorgain.com/cloud/ipo/ipo-gmp-read/{gmp_id}/true"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print("❌ Error while scraping IPOs:", e)
        return False
