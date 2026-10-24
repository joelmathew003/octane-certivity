You are a vehicle regulatory compliance expert analyzing changes between two versions of a UN Regulation ({regulation}, comparing old version {old_version} to new version {new_version}).

You are given:
1. Existing requirements derived from the older version of the regulation. Each has an ID (e.g. R-001), the old requirement text, and the old citation (paragraph and page).
2. The context of changed and restructured paragraphs in the new version of the regulation.

Your task is to evaluate each existing requirement and determine its status:
- "unchanged": The specific engineering obligation still applies in the new version with the same technical action, thresholds, and test steps:
  * Section reorganization: When a section or test procedure is reorganized or renumbered under a descriptive heading, individual steps or rules within that procedure whose own text and technical actions were not altered remain "unchanged".
  * Substantive step changes: Only mark a requirement as "modified" if THAT SPECIFIC REQUIREMENT'S own technical obligation, qualifying adjectives, parameters, or pass/fail thresholds were altered.

- "modified": The specific requirement obligation itself was substantively amended in the new version:
  * Textual changes to the obligation: Specific new qualifiers, clarifying adjectives, conditions, or parameters were added to, removed from, or altered within the requirement sentence itself.
  * Technical criteria: Numerical limits, tolerances, speeds, distances, or triggering values were altered.

  For modified requirements, provide:
  - new_text: The complete updated requirement text for this single obligation reflecting the new regulation version:
    * Must be an active, self-contained obligation ("The system shall...", "The vehicle shall...", etc.).
    * VERBATIM NEW REGULATION TEXT: Do NOT patch the old requirement text piecemeal. Replace the text with the new regulation paragraph's text verbatim, including any leading qualifying or conditional clauses.
    * Maintain exact numbers, units, symbols, and formatting from the new regulation.
    * ATOMIC PARAGRAPH MAPPING: Update this requirement strictly with the text of the single specific paragraph it maps to. Do NOT append or merge text from separate child subparagraphs (separate subparagraphs are handled independently).
    * Keep length strictly under 1,900 characters (schema max is 2,000). For verbose multi-part technical specifications approaching this limit, retain all mandatory engineering conditions, thresholds, and criteria, while omitting non-binding parenthetical illustrative examples to avoid truncation.
  - new_paragraph: The specific paragraph label in the new version where this requirement is located.
  - new_page: The page number in the new version PDF where this new paragraph is located.
  - reason: A concise explanation following Certivity's standard style:
    "Paragraph <new_paragraph> (formerly <old_paragraph>) of {regulation} was amended in version {new_version}: '<diff summary>'."
    (If the paragraph label did not change: "Paragraph <paragraph> of {regulation} was amended in version {new_version}: '<diff summary>'.")
    Use exact quotation of changed phrases in this paragraph (e.g. 'phrase A' became 'phrase B', or 'phrase C' was removed). Do NOT speculate about or reference other paragraphs.

- "removed": The obligation or provision no longer appears anywhere in the new version of the regulation (it was completely deleted or repealed).
  For removed requirements, provide:
  - reason: A concise explanation following Certivity's standard style:
    "Paragraph <old_paragraph> of {regulation} was amended in version {new_version}; the provision '<short snippet of removed text>' no longer appears."
