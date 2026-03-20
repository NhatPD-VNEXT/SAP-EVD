import os
import re
import json
from datetime import datetime
from playwright.sync_api import Playwright, sync_playwright, expect
import subprocess

GIT_REPO = r"C:\Users\Admin\.openclaw\workspace"

EVD_BASE = r"C:\Users\Admin\.openclaw\workspace\evd"
LOG_DIR  = r"C:\Users\Admin\.openclaw\workspace\log"
os.makedirs(LOG_DIR, exist_ok=True)
EVD_DIR = os.path.join(EVD_BASE, f"PO_CREATE_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
os.makedirs(EVD_DIR, exist_ok=True)

_step = [0]


def _git(args: list[str]) -> str:
    result = subprocess.run(
        ["git"] + args,
        cwd=GIT_REPO,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed:\n{result.stderr.strip()}")
    return result.stdout.strip()


def commit_evidence_to_git(local_folder: str, po_number: str):
    rel_path = os.path.relpath(local_folder, GIT_REPO).replace("\\", "/")
    _git(["add", rel_path])
    _git(["commit", "-m", f"evidence: PO {po_number} created"])
    _git(["push"])
    print(f"[Git] Pushed evidence folder: {rel_path}")


def snap(page, label):
    _step[0] += 1
    filename = f"{_step[0]:02d}_{label}.png"
    page.screenshot(path=os.path.join(EVD_DIR, filename))


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width":1600,"height":900})
    page = context.new_page()
    page.goto("https://my422346.s4hana.cloud.sap/ui#PurchaseOrder-create?sap-ui-tech-hint=GUI&uitype=advanced")
    page.get_by_role("textbox", name="Email").click()
    page.get_by_role("textbox", name="Email").fill("nhatpd@vnext.vn")
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill("Tuan130599@@")
    page.get_by_role("button", name="Continue").click()
    page.wait_for_timeout(3000)

    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("button", name="Close").click()
    page.wait_for_timeout(3000)

    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("textbox", name="Supplier").click()
    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("textbox", name="Supplier").fill("15310047")
    page.wait_for_timeout(3000)

    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("textbox", name="Supplier").press("Enter")
    page.wait_for_timeout(3000)
    snap(page, "supplier_fill")

    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("textbox", name="Purch. Org.").fill("1510")
    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("textbox", name="Purch. Org.").press("Tab")
    page.wait_for_timeout(3000)

    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("textbox", name="Purch. Group").fill("001")
    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("textbox", name="Purch. Group").press("Tab")
    page.wait_for_timeout(3000)

    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("textbox", name="Company Code").fill("1510")
    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("textbox", name="Company Code").press("Enter")
    page.wait_for_timeout(3000)
    snap(page, "header_fill")

    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("button", name="Expand Items Ctrl+F3").click()
    page.wait_for_timeout(3000)

    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("textbox", name="Material").first.click()
    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("textbox", name="Material").first.press("ControlOrMeta+V")
    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("textbox", name="Material").first.fill("FG129")
    page.wait_for_timeout(3000)
    snap(page, "material_fill")

    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("textbox", name="PO Quantity").first.click()
    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("textbox", name="PO Quantity").first.fill("10")
    page.wait_for_timeout(3000)
    snap(page, "po_quantity_fill")

    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("textbox", name="Net Price").first.click()
    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("textbox", name="Net Price").first.fill("100")
    page.wait_for_timeout(3000)
    snap(page, "net_price_fill")

    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("textbox", name="Plant").first.click()
    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("textbox", name="Plant").first.fill("1510")
    page.wait_for_timeout(3000)
    snap(page, "plant_fill")

    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("button", name="Save  Emphasized").click()
    page.wait_for_timeout(3000)
    snap(page, "save")

    success_note = page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("note", name="Success Message Bar Standard")
    success_note.wait_for(state="visible", timeout=10000)
    success_text = success_note.inner_text()
    page.wait_for_timeout(3000)
    snap(page, "success")

    match = re.search(r"(\d{10})", success_text)
    po_number = match.group(1) if match else "UNKNOWN"
    print(f"PO Number created: {po_number}")

    new_evd_dir = os.path.join(EVD_BASE, f"PO{po_number}_CREATE")
    os.rename(EVD_DIR, new_evd_dir)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "status": "SUCCESS",
        "po_number": po_number,
        "message": success_text.strip(),
        "evidence_dir": new_evd_dir,
    }
    log_path = os.path.join(LOG_DIR, f"PO_CREATE_{ts}.json")
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log_entry, f, ensure_ascii=False, indent=2)
    print(f"Log saved: {log_path}")

    commit_evidence_to_git(new_evd_dir, po_number)

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
