# SKILL.md for PO Update on Vnext TDD Environment

This skill automates updating a Purchase Order (PO) in the Vnext TDD environment. It handles the following workflow:

1. Calls the `sap_po_update` script with given PO number and quantity parameters.
2. Waits for the script to complete execution.
3. Confirms the operation was successful by checking the log.
4. Retrieves evidence related to the update from the GitHub repository and provides the link.

---

## Skill Actions

### Trigger Phrase
When the user sends a message like:
- "Update PO XXXXXXXX với Quantity = XXXXXXX ở môi trường Vnext TDD"

### Steps to Execute

1. Call the update script with parameters:
   ```shell
   C:\Users\Admin\.openclaw\workspace\script> python sap_po_update.py --po-number <XXXXXXXXXX> --po-quantity <XXXXXXXX>
   ```

   - Replace `<XXXXXXXXXX>` with the actual PO number.
   - Replace `<XXXXXXXX>` with the actual PO quantity.

2. Monitor script execution and wait until it completes.
3. Fetch the evidence from GitHub at:
   ```
   https://github.com/NhatPD-VNEXT/SAP-EVD/tree/main/evd
   ```

---

## Implementation Notes

- Ensure the `sap_po_update` script runs smoothly and handles parameters correctly.
- Verify the log to confirm a successful update.
   - Location: `C:\Users\Admin\.openclaw\workspace\log\`
- Evidence retrieval:
   - Reuse the evidence directory path for the GitHub repository organization.
- Errors during any step (script execution, log checking, etc.) should be reported immediately with details.

## Logging
Maintain logs in the workspace:
- Success and failure messages logged in `C:\Users\Admin\.openclaw\workspace\log\`
- Evidence GitHub directory: `https://github.com/NhatPD-VNEXT/SAP-EVD/tree/main/evd`.