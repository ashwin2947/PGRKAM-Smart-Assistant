# pgrkam_full_scraper.py

import os
import sys
import time
import signal
from datetime import datetime, timezone
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

from pymongo import MongoClient, ASCENDING
from playwright.sync_api import sync_playwright

# ------------------ CONFIG ------------------
PGRKAM_URL_PRIVATE = "https://www.pgrkam.com/search-results/?job_type=1"
PGRKAM_URL_GOVT = "https://www.pgrkam.com/search-results/?job_type=2"

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME")
COLL_PRIVATE = os.getenv("COLL_PRIVATE")
COLL_GOVT = os.getenv("COLL_GOVT")

HEADLESS = True
PAGE_TIMEOUT = 30000
REQUEST_DELAY_SEC = 0.5

# ------------------ DB ------------------
def connect_mongo():
    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]
    private = db[COLL_PRIVATE]
    govt = db[COLL_GOVT]

    # FIX: Remove the wrong source_url unique index
    # ADD: Proper compound unique index to avoid duplicates
    private.create_index(
        [("name_of_post", ASCENDING), ("name_of_employer", ASCENDING)],
        unique=True
    )
    govt.create_index(
        [("name_of_post", ASCENDING), ("name_of_employer", ASCENDING)],
        unique=True
    )

    return client, db, private, govt
#-----------------------------------------------------------------
def extract_modal_text(page):
    # Extract text from the modal body
    body = page.query_selector("#descriptionModal .modal-body")
    if body:
        return body.inner_text().strip()
    return None

#-----------------------------------------------------------------

def get_required_qualification_from_modal(card, page, wait_ms=8000):
    # 1) Try to close an already-open modal (it intercepts clicks)
    try:
        if page.locator("#descriptionModal.show").count() or page.is_visible("#descriptionModal.show"):
            # click close button if present, else press Escape
            close_btn = page.locator("#descriptionModal.show .close, #descriptionModal.show [data-dismiss='modal']")
            if close_btn.count():
                close_btn.first.click(timeout=2000)
            else:
                page.keyboard.press("Escape")
            page.wait_for_selector("#descriptionModal", state="hidden", timeout=5000)
    except Exception:
        # best-effort — keep going
        pass

    # 2) Find the + More link inside this card
    more_link = card.query_selector("a[data-target='#descriptionModal']")
    if not more_link:
        return None

    # 3) Click the link to populate the modal and wait for content
    try:
        more_link.scroll_into_view_if_needed()
        # force click to bypass minor overlays; don't wait for navigation
        more_link.click(force=True, no_wait_after=True)
        page.wait_for_selector("#descriptionModal.show .modal-body", timeout=wait_ms)
        body = page.query_selector("#descriptionModal.show .modal-body")
        if body:
            text = body.inner_text().strip()
        else:
            text = None
    except Exception:
        text = None

    # 4) Close the modal so it doesn’t block further clicks
    try:
        close_btn = page.locator("#descriptionModal.show .close, #descriptionModal.show [data-dismiss='modal']")
        if close_btn.count():
            close_btn.first.click(timeout=2000)
        else:
            page.keyboard.press("Escape")
        page.wait_for_selector("#descriptionModal", state="hidden", timeout=5000)
    except Exception:
        pass

    return text
    

#-----------------------------------------------------------------

# ------------------ PRIVATE JOB CARD EXTRACTOR ------------------
def extract_private_card(card):
    def safe(q):
        el = card.query_selector(q)
        return el.inner_text().strip() if el else None

    name_of_post = safe("h4.company-name a")
    if name_of_post and "Name Of Post:" in name_of_post:
        name_of_post = name_of_post.replace("Name Of Post:", "").strip()

    name_of_employer = safe("h6.company-name2 span.date-clr")
    place_of_posting = safe("ul.nav li span.date-clr")

    required_qualification = None
    rq = card.query_selector("p:has-text('Required Qualification') span.date-clr")
    if rq:
        required_qualification = rq.inner_text().strip()

    salary = None
    sal = card.query_selector("p:has-text('Salary') span.date-clr")
    if sal:
        salary = sal.inner_text().strip()

    vacancies = safe(".bgLightOrange div:nth-child(1) span.date-clr")
    minimum_age = safe(".bgLightOrange div:nth-child(2) span.date-clr")
    experience = safe(".bgLightOrange div:nth-child(3) span.date-clr")
    gender = safe(".bgLightOrange div:nth-child(4) span.date-clr")

    apply_el = card.query_selector("a.date-clr[href*='job-details-home']")
    apply_link = None
    if apply_el:
        href = apply_el.get_attribute("href")
        if href.startswith("/"):
            apply_link = "https://www.pgrkam.com" + href
        else:
            apply_link = href

    return {
        "name_of_post": name_of_post,
        "name_of_employer": name_of_employer,
        "place_of_posting": place_of_posting,
        "required_qualification": required_qualification,
        "salary": salary,
        "vacancies": vacancies,
        "minimum_required_age": minimum_age,
        "experience": experience,
        "gender": gender,
        "apply_link": apply_link,
    }

# ------------------ GOVERNMENT JOB CARD EXTRACTOR ------------------
def extract_govt_card(card, page):
    def safe(q):
        el = card.query_selector(q)
        return el.inner_text().strip() if el else None

    name_of_post = safe("h4.company-name a")
    if name_of_post and "Name Of Post:" in name_of_post:
        name_of_post = name_of_post.replace("Name Of Post:", "").strip()

    name_of_employer = safe("h6.company-name2 span.date-clr")
    place_of_posting = safe("ul.nav li span.date-clr")

    # Try modal first
    required_qualification = None
    try:
        required_qualification = get_required_qualification_from_modal(card, page, wait_ms=8000)
    except Exception as e:
        print(f"[WARN] Modal extraction failed: {e}")

    # Fallback to inline text (strip the '+ More' label if present)
    if not required_qualification:
        rq_span = card.query_selector("p:has-text('Required Qualification') span.date-clr")
        if rq_span:
            txt = rq_span.inner_text().strip()
            # Remove the literal '+ More' if it got included in the text
            required_qualification = txt.replace("+ More", "").strip()

    vacancies = safe(".bgLightOrange div:nth-child(1) span.date-clr")
    last_apply_date = safe(".bgLightOrange div:nth-child(2) span.date-clr")
    maximum_age = safe(".bgLightOrange div:nth-child(3) span.date-clr")
    experience = safe(".bgLightOrange div:nth-child(4) span.date-clr")
    gender = safe(".bgLightOrange div:nth-child(5) span.date-clr")

    apply_el = card.query_selector(".bgLightOrange div:nth-child(6) a")
    apply_link = apply_el.get_attribute("href") if apply_el else None

    notif_el = card.query_selector(".bgLightOrange div:nth-child(7) a")
    notification_link = notif_el.get_attribute("href") if notif_el else None

    where_to_apply = safe(".bgLightOrange div:nth-child(8) span.date-clr")

    posted_on = None
    posted_el = card.query_selector("span:has-text('Posted on')")
    if posted_el:
        txt = posted_el.inner_text()
        posted_on = txt.replace("Posted on", "").strip()

    return {
        "name_of_post": name_of_post,
        "name_of_employer": name_of_employer,
        "place_of_posting": place_of_posting,
        "required_qualification": required_qualification,
        "vacancies": vacancies,
        "last_apply_date": last_apply_date,
        "maximum_applicable_age": maximum_age,
        "experience": experience,
        "gender": gender,
        "apply_link": apply_link,
        "notification_link": notification_link,
        "where_to_apply": where_to_apply,
        "posted_on": posted_on,
    }




# ------------------ SCRAPE LIST PAGE ------------------
def scrape_list_page(play, url: str, job_type: int) -> List[Dict]:
    browser = None
    try:
        browser = play.chromium.launch(headless=HEADLESS)
        ctx = browser.new_context()
        page = ctx.new_page()

        page.goto(url, timeout=PAGE_TIMEOUT)
        page.wait_for_load_state("domcontentloaded")
        time.sleep(1.5)

        records = []

        while True:
            cards = page.query_selector_all(".first-job")

            for card in cards:
                try:
                    if job_type == 1:
                        rec = extract_private_card(card)
                        job_name = "private"
                    else:
                        rec = extract_govt_card(card,page)
                        job_name = "government"

                    rec["job_type"] = job_name
                    rec["source_url"] = url
                    rec["scraped_at"] = datetime.now(timezone.utc)
                    records.append(rec)
                except Exception as e:
                    print(f"[ERR] Card extraction failed: {e}")

            next_btn = page.query_selector("a.page-link:has-text('Next')")
            if next_btn and next_btn.is_enabled():
                next_btn.click()
                page.wait_for_load_state("domcontentloaded")
                time.sleep(1.0)
            else:
                break

        return records
    except KeyboardInterrupt:
        print("[INFO] Scraping interrupted by user")
        return []
    except Exception as e:
        print(f"[ERR] Scraping failed: {e}")
        return []
    finally:
        if browser:
            try:
                browser.close()
            except Exception:
                pass

# ------------------ UPSERT ------------------
def upsert_records(coll, records):
    c = 0
    for r in records:
        coll.update_one(
            {"name_of_post": r["name_of_post"], "name_of_employer": r["name_of_employer"]},
            {"$set": r},
            upsert=True
        )
        c += 1
    return c

# ------------------ MAIN ------------------
def main():
    def signal_handler(signum, frame):
        print("\n[INFO] Received interrupt signal, shutting down gracefully...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    client, db, private_coll, govt_coll = connect_mongo()

    try:
        with sync_playwright() as p:
            private_records = scrape_list_page(p, PGRKAM_URL_PRIVATE, 1)
            govt_records = scrape_list_page(p, PGRKAM_URL_GOVT, 2)

        up1 = upsert_records(private_coll, private_records)
        up2 = upsert_records(govt_coll, govt_records)

        print({
            "private_upserts": up1,
            "govt_upserts": up2,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
    except KeyboardInterrupt:
        print("\n[INFO] Script interrupted by user")
    except Exception as e:
        print(f"[ERR] Script failed: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
