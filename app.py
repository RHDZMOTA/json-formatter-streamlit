import uuid
import json
import ast
import logging
import textwrap
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

import streamlit as st


logger = logging.getLogger(__name__)


@dataclass
class JSONParser:
    string: str
    single_quote: bool = False

    @property
    def uuid(self) -> str:
        return str(uuid.uuid5(uuid.NAMESPACE_OID, self.string))


    def parse(self) -> Tuple[bool, Optional[Dict], Optional[str]]:
        try:
            json_parsed = ast.literal_eval(self.string) if self.single_quote else json.loads(self.string)
            return True, json_parsed, "Success!"
        except Exception as e: 
            logger.error("Error when parsing %s: %s", self.uuid, str(e))
            logger.debug("Problematic json detected (%s) %s", self.uuid, str(e))
            return False, None, "Failure: Error while parsing json"
    

def json_input() -> Optional[Tuple[bool, str]]:
    with st.form("json-input"):
        raw = st.text_area(label="JSON String")
        content_uuid = st.checkbox("Content UUID")
        single_quote = st.checkbox("Use Single-Quotes")
        submitted = st.form_submit_button("Parse!")
    if not submitted:
        return False, None
    return content_uuid, JSONParser(string=raw, single_quote=single_quote)


def main():
    content_uuid, parser = json_input()
    if parser is None:
        return
    ok, payload, message = parser.parse()
    if not ok:
        return st.warning(message)
    st.info(message)
    st.markdown("## Parsed JSON")
    st.markdown(
        textwrap.dedent(
            f"""
            Content UUID:
            ```text
            {parser.uuid}
            ```
            """
        )
    )
    st.write("Result:")
    st.json(payload)



if __name__ == "__main__":
    main()

