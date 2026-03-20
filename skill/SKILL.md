# SKILL.md for PO Creation on Vnext TDD Environment

This skill automates the creation of a Purchase Order (PO) in the Vnext TDD environment. It performs the following steps in sequence:

1. Calls the script `sap_po_create` located in the script directory.
2. Waits for the script to complete execution.
3. Reads the latest log to determine the PO created.
4. Retrieves the evidence image associated with the PO creation.
5. Sends the relevant information and image.

## Skill Actions

### Trigger Phrase
When the user sends the message:
- "Tạo PO ở môi trường Vnext TDD"

### Steps to Execute

1. Call the script:
   ```shell
   PS C:\Users\Admin\.openclaw\workspace\script> python sap_po_create.py
   ```

2. Monitor script execution and wait until it completes.
   - Poll the script state (implementation to handle waiting internally.)

3. Extract details from the most recent log in:
   ```shell
   C:\Users\Admin\.openclaw\workspace\log
   ```
   - Confirm which PO was successfully created.

4. Collect the relevant evidence image from:
   ```shell
   C:\Users\Admin\.openclaw\workspace\evd
   ```

5. Deliver the PO details and image to the channel.

---

## Implementation Notes

- The skill must:
  - Ensure the `sap_po_create` script executes without disruptions.
  - Identify and parse only the **latest log entry**.
  - Retrieve the **appropriate image file**.
- Errors during any step should be clearly communicated.

To implement this skill, ensure access permissions are in place for the `script`, `log`, and `evd` directories.