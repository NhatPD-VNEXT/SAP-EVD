import os
import re
import argparse
from playwright.sync_api import Playwright, sync_playwright, expect

parser = argparse.ArgumentParser()
parser.add_argument("--po-number", required=True, help="Purchase Order number")
parser.add_argument("--po-quantity", required=True, help="PO Quantity to fill")
args = parser.parse_args()

PO_NUMBER = args.po_number
PO_QUANTITY = args.po_quantity

EVD_BASE = r"C:\Users\Admin\OneDrive\Máy tính\TOOL SAP\EVD"
EVD_DIR = os.path.join(EVD_BASE, f"PO{PO_NUMBER}_QTY{PO_QUANTITY}")
os.makedirs(EVD_DIR, exist_ok=True)

_step = [0]

def snap(page, label):
    _step[0] += 1
    filename = f"{_step[0]:02d}_{label}.png"
    page.screenshot(path=os.path.join(EVD_DIR, filename))


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://my422346.s4hana.cloud.sap/ui#PurchaseOrder-display?sap-ui-tech-hint=GUI&uitype=advancedNoPar")
    page.get_by_role("textbox", name="Email").click()
    page.get_by_role("textbox", name="Email").fill("nhatpd@vnext.vn")
    page.locator("#j_password-group > .ids-label-container").click()
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill("Tuan130599@@")
    page.get_by_role("button", name="Continue").click()
    page.wait_for_timeout(3000)

    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("button", name="Other Purchase Order").click()
    page.wait_for_timeout(3000)

    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("textbox", name="Pur. Order").click()
    page.wait_for_timeout(3000)
    snap(page, "pur_order_click")

    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("textbox", name="Pur. Order").fill(PO_NUMBER)
    page.wait_for_timeout(3000)
    snap(page, "pur_order_fill")

    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("textbox", name="Pur. Order").press("Enter")
    page.wait_for_timeout(3000)

    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("button", name="Expand Items Ctrl+F3").click()
    page.wait_for_timeout(3000)

    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("button", name="Display/Change").click()
    page.wait_for_timeout(3000)

    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("textbox", name="PO Quantity").first.click()
    page.wait_for_timeout(3000)
    snap(page, "po_quantity_click")

    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("textbox", name="PO Quantity").first.fill(PO_QUANTITY)
    page.wait_for_timeout(3000)
    snap(page, "po_quantity_fill")

    page.locator("iframe[name=\"__container1-iframe\"]").content_frame.get_by_role("button", name="Save  Emphasized").click()
    page.wait_for_timeout(3000)
    snap(page, "save")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
